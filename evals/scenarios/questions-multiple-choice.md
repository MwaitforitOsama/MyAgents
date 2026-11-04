# Questions: multiple choice with a recommendation

**Setup:** any scenario where Mr. Plumb must ask something (e.g. `feature-go-delete.md`).

## Expected
- Questions are numbered, at most 3 per turn, and each says why it matters.
- Each offers 2–4 distinct options plus "Other", with the **recommended option first**, marked, with a reason and evidence.
- Each non-recommended option states its trade-off.
- In Claude Code, the AskUserQuestion picker is acceptable if the content is the same.
- Open-ended questions only where choices don't make sense (e.g. "paste the error").

## Failure signals
- Open-ended questions where clear options exist.
- No recommendation, or a recommendation without a reason.
- Filler options nobody would pick.
