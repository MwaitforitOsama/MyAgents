# Go

## Detect and version
- `go.mod` (the `go` directive and `toolchain` line), `go.work`, `*.go`
- `go version`, `go list -m all` (dependencies), `go env GOVERSION`

## Official sources
- Docs home: https://go.dev/doc/
- Language spec: https://go.dev/ref/spec
- Standard library: https://pkg.go.dev/std
- Release history and notes: https://go.dev/doc/devel/release
- Module layout guidance: https://go.dev/doc/modules/layout
- Effective Go: https://go.dev/doc/effective_go
- Code review comments (style): https://go.dev/wiki/CodeReviewComments
- Blog: https://go.dev/blog/
- Third-party package docs: https://pkg.go.dev/<module path>

## Decision checkpoints
- **Layout:** the module/package structure and its boundaries. Do packages follow the domain or the technical layer?
- **HTTP:** standard library routing vs a router/framework. Check what the detected Go version's `net/http` supports in the release notes.
- **Data access:** `database/sql` + driver, `pgx` directly, generated queries (sqlc), or an ORM. Transactions and context handling.
- **Errors:** wrapping and checking style; how errors map to API responses.
- **Concurrency:** goroutine lifecycle, cancellation, bounded worker pools.
- **Config and secrets:** env vars, files, secret managers.
- **Observability:** structured logging, metrics, tracing.
- **Testing:** table tests, integration tests with a real DB (containers), mocks vs fakes.

## Checks (verify against the detected version)
- `context.Context` flows from the request through to DB and HTTP calls.
- Every goroutine has a way to stop. No leaks on cancellation.
- `http.Server` timeouts are set explicitly (check the `net/http` docs for zero-value behavior).
- `database/sql` pool settings (`SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`) match the DB's limits.
- Errors are wrapped with `%w` and checked with `errors.Is` / `errors.As`.
- Graceful shutdown on SIGTERM (important for containers and Kubernetes).
- `go vet ./...` and `go test -race ./...` are clean.

## Version-sensitive areas
The standard library keeps gaining features (routing, logging, iterators, generics-related packages). Before recommending a third-party library, check whether the detected Go version's standard library already covers it.

## Implementation (Mason)
- Run `gofmt` (or the project's `goimports`/`golangci-lint` setup) on changed files. Then `go vet ./...`, `go test -race ./...` and `go build ./...` before handing back.
- Follow the package layout already in place. New code goes in the package that owns the domain, not in a new `utils`.
- Pass `context.Context` as the first parameter. Wrap errors with `%w` and context (`fmt.Errorf("load todo %d: %w", id, err)`).
- Table-driven tests next to the code (`*_test.go`). Use the project's existing test helpers and fakes before adding a mocking library.
- Close what you open (`defer rows.Close()`, `defer resp.Body.Close()`), and check `rows.Err()`.
- Run `go mod tidy` only when you changed imports, and mention the `go.mod`/`go.sum` diff.
