# Other clouds: research procedure

For any provider without a file here (AWS, Azure, Hetzner, Cloudflare, Fly.io, Vercel, …). First check if `clouds/<provider>.draft.md` already exists. If it does, use it, but re-verify anything you rely on.

## Procedure

1. **Find the official documentation root,** the pricing page and the status page. Use WebSearch, then confirm by fetching. Never guess URLs.
2. **Map the resource hierarchy and access model:** accounts, projects or subscriptions, organizations, IAM concepts.
3. **Map services to these categories:** compute/containers, functions, relational DB, NoSQL, cache, object/block storage, networking (VPC, load balancing, DNS, CDN), secrets/keys, messaging, registry/CI, observability.
4. **Check the CLI** and which commands are read-only (list/describe/get). Note that the guard does **not** allow this provider's CLI. Ask the user to run read-only commands and share the output, or to add the CLI to the guard after review.
5. **Check pricing, free tier and limits** for the services in question, with check dates.
6. **Compare** with the user's other clouds using the same criteria (`rules/bias.md`).

## Draft a knowledge file

At the end of the research, offer to save it as `knowledge/clouds/<provider>.draft.md` (lowercase, e.g. `aws.draft.md`). Use the same sections as `gcp.md`:

```markdown
# <Provider> (DRAFT: researched YYYY-MM-DD, review before relying on it)

## Detect
## Resource hierarchy and access
## Service map (verify current names and features in docs)
## Official sources
## Read-only inspection
## Decision checkpoints
```

Rules for drafts:
- Every fact links to the page it came from.
- Mark the file as a DRAFT in its title. The user reviews it and renames it to `<provider>.md` when satisfied. Mr. Plumb can't write non-draft knowledge files.
- Tell the user the draft exists and what to review.
