# Node.js

## Detect and version
- `package.json` (`engines`, `type: "module"`), `.nvmrc` / `.node-version`, Dockerfile base image
- `node --version`, `npm ls --depth=0`, `npm outdated`

## Official sources
- API docs (latest; versioned docs linked from there): https://nodejs.org/docs/latest/api/
- Release schedule and LTS status: https://nodejs.org/en/about/previous-releases
- Release working group schedule: https://github.com/nodejs/release#release-schedule
- npm docs: https://docs.npmjs.com
- Framework docs as detected: Express https://expressjs.com, Fastify https://fastify.dev, NestJS https://docs.nestjs.com

## Decision checkpoints
- **Framework:** none, Express, Fastify, NestJS… and why.
- **Module system:** ESM vs CommonJS; TypeScript build setup.
- **Validation and typing** at API boundaries.
- **Error handling:** central handler, async errors, process-level handlers.
- **Data access:** driver, query builder or ORM; connection pooling.
- **Runtime:** container, process manager, serverless; the LTS version in use.

## Checks (verify against the detected version)
- Running an LTS (or supported) Node version (check the release schedule).
- No blocking synchronous work (sync FS, heavy CPU) in request paths.
- Unhandled promise rejections are handled or logged centrally.
- Graceful shutdown on SIGTERM closes servers and DB pools.
- `npm audit` findings reviewed (report them, never `audit fix`).
- Lockfile is committed and matches `package.json`.

## Implementation (Mason)
- Follow the framework's patterns already in the project (routers, middleware, DI in NestJS).
- Validate request input at the boundary with the project's validator (zod, class-validator, ajv...).
- Every async route handler's errors reach the central error handler.
- Before handing back: lint, typecheck, tests, and start the server once to check that it boots.
