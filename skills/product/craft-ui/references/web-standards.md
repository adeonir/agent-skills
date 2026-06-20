# Web Standards

Technical correctness rules for rendered UI — the implementation counterpart to
the craft dimension references' visual recipes. They serve two jobs: rules
that render applies to every variant it generates, **and** the rubric that audit
checks a running UI against (accessibility, performance, responsive, theming).

## When to Use

Composed by render.md (as generation rules) and audit.md (as the technical audit
rubric, mapped to its five dimensions). Not a direct trigger.

## Accessibility

- Icon-only buttons need `aria-label`.
- Form controls need `<label>` (with `htmlFor`) or `aria-label`.
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`) when not using native elements.
- `<button>` for actions, `<a>`/`<Link>` for navigation — never `<div onClick>` or `<span onClick>`.
- Images need `alt` (or `alt=""` if decorative).
- Decorative icons need `aria-hidden="true"`.
- Async updates (toasts, validation messages) need `aria-live="polite"`.
- Use semantic HTML before ARIA — `<button>`, `<a>`, `<label>`, `<table>`, `<nav>`, `<dialog>`.
- Headings follow hierarchical order `<h1>` through `<h6>` — never skip levels.
- Include skip-to-content link as first focusable element.
- Anchor targets with `scroll-margin-top` to clear fixed headers.

## Focus States

- Every interactive element needs visible focus: `focus-visible:ring-*` or equivalent outline.
- Never `outline-none` / `outline: none` without a `focus-visible` replacement.
- Use `:focus-visible` over `:focus` — avoids focus ring on mouse click.
- Group focus with `:focus-within` for compound controls (search bar with button, input groups).

## Forms

- Inputs need `autocomplete` and meaningful `name` attributes.
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode` for mobile keyboards.
- Never block paste (`onPaste` + `preventDefault`).
- Labels must be clickable — `htmlFor` or wrapping the control.
- `spellCheck={false}` on emails, codes, usernames.
- Checkbox/radio: label + control share a single hit target with no dead zones.
- Submit button stays enabled until request starts; show spinner during request.
- Errors inline next to fields; focus first error on submit.
- Placeholders end with `...` and show an example pattern when useful.
- `autocomplete="off"` on non-auth fields to avoid password manager triggers.
- Warn before navigation with unsaved changes (`beforeunload` or router guard).

## Animation (Technical)

Rules for implementation — see motion.md for creative direction.

- Honor `prefers-reduced-motion`: provide reduced variant or disable entirely.
- Animate only `transform` and `opacity` (compositor-friendly, no layout thrashing).
- Never `transition: all` — list properties explicitly.
- Set correct `transform-origin` for scale and rotation.
- SVG transforms go on `<g>` wrapper with `transform-box: fill-box; transform-origin: center`.
- Animations must be interruptible — respond to user input mid-animation.

## Typography (Technical)

Rules for text rendering — see typography.md for pairing and heuristics.md for hierarchy.

- Ellipsis character: `...` not `...` in static text (use CSS `text-overflow: ellipsis` for truncation).
- Curly quotes `\u201c` `\u201d` in copy, not straight `"`.
- Non-breaking spaces: `10&nbsp;MB`, `\u2318&nbsp;K`, multi-word brand names.
- Loading states end with `...`: `"Loading..."`, `"Saving..."`.
- `font-variant-numeric: tabular-nums` on number columns, prices, and comparisons.
- `text-wrap: balance` or `text-wrap: pretty` on headings to prevent widows.

## Content Handling

- Text containers must handle long content: `truncate`, `line-clamp-*`, or `break-words`.
- Flex children need `min-w-0` (or `min-width: 0`) to allow text truncation.
- Handle empty states — never render broken UI for empty strings or arrays.
- Anticipate short, average, and very long user-generated content.

## Images

- `<img>` needs explicit `width` and `height` attributes to prevent CLS.
- Below-fold images: `loading="lazy"`.
- Above-fold critical images: `priority` (Next.js) or `fetchpriority="high"`.
- Aspect ratio containers (`aspect-video`, `aspect-square`) for placeholder slots.

## Performance

Loading, rendering, network, framework, and Core Web Vitals live in
[performance.md](performance.md) — the audit's Performance dimension composes it.

## Navigation and State

- URL reflects meaningful state — filters, tabs, pagination, expanded panels in query params.
- Links use `<a>` / `<Link>` for proper Cmd/Ctrl+click and middle-click support.
- Deep-link all stateful UI: if it uses `useState`, consider URL sync (nuqs, searchParams).
- Destructive actions need confirmation modal or undo window — never immediate delete.

## Touch and Interaction

- `touch-action: manipulation` on interactive areas (prevents double-tap zoom delay).
- `-webkit-tap-highlight-color` set intentionally (transparent or themed).
- `overscroll-behavior: contain` in modals, drawers, and sheets.
- During drag operations: disable text selection, `inert` on dragged element.
- `autoFocus` sparingly — desktop only, single primary input. Avoid on mobile.

## Safe Areas

- Full-bleed layouts need `env(safe-area-inset-*)` padding for notch devices.
- Avoid unwanted scrollbars: `overflow-x-hidden` on root, fix content overflow at source.
- Prefer flex/grid over JS measurement for layout.

## Dark Mode (Technical)

Rules for implementation — see color.md for color direction.

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
- `suppressHydrationWarning` only where genuinely needed — never as a blanket fix.

## Hover and Interactive States

- Buttons and links need `hover:` state for visual feedback.
- Interactive states increase contrast progressively: rest < hover < active < focus.

## Content and Copy

- Active voice: "Install the CLI" not "The CLI will be installed".
- Title Case for headings and button labels (Chicago style).
- Numerals for counts: "8 deployments" not "eight deployments".
- Specific button labels: "Save API Key" not "Continue".
- Error messages include fix or next step, not just the problem description.

For failure-mode rules and HTML examples, see [anti-patterns.md](anti-patterns.md).
