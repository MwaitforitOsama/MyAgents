# Mode: Bugfix

Plan the fix for a bug whose **root cause is already known**. If the cause is only suspected, go back to Debugging mode.

## Entry signals
- "The cause is X, how should we fix it?", or coming from Debugging with a confirmed cause.

## Evidence first
1. Confirm the root cause evidence: a reproduction, log line or code path. If it's missing, switch to Debugging.
2. Read the affected code and its callers. Who else depends on this behavior?
3. Check tests: is there a test that should have caught this? Why didn't it?
4. Check for the same pattern elsewhere: `grep` for similar code that might have the same bug.

## Required facts (stop rule)
1. Confirmed root cause, with evidence.
2. Blast radius: who and what is affected, and whether data was corrupted.
3. Urgency: a hotfix now, or a proper fix in normal flow?
4. Constraints: deadlines, freeze windows, compatibility promises.

## Question bank
- Has bad data already been written, so it needs a repair as well as a code fix? (data cleanup)
- Hotfix now, with a proper fix later, or one proper fix? (options)
- Can clients depend on the buggy behavior? (compatibility)
- How will you know in production that the fix worked? (verification, monitoring)

## Options to consider
- **Minimal fix** at the cause.
- **Structural fix** that removes the class of bug, if it's worth the cost.
- **Mitigation** (feature flag, config change, rollback) if a fix takes time.

Compare them with `rules/bias.md`. A minimal fix is often right. Say why if it isn't.

## Output
- **Plan** (always): the fix steps, a **regression test** that fails before and passes after, data repair steps if needed, rollout and rollback, how to verify in production.
- **ADR** only if the fix changes a design decision.
