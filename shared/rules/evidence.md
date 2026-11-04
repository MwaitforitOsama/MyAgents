# Evidence rules

Every factual claim carries a label. Opinions are fine as long as they are labeled as reasoning.

## Labels

| Label | Meaning | Citation format |
|---|---|---|
| `[code]` | You read it in this project | `path/to/file.go:42` or `path/file.ts:10-25` |
| `[run]` | You observed it from a command you ran | the command, plus the key output line |
| `[docs]` | Official documentation you fetched this session | URL · version · checked YYYY-MM-DD |
| `[spec]` | RFC, standard or formal specification | URL or RFC number + section |
| `[maintainers]` | GitHub issue, discussion or PR by the project's maintainers | URL |
| `[blog]` | Engineering blog of a named organization or recognized expert | URL · author/org · date |
| `[community]` | Community posts, Q&A, forums | URL · date |
| `[adr]` | A recorded decision in this project | `docs/adr/0004-...md` |
| `[ticket]` | A Jira ticket you read this session (what the reporter says, not proven) | `ABC-123` · field (description/comment by role) |
| `[session]` | Something you observed in a Fullstory session this session | session URL · timestamp |
| `[reasoning]` | Your own analysis or inference | none; say what it is based on |
| `[unverified]` | You believe it but could not confirm it | say what would confirm it |

## Source ranking

When sources disagree, the higher rank wins. Say that they disagree.

1. Official documentation (version-matched)
2. RFCs and specifications
3. Maintainers' GitHub issues, discussions and PRs
4. Engineering blogs from named organizations or recognized experts
5. Community posts

Code in the project (`[code]`, `[run]`) is about what *is*, not what *should be*. It is the strongest evidence of current behavior.

## Hard rules

- **Cite only what you read.** `[docs]`, `[spec]`, `[maintainers]`, `[blog]` and `[community]` require a page you actually fetched in this session. Anything you remember from training is `[reasoning]` or `[unverified]`, never `[docs]`.
- **Never invent** URLs, versions, flags, API names, config keys, console menu paths or prices.
- **Match versions.** Check the version first (go.mod, package.json, lockfiles, Dockerfiles, CLI `--version`), then cite docs for that version. If the docs are for a different version, say so.
- **Date volatile facts.** Prices, quotas, free tiers, console navigation and preview features change. Always add the check date, and recommend re-checking before acting.
- **Offline or blocked.** If you can't fetch docs, say so plainly. Downgrade the claim to `[reasoning]` or `[unverified]` and tell the user what to verify.

## Example

> Soft delete fits here. Your handlers already filter by `user_id` on every query `[code] internal/todo/repo.go:31-48`, so adding `deleted_at IS NULL` follows the same pattern. Postgres partial indexes can keep this fast `[docs] https://www.postgresql.org/docs/16/indexes-partial.html · v16 · checked 2026-10-31`. My concern is that list endpoints might forget the filter. Wrapping it in one query helper reduces that risk `[reasoning]`.
