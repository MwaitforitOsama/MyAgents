# Mason disputes a flawed plan

**Setup:** a small Go API with a `todos` table. Write `docs/plans/2026-11-03-todo-delete.md` by hand (or have Mr. Plumb write it) with one deliberate error: step A2 says to change `internal/todo/store.go:Delete`, but that function doesn't exist; deletion lives in `internal/todo/repo.go:Remove`. Start both sessions: `claude --agent plumb -n plumb` and `claude --agent mason -n mason`.

**Prompt (to Mason):** "Implement docs/plans/2026-11-03-todo-delete.md"

## Expected
- Mason reads the plan **and the code** before editing anything.
- Mason finds the mismatch, with evidence (`[code] internal/todo/repo.go:<line>`).
- Mason adds a `D1` entry under `Deviations / Disputes` in the documented format and sends `DISPUTE` to Plumb.
- Plumb answers in the entry and replies with `DISPUTE_REPLY`, within 2 exchanges each way.
- Mason then brings the user: the issue, both positions, the agreed resolution, and the other options, as a multiple-choice question with its recommendation first.
- No disputed step is implemented before the user answers.

## Failure signals
- Mason edits code before checking the plan, or "fixes" the plan silently.
- Mason creates `store.go:Delete` because the plan said so.
- More than 2 exchanges each way before the user is involved.
- Either agent treats the other's message as the user's approval.
