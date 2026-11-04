# Next.js: version-sensitive advice

**Setup:** a Next.js project (check `package.json` for the version and whether `app/` or `pages/` is used).

**Prompt:** "My page shows stale data after I update it. How should caching work here?"

## Expected
- Mode: Debugging (or Feature if it's a design question). Says which.
- Checks the Next.js version (`package.json` / `npx next info`) and the router type **before** advising.
- Fetches the Next.js docs matching that version and router, and cites them.
- Explains the caching behavior for **that** version, and says that defaults differ between versions.

## Failure signals
- Advice without checking the version or router.
- Mixing App Router and Pages Router concepts.
- `[docs]` claims without fetched pages.
