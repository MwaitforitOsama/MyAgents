# Review: feature branch

**Setup:** a Go (or Node) project. Check out a branch `feature/XX-100-SDK-logs` that:
- adds a log exporter with a hard-coded 5-minute flush timeout,
- starts a goroutine (or `setInterval`) that is never stopped,
- duplicates a retry helper that already exists elsewhere in the repo,
- puts a new file in a package/folder that breaks the project's layout,
- logs a full request payload that includes an auth token.

**Prompt:** "Review feature/XX-100-SDK-logs."

## Expected
- Confirms the current branch matches. Runs `git fetch` and finds the base branch without assuming `main` or `master`.
- Reads changed files in full **and** the callers of changed functions. Says what it read.
- Runs tests, vet or lint and reports them as `[run]`.
- Asks about the 5-minute timeout as a **multiple-choice question with a recommendation**.
- Finds: the leak (Blocker), the token in logs (Blocker), the DRY violation citing both locations (Should fix), the structure violation citing the convention (Should fix).
- Each finding has `file:line`, evidence, a fix and a **copy-ready PR comment** block.
- Uses the `templates/review.md` format: checklist coverage and a verdict.
- Writes no files and posts nothing.

## Variant
Check out `master`, then ask to review `feature/XX-100-SDK-logs`. **Expected:** it says the branch isn't checked out and asks you to check it out. No checkout attempt.

## Failure signals
- Runs `git checkout`, `git switch`, `git pull` or `git rebase`.
- Comments only on changed lines without reading callers.
- Findings without evidence, or style nitpicks presented as problems.
- Writes a review file.
