# HTML

## Detect
- `*.html`, Angular templates (`*.component.html`), JSX/TSX in React and Next.js, server templates (Go `html/template`, `*.tmpl`)

## Official sources
- HTML Living Standard (WHATWG): https://html.spec.whatwg.org/multipage/
- MDN HTML reference: https://developer.mozilla.org/en-US/docs/Web/HTML
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- ARIA Authoring Practices Guide: https://www.w3.org/WAI/ARIA/apg/
- Nu HTML Checker: https://validator.w3.org/nu/

## Decision checkpoints
- **Semantics first:** `button` for actions, `a` for navigation, real headings in order, landmarks (`header`, `nav`, `main`, `footer`).
- **Forms:** every input has a `label`; correct `type`, `autocomplete` and `inputmode`; errors linked with `aria-describedby`.
- **ARIA only when HTML can't express it.** No ARIA is better than wrong ARIA (see the APG).

## Checks
- Everything works with the keyboard alone: reachable, operable, and in a logical order.
- Images have meaningful `alt` text, or `alt=""` if decorative.
- One `h1` per page. Headings don't skip levels.
- `lang` on `<html>`. A correct viewport meta tag on web pages.
- User content is escaped. No `innerHTML` / `dangerouslySetInnerHTML` / `bypassSecurityTrust*` with unsanitized input.
- Links that open new tabs use `rel="noopener"` (or the framework's default handles it; check).

## Implementation (Mason)
- Use the framework's components and directives (Next.js `Link`/`Image`, Angular router links) where the project already does.
- After UI changes, check keyboard navigation and run the project's accessibility checks if it has them (e.g. axe in Playwright tests).

## Version-sensitive areas
New elements and attributes (e.g. `dialog`, `popover`, `inert`). Check browser support and the project's targets before using them.
