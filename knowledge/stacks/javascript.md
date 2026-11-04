# JavaScript and TypeScript

Applies to every JS/TS project (Node, Next.js, Angular, React Native, plain browser code). Load it together with the framework file.

## Detect and version
- `package.json`, lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`). The lockfile tells you which package manager to use.
- `tsconfig*.json` (TypeScript: check `strict`, `target`, `module`, `moduleResolution`), `"typescript"` version in `package.json`
- `"type": "module"` (ESM) vs CommonJS; `.mjs` / `.cjs`
- Lint and format config: `eslint.config.*` / `.eslintrc*`, `.prettierrc*`, `biome.json`
- Test runner: `jest`, `vitest`, `mocha`, `node --test`, Playwright, Cypress

## Official sources
- JavaScript reference (MDN): https://developer.mozilla.org/en-US/docs/Web/JavaScript
- Language specification (ECMAScript): https://tc39.es/ecma262/
- TC39 proposals and their stages: https://github.com/tc39/proposals
- TypeScript handbook: https://www.typescriptlang.org/docs/
- TypeScript compiler options: https://www.typescriptlang.org/tsconfig
- TypeScript release notes: https://www.typescriptlang.org/docs/handbook/release-notes/overview.html
- Browser support data: https://caniuse.com
- ESLint: https://eslint.org/docs/latest/

## Decision checkpoints
- **Typing at boundaries:** where untrusted data enters (HTTP, storage, messages), validate at runtime. Types alone don't check data.
- **Module system** and how it matches the runtime and bundler.
- **Async model:** promises and `async/await` everywhere. No mixing callback styles in new code.
- **Dependencies:** does the platform or an existing dependency already do it? Every new package is code you ship and maintain.

## Checks
- `await` isn't missing (floating promises), and promise rejections are handled.
- No `any` that hides a real type in new TS code. `unknown` plus narrowing at boundaries.
- Equality uses `===`. No implicit coercion bugs.
- Dates and time zones are handled deliberately. Money is never a binary float.
- Event listeners, intervals, timeouts and subscriptions are removed or cleared when no longer needed.
- No secrets in code that ships to a browser or app bundle.

## Implementation (Mason)
- Use the package manager the lockfile shows. Never mix them, and never delete a lockfile to "fix" an install.
- Before finishing, run the project's own scripts: typecheck (`tsc --noEmit` or the script that wraps it), lint, tests, build. Report their output.
- Match the existing style. Run the formatter the project already uses, and only on files you changed.
- Add a dependency only when the plan or the user agreed to it. Install the exact version range the plan names.
- Prefer small, pure functions you can unit test. Put I/O at the edges.

## Version-sensitive areas
New language features (check the target in `tsconfig` and the browser or Node support before using them), TypeScript major versions (stricter checks), ESLint flat config vs legacy config.
