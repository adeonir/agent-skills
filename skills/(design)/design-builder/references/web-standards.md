# Web Standards

Implementation rules for generated HTML and React code.
These complement [aesthetics.md](aesthetics.md) (visual principles) with technical correctness.
Apply to every component produced by frontend.md and variants.md.

## When to Use

Auto-loaded by frontend.md and variants.md as implementation rules. Not a direct trigger.

## Accessibility

- Icon-only buttons need `aria-label`.
- Form controls need `<label>` (with `htmlFor`) or `aria-label`.
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`) when not using native elements.
- `<button>` for actions, `<a>`/`<Link>` for navigation -- never `<div onClick>` or `<span onClick>`.
- Images need `alt` (or `alt=""` if decorative).
- Decorative icons need `aria-hidden="true"`.
- Async updates (toasts, validation messages) need `aria-live="polite"`.
- Use semantic HTML before ARIA -- `<button>`, `<a>`, `<label>`, `<table>`, `<nav>`, `<dialog>`.
- Headings follow hierarchical order `<h1>` through `<h6>` -- never skip levels.
- Include skip-to-content link as first focusable element.
- Anchor targets with `scroll-margin-top` to clear fixed headers.

## Focus States

- Every interactive element needs visible focus: `focus-visible:ring-*` or equivalent outline.
- Never `outline-none` / `outline: none` without a `focus-visible` replacement.
- Use `:focus-visible` over `:focus` -- avoids focus ring on mouse click.
- Group focus with `:focus-within` for compound controls (search bar with button, input groups).

## Forms

- Inputs need `autocomplete` and meaningful `name` attributes.
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode` for mobile keyboards.
- Never block paste (`onPaste` + `preventDefault`).
- Labels must be clickable -- `htmlFor` or wrapping the control.
- `spellCheck={false}` on emails, codes, usernames.
- Checkbox/radio: label + control share a single hit target with no dead zones.
- Submit button stays enabled until request starts; show spinner during request.
- Errors inline next to fields; focus first error on submit.
- Placeholders end with `...` and show an example pattern when useful.
- `autocomplete="off"` on non-auth fields to avoid password manager triggers.
- Warn before navigation with unsaved changes (`beforeunload` or router guard).

## Animation (Technical)

Rules for implementation -- see aesthetics.md for creative direction.

- Honor `prefers-reduced-motion`: provide reduced variant or disable entirely.
- Animate only `transform` and `opacity` (compositor-friendly, no layout thrashing).
- Never `transition: all` -- list properties explicitly.
- Set correct `transform-origin` for scale and rotation.
- SVG transforms go on `<g>` wrapper with `transform-box: fill-box; transform-origin: center`.
- Animations must be interruptible -- respond to user input mid-animation.

## Typography (Technical)

Rules for text rendering -- see aesthetics.md for pairing and hierarchy.

- Ellipsis character: `...` not `...` in static text (use CSS `text-overflow: ellipsis` for truncation).
- Curly quotes `\u201c` `\u201d` in copy, not straight `"`.
- Non-breaking spaces: `10&nbsp;MB`, `\u2318&nbsp;K`, multi-word brand names.
- Loading states end with `...`: `"Loading..."`, `"Saving..."`.
- `font-variant-numeric: tabular-nums` on number columns, prices, and comparisons.
- `text-wrap: balance` or `text-wrap: pretty` on headings to prevent widows.

## Content Handling

- Text containers must handle long content: `truncate`, `line-clamp-*`, or `break-words`.
- Flex children need `min-w-0` (or `min-width: 0`) to allow text truncation.
- Handle empty states -- never render broken UI for empty strings or arrays.
- Anticipate short, average, and very long user-generated content.

## Images

- `<img>` needs explicit `width` and `height` attributes to prevent CLS.
- Below-fold images: `loading="lazy"`.
- Above-fold critical images: `priority` (Next.js) or `fetchpriority="high"`.
- Aspect ratio containers (`aspect-video`, `aspect-square`) for placeholder slots.

## Performance

- Large lists (50+ items): virtualize with `virtua`, `react-window`, or `content-visibility: auto`.
- No layout reads in render path (`getBoundingClientRect`, `offsetHeight`, `scrollTop`).
- Batch DOM reads and writes -- never interleave.
- Prefer uncontrolled inputs for performance; controlled inputs must be cheap per keystroke.
- `<link rel="preconnect">` for CDN and asset domains.
- Critical fonts: `<link rel="preload" as="font" crossorigin>` with `font-display: swap`.

## Navigation and State

- URL reflects meaningful state -- filters, tabs, pagination, expanded panels in query params.
- Links use `<a>` / `<Link>` for proper Cmd/Ctrl+click and middle-click support.
- Deep-link all stateful UI: if it uses `useState`, consider URL sync (nuqs, searchParams).
- Destructive actions need confirmation modal or undo window -- never immediate delete.

## Touch and Interaction

- `touch-action: manipulation` on interactive areas (prevents double-tap zoom delay).
- `-webkit-tap-highlight-color` set intentionally (transparent or themed).
- `overscroll-behavior: contain` in modals, drawers, and sheets.
- During drag operations: disable text selection, `inert` on dragged element.
- `autoFocus` sparingly -- desktop only, single primary input. Avoid on mobile.

## Safe Areas

- Full-bleed layouts need `env(safe-area-inset-*)` padding for notch devices.
- Avoid unwanted scrollbars: `overflow-x-hidden` on root, fix content overflow at source.
- Prefer flex/grid over JS measurement for layout.

## Dark Mode (Technical)

Rules for implementation -- see aesthetics.md for color direction.

- `color-scheme: dark` on `<html>` for dark themes (fixes scrollbar and input colors).
- `<meta name="theme-color">` matches the page background color.
- Native `<select>`: set explicit `background-color` and `color` (Windows dark mode breaks without them).

## Internationalization

- Dates and times: use `Intl.DateTimeFormat`, not hardcoded formats.
- Numbers and currency: use `Intl.NumberFormat`, not hardcoded formats.
- Language detection via `Accept-Language` / `navigator.languages`, not IP geolocation.

## Hydration Safety (React/Next.js)

- Inputs with `value` need `onChange` handler (or use `defaultValue` for uncontrolled).
- Date/time rendering: guard against server/client mismatch with `useEffect` or `suppressHydrationWarning`.
- `suppressHydrationWarning` only where genuinely needed -- never as a blanket fix.

## Hover and Interactive States

- Buttons and links need `hover:` state for visual feedback.
- Interactive states increase contrast progressively: rest < hover < active < focus.

## Content and Copy

- Active voice: "Install the CLI" not "The CLI will be installed".
- Title Case for headings and button labels (Chicago style).
- Numerals for counts: "8 deployments" not "eight deployments".
- Specific button labels: "Save API Key" not "Continue".
- Error messages include fix or next step, not just the problem description.

## Anti-Patterns

Flag and avoid these in generated code:

| Pattern | Fix |
|---------|-----|
| `user-scalable=no` or `maximum-scale=1` | Remove -- never disable pinch zoom |
| `onPaste` + `preventDefault` | Remove paste blocking |
| `transition: all` | List properties explicitly |
| `outline-none` without `focus-visible` replacement | Add visible focus state |
| `<div onClick>` / `<span onClick>` for actions | Use `<button>` or `<a>` |
| Images without `width`/`height` | Add dimensions to prevent CLS |
| Large arrays with `.map()` and no virtualization | Virtualize lists over 50 items |
| Form inputs without labels | Add `<label>` or `aria-label` |
| Icon buttons without `aria-label` | Add descriptive label |
| Hardcoded date/number formats | Use `Intl.*` formatters |
| `autoFocus` without justification | Remove or limit to desktop primary input |
