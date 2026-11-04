# Plan: <title>

- **Status:** Proposed | Accepted | Assigned to Mason | In progress | In review | Done
- **Date:** YYYY-MM-DD
- **Mode:** Feature | Bugfix | Refactoring | Migration | Greenfield | Debugging (next diagnostic steps)
- **Related ADRs:** <ADR-NNNN, or none>

## Goal
<One or two sentences: what will be true when this is done.>

## Context and evidence
- <fact> `[label]`

## Scope
- **In:** <...>
- **Out:** <...>

## Human steps
<Steps the user does by hand: consoles, accounts, secrets, approvals. Use the format in rules/manual-steps.md. Write "None." if there are none.>

### Step 0: Prerequisites
**Where:** ...
**Do:** ...
**Verify:** ...
**Source:** ...

## Agent steps
<Steps for the implementation agent. Each step is self-contained and verifiable.>

### A1: <short title>
- **Files:** `path/to/file.go` (modify), `path/to/new_test.go` (create)
- **Change:** <what to change, following the existing pattern in `path:line`>
- **Acceptance:** <a concrete check, e.g. "`go test ./internal/todo/...` passes; `DELETE /todos/{id}` returns 204">
- **Depends on:** <A0 / Human step N / none>

## Tests
- <Test to add or update, and what it proves>

## Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| | | | |

## Rollout and rollback
- **Rollout:** <order, flags, migrations>
- **Rollback:** <how to undo each step, and the point of no return if any>

## Verification after release
- <How to confirm it works in the real environment>

## Open questions
- <Unknowns that could change this plan>

## Sources
- <label> <URL or path> · <version> · checked YYYY-MM-DD

## Deviations / Disputes
<Mason writes here; Mr. Plumb answers inside each entry. Format: rules/handoff.md. Write "None." until there are any.>

## Review rounds
<Mr. Plumb writes here after the user agrees to send findings back. One `### R<n>` per round: findings with severity and evidence, and the verdict.>
