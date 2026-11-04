# OsamaAgents

Personal AI agents, defined once and usable across models and harnesses.

Two agents that work together, with you approving every step:

- **Mr. Plumb** plans and reviews (read-only, runs on Fable).
- **Mason** implements (writes code, runs on Opus). It also works on its own.

## Working together

Start each agent in its own terminal, **in the same project directory**:

```bash
claude --agent plumb -n plumb     # plans and reviews
claude --agent mason -n mason     # implements
```

They find each other by those names and exchange short messages with Claude Code's cross-session messaging (`ListAgents` / `SendMessage`). The plan file in `docs/plans/` is the contract: messages only point to it. The full protocol is in `shared/rules/handoff.md`.

1. Mr. Plumb writes a plan. When you accept it, Plumb asks **"Assign this plan to Mason?"**
2. On yes, Mason checks the plan against the code and doesn't trust it blindly. If something is wrong, it opens a dispute with Plumb in the plan file (at most 2 exchanges each way). Then Mason brings you the issue, both positions and every option raised, as a multiple-choice question. Nothing disputed is built until you decide.
3. Mason implements, runs tests, lint and build, and sends the work to Plumb for review. The changes stay uncommitted.
4. If Plumb finds problems, it asks you **"Send these findings back to Mason?"** before sending them. At most 3 rounds, then you decide.
5. When the review passes, Mason asks you about commit, push or PR. Each one is a separate yes.

If Plumb needs a command its guard blocks, it can send it to Mason as a `RUN_REQUEST`. Mason **always** asks you first (run / don't run / run a changed version), whatever mode it is in.

**Approvals:** everything goes through you until **you** change the permission mode (Shift+Tab, or allow rules via `/permissions`). Neither agent treats a chat message, from you or from the other agent, as a change to its permissions. Even after you grant freedom, Mason's guard still forces a prompt for commit, push, deploys, cloud changes, migrations and destructive commands.

## Mason: implementation agent

Mason writes and changes code in Go, Angular, Next.js, React Native, JavaScript/TypeScript, CSS and HTML, and handles DigitalOcean and OCI infrastructure. It reads the code and its callers before changing anything, follows the project's existing patterns, adds tests, and reports real check results.

- **From a plan:** "implement docs/plans/2026-11-03-x.md", or a `PLAN_READY` message from Plumb.
- **Standalone:** ask it directly. For small tasks it writes a short plan in chat and asks before starting. For large or hard-to-undo work (database, auth, API contract, cloud architecture) it recommends Plumb plan it first.
- **Jira and Fullstory:** read-only, like Plumb.

### What Mason's guard enforces (`claude --agent mason` only)

- **Always prompt, in every mode:** git commit/push/merge/rebase/reset/tag/branch deletion, `gh` actions, image pushes, `kubectl`/`helm`/Terraform changes, cloud CLI commands that aren't list/get/describe (DigitalOcean, OCI, GCP, AWS, Azure), hosting deploys, app store builds, package publishing, database writes and migrations, `rm -rf`, remote access (`ssh`, `scp`, `rsync`), HTTP writes to remote hosts, `sudo`, and shell indirection that could hide any of these (`eval`, `sh -c`, `| bash`, `xargs`, `python -c`). Writing `.env` files, keys and CI/CD pipelines also prompts.
- **Blocked:** changing Claude Code settings, permissions, hooks, agents or skills, writing inside `.git/`, and editing the agents' own rules in this repo. Mason's own `memory/` is allowed.
- **Subagents:** Mason may only spawn `Explore` and `fullstory:session-context`, both read-only. Anything else would run outside the guard.
- Tests: `python3 claude/hooks/tests/run_mason_tests.py`.

### Limits of Mason's guard

1. **It's text matching, not a sandbox.** A false match costs one extra prompt. A deliberately disguised command could slip through. In the default mode Claude Code prompts for everything anyway.
2. **It can't tell which commands came from Plumb.** "Plumb's requests always ask" outside the guard's list relies on Mason's instructions once you've granted more freedom.
3. **Bash edits to the protected repo folders** (as opposed to Write/Edit) aren't blocked by path. They prompt in the default mode.

## Mr. Plumb: architecture advisor

Mr. Plumb questions, recommends and documents architecture decisions. It reads your code, asks only what the code can't answer, backs every claim with evidence (code, official docs, community practice), stays neutral between options, and writes ADRs and plans. It never implements, commits or pushes.

Modes: **greenfield · feature · debugging · bugfix · refactoring · migration · review**

Reviews: check out the branch yourself, then ask "review feature/XX-100-SDK-logs" or "review my changes". The review appears in chat with copy-ready PR comments. Mr. Plumb never checks out or posts anything.

Questions are always multiple choice, with Mr. Plumb's recommendation first.

**Jira and Fullstory (read-only).** In `claude --agent plumb`, Mr. Plumb can read Jira tickets (Atlassian MCP) and review Fullstory sessions (Fullstory plugin) while debugging. Only read tools appear in the agent's `tools:` list (`claude/agents/plumb.md`), so it cannot comment on, edit, transition or create tickets, or build segments or metrics. Rules: `skills/plumb/rules/tickets-and-sessions.md`. Prerequisites on each device: the `atlassian` MCP server (`https://mcp.atlassian.com/v1/mcp`, user scope) and the `fullstory@fullstory` plugin, both signed in. Never use a server wildcard like `mcp__atlassian__*` in `tools:`, because it would also grant the write tools.

### Install (any device)

```bash
git clone <your-private-repo-url> ~/Documents/OsamaAgents
cd ~/Documents/OsamaAgents
./install.sh
```

Requirements: `python3` (guard hooks), `jq` (settings edit), Claude Code 2.1.224 or later (cross-session messaging).

`install.sh` (installs both agents):
1. Symlinks `skills/plumb` and `skills/mason` into `~/.claude/skills/`, and `claude/agents/plumb.md` and `mason.md` into `~/.claude/agents/`.
2. For each guard hook, shows the diff and asks before adding it to `~/.claude/settings.json` (backup kept).
3. Runs both guard test suites.

Uninstall: `./install.sh --uninstall`. Because the install uses symlinks, `git pull` updates both agents immediately.

### Use

| Situation | How | Enforcement |
|---|---|---|
| Dedicated architecture session | `claude --agent plumb -n plumb` | Guard hook (hard) + rules (soft) |
| Regular Claude Code chat | Auto-triggers on architecture topics, or `/plumb` | Rules only (soft). That chat can still commit if you ask. |
| Other agents (e.g. Mason) | — | Not affected by Plumb's guard |

### What the guard enforces (`claude --agent plumb` only)

- **Bash:** an allowlist of read-only commands plus tests and running the project. Details are in `skills/plumb/rules/commands.md`, and the code is in `claude/hooks/plumb_guard.py`. Commit/push and anything not on the list are blocked.
- **Git:** read-only commands plus `git fetch`. Checkout, switch, pull, rebase, merge, commit and push are blocked.
- **Writes:** only `.md` files in `docs/adr/`, `docs/plans/`, Mr. Plumb's `memory/`, `knowledge/clouds/*.draft.md`, plus anything in `/tmp/plumb/`.
- Tests: `python3 claude/hooks/tests/run_guard_tests.py` (add a case to `guard-cases.txt` whenever you change the allowlist).

### Limits of the guard

1. **Tests and running the project execute the project's own code.** `npm test`, `npm run dev`, `go run` and `docker compose up` can do whatever their scripts do. The guard sees only the command.
2. **Database read-only mode is best-effort.** Postgres runs with `default_transaction_read_only=on` and write SQL is blocked by keyword. Mongo writes are blocked by method name. **Use a read-only database user for real protection.**
3. **Text inspection is not a sandbox.** It catches realistic commands, not deliberate evasion.
4. Subagents spawned from a plumb session would not be guarded, so the `plumb` agent has no Agent tool.

## Layout

```
skills/plumb/        Mr. Plumb: SKILL.md, modes/, rules/, templates/, memory/
skills/mason/        Mason: SKILL.md, rules/, memory/
shared/rules/        rules both agents use (handoff, evidence, questioning, bias, tickets-and-sessions), linked into each skill's rules/
knowledge/           stack and cloud files both agents use, linked into each skill as knowledge/
claude/              Claude Code wrappers (agents/plumb.md, agents/mason.md), guard hooks + tests, hook registration
evals/               behavior scenarios to compare models
install.sh           installer
```

## Portability

`skills/plumb/` and `skills/mason/` follow the Agent Skills format (`SKILL.md`), which Claude Code, OpenAI Codex CLI and Gemini CLI support. To use them with Codex or Gemini later, link them into their skills folder (verify the current path in their docs). The shared `rules/` and `knowledge/` entries are relative symlinks inside the repo, so keep the repo whole. The guard hooks and cross-session messaging are Claude Code–specific. Other harnesses need their own permission settings and a manual handoff (you tell each agent the plan is ready).

Offline use (Ollama + local models) is planned. It will be tested later.
