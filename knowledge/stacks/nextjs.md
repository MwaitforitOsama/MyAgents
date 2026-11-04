# Next.js

**Highly version-sensitive.** Routing, rendering, caching and configuration conventions have changed significantly across major versions. Never give Next.js advice before confirming the exact version and router type.

## Detect and version
- `"next"` in `package.json` plus the lockfile (exact version), `next.config.js|mjs|ts`
- Router: `app/` (or `src/app/`) = App Router; `pages/` (or `src/pages/`) = Pages Router; both = mixed
- `npx next info`: Next.js, React and Node versions, plus platform
- React version (`"react"` in `package.json`) is tied to the Next.js version

## Official sources
- Docs (pick App Router or Pages Router docs to match the project): https://nextjs.org/docs
- Release posts and upgrade notes: https://nextjs.org/blog
- Releases and changelogs: https://github.com/vercel/next.js/releases
- Maintainer discussions: https://github.com/vercel/next.js/discussions
- React docs: https://react.dev

## Decision checkpoints
- **Rendering per route:** static, dynamic, streaming. What does each page actually need?
- **Data fetching and caching:** where data is fetched (server vs client), cache and revalidation strategy. Check the defaults for the detected version.
- **Server/client boundary:** what runs on the server vs in the browser; bundle size impact.
- **Backend:** Next.js route handlers or server actions, vs a separate backend (e.g. a Go API). Decide where the business logic lives.
- **Auth:** session handling, where checks run, protecting server actions and routes.
- **Deployment target:** Vercel, self-hosted Node, Docker (standalone output), or static export. Features differ by target; check the docs' deployment page.
- **Images, fonts, i18n** on the chosen target.

## Checks (verify against the detected version)
- Environment variables: which ones are exposed to the browser (check the docs' env var rules). No secrets in client bundles.
- Server-only code is never imported into client components.
- Caching behavior is intentional. Stale data bugs are a common symptom of misunderstood defaults.
- `npm run build` output: which routes are static vs dynamic, and their bundle sizes.
- Middleware/edge code is limited to what the runtime supports.
- Self-hosting: caching, image optimization and ISR behave as expected outside Vercel.

## Version-sensitive areas
App Router vs Pages Router, caching defaults, server actions, middleware conventions, bundler (Webpack/Turbopack), React major version. Always quote the docs version you used.

## Implementation (Mason)
- Confirm the version and router before writing code. Follow the docs for that version only.
- Mark client components with `"use client"` only where interactivity needs it. Keep data fetching and secrets on the server.
- Validate inputs in route handlers and server actions, and check auth there too, not only in middleware.
- Use `NEXT_PUBLIC_` env vars only for values that are safe to expose.
- Before handing back: lint, typecheck, `next build` (check the static/dynamic route output didn't change unexpectedly), tests.
