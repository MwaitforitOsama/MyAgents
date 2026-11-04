# Angular

## Detect and version
- `angular.json`, `"@angular/core"` in `package.json` plus the lockfile
- `npx ng version`: Angular, CLI, Node and TypeScript versions

## Official sources
- Docs: https://angular.dev
- Update guide (version-to-version steps): https://angular.dev/update-guide
- Release schedule and support policy: https://angular.dev/reference/releases
- Releases and changelog: https://github.com/angular/angular/releases
- Blog: https://blog.angular.dev
- RxJS: https://rxjs.dev

## Decision checkpoints
- **Component model:** standalone components vs NgModules (check what the detected version recommends).
- **Reactivity and state:** signals, RxJS, or a state library. Keep one consistent approach.
- **Change detection:** default vs OnPush, zone-based vs zoneless (version-dependent).
- **Rendering:** client-only, SSR, prerendering, hydration.
- **Routing:** lazy loading boundaries, guards, resolvers.
- **Forms:** reactive vs template-driven.
- **Backend integration:** HTTP client, interceptors (auth, errors), API typing.

## Checks (verify against the detected version)
- Subscriptions are cleaned up (or managed by the framework/async pipe).
- Bundle budgets in `angular.json` exist and pass on `ng build`.
- Feature areas are lazy-loaded.
- `ng test` and `ng lint` pass.
- Version is inside the support window (check the release schedule).

## Version-sensitive areas
Standalone APIs, signals, built-in control flow, zoneless change detection, the build system, SSR/hydration. Angular upgrades go one major version at a time per the update guide. Use it for Migration mode.

## Implementation (Mason)
- Generate with the CLI (`ng generate component|service|...`) so files follow the project's schematics and naming.
- Follow the project's pattern: standalone or NgModule, signals or RxJS. Don't mix in a second style.
- Clean up subscriptions (`async` pipe, `takeUntilDestroyed`, or the project's pattern). Use `OnPush` if the project does.
- Put HTTP calls in services, not components. Typed responses and interceptors as the project already uses them.
- Before handing back: `ng lint`, `ng test` (headless, e.g. `--watch=false`), `ng build`. Check the bundle budgets still pass.
