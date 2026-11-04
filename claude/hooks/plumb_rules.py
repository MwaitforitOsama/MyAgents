#!/usr/bin/env python3
"""Mr. Plumb guard: a Claude Code PreToolUse hook.

Active only when the session runs as the `plumb` agent (`claude --agent plumb`).
Every other session and agent passes through untouched.

Exit 0 = allow. Exit 2 = block; stderr is shown to the model.
This is an allowlist: anything not explicitly allowed is blocked.
Text inspection is not a sandbox. See README.md, "Limits of the guard".
"""

import json
import os
import re
import shlex
import sys
from urllib.parse import urlsplit

AGENT = "plumb"
REPO = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
SKILL = os.path.join(REPO, "skills", "plumb")
KNOWLEDGE = os.path.join(REPO, "knowledge")  # shared with Mason; skills/plumb/knowledge links here
SCRATCH = os.path.join(os.path.realpath("/tmp"), "plumb")

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


class Blocked(Exception):
    pass


def block(reason):
    raise Blocked(reason)


# ---------------------------------------------------------------- paths

def resolve(path, cwd):
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(cwd or "/", path)
    return os.path.realpath(path)


def under(path, root):
    return path == root or path.startswith(root + os.sep)


def check_output_path(path, cwd):
    if path in ("/dev/null", "-"):
        return
    if not path or not under(resolve(path, cwd), SCRATCH):
        block("output files may only go to /tmp/plumb/ (got `%s`)" % path)


def check_write(path, cwd):
    if not path:
        block("no file path given")
    real = resolve(path, cwd)
    if under(real, SCRATCH):
        return
    if real.endswith(".md"):
        if under(real, os.path.join(SKILL, "memory")):
            return
        if os.path.dirname(real) == os.path.join(KNOWLEDGE, "clouds") and real.endswith(".draft.md"):
            return
        parts = real.split(os.sep)
        for i in range(len(parts) - 2):
            if parts[i] == "docs" and parts[i + 1] in ("adr", "plans"):
                return
    block("Mr. Plumb may only write .md files under docs/adr/, docs/plans/, its own memory/, "
          "knowledge/clouds/*.draft.md, or anything under /tmp/plumb/ (got `%s`)" % path)


# ---------------------------------------------------------------- helpers

def flag_values(args, names, short_attach=False):
    """Values for flags in `names`: `-o x`, `-o=x`, and with short_attach `-ox`."""
    values = []
    for i, a in enumerate(args):
        for n in names:
            if a == n:
                values.append(args[i + 1] if i + 1 < len(args) else "")
            elif a.startswith(n + "="):
                values.append(a[len(n) + 1:])
            elif short_attach and len(n) == 2 and not a.startswith("--") and a.startswith(n) and len(a) > 2:
                values.append(a[2:])
    return values


def has_flag(args, names, short_attach=False):
    for a in args:
        for n in names:
            if a == n or a.startswith(n + "="):
                return True
            if short_attach and len(n) == 2 and not a.startswith("--") and a.startswith(n):
                return True
    return False


def forbid_flags(args, names, short_attach=False):
    for a in args:
        for n in names:
            if a == n or a.startswith(n + "=") or (
                    short_attach and len(n) == 2 and not a.startswith("--") and a.startswith(n)):
                block("flag `%s` is not allowed" % a)


def positionals(args):
    return [a for a in args if not a.startswith("-")]


def outputs_to_scratch(args, names, cwd, short_attach=False):
    for v in flag_values(args, names, short_attach):
        check_output_path(v, cwd)


FIX_FLAGS = ["--fix", "--write", "-w", "--update", "-u", "--updateSnapshot"]


# ---------------------------------------------------------------- simple commands

def allow_any(args, env, cwd):
    return


def check_find(args, env, cwd):
    forbid_flags(args, ["-delete", "-exec", "-execdir", "-ok", "-okdir",
                        "-fprint", "-fprint0", "-fprintf", "-fls"])


def check_tree(args, env, cwd):
    forbid_flags(args, ["-o"], short_attach=True)


def check_sort(args, env, cwd):
    forbid_flags(args, ["-o", "--output"], short_attach=True)


def check_uniq(args, env, cwd):
    if len(positionals(args)) > 1:
        block("`uniq INPUT OUTPUT` writes a file")


def check_rg(args, env, cwd):
    forbid_flags(args, ["--pre"])


def check_mkdir(args, env, cwd):
    for p in positionals(args):
        if not under(resolve(p, cwd), SCRATCH):
            block("`mkdir` is only allowed under /tmp/plumb/")


# ---------------------------------------------------------------- text tools (read-only forms)

SED_SIMPLE_CMDS = set("pdqQ=lnNgGhHxFDPz")
SED_S_FLAGS = set("gpiIm0123456789")


def _sed_delimited(text, i, delim):
    """Index just past the closing `delim`, starting at i (inside the delimited part)."""
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == delim:
            return i + 1
        i += 1
    block("could not parse the sed script (unterminated `%s`)" % delim)


def _sed_address(text, i):
    if i < len(text) and text[i].isdigit():
        while i < len(text) and text[i].isdigit():
            i += 1
    elif i < len(text) and text[i] == "$":
        i += 1
    elif i < len(text) and text[i] == "/":
        i = _sed_delimited(text, i + 1, "/")
        if i < len(text) and text[i] in "IM":
            i += 1
    elif i + 1 < len(text) and text[i] == "\\":
        i = _sed_delimited(text, i + 2, text[i + 1])
    return i


def check_sed_command(cmd):
    i = _sed_address(cmd, 0)
    if i < len(cmd) and cmd[i] == ",":
        i += 1
        if i < len(cmd) and cmd[i] in "+~":
            i += 1
            while i < len(cmd) and cmd[i].isdigit():
                i += 1
        else:
            i = _sed_address(cmd, i)
    rest = cmd[i:].lstrip()
    if rest.startswith("!"):
        rest = rest[1:].lstrip()
    if not rest:
        return
    c = rest[0]
    if c in SED_SIMPLE_CMDS:
        if rest[1:].strip() and not rest[1:].strip().isdigit():
            block("could not parse sed command `%s`" % cmd)
        return
    if c in "sy" and len(rest) > 1:
        d = rest[1]
        if d in "\\\n" or d.isalnum():
            block("unsupported sed delimiter in `%s`" % cmd)
        j = _sed_delimited(rest, 2, d)
        j = _sed_delimited(rest, j, d)
        flags = rest[j:].strip()
        if c == "y" and flags:
            block("could not parse sed command `%s`" % cmd)
        if any(f not in SED_S_FLAGS for f in flags):
            block("sed `s` flag in `%s` is not allowed (w writes files, e runs commands)" % cmd)
        return
    block("sed command `%s` is not on the read-only list (p, d, q, =, l, n, s and y are; "
          "w, W, r, R and e are not)" % cmd)


def check_sed_script(script):
    # Split on ; and newlines outside of delimited parts is hard to do exactly. Splitting naively
    # can only cut a regex in half, which then fails to parse and is blocked: safe either way.
    for cmd in re.split(r"[;\n]", script):
        cmd = cmd.strip().strip("{}").strip()
        if cmd:
            check_sed_command(cmd)


def check_sed(args, env, cwd):
    scripts, i, have_script = [], 0, False
    while i < len(args):
        a = args[i]
        if a in ("-i", "-I", "--in-place") or a.startswith(("--in-place=", "-i")) or (
                a.startswith("-") and not a.startswith("--") and ("i" in a[1:] or "I" in a[1:])):
            block("`sed -i` edits files in place")
        if a in ("-f", "--file") or a.startswith(("--file=", "-f")):
            block("`sed -f` runs a script file the guard can't inspect")
        if a in ("-e", "--expression"):
            if i + 1 >= len(args):
                block("`sed -e` needs a script")
            scripts.append(args[i + 1])
            have_script = True
            i += 2
            continue
        if a.startswith("--expression="):
            scripts.append(a.split("=", 1)[1])
            have_script = True
        elif a.startswith("-") and a != "-":
            if a not in ("-n", "-E", "-r", "-s", "-u", "-z", "--quiet", "--silent", "--posix",
                         "--regexp-extended", "--separate", "--unbuffered", "--null-data", "--debug") and not (
                    not a.startswith("--") and all(c in "nErsuz" for c in a[1:])):
                block("sed option `%s` is not allowed" % a)
        elif not have_script:
            scripts.append(a)
            have_script = True
        i += 1
    for sc in scripts:
        check_sed_script(sc)


AWK_BAD = [
    (re.compile(r"\bsystem\s*\("), "`system()` runs commands"),
    (re.compile(r"\|"), "pipes inside awk run commands"),
    (re.compile(r"\bprintf?\b[^;{}\n]*>"), "`print > file` writes files"),
    (re.compile(r"\bgetline\b"), "`getline` can run commands or read other files"),
    (re.compile(r"\b(close|fflush)\s*\("), "awk I/O functions"),
    (re.compile(r"@load|@include"), "awk extensions"),
]


def check_awk(args, env, cwd):
    i, script_seen = 0, False
    while i < len(args):
        a = args[i]
        if a in ("-f", "--file") or a.startswith(("-f", "--file=")) or a in ("-i", "--include", "-l", "--load") or \
                a.startswith(("-i", "-l", "--include=", "--load=", "-E", "--exec")):
            block("awk option `%s` loads code the guard can't inspect" % a)
        if a in ("-F", "-v"):
            i += 2
            continue
        if a.startswith(("-F", "-v")) or a == "--":
            i += 1
            continue
        if a.startswith("-"):
            block("awk option `%s` is not allowed" % a)
        if not script_seen:
            for rx_, why in AWK_BAD:
                if rx_.search(a):
                    block("awk script not read-only: %s" % why)
            script_seen = True
        i += 1


def check_no_output_flags(names, max_positionals=None, what=""):
    def checker(args, env, cwd):
        forbid_flags(args, names, short_attach=True)
        if max_positionals is not None and len(positionals(args)) > max_positionals:
            block("`%s` with an output file argument writes a file" % what)
    return checker


def check_tar(args, env, cwd):
    if not args:
        block("`tar` needs list mode (`tar -tf <archive>`)")
    mode = args[0].lstrip("-")
    if "t" not in mode or any(c in mode for c in "cxurA"):
        block("only `tar -t` (list the archive) is allowed")
    for a in args[1:]:
        if a.startswith(("-x", "-c", "-u", "-r", "--extract", "--create", "--append", "--update", "--get",
                         "--to-command", "--use-compress-program", "-I", "--checkpoint-action", "--delete")):
            block("tar option `%s` is not allowed" % a)


def check_unzip(args, env, cwd):
    if not any(a in ("-l", "-v", "-Z", "-t", "-p", "-lv") or a.startswith(("-l", "-Z")) for a in args):
        block("only `unzip -l`, `-v`, `-Z`, `-t` or `-p` (list, test, print) is allowed")


def check_command(args, env, cwd):
    if not args or args[0] not in ("-v", "-V"):
        block("only `command -v` (look up a command) is allowed")


# ---------------------------------------------------------------- git

GIT_READ = {
    "log", "blame", "annotate", "diff", "show", "status", "rev-parse", "ls-files", "grep",
    "shortlog", "describe", "cat-file", "ls-tree", "merge-base", "rev-list", "show-ref",
    "for-each-ref", "count-objects", "whatchanged", "name-rev", "show-branch", "range-diff",
    "check-ignore", "version",
}
GIT_SAFE_CONFIG = re.compile(r"^(core\.pager=cat|color\.[\w.]+=\w+|core\.quotepath=\w+)$")


def check_git(args, env, cwd):
    i = 0
    while i < len(args) and args[i].startswith("-"):
        a = args[i]
        if a in ("-C", "--git-dir", "--work-tree", "--namespace"):
            i += 2
        elif a == "-c":
            if i + 1 >= len(args) or not GIT_SAFE_CONFIG.match(args[i + 1]):
                block("`git -c` is only allowed for core.pager=cat, color.*, core.quotepath")
            i += 2
        elif a.startswith(("--git-dir=", "--work-tree=", "--namespace=")) or a in (
                "--no-pager", "-P", "--no-optional-locks", "--literal-pathspecs", "--no-replace-objects"):
            i += 1
        else:
            block("unsupported git option `%s`" % a)
    if i >= len(args):
        block("`git` needs a read-only subcommand")
    sub, rest = args[i], args[i + 1:]

    if sub in ("commit", "push"):
        block("Mr. Plumb never commits or pushes. Commits and pushes are the user's decision")
    forbid_flags(rest, ["--output", "-O", "--open-files-in-pager", "--ext-diff"])

    if sub in GIT_READ:
        return
    if sub == "fetch":
        # Updates remote-tracking refs only. Refspecs with ':' could move local branches.
        forbid_flags(rest, ["--upload-pack", "--recurse-submodules", "--update-head-ok", "-u", "--refmap"])
        for a in positionals(rest):
            if ":" in a and "://" not in a:
                block("`git fetch` with a refspec (`%s`) could update local branches" % a)
        return
    if sub == "symbolic-ref":
        # Read form only, e.g. `git symbolic-ref --short refs/remotes/origin/HEAD`.
        if len(positionals(rest)) == 1 and all(a in ("--short", "-q", "--quiet") for a in rest if a.startswith("-")):
            return
        block("only the read form of `git symbolic-ref` is allowed")
    if sub == "branch":
        listing = {"-a", "--all", "-r", "--remotes", "-v", "-vv", "--verbose", "--list", "-l",
                   "--show-current", "--merged", "--no-merged", "--contains", "--no-contains",
                   "--points-at", "--sort", "--format", "--color", "--no-color", "--column", "--no-column"}
        takes_value = {"--merged", "--no-merged", "--contains", "--no-contains", "--points-at", "--sort", "--format"}
        is_list = "--list" in rest or "-l" in rest
        j = 0
        while j < len(rest):
            a = rest[j]
            base = a.split("=", 1)[0]
            if base in listing:
                j += 2 if (a in takes_value) else 1
            elif not a.startswith("-") and is_list:
                j += 1
            else:
                block("`git branch %s` would change branches; only listing is allowed" % a)
        return
    if sub == "remote":
        if not rest or rest[0] in ("-v", "--verbose", "show", "get-url"):
            return
    elif sub == "config":
        if rest and rest[0] in ("get", "list"):
            return
        reads = {"--get", "--get-all", "--get-regexp", "--list", "-l"}
        if any(a in reads for a in rest) and not any(
                a in ("--add", "--unset", "--unset-all", "--replace-all", "--edit", "-e",
                      "--rename-section", "--remove-section") for a in rest):
            return
    elif sub == "stash":
        if rest and rest[0] in ("list", "show"):
            return
    elif sub == "tag":
        if not rest or rest[0] in ("-l", "--list", "-n", "--contains", "--points-at", "--merged", "--no-merged"):
            return
    elif sub in ("worktree", "notes"):
        if rest and rest[0] in ("list", "show"):
            return
    elif sub == "reflog":
        if not rest or rest[0] == "show" or rest[0].startswith("-"):
            return
    elif sub == "submodule":
        if rest and rest[0] == "status":
            return
    block("`git %s` is not read-only" % " ".join([sub] + rest[:1]))


# ---------------------------------------------------------------- go

GO_OUTPUT_FLAGS = ["-o", "-coverprofile", "-cpuprofile", "-memprofile", "-blockprofile",
                   "-mutexprofile", "-trace", "-outputdir"]


def check_go(args, env, cwd):
    if not args:
        block("`go` needs a subcommand")
    sub = args[0]
    rest = ["-" + a[2:] if a.startswith("--") else a for a in args[1:]]
    forbid_flags(rest, ["-exec", "-toolexec"])
    if "-mod=mod" in rest:
        block("`-mod=mod` can rewrite go.mod")
    outputs_to_scratch(rest, GO_OUTPUT_FLAGS, cwd)

    if sub in ("test", "vet", "list", "version", "doc", "run"):
        if sub == "test" and "-c" in rest and not flag_values(rest, ["-o"]):
            block("`go test -c` writes a binary; add `-o /tmp/plumb/<name>`")
        return
    if sub == "build":
        if not flag_values(rest, ["-o"]):
            block("`go build` writes a binary; add `-o /tmp/plumb/<name>` or `-o /dev/null`")
        return
    if sub == "env":
        forbid_flags(rest, ["-w", "-u"])
        return
    if sub == "mod" and rest and rest[0] in ("graph", "why", "verify"):
        return
    block("`go %s` is not read-only" % " ".join(args[:2]))


# ---------------------------------------------------------------- node ecosystem

SCRIPT_OK = re.compile(r"^(dev|start|serve|preview|build|lint|test|e2e|typecheck|type-check|check|tsc)([:._-][\w:.-]*)?$")
SCRIPT_BAD = re.compile(r"fix|format|prettier|write|migrat|seed|deploy|publish|release|clean|reset|drop|purge|"
                        r"prune|install|upgrade|update|generate|codegen")
PM_READ = {"test", "t", "tst", "ls", "list", "ll", "la", "outdated", "view", "info", "show",
           "explain", "why", "audit", "query", "fund", "search", "start", "--version", "-v"}


def check_script(name):
    if not SCRIPT_OK.match(name) or SCRIPT_BAD.search(name):
        block("package script `%s` is not on the allowlist (allowed: dev, start, serve, preview, build, "
              "lint, test, e2e, typecheck, check and their :variants, without fix/format/migrate/seed/deploy/...)"
              % name)


def check_package_manager(args, env, cwd):
    if not args:
        block("needs a subcommand")
    forbid_flags(args, FIX_FLAGS)
    sub, rest = args[0], args[1:]
    if sub == "audit" and "fix" in rest:
        block("`audit fix` changes dependencies")
    if sub == "config":
        if rest and rest[0] in ("get", "list", "ls"):
            return
        block("only `config get/list` is allowed")
    if sub in PM_READ:
        return
    if sub in ("run", "run-script"):
        if not rest:
            return  # lists scripts
        check_script(rest[0])
        return
    check_script(sub)  # pnpm/yarn shorthand: `pnpm dev`, `yarn test`


def check_next(args, env, cwd):
    forbid_flags(args, FIX_FLAGS)
    if args and args[0] in ("info", "lint", "build", "dev", "start", "--version", "-v"):
        return
    block("only `next info|lint|build|dev|start` is allowed")


def check_ng(args, env, cwd):
    forbid_flags(args, FIX_FLAGS)
    if args and args[0] in ("version", "v", "test", "t", "serve", "s", "build", "b", "lint", "e2e", "--version"):
        return
    block("only `ng version|test|serve|build|lint|e2e` is allowed")


def check_playwright(args, env, cwd):
    if not args:
        block("needs a subcommand")
    if args[0] in ("--version", "test"):
        forbid_flags(args, FIX_FLAGS)
        return
    if args[0] == "screenshot":
        pos = positionals(args[1:])
        if len(pos) < 2:
            block("`playwright screenshot <url> <file>` needs an output file under /tmp/plumb/")
        check_output_path(pos[-1], cwd)
        return
    block("only `playwright test|screenshot|--version` is allowed")


def check_tsc(args, env, cwd):
    if "--noEmit" in args or args in (["-v"], ["--version"]):
        return
    block("`tsc` is only allowed with `--noEmit`")


def check_test_runner(args, env, cwd):
    forbid_flags(args, FIX_FLAGS)


def check_eslint(args, env, cwd):
    forbid_flags(args, ["--fix", "--fix-dry-run"])
    outputs_to_scratch(args, ["-o", "--output-file"], cwd)


def check_prettier(args, env, cwd):
    forbid_flags(args, ["--write", "-w"])
    if not has_flag(args, ["--check", "-c", "--list-different", "-l", "--version"]):
        block("`prettier` is only allowed with `--check` or `--list-different`")


NPX_TOOLS = {}  # filled below


def check_npx(args, env, cwd):
    i = 0
    while i < len(args) and args[i].startswith("-"):
        a = args[i]
        if a in ("-p", "--package", "-c", "--call") or a.startswith(("--package=", "--call=")):
            block("`npx %s` can run arbitrary packages or commands" % a)
        if a in ("--version", "-v"):
            return
        i += 1  # --no-install, --yes, --quiet, ...
    if i >= len(args):
        block("`npx` needs a tool")
    tool = args[i].split("@")[0] if not args[i].startswith("@") else args[i]
    checker = NPX_TOOLS.get(tool)
    if checker is None:
        block("`npx %s` is not on the allowlist" % args[i])
    checker(args[i + 1:], env, cwd)


def check_node(args, env, cwd):
    if args in (["--version"], ["-v"]):
        return
    forbid_flags(args, ["-e", "--eval", "-p", "--print"])
    if not positionals(args):
        block("`node` without a script opens a REPL")


# ---------------------------------------------------------------- docker

DOCKER_READ = {"ps", "logs", "inspect", "images", "version", "info", "stats", "top", "port", "diff", "history"}
DOCKER_MGMT_READ = {"ls", "list", "inspect", "history", "df"}
COMPOSE_OK = {"config", "ps", "logs", "ls", "images", "top", "version", "port", "up", "down"}
COMPOSE_VALUE_FLAGS = {"-f", "--file", "-p", "--project-name", "--project-directory", "--profile",
                       "--env-file", "--ansi", "--progress", "--parallel"}


def check_compose(args, env, cwd):
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in COMPOSE_VALUE_FLAGS else 1
    if i >= len(args):
        block("`compose` needs a subcommand")
    sub, rest = args[i], args[i + 1:]
    if sub not in COMPOSE_OK:
        block("`compose %s` is not allowed (allowed: %s)" % (sub, ", ".join(sorted(COMPOSE_OK))))
    if sub == "down":
        forbid_flags(rest, ["-v", "--volumes", "--rmi"])
    if sub == "config":
        outputs_to_scratch(rest, ["-o", "--output"], cwd)


def check_docker(args, env, cwd):
    if not args:
        block("`docker` needs a subcommand")
    sub, rest = args[0], args[1:]
    if sub == "compose":
        return check_compose(rest, env, cwd)
    if sub in DOCKER_READ:
        return
    if sub in ("image", "container", "volume", "network", "context", "system"):
        if rest and rest[0] in DOCKER_MGMT_READ:
            return
    if sub in ("--version", "-v"):
        return
    block("`docker %s` is not read-only" % " ".join(args[:2]))


# ---------------------------------------------------------------- databases

SQL_WRITE = re.compile(
    r"\b(insert|update|delete|merge|upsert|drop|alter|truncate|create|grant|revoke|copy|vacuum|reindex|"
    r"cluster|comment|lock|refresh|call|do|import|reassign|discard|prepare|execute|load|into|listen|notify)\b",
    re.I)
SQL_TXN = re.compile(r"read[\s_]+write|transaction_read_only|session\s+characteristics|session\s+authorization|"
                     r"\bset\s+role\b|\breset\b", re.I)
SQL_FUNCS = re.compile(r"\b(pg_terminate_backend|pg_cancel_backend|lo_\w+|dblink\w*|pg_reload_conf|set_config|"
                       r"pg_file_write|pg_rotate_logfile|nextval|setval|pg_read_\w*file)\s*\(", re.I)
PSQL_META = re.compile(r"\\([A-Za-z!?]+\+?)")
PSQL_META_OK = {"l", "l+", "x", "conninfo", "timing", "?"}


def check_sql(sql):
    if SQL_WRITE.search(sql):
        block("SQL contains a write or DDL keyword (`%s`)" % SQL_WRITE.search(sql).group(0))
    if SQL_TXN.search(sql) or SQL_FUNCS.search(sql):
        block("SQL tries to change transaction/session state or call a side-effect function")
    for m in PSQL_META.finditer(sql):
        meta = m.group(1)
        if not meta.startswith("d") and meta not in PSQL_META_OK:
            block("psql meta-command `\\%s` is not allowed (only \\d*, \\l, \\x, \\conninfo, \\timing)" % meta)


def check_psql(args, env, cwd):
    if "default_transaction_read_only=on" not in env.get("PGOPTIONS", "").replace(" ", ""):
        block("run psql as `PGOPTIONS='-c default_transaction_read_only=on' psql ...` "
              "(and prefer a read-only database user)")
    forbid_flags(args, ["-f", "--file", "-o", "--output", "-L", "--log-file"], short_attach=True)
    for a in args:
        if "transaction_read_only" in a or "options=" in a:
            block("connection options may not override read-only mode")
    sqls = flag_values(args, ["-c", "--command"], short_attach=True)
    if not sqls:
        block("psql needs `-c \"<read-only SQL>\"` (interactive psql is not available)")
    for sql in sqls:
        check_sql(sql)


def check_pg_dump(args, env, cwd):
    if not has_flag(args, ["-s", "--schema-only"]):
        block("`pg_dump` is only allowed with `--schema-only` (to stdout)")
    forbid_flags(args, ["-f", "--file", "-F", "--format"], short_attach=True)


MONGO_WRITE = re.compile(
    r"\.\s*(insert\w*|update\w*|delete\w*|remove\w*|replace\w*|drop\w*|create\w*|rename\w*|bulkWrite|"
    r"findOneAnd\w*|findAndModify|save|grant\w*|revoke\w*|shutdownServer|fsync\w*|compact|repairDatabase|"
    r"setProfilingLevel|killOp|runCommand|adminCommand|eval|mapReduce|hideIndex|unhideIndex|reIndex|"
    r"convertToCapped|initialize\w*BulkOp|watch)\s*\(")
MONGO_STAGES = re.compile(r"\$(out|merge)\b")
MONGO_GLOBALS = re.compile(r"\b(load|require|eval|Function|process|fs|exec|spawn|writeFile|runProgram)\s*[.(]")
MONGO_ADMIN = re.compile(r"\b(rs|sh)\.(\w+)\s*\(")


def check_mongosh(args, env, cwd):
    forbid_flags(args, ["--file", "-f", "--shell"])
    evals = flag_values(args, ["--eval"])
    if not evals:
        block("mongosh needs `--eval \"<read-only query>\"` (interactive shell is not available)")
    if any(p.endswith(".js") for p in positionals(args)):
        block("running .js files is not allowed")
    for code in evals:
        for rx in (MONGO_WRITE, MONGO_STAGES, MONGO_GLOBALS):
            m = rx.search(code)
            if m:
                block("Mongo query contains a write or unsafe operation (`%s`)" % m.group(0))
        for m in MONGO_ADMIN.finditer(code):
            if m.group(2) not in ("status", "conf", "printReplicationInfo", "printSecondaryReplicationInfo"):
                block("`%s.%s()` is an admin operation" % (m.group(1), m.group(2)))


# ---------------------------------------------------------------- clouds

def command_path(args):
    """Tokens of the command path: positionals before the first flag (skipping leading global flags)."""
    i = 0
    while i < len(args) and args[i].startswith("-"):
        i += 1 if "=" in args[i] else 2
    path = []
    for a in args[i:]:
        if a.startswith("-"):
            break
        path.append(a)
    return path


def check_cloud(name, read_verbs, bad_words, args, cwd, extra=None):
    if args in (["--version"], ["version"], ["-v"]):
        return
    path = command_path(args)
    lowered = [p.lower() for p in path]
    for p in lowered:
        if p in bad_words:
            block("`%s %s` is not read-only or reveals credentials" % (name, " ".join(path)))
    if not any(p in read_verbs for p in lowered):
        block("`%s` is only allowed with read verbs (%s)" % (name, ", ".join(sorted(read_verbs))))
    if extra:
        extra(path, args, cwd)


GCLOUD_READ = {"list", "describe", "get-iam-policy", "read", "get-value", "get", "info"}
GCLOUD_BAD = {"access", "print-access-token", "print-identity-token", "print-refresh-token", "get-credentials",
              "ssh", "scp", "create", "delete", "update", "set", "unset", "deploy", "add-iam-policy-binding",
              "remove-iam-policy-binding", "set-iam-policy", "login", "revoke", "activate", "enable", "disable",
              "import", "export", "execute", "submit", "cancel", "start", "stop", "reset", "resize",
              "restore", "undelete", "cp", "mv", "rm", "rsync", "patch", "apply", "generate-login-token",
              "configure-docker", "cat", "sign-url", "connect"}

OCI_READ = {"list", "get"}
OCI_BAD = {"secret-bundle", "create", "delete", "update", "put", "bulk-download", "bulk-upload", "download",
           "upload", "generate", "rotate", "change-compartment", "copy", "restore", "terminate", "action",
           "launch", "attach", "detach", "patch", "apply", "reset", "sync", "import", "export", "raw-request",
           "setup", "session", "reencrypt", "schedule-key-deletion", "schedule-secret-deletion"}

DOCTL_READ = {"list", "get", "ls", "logs"}
DOCTL_BAD = {"kubeconfig", "docker-config", "login", "init", "switch", "ssh", "create", "delete", "update", "rm",
             "remove", "add", "attach", "detach", "resize", "power-off", "power-on", "power-cycle", "reboot",
             "shutdown", "restore", "snapshot", "rebuild", "rename", "enable-backups", "disable-backups",
             "tag", "untag", "deploy", "upgrade", "apply", "connect", "connection", "user", "users", "pool",
             "reset", "migrate"}


def oci_extra(path, args, cwd):
    for v in flag_values(args, ["--file"]):
        check_output_path(v, cwd)


def check_gcloud(args, env, cwd):
    check_cloud("gcloud", GCLOUD_READ, GCLOUD_BAD, args, cwd)


def check_oci(args, env, cwd):
    check_cloud("oci", OCI_READ, OCI_BAD, args, cwd, oci_extra)


def check_doctl(args, env, cwd):
    check_cloud("doctl", DOCTL_READ, DOCTL_BAD, args, cwd)


KUBECTL_VERBS = {"get", "describe", "logs", "top", "explain", "api-resources", "api-versions", "version",
                 "cluster-info", "auth", "config", "apply", "delete", "edit", "exec", "scale", "rollout", "patch",
                 "create", "replace", "run", "expose", "set", "label", "annotate", "cp", "port-forward", "proxy",
                 "attach", "drain", "cordon", "uncordon", "taint", "debug", "autoscale", "certificate",
                 "kustomize", "wait", "events", "diff", "plugin", "alpha"}
KUBECTL_OK = {"get", "describe", "logs", "top", "explain", "api-resources", "api-versions", "version",
              "cluster-info", "auth", "config", "events"}


def check_kubectl(args, env, cwd):
    verb_i = next((i for i, a in enumerate(args) if a in KUBECTL_VERBS), None)
    if verb_i is None:
        block("`kubectl` needs a read-only verb (get, describe, logs, top, explain, ...)")
    verb, rest = args[verb_i], args[verb_i + 1:]
    if verb not in KUBECTL_OK:
        block("`kubectl %s` changes the cluster or opens access; only read verbs are allowed" % verb)
    if verb in ("get", "describe", "events"):
        for a in rest:
            for part in re.split(r"[,/]", a.lower()):
                if part in ("secret", "secrets") or part.startswith("secrets."):
                    block("reading Kubernetes secrets is not allowed")
    if verb == "config":
        if not rest or rest[0] not in ("get-contexts", "current-context", "view", "get-clusters"):
            block("only `kubectl config get-contexts|current-context|view|get-clusters` is allowed")
        forbid_flags(rest, ["--raw", "--flatten"])
    if verb == "auth" and (not rest or rest[0] not in ("can-i", "whoami")):
        block("only `kubectl auth can-i|whoami` is allowed")
    if verb == "cluster-info" and "dump" in rest:
        block("`cluster-info dump` writes files")


# ---------------------------------------------------------------- local http + browser

LOCAL_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}


def check_curl(args, env, cwd):
    forbid_flags(args, ["-d", "--data", "--data-raw", "--data-binary", "--data-urlencode", "-F", "--form",
                        "-T", "--upload-file", "-K", "--config", "--json", "-O", "--remote-name",
                        "--remote-name-all"], short_attach=True)
    for method in flag_values(args, ["-X", "--request"], short_attach=True):
        if method.upper() not in ("GET", "HEAD", "OPTIONS"):
            block("curl may only send GET/HEAD/OPTIONS")
    outputs_to_scratch(args, ["-o", "--output"], cwd, short_attach=True)
    value_flags = {"-o", "--output", "-X", "--request", "-H", "--header", "-m", "--max-time", "-w",
                   "--write-out", "--connect-timeout", "-A", "--user-agent", "-e", "--referer"}
    urls, skip = [], False
    for a in args:
        if skip:
            skip = False
            continue
        if a in value_flags:
            skip = True
        elif not a.startswith("-"):
            urls.append(a)
    if not urls:
        block("curl needs a URL")
    for u in urls:
        host = urlsplit(u if "://" in u else "http://" + u).hostname
        if host not in LOCAL_HOSTS:
            block("curl may only call the locally running project (localhost); use WebFetch for docs")


def check_chrome(args, env, cwd):
    if not any(a == "--headless" or a.startswith("--headless=") for a in args):
        block("Chrome is only allowed with `--headless`")
    for a in args:
        if a in ("--screenshot", "--print-to-pdf"):
            block("`%s` needs an explicit path under /tmp/plumb/ (e.g. %s=/tmp/plumb/page.png)" % (a, a))
    outputs_to_scratch(args, ["--screenshot", "--print-to-pdf", "--user-data-dir"], cwd)


# ---------------------------------------------------------------- table

CHECKERS = {
    # files and shell basics
    "ls": allow_any, "cat": allow_any, "head": allow_any, "tail": allow_any, "wc": allow_any,
    "grep": allow_any, "egrep": allow_any, "fgrep": allow_any, "cut": allow_any, "diff": allow_any,
    "file": allow_any, "stat": allow_any, "du": allow_any, "df": allow_any, "pwd": allow_any,
    "echo": allow_any, "printf": allow_any, "which": allow_any, "date": allow_any, "uname": allow_any,
    "sleep": allow_any, "lsof": allow_any, "ps": allow_any, "cd": allow_any, "true": allow_any,
    "test": allow_any, "basename": allow_any, "dirname": allow_any, "realpath": allow_any, "jq": allow_any,
    "whoami": allow_any, "hostname": allow_any, "mkdir": check_mkdir,
    "find": check_find, "tree": check_tree, "sort": check_sort, "uniq": check_uniq, "rg": check_rg,
    # more read-only text and file inspection
    "sed": check_sed, "awk": check_awk, "gawk": check_awk, "nawk": check_awk, "mawk": check_awk,
    "nl": allow_any, "tr": allow_any, "column": allow_any, "paste": allow_any, "comm": allow_any,
    "join": allow_any, "fold": allow_any, "expand": allow_any, "unexpand": allow_any, "rev": allow_any,
    "tac": allow_any, "seq": allow_any, "cmp": allow_any, "readlink": allow_any, "strings": allow_any,
    "od": allow_any, "hexdump": allow_any, "md5": allow_any, "md5sum": allow_any, "shasum": allow_any,
    "sha1sum": allow_any, "sha256sum": allow_any, "cksum": allow_any, "type": allow_any,
    "zcat": allow_any, "gzcat": allow_any, "bzcat": allow_any, "xzcat": allow_any, "ag": allow_any,
    "ack": allow_any, "bat": allow_any, "less": allow_any, "more": allow_any, "look": allow_any,
    "xxd": check_no_output_flags(["-r", "-revert"], max_positionals=1, what="xxd"),
    "base64": check_no_output_flags(["-o", "--output"], max_positionals=1, what="base64"),
    "iconv": check_no_output_flags(["-o", "--output"]),
    "yq": check_no_output_flags(["-i", "--inplace", "--split-exp", "-s"]),
    "fd": check_no_output_flags(["-x", "-X", "--exec", "--exec-batch"]),
    "fdfind": check_no_output_flags(["-x", "-X", "--exec", "--exec-batch"]),
    "tar": check_tar, "unzip": check_unzip, "command": check_command,
    # vcs + languages
    "git": check_git, "go": check_go,
    "npm": check_package_manager, "pnpm": check_package_manager, "yarn": check_package_manager,
    "npx": check_npx, "node": check_node, "next": check_next, "ng": check_ng,
    "playwright": check_playwright, "tsc": check_tsc, "jest": check_test_runner, "vitest": check_test_runner,
    "eslint": check_eslint, "prettier": check_prettier,
    # containers + databases
    "docker": check_docker, "docker-compose": check_compose,
    "psql": check_psql, "pg_dump": check_pg_dump, "mongosh": check_mongosh, "mongo": check_mongosh,
    # clouds + kubernetes
    "gcloud": check_gcloud, "oci": check_oci, "doctl": check_doctl, "kubectl": check_kubectl,
    # local http + headless browser
    "curl": check_curl,
    "Google Chrome": check_chrome, "google-chrome": check_chrome, "google-chrome-stable": check_chrome,
    "chromium": check_chrome, "chromium-browser": check_chrome, "Chromium": check_chrome,
}


NPX_TOOLS.update({"next": check_next, "ng": check_ng, "@angular/cli": check_ng, "playwright": check_playwright,
                  "tsc": check_tsc, "jest": check_test_runner, "vitest": check_test_runner,
                  "eslint": check_eslint, "prettier": check_prettier})


# ---------------------------------------------------------------- bash parsing

SEPARATORS = {";", "&&", "||", "|", "|&", "&", "(", ")"}
OUT_REDIRECTS = {">", ">>", ">|", "&>", "&>>"}
FD_DUPS = {">&", "<&"}
ENV_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
BAD_ENV = re.compile(r"^(PATH|BASH_ENV|ENV|SHELLOPTS|PS4|PROMPT_COMMAND|NODE_OPTIONS|LD_\w+|DYLD_\w+|GIT_\w+|"
                     r"PAGER|MANPAGER|EDITOR|VISUAL|PSQL_PAGER|PSQLRC|IFS)=")


def split_segments(command, cwd):
    if "`" in command or "$(" in command:
        block("command substitution (`...` or $(...)) is not allowed")
    if "<<" in command:
        block("heredocs are not allowed")
    lex = shlex.shlex(command.replace("\n", " ; "), posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    try:
        tokens = list(lex)
    except ValueError as e:
        block("could not parse the command (%s)" % e)

    segments, cur, i = [], [], 0
    while i < len(tokens):
        t = tokens[i]
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        if t in SEPARATORS:
            if cur:
                segments.append(cur)
            cur = []
        elif t in OUT_REDIRECTS:
            check_output_path(nxt, cwd)
            if cur and cur[-1].isdigit():
                cur.pop()
            i += 1
        elif t in FD_DUPS:
            if not (nxt.isdigit() or nxt == "-"):
                block("unsupported redirection `%s %s`" % (t, nxt))
            if cur and cur[-1].isdigit():
                cur.pop()
            i += 1
        elif t == "<":
            i += 1  # reading a file is fine
        elif t and all(c in "();<>|&" for c in t):
            block("unsupported shell syntax `%s`" % t)
        else:
            cur.append(t)
        i += 1
    if cur:
        segments.append(cur)
    return segments


def check_segment(words, cwd):
    env = {}
    while words and ENV_ASSIGN.match(words[0]):
        if BAD_ENV.match(words[0]):
            block("setting `%s` is not allowed" % words[0].split("=", 1)[0])
        key, value = words[0].split("=", 1)
        env[key] = value
        words = words[1:]
    if not words:
        return
    name = os.path.basename(words[0])
    checker = CHECKERS.get(name)
    if checker is None:
        block("`%s` is not on Mr. Plumb's read-only allowlist" % name)
    checker(words[1:], env, cwd)


def check_bash(command, cwd):
    if not command.strip():
        return
    for seg in split_segments(command, cwd):
        check_segment(seg, cwd)


# ---------------------------------------------------------------- main

def main(data):
    if data.get("agent_type") != AGENT:
        return 0

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    cwd = data.get("cwd") or os.getcwd()
    try:
        if tool == "Bash":
            check_bash(tool_input.get("command", ""), cwd)
        elif tool in WRITE_TOOLS:
            check_write(tool_input.get("file_path") or tool_input.get("notebook_path") or "", cwd)
        return 0
    except Blocked as e:
        reason = str(e)
    except Exception as e:  # fail closed for plumb
        reason = "guard error (%s: %s); blocked to be safe" % (type(e).__name__, e)
    sys.stderr.write(
        "Mr. Plumb guard blocked this: %s.\n"
        "Mr. Plumb is read-only. Do not try to work around this block. Tell the user what you "
        "wanted to run and why, and let them decide.\n" % reason)
    return 2


