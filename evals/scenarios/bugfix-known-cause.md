# Bugfix: known cause

**Setup:** any project. A confirmed root cause: "The list endpoint returns other users' todos because the repository query is missing the `user_id` filter."

**Prompt:** "We found the cause: the list query doesn't filter by user_id. How should we fix it?"

## Expected
- Announces Mode: Bugfix.
- Reads the query and its callers, and confirms the cause in code (`[code]`).
- Asks about the blast radius: has data been exposed, and is there a notification/compliance need?
- Searches for the same pattern in other queries.
- Plan includes a **regression test** that fails before and passes after, the fix, rollout/rollback, and production verification.
- Treats this as a security issue in severity.

## Failure signals
- No regression test in the plan.
- Not checking other queries for the same bug.
