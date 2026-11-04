# Coding rules

## Before writing
- Read the files you'll change, in full. Read the callers of every function, method, type or exported symbol you'll change (`grep`/`rg` the repo).
- Find how the project already does this kind of thing (error handling, logging, validation, tests, naming, folder layout), and do it the same way. Cite the example you followed (`path:line`) in your report.
- Search for existing code that already does what you need. Reuse it before writing new code.
- Check versions (go.mod, package.json plus the lockfile) and use the docs for those versions. Don't use APIs that the detected version doesn't have.

## While writing
- **Smallest change that does the job.** No unrelated refactors, renames or formatting of untouched code.
- **Tests with the change.** Add or update tests that would have failed before and pass after. Bug fixes get a regression test.
- **Errors are handled,** not swallowed. Messages carry context. Nothing sensitive (tokens, passwords, personal data) goes into logs or errors.
- **Resources are released:** connections, files, response bodies, goroutines, subscriptions, listeners, timers.
- **Validate input at boundaries** (HTTP, messages, storage, user input) and check authorization where data is accessed.
- **No secrets in code,** config committed to git, or client bundles.
- **Dependencies:** only those the plan or the user agreed to. Use the lockfile's package manager.
- **Comments** explain why, not what. Don't leave TODOs without telling the user.

## Before handing back
Run what applies, using the project's own scripts where they exist. Report each result.

| Stack | Checks |
|---|---|
| Go | `gofmt -l` on changed files (empty), `go vet ./...`, `go test -race ./...`, `go build ./...`, `golangci-lint run` if configured |
| JS/TS (any) | typecheck, lint, tests, build via `package.json` scripts |
| Angular | `ng lint`, `ng test --watch=false`, `ng build` (budgets pass) |
| Next.js | lint, typecheck, `next build` (check the route output), tests |
| React Native | lint, typecheck, tests; run on iOS and/or Android if possible, and say which |
| CSS/HTML | look at it in a browser at mobile and desktop widths; keyboard navigation; the project's a11y checks |
| Infra as code | `terraform validate` / `plan` (asks first if it needs cloud credentials), or the provider's spec validation |

- **Run the app** when the change is behavioral or visible, and check it (curl the endpoint, open the page, screenshot). Stop servers you started, or tell the user they are running.
- **Re-read your diff** (`git diff`) as a reviewer would: leftovers, debug prints, commented-out code, unrelated changes, missed callers.
- If a check fails and the fix is inside the task, fix it. If it's outside the task (a pre-existing failure), report it and don't fix it without asking.
