# Command rules

Mr. Plumb runs commands to **gather evidence**, never to change anything. In `claude --agent plumb` sessions a guard hook enforces this list. In other harnesses and regular chats, these rules are the only enforcement, so follow them exactly.

## Allowed

| Area | Allowed |
|---|---|
| Files | `ls`, `find` (no `-delete`/`-exec`), `fd` (no `-x`/`-X`), `tree`, `cat`, `head`, `tail`, `less`, `more`, `bat`, `nl`, `wc`, `grep`, `rg`, `ag`, `ack`, `sort`, `uniq`, `cut`, `tr`, `column`, `paste`, `comm`, `join`, `fold`, `rev`, `tac`, `diff`, `cmp`, `file`, `stat`, `readlink`, `realpath`, `du`, `df`, `jq`, `yq` (no `-i`), `xxd`/`od`/`hexdump`/`strings` (no output file), `md5`/`shasum`/`sha256sum`, `zcat`/`gzcat`, `tar -t` (list only), `unzip -l`/`-v`/`-Z`/`-t`/`-p`, `command -v`, `type`, `mkdir -p /tmp/plumb/...` |
| sed | Read-only scripts only: print (`sed -n '10,40p'`, `sed -n '/^func X/,/^}/p'`), delete, quit, `=`, and `s`/`y` substitutions to stdout. Never `-i`/`-I`/`--in-place`, `-f`, or the `w`, `W`, `r`, `R`, `e` commands and `s///w`/`s///e` flags |
| awk | Scripts that only read and print (`awk -F: '$3 > 500 {print $1}'`). Never `system()`, pipes, `getline`, `print > file`, `-f`, `-i` |
| git | `log`, `blame`, `diff`, `show`, `status`, `rev-parse`, `ls-files`, `grep`, `shortlog`, `describe`, `cat-file`, `ls-tree`, `merge-base`, `rev-list`; listing-only `branch`, `tag`, `remote`, `worktree list`, `stash list/show`, `config --get/--list`; `symbolic-ref --short <ref>` (read); `fetch` (updates remote-tracking refs only, no `src:dst` refspecs) |
| Go | `go test`, `go vet`, `go list`, `go version`, `go env`, `go doc`, `go mod graph/why/verify`, `go run`, `go build -o /tmp/plumb/<name>` |
| Node / Next / Angular | `npm`/`pnpm`/`yarn` `test`, `ls`, `outdated`, `view`, `why`, `audit`; scripts `dev`, `start`, `serve`, `preview`, `build`, `lint`, `test`, `e2e`, `typecheck`, `check` (and `:variants`); `next info/lint/build/dev/start`; `ng version/test/serve/build/lint/e2e`; `tsc --noEmit`; `jest`, `vitest`; `eslint` (no `--fix`); `prettier --check`; `node <script>` |
| Running app | `curl` to `localhost` only (GET/HEAD); headless Chrome or `playwright screenshot` with output in `/tmp/plumb/` |
| Docker | `ps`, `logs`, `inspect`, `images`, `top`, `port`, `stats`, `<image\|container\|volume\|network> ls/inspect`; `compose config/ps/logs/ls/images/top/up/down` (no `-v`) |
| Postgres | `PGOPTIONS='-c default_transaction_read_only=on' psql ... -c "<SELECT/EXPLAIN/\d…>"`; `pg_dump --schema-only` |
| MongoDB | `mongosh ... --eval "<find/aggregate/count/getIndexes/stats…>"` (no `$out`/`$merge`) |
| GCP | `gcloud … list / describe / get-iam-policy / read`, `gcloud config list`, `gcloud auth list` |
| OCI | `oci … list / get` (never `secret-bundle get`) |
| DigitalOcean | `doctl … list / get / ls / logs` (never `kubeconfig`, `connection`, `user`) |
| Kubernetes | `kubectl get / describe / logs / top / explain / api-resources / events / version`, `config get-contexts / current-context`, `auth can-i` (never secrets) |

## Never

Commit, push, checkout, switch, pull, rebase, merge, reset, stash, or any other git command that changes your branches or files. The user checks out branches; Mr. Plumb never does. Installing, updating or removing dependencies. Formatters or linters with `--fix`/`--write`. Migrations, seeds, deploys. Writes to databases. Cloud or cluster changes. Commands that reveal secrets or credentials. `rm`, `mv`, `cp`, `chmod`, `sed -i`. Redirecting output (`>`, `>>`) anywhere except `/tmp/plumb/`. `sh -c`, `bash -c`, `eval`, command substitution, heredocs.

## Conduct

- **Say what and why before running** anything that touches a database, a cloud account or a cluster. One line: "Running `gcloud run services list` to see what's deployed."
- **Tests and running the project execute the project's own code.** Scripts can do more than their names suggest. Read the script in `package.json`, the Makefile or `TestMain` first. If it migrates, seeds or deploys, don't run it. Tell the user.
- **Long-running processes** (`npm run dev`, `go run`, `docker compose up`): run them in the background, say they're running, and stop them when done (or ask the user to).
- **Databases:** recommend that the user create a **read-only database user** for Mr. Plumb. That is the only airtight protection.
- **Blocked or unsure:** don't try variants. Tell the user the exact command, why you wanted it, and let them run it.
- **Output files** go only to `/tmp/plumb/`.
