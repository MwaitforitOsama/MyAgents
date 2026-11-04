# Review output format (chat only, never saved)

````markdown
## Review: <branch> → <base>
**Scope:** <N> commits, <N> files changed (+X / −Y)<, plus uncommitted changes>
**Checks:** `go test ./...` ✅ · `go vet ./...` ✅ · `npm run lint` ❌ 2 errors   `[run]`
**Read:** <changed files in full; callers of X, Y; related ADR-000N; plan docs/plans/...>

### Summary
<2–4 sentences: what the change does, overall quality, the main risks.>

### Blockers
#### B1. <short title>
**Where:** `path/file.go:42-58` (also `path/other.go:12`)
**Problem:** <what is wrong and why it matters, with evidence labels>
**Fix:** <concrete suggestion; a short code snippet if it helps>

PR comment (copy-paste):
```
<self-contained comment text for the PR, written to the author, with the fix>
```

### Should fix
#### S1. ...

### Suggestions
#### G1. ...

### Questions
<Multiple-choice questions per rules/questioning.md, if not already asked.>

### Checklist coverage
Intent ✅ · Correctness ✅ · DRY ⚠️ S1 · Leaks ❌ B1 · Structure ✅ · Security ✅ · Data/API — n/a · Performance ✅ · Errors/Observability ⚠️ G2 · Tests ⚠️ S2 · Config/Ops ✅

### Verdict
**Changes needed** | **Approve with suggestions** | **Approve**: <one-line reason>
````

## Rules
- Number findings by severity: B1, B2… / S1… / G1… so the user can refer to them ("explain S2").
- Each PR comment is self-contained, polite and specific, so it makes sense without the rest of the review.
- Empty sections: write "None." Don't drop the heading, so the user can see the area was checked.
