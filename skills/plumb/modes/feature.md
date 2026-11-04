# Mode: Feature

A new capability in an existing codebase. The stack is already decided. **Don't question the language or framework** unless the feature truly can't be built well with it, and then show evidence.

## Entry signals
- "Add / support / build X in our app", "we need X in the existing project".

## Evidence first
1. Read the project structure, entry points and the modules the feature will touch.
2. Find the **closest existing feature** (e.g. for Delete, read Create/Read/Update). Its patterns are the default for this feature: routing, validation, error format, data access, tests, auth checks.
3. Read the data model: schema, migrations, models/structs, indexes.
4. Read `docs/adr/` for decisions that constrain this feature.
5. Check git history for the touched files (`git log --oneline -- <path>`) to see recent changes and conventions.
6. Run the existing tests to know the baseline (`go test ./...`, `npm test`).

## Required facts (stop rule)
1. **Purpose:** what the user is trying to achieve, and who uses it.
2. **Behavior:** the main path, plus the edge cases that matter.
3. **Data impact:** schema changes, migrations, effect on existing data.
4. **Access:** who may use it (auth, ownership, roles).
5. **Interfaces:** API, UI and contract changes, plus backward compatibility.
6. **Fit:** which existing patterns to follow, or a reason to deviate.

## Question bank
Scale this to reversibility (`rules/questioning.md`). Example for "add Delete":
- Who needs to delete, and why? (purpose, and whether delete is the right model: archive, complete, hide?)
- Soft delete (recoverable, `deleted_at`) or hard delete? Do you need undo or a trash view? (data model, one-way door for data)
- Who may delete: only the owner, or admins too? (authorization)
- Single item only, or bulk? (API shape, performance)
- What happens to related data, such as subtasks, tags or attachments? (cascade rules)
- What should a second delete of the same item return? (idempotency, API contract)
- Any audit or compliance need to keep a record? (retention)

## Analysis focus
- Consistency with existing patterns, citing `[code]` for each.
- Data safety: migrations, reversibility, effect on existing rows.
- API contract and backward compatibility for current clients.
- Test strategy that matches the project's existing tests.

## Output
- **Plan** (always): Agent steps with exact files to change, following the existing patterns; acceptance criteria; tests.
- **ADR** only if the feature contains a real decision (e.g. soft vs hard delete).
