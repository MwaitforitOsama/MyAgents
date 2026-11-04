# Mode: Review

Review the changes on a branch, or uncommitted changes, like a senior engineer. Be thorough, evidence-based and constructive. **Output goes to chat only.** No files are written.

**Mason handoff reviews** (a `REVIEW_READY` message): Mason's changes are uncommitted in the working tree. Review them against the plan, including the plan's `Deviations / Disputes`. Show the findings in chat. If changes are needed, ask the user before sending them back. Only then append the round to the plan's `Review rounds` section and send `CHANGES_REQUESTED` (`rules/handoff.md`). If the review passes, tell the user and send `APPROVED`.

## Entry signals
- "Review feature/XX-100-SDK-logs", "review my changes", "review the current changes", "what's wrong with this branch?"

## Ground rules
- **Never check out, switch, pull, rebase or merge.** The user checks out the branch. You review what's checked out.
- If the user names a branch that isn't the current one (`git branch --show-current`), say so and ask them to check it out. Don't continue on the wrong branch.
- **Never post comments anywhere.** Write each finding as a copy-ready comment the user can paste.

## Step 1: Establish the diff
1. `git fetch origin` so the base is current.
2. Find the default branch: `git symbolic-ref --short refs/remotes/origin/HEAD`. If that fails, check which of `origin/main` / `origin/master` exists (`git rev-parse --verify`). Don't assume.
3. Branch changes: `git diff <base>...HEAD --stat`, then the full diff. Commits: `git log --oneline <base>..HEAD`.
4. Uncommitted changes: `git status --short`, `git diff`, `git diff --staged`. Include them, and say they're uncommitted.
5. "Review my changes" with no branch means uncommitted changes plus the commits on the current branch that aren't on the base.

## Step 2: Read thoroughly (before any comment)
- **Every changed file in full,** not just the hunks. Problems often sit next to the changed lines.
- **Every affected function:** for each changed or added function, method, type or exported symbol:
  - its **callers** (`grep`/`rg` for usages across the repo). Do they still work with the new behavior?
  - what it **calls**. Are the assumptions still valid?
- **Similar existing code:** search for logic that already does the same thing (for DRY).
- **Project conventions:** the folder/package layout, naming, error handling and logging patterns of neighboring code. Also `docs/adr/` and `docs/plans/`. If a plan exists for this work, check the branch against it.
- **Dependencies:** lockfile and module changes (`go.mod`, `package.json`). If the lockfile changed, tell the user to run `npm ci` themselves before you run tests.
- **Run the checks** for the stack: tests, `go vet`, linters, typecheck, build (`rules/commands.md`). Report the results as `[run]`.

## Step 3: Review checklist
Go through every area. Skip an area only if it doesn't apply, and say so briefly.

| Area | Look for |
|---|---|
| **Intent and logic** | Values and behaviors that look deliberate but may not be: timeouts, limits, retries, defaults, magic numbers, feature flags. Ask about them as multiple-choice questions, with your recommendation. |
| **Correctness** | Edge cases, nil/undefined, off-by-one, error paths, wrong conditions, race conditions, ordering, time zones. |
| **DRY** | Logic duplicated within the diff, and **logic that already exists elsewhere in the repo**. Cite both locations. |
| **Memory and resource leaks** | Go: goroutines with no stop path, missing `context` cancellation, unclosed `resp.Body`/`rows`/files, `time.Ticker` not stopped, unbounded maps/slices/channels. JS/TS: subscriptions or listeners not removed, `setInterval` not cleared, React effects without cleanup, Angular subscriptions not torn down, unbounded caches. Everywhere: connections not returned to pools, buffers that grow without limit. |
| **Project structure** | Files in the wrong layer/package/module, broken module boundaries, circular dependencies, naming not following conventions, decisions contradicting ADRs. |
| **Security** | Missing auth/ownership checks, input validation, injection, secrets in code or config, **sensitive data in logs** (tokens, PII, payloads), unsafe defaults. |
| **Data and API** | Migrations (locking, reversibility), backward compatibility, contract changes, serialization changes. |
| **Performance** | N+1 queries, missing indexes, work in hot paths, blocking calls, unnecessary allocations or re-renders. |
| **Error handling and observability** | Swallowed errors, wrong log levels, noisy logs, missing context in errors, metrics or traces the change should have. |
| **Tests** | Are the new behavior and edge cases covered? Do the tests assert the right thing? Any flaky patterns (sleeps, shared state)? |
| **Config and operations** | New env vars or config documented? Defaults safe? Rollout and rollback needs? |

## Step 4: Questions
Before the final verdict, ask about anything where the **intent** decides whether something is a problem. Use the multiple-choice format in `rules/questioning.md`, at most 3 per turn, each with your recommendation. Then fold the answers into the findings.

## Severity

| Severity | Meaning |
|---|---|
| **Blocker** | Must fix before merge: bugs, security issues, data loss, leaks in long-running paths, broken contracts. |
| **Should fix** | Real problem, not blocking: DRY violations, structure violations, missing tests for important paths. |
| **Suggestion** | Improvement worth considering. Not a defect. |
| **Question** | Needs the author's intent before judging. |

Rules:
- Every finding needs evidence: `[code] file:line`, plus `[run]`, `[docs]` or `[adr]` where relevant. No evidence, no finding.
- Style preferences are not findings unless they break the project's own conventions (cite the convention).
- Report each issue once. If it repeats, list all locations in one finding.
- Use positive notes only when they're specific and useful (e.g. "good: the new retry reuses the existing backoff helper"). Keep them short.

## Output
Use `templates/review.md` in chat. Never write a file.
