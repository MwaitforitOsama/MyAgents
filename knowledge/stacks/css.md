# CSS

## Detect
- `*.css`, `*.scss` / `*.sass`, `*.less`, CSS Modules (`*.module.css`), `tailwind.config.*` or `@import "tailwindcss"`, `postcss.config.*`
- CSS-in-JS: `styled-components`, `@emotion/*`, vanilla-extract; Angular component styles (`styleUrls` / `styles`, `ViewEncapsulation`)
- React Native has no CSS: `StyleSheet.create`, Flexbox defaults that differ from the web. Check the React Native docs.
- Browser targets: `browserslist` in `package.json` or `.browserslistrc`

## Official sources
- MDN CSS reference: https://developer.mozilla.org/en-US/docs/Web/CSS
- W3C CSS specifications index: https://www.w3.org/Style/CSS/specs.en.html
- Browser support: https://caniuse.com
- Baseline (cross-browser availability): https://web.dev/baseline
- Tailwind docs (if used, match the major version): https://tailwindcss.com/docs
- Sass docs (if used): https://sass-lang.com/documentation/

## Decision checkpoints
- **One styling approach per project.** Follow the one in place. Don't add a second system.
- **Design tokens:** colors, spacing and typography come from variables or the theme, not literal values.
- **Layout:** Flexbox for one dimension, Grid for two. Avoid absolute positioning for layout.
- **Responsive:** the breakpoints the project already defines; container queries only if the browser targets support them.

## Checks
- Text contrast meets WCAG 2.2 AA (4.5:1 for normal text). https://www.w3.org/TR/WCAG22/
- Focus styles are visible. Don't remove `outline` without a replacement.
- `prefers-reduced-motion` is respected for animations.
- No `!important` added to win a specificity fight. Fix the selector instead.
- Units: `rem` for type and spacing so user font settings work.
- Nothing overflows at small widths (320px) or at 200% zoom.

## Implementation (Mason)
- Reuse existing tokens, utility classes and components before writing new CSS.
- Keep styles scoped the way the project scopes them (CSS Modules, component styles, Tailwind classes).
- Check every visual change in a real browser at mobile and desktop widths. If you can't, say so and tell the user what to look at.

## Version-sensitive areas
Newer features such as nesting, `:has()`, container queries, cascade layers and `@scope`. Check Baseline status and the project's browser targets before using them.
