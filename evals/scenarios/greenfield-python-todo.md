# Greenfield: Python TODO app

**Setup:** empty directory, no code.

**Prompt:** "I am building a TODO app in Python."

## Expected
- Announces Mode: Greenfield.
- Asks about requirements first (purpose, users, clients, data, constraints, team). At most 3 questions per turn, numbered, each with why it matters.
- Does **not** challenge Python before knowing requirements.
- Once requirements are known, challenges Python only against a specific requirement, or says Python fits and why.
- Treats frontend and backend as separate decisions. Never says "you need Node.js because you need a UI".
- Final recommendation uses criteria → options → table → recommendation → counter-argument → what would change my mind.
- Offers to write an ADR to `docs/adr/0001-...md` with `Status: Proposed`.

## Failure signals
- "Why not Go?" in the first reply.
- More than 3 questions in one turn.
- A recommendation without a comparison table or evidence labels.
- Claims marked `[docs]` without a page fetched in the session.
