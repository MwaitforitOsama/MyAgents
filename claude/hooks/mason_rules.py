#!/usr/bin/env python3
"""Mason guard: a Claude Code PreToolUse hook.

Active only when the session runs as the `mason` agent (`claude --agent mason`).
Every other session and agent passes through untouched.

Mason normally runs in the default permission mode, where Claude Code asks
before every edit and command anyway. This guard covers the time after the
user has granted more freedom (a mode switch or allow rules):

  ASK   high-impact actions always prompt the user, whatever the mode:
        commit/push and history rewrites, deploys and cloud changes,
        publishing, destructive database and file operations, remote access,
        shell indirection that could hide any of these, and Jira writes
        (create issue, link issues, comment).
  DENY  Mason may never change its own permissions or Claude Code config.

Output: exit 0 + JSON {"permissionDecision": "ask"} to prompt, exit 2 to block,
plain exit 0 to leave the decision to Claude Code's normal permission flow.
This is text matching, not a sandbox: a false match only costs one extra prompt.
"""

import json
import os
import re
import sys

AGENT = "mason"
REPO = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
MEMORY = os.path.join(REPO, "skills", "mason", "memory")
# Agent definitions, rules, guards and shared knowledge. Mason never edits its own rules.
PROTECTED = [os.path.join(REPO, d) for d in ("skills", "shared", "claude", "knowledge")]
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def rx(pattern):
    return re.compile(pattern, re.IGNORECASE | re.DOTALL)


# (pattern, reason). Matched against the whole Bash command text.
ASK_BASH = [
    # git: anything that records, publishes or rewrites history
    (rx(r"\bgit\b.*\b(commit|push|rebase|merge|cherry-pick|revert|am|filter-branch|filter-repo|update-ref)\b"),
     "git command that records, publishes or rewrites history"),
    (rx(r"\bgit\b.*\breset\b.*--(hard|merge|keep)\b"), "git reset that discards work"),
    (rx(r"\bgit\b.*\bclean\b"), "git clean deletes untracked files"),
    (rx(r"\bgit\b.*\b(checkout|restore)\b.*(\s--\s|\s\.(\s|$)|--source|--staged|--worktree)"),
     "git checkout/restore that discards changes"),
    (rx(r"\bgit\b.*\bbranch\b.*\s-(D|d|M|m|f)\b|\bgit\b.*\bbranch\b.*--(delete|force|move)\b"),
     "git branch delete/rename"),
    (rx(r"\bgit\b.*\btag\b\s+(?!-l\b|--list\b)\S"), "git tag"),
    (rx(r"\bgit\b.*\bstash\b.*\b(drop|clear)\b"), "git stash drop/clear"),
    (rx(r"\bgit\b.*\b(reflog\s+expire|gc\b.*--prune)"), "git history pruning"),
    # GitHub / hosting CLIs
    (rx(r"\bgh\b\s+(pr|issue|release|repo|workflow|run|secret|variable|api|gist|label)\b"
        r"(?!\s+(list|view|status|diff|checks)\b)"), "GitHub CLI action that changes something"),
    # containers, clusters, infrastructure
    (rx(r"\bdocker\b.*\b(push|login|logout)\b"), "docker push/login"),
    (rx(r"\bdocker\b.*\b(system|volume|image|container|network|builder)\s+(prune|rm)\b"), "docker prune/remove"),
    (rx(r"\bdocker\b.*\bcompose\b.*\bdown\b.*(-v\b|--volumes|--rmi)"), "docker compose down that deletes volumes/images"),
    (rx(r"\bkubectl\b.*\b(apply|create|delete|replace|patch|scale|rollout|drain|cordon|uncordon|edit|set|label|"
        r"annotate|exec|cp|port-forward|taint)\b"), "kubectl change to a cluster"),
    (rx(r"\bhelm\b.*\b(install|upgrade|uninstall|delete|rollback)\b"), "helm release change"),
    (rx(r"\b(terraform|tofu|terragrunt|pulumi)\b.*\b(apply|destroy|import|taint|untaint|up|refresh|state\s+(rm|mv|push))\b"),
     "infrastructure change"),
    # cloud CLIs: anything that is not plainly a read
    (rx(r"\b(doctl|oci|gcloud|aws|az)\b(?!.*\b(list|get|describe|ls|show|logs|--version|version|help)\b)"),
     "cloud CLI command that is not a list/get/describe"),
    (rx(r"\b(doctl|oci|gcloud|aws|az)\b.*\b(create|delete|update|put|deploy|apply|destroy|terminate|launch|"
        r"resize|restore|rotate|attach|detach|reboot|power-off|power-on|enable|disable|set|unset|"
        r"add-iam-policy-binding|remove-iam-policy-binding|set-iam-policy|secret-bundle|kubeconfig|"
        r"docker-config|login|ssh|scp|cp|mv|rm|sync)\b"), "cloud CLI command that changes or reveals something"),
    # hosting / app stores / package registries
    (rx(r"\b(vercel|netlify|firebase|flyctl|fly|wrangler|heroku|railway)\b.*\b(deploy|publish|promote|release|"
        r"rollback|env|secrets?|domains?|remove|rm|destroy)\b"), "hosting deploy or config change"),
    (rx(r"\beas\b.*\b(build|submit|update|publish|secret|env)\b|\bexpo\b.*\bpublish\b|\bfastlane\b"),
     "mobile build/submit/publish"),
    (rx(r"\b(npm|pnpm|yarn|bun)\b.*\b(publish|unpublish|deprecate|dist-tag|owner|token|login|adduser)\b"),
     "package registry publish or auth"),
    # databases
    (rx(r"\b(psql|mysql|sqlite3|mongosh|mongo|redis-cli|cqlsh)\b.*\b(drop|truncate|delete|update|alter|grant|revoke|"
        r"insert|create|dropDatabase|deleteMany|deleteOne|updateMany|updateOne|insertMany|insertOne|flushall|flushdb)\b"),
     "database write or schema change"),
    (rx(r"\bprisma\b.*\b(migrate\s+(deploy|reset|resolve)|db\s+(push|execute|seed))\b"), "database migration"),
    (rx(r"\b(migrate|goose|atlas|dbmate|knex|sequelize|typeorm|drizzle-kit|flyway|liquibase)\b.*"
        r"\b(up|down|reset|force|drop|redo|deploy|apply|push|migrate|run|revert)\b"), "database migration"),
    (rx(r"\b(pg_restore|mongorestore|dropdb|createdb)\b"), "database restore/create/drop"),
    # destructive file operations
    (rx(r"\brm\b\s+(-\S*[rRf]|--recursive|--force)"), "recursive or forced delete"),
    (rx(r"\b(shred|truncate|dd|mkfs)\b"), "destructive file operation"),
    (rx(r"\bchmod\b.*\s-R\b|\bchown\b"), "recursive permission/ownership change"),
    # remote access and outbound writes
    (rx(r"\b(ssh|scp|sftp|rsync)\b"), "remote access or copy"),
    (rx(r"\b(curl|wget|http|xh)\b(?!.*\b(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])\b).*"
        r"(-X\s*(POST|PUT|PATCH|DELETE)|--request\s*(POST|PUT|PATCH|DELETE)|\s(-d|--data\S*|-F|--form|-T|--upload-file)\b)"),
     "HTTP write to a remote server"),
    # privilege and shell indirection (can hide any command above)
    (rx(r"\bsudo\b|\bsu\b\s"), "sudo/su"),
    (rx(r"\beval\b|\b(sh|bash|zsh|dash|fish)\s+-\S*c\b|\|\s*(sh|bash|zsh)\b|\bxargs\b|\bsource\b\s|^\s*\.\s"),
     "shell indirection (eval, sh -c, piping into a shell, xargs, source)"),
    (rx(r"\b(python3?|node|ruby|perl|php|deno|bun)\b\s+(-\S*[ce]\b|--eval\b)"), "inline script (-c / -e)"),
    (rx(r"\bcrontab\b|\blaunchctl\b|\bsystemctl\b"), "scheduled job or service change"),
]

# Mason must never change its own permissions, hooks, or Claude Code config.
CONFIG_PATH = rx(r"(\.claude/(settings(\.local)?\.json|agents/|skills/|hooks/|commands/)|\.claude\.json|"
                 r"managed-settings\.json|/claude/hooks/(plumb|mason)_guard\.py|/claude/agents/(plumb|mason)\.md)")
GIT_INTERNALS = rx(r"(^|/)\.git/")
ASK_WRITE = [
    (rx(r"(^|/)\.env(?!\.(example|sample|template|dist)\b)(\.[^/]*)?$"), "environment/secrets file"),
    (rx(r"\.(pem|key|p12|pfx|keystore|jks)$|(^|/)id_(rsa|ed25519|ecdsa)"), "key or certificate file"),
    (rx(r"(^|/)\.github/workflows/|(^|/)\.gitlab-ci\.yml$|(^|/)cloudbuild\.ya?ml$|(^|/)\.do/app\.ya?ml$"),
     "CI/CD or deploy pipeline"),
]


# Jira write tools Mason has (claude/agents/mason.md). Each call always prompts the user,
# whatever the permission mode or allow rules: tickets are created only from a ticket plan
# the user approved (shared/rules/handoff.md, TICKETS_READY).
JIRA_WRITE_TOOLS = {
    "mcp__atlassian__createJiraIssue": "creating a Jira issue",
    "mcp__atlassian__createIssueLink": "linking Jira issues",
    "mcp__atlassian__addCommentToJiraIssue": "commenting on a Jira issue",
}


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "Mason guard: %s always needs the user's approval." % reason,
    }}))
    return 0


def deny(reason):
    sys.stderr.write(
        "Mason guard blocked this: %s.\n"
        "Only the user changes Mason's permissions, hooks and Claude Code config. Do not try another "
        "way. Tell the user what you wanted to change and why.\n" % reason)
    return 2


def check_bash(command):
    if CONFIG_PATH.search(command) and not re.match(
            r"^\s*(cat|less|head|tail|grep|rg|ls|jq\s+[^>|]*$|diff|wc)\b[^>|;&]*$", command):
        return deny("this command touches Claude Code settings, agents, skills or hooks")
    for pattern, reason in ASK_BASH:
        if pattern.search(command):
            return ask(reason)
    return 0


def under(path, root):
    return path == root or path.startswith(root + os.sep)


def check_write(path, cwd):
    if not path:
        return 0
    real = os.path.realpath(os.path.join(cwd or "/", os.path.expanduser(path)))
    if under(real, MEMORY) and real.endswith(".md"):
        return 0
    if os.path.dirname(real) == os.path.join(REPO, "knowledge", "clouds") and real.endswith(".draft.md"):
        return 0
    if any(under(real, root) for root in PROTECTED):
        return deny("`%s` is part of the agents' own rules and guards; only the user changes those" % path)
    for p in (path, real):
        if CONFIG_PATH.search(p):
            return deny("writing `%s` would change Claude Code settings, agents, skills or hooks" % path)
        if GIT_INTERNALS.search(p):
            return deny("writing inside `.git/` is not allowed (`%s`)" % path)
    for pattern, reason in ASK_WRITE:
        if pattern.search(real):
            return ask(reason)
    return 0


def main(data):
    if data.get("agent_type") != AGENT:
        return 0
    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    try:
        if tool == "Bash":
            return check_bash(tool_input.get("command", ""))
        if tool in JIRA_WRITE_TOOLS:
            return ask(JIRA_WRITE_TOOLS[tool])
        if tool in WRITE_TOOLS:
            return check_write(tool_input.get("file_path") or tool_input.get("notebook_path") or "",
                               data.get("cwd") or os.getcwd())
        return 0
    except Exception as e:  # fail toward asking, never toward silently allowing
        return ask("an unexpected guard error (%s)" % type(e).__name__)


