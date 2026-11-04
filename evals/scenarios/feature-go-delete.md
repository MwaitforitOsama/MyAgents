# Feature: add Delete to an existing Go TODO API

**Setup:** a small Go TODO API with Create, Read and Update handlers, a Postgres repository and tests. No Delete.

**Prompt:** "I need to add delete functionality to this TODO project."

## Expected
- Announces Mode: Feature (existing Go project).
- Reads the existing handlers, repository and tests **before** asking, and cites them as `[code] path:line`.
- Does **not** question the language or framework.
- Asks feature-level questions: purpose, soft vs hard delete, who may delete, bulk, related data, idempotency. At most 3 per turn.
- Plan follows the existing patterns (routing, error format, tests), citing where each pattern comes from.
- Writes a plan to `docs/plans/YYYY-MM-DD-...md`, plus an ADR only for soft vs hard delete.
- Agent steps list exact files and acceptance criteria.

## Failure signals
- "Why Go?" or suggesting another language.
- Asking something the code already answers (e.g. "which database do you use?").
- Editing any `.go` file.
