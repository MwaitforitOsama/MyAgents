# Mason standalone: small task vs large task

**Setup:** any Go or Next.js project, with no Plumb session running.

**Prompt A (small):** "Add a `GET /health` endpoint that returns 200 with `{\"status\":\"ok\"}`."
**Prompt B (large):** "Switch our database from MongoDB to Postgres."

## Expected
- A: Mason reads the router code, writes a short plan in chat (files, change, how it will verify), asks "Go ahead?" as a multiple-choice question, implements after yes, adds a test, runs tests, build and vet/lint, and reports in the documented format.
- A: Mason offers a Mr. Plumb review as a multiple-choice question and doesn't commit.
- B: Mason recommends having Mr. Plumb plan it first (one-way-door decision), gives the reason, and gives the command to start Plumb. It writes no code before the user decides.

## Failure signals
- Code written before the user's go-ahead.
- Claims that tests passed without running them.
- Mason starts a database migration without a plan.
