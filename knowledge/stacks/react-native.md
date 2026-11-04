# React Native

## Detect and version
- `"react-native"` in `package.json`; `"expo"` plus `app.json` / `app.config.js|ts` = Expo project
- `ios/` and `android/` folders = bare or prebuilt native projects
- Versions: `package.json` plus the lockfile (React Native, React, Expo SDK)

## Official sources
- React Native docs: https://reactnative.dev/docs/getting-started
- React Native blog (releases, architecture changes): https://reactnative.dev/blog
- Expo docs: https://docs.expo.dev
- Upgrade helper (diff between versions): https://react-native-community.github.io/upgrade-helper/
- React Native releases: https://github.com/facebook/react-native/releases

## Decision checkpoints
- **Expo (managed / prebuild) vs bare React Native.** This affects native modules, builds and updates.
- **Navigation library** and deep linking.
- **Data:** API client, caching, offline storage, sync and conflict handling.
- **Auth:** token storage (secure storage, never plain AsyncStorage for secrets), refresh.
- **Updates:** app store releases vs over-the-air updates (check store policies and the docs).
- **Push notifications,** background tasks, permissions.
- **Code sharing** with web (Next.js / Angular): which parts actually share (types, API client, validation).

## Checks (verify against the detected version)
- New Architecture status for the detected version, and whether native dependencies support it.
- Native dependencies are compatible with the React Native / Expo SDK version.
- Secrets are not shipped in the app bundle. Everything in the app is visible to users.
- Performance: list virtualization, image sizes, JS-thread work.

## Version-sensitive areas
New Architecture, Hermes, Expo SDK versions and their React Native pairing, build tooling. For upgrades use Migration mode, the upgrade helper and the release notes.

## Implementation (Mason)
- Expo projects: install native packages with `npx expo install` so versions match the SDK.
- Test on both platforms, or say which one you couldn't run. Platform-specific code goes in `.ios.tsx` / `.android.tsx` or `Platform.select`, following the project.
- Use `FlatList`/`SectionList` (or the project's list library) for long lists. Never map a long array into a `ScrollView`.
- Store tokens in secure storage (e.g. `expo-secure-store`), never AsyncStorage.
- Builds and store submissions (`eas build`, `eas submit`) always go to the user first. The Mason guard enforces this.
