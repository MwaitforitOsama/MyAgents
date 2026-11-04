# Knowledge index

Shared by Mr. Plumb and Mason. These files say **how to detect a technology, where its authoritative sources are, and what to check**. Each file's `Implementation (Mason)` section is for writing code; Mr. Plumb can use it to judge whether a plan is implementable. They are not a substitute for current documentation: always fetch version-matched docs before making `[docs]` claims (`rules/evidence.md`).

URLs were checked on 2026-10-31 (JavaScript, CSS and HTML files: 2026-11-03). If a link fails, search the official site rather than guessing a new URL.

## Detect the stack

| Signal in the repo | Load |
|---|---|
| `go.mod`, `go.work`, `*.go` | `stacks/go.md` |
| `"next"` in `package.json`, `next.config.*`, `app/` or `pages/` directory | `stacks/nextjs.md` (+ `stacks/node.md`) |
| `angular.json`, `"@angular/core"` in `package.json` | `stacks/angular.md` |
| `"react-native"` or `"expo"` in `package.json`, `app.json` / `app.config.*`, `ios/` + `android/` | `stacks/react-native.md` |
| `package.json` with none of the above (Express, Fastify, NestJS, plain Node) | `stacks/node.md` |
| Any `package.json`, `tsconfig*.json`, `*.js` / `*.ts` | `stacks/javascript.md` (in addition to the framework file) |
| `*.css`, `*.scss`, Tailwind / PostCSS config, CSS-in-JS | `stacks/css.md` |
| `*.html`, Angular templates, JSX/TSX, server templates | `stacks/html.md` |
| Postgres drivers (`pgx`, `lib/pq`, `pg`, `postgres`), Prisma/Drizzle/TypeORM with postgres, `postgres://` URLs, `postgres` image | `stacks/postgres.md` |
| Mongo drivers (`mongo-driver`, `mongodb`, `mongoose`), `mongodb://` or `mongodb+srv://` URLs, `mongo` image | `stacks/mongodb.md` |

## Detect the cloud

| Signal | Load |
|---|---|
| `gcloud` usage, `app.yaml`, `cloudbuild.yaml`, Terraform `google` provider, `*.run.app`, GCR/Artifact Registry image paths | `clouds/gcp.md` |
| `~/.oci` references, `ocid1.` IDs, Terraform `oci` provider, OCIR image paths (`*.ocir.io`) | `clouds/oci.md` |
| `doctl` usage, `.do/app.yaml`, Terraform `digitalocean` provider, `registry.digitalocean.com` | `clouds/digitalocean.md` |
| Any other provider | `clouds/other-clouds.md` (and any `clouds/<provider>.draft.md` already present) |

Load only what applies. Several files can apply at once (e.g. Go + Postgres + OCI).

## Not covered here

For any technology without a file (Traefik, Redis, Kafka, NGINX…): identify its version in the project, find the official documentation, and follow `rules/evidence.md`. The same rules apply. Only the shortcut file is missing.
