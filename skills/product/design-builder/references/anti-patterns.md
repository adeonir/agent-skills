# Anti-Patterns

Deterministic anti-pattern catalog for design validation and HTML preview checks.
Each rule documents a recognizable failure mode with the smallest sufficient fix
and a paired HTML example.

## When to Use

Auto-loaded by `validate.md` as a gate before DESIGN.md lands and during HTML preview review.
Also referenced by `preview.md` during variant generation to avoid known failure shapes upfront.

## Categories

- **Typography** — fonts, weights, scale, pairing
- **Color and Theme** — palette, contrast, theme commitment
- **Layout and Spacing** — composition, density, alignment, rhythm
- **Decoration and Depth** — shadow, radius, glass, layering
- **Component States** — hover, focus, disabled, loading, empty
- **Motion and Interaction** — easing, transitions, hover feedback
- **Accessibility** — keyboard nav, semantic HTML, ARIA, contrast ratios
- **Performance** — CDN abuse, layout shift, blocking renders
- **Hydration and SSR** — React/Next.js client/server divergence
- **Drift** — HTML output not aligned with DESIGN.md tokens (single-source violations)

## Rule Template

ALWAYS use this exact template structure:

```markdown
### {rule-id-kebab-case}
**Category:** {category name from above}
**Severity:** {error | warning}
**Check:** {prose description of what to detect — one or two sentences}
**Fix:** {what to do instead}
**Example fail:**
```html
{minimal HTML snippet that triggers the rule}
```
**Example pass:**
```html
{minimal HTML snippet that satisfies the rule}
```
```

## Typography

### inter-as-primary-font
**Category:** Typography
**Severity:** warning
**Check:** Primary font-family of headings or body is `Inter`, `Roboto`, `Arial`, or `Helvetica` on a marketing/editorial surface (landing-page, website, e-commerce) without being a declared brand token in DESIGN.md `typography.*.fontFamily`.
**Fix:** Pick a distinctive display font (Fraunces, Spectral, Crimson, Inter Tight, IBM Plex, JetBrains Mono, etc.) and declare it in DESIGN.md. System fonts are acceptable only for `web-app`/`mobile-app` project types.
**Example fail:**
```html
<h1 style="font-family: Inter, system-ui, sans-serif">Welcome</h1>
```
**Example pass:**
```html
<h1 style="font-family: var(--font-display)">Welcome</h1>
```

### system-font-stack-on-marketing
**Category:** Typography
**Severity:** warning
**Check:** `font-family: system-ui` or `-apple-system, ...` stack used on marketing/editorial pages where brand voice matters.
**Fix:** Reserve system stacks for utility surfaces (admin, dashboards). On marketing, use a characterful display font and a refined body font.
**Example fail:**
```html
<h1 class="font-sans">Pricing</h1>
```
**Example pass:**
```html
<h1 style="font-family: var(--font-display)">Pricing</h1>
```

### weight-range-flat
**Category:** Typography
**Severity:** warning
**Check:** All text in the page uses weights between `400` and `700` only — no `100-200` for subtlety, no `800-900` for impact.
**Fix:** Push at least one role into the 100-200 or 800-900 range to create typographic drama.
**Example fail:**
```html
<h1 style="font-weight: 600">Strong but timid</h1>
<p style="font-weight: 400">Body copy</p>
```
**Example pass:**
```html
<h1 style="font-weight: 900">Bold statement</h1>
<p style="font-weight: 300">Light body for contrast</p>
```

### heading-body-ratio-shy
**Category:** Typography
**Severity:** warning
**Check:** Largest heading is less than `2.5x` the body font-size, flattening hierarchy.
**Fix:** Target at least `3x` on desktop hero; ramp down gracefully on mobile, but never collapse below `2x`.
**Example fail:**
```html
<h1 style="font-size: 24px">Headline</h1>
<p style="font-size: 16px">Body</p>
```
**Example pass:**
```html
<h1 style="font-size: 64px">Headline</h1>
<p style="font-size: 16px">Body</p>
```

### single-font-family-hierarchy
**Category:** Typography
**Severity:** warning
**Check:** Display, heading, and body all use the same font-family, eroding hierarchy.
**Fix:** Pair a display/serif/character font with a refined body sans (or inverse). Two families minimum on marketing surfaces.
**Example fail:**
```html
<h1 style="font-family: Inter">Title</h1>
<p style="font-family: Inter">Body</p>
```
**Example pass:**
```html
<h1 style="font-family: 'Fraunces', serif">Title</h1>
<p style="font-family: 'Inter', sans-serif">Body</p>
```

## Color and Theme

### purple-to-blue-gradient
**Category:** Color and Theme
**Severity:** warning
**Check:** Background or text uses `linear-gradient` from purple (`#a78bfa`, `#8b5cf6`, `#7c3aed`, etc.) to blue (`#3b82f6`, `#2563eb`, etc.). Most overused AI default.
**Fix:** Pick a single committed accent OR pair two colors that aren't the purple→blue cliché (warm→cool, neon→neutral, brand→brand-shadow).
**Example fail:**
```html
<div style="background: linear-gradient(135deg, #8b5cf6, #3b82f6)">Hero</div>
```
**Example pass:**
```html
<div style="background: linear-gradient(135deg, #ff5722, #ffb300)">Hero</div>
```

### gray-text-on-saturated-color
**Category:** Color and Theme
**Severity:** error
**Check:** Gray text (`#6b7280`, `#9ca3af`, `slate-500`, etc.) placed on saturated colored background fails WCAG AA 4.5:1 contrast.
**Fix:** Use the corresponding `*-foreground` token from DESIGN.md or recompute contrast: white/near-white on saturated backgrounds, dark gray only on neutral backgrounds.
**Example fail:**
```html
<button style="background: #3b82f6; color: #6b7280">Action</button>
```
**Example pass:**
```html
<button style="background: var(--primary); color: var(--primary-foreground)">Action</button>
```

### pure-saturated-accent
**Category:** Color and Theme
**Severity:** warning
**Check:** Accent color is pure saturated hex (`#ff0000`, `#00ff00`, `#0000ff`) without muted variant or oklch refinement.
**Fix:** Use oklch object form `{ hex, oklch }` in DESIGN.md and emit oklch values. Soften with reduced chroma or shift toward a brand-specific hue.
**Example fail:**
```html
<a style="color: #ff0000">Buy now</a>
```
**Example pass:**
```html
<a style="color: oklch(0.65 0.22 25)">Buy now</a>
```

### evenly-distributed-palette
**Category:** Color and Theme
**Severity:** warning
**Check:** Four or more brand colors used at roughly equal frequency across the page (25/25/25/25 distribution) — no hierarchy, no focal point.
**Fix:** Apply 60-30-10 rule. 60% dominant surface, 30% secondary, 10% accent. Sharp accents on committed base outperform timid even distribution.
**Example fail:**
```html
<div><span style="color:red">A</span><span style="color:blue">B</span><span style="color:green">C</span><span style="color:orange">D</span></div>
```
**Example pass:**
```html
<div><h1>A</h1><p>B</p><a style="color: var(--accent)">C</a></div>
```

### dark-pure-black-body
**Category:** Color and Theme
**Severity:** warning
**Check:** Dark theme uses true `#000000` for entire body surface (not just OLED hero accents). Causes halation and harms long-form legibility.
**Fix:** Use `#000000` only for OLED-punchy hero or accent surfaces. Soften body background to `#0a0a0a`/`#111111`/`oklch(0.15 0 0)`.
**Example fail:**
```html
<body style="background: #000; color: #fff">
  <article>Long-form content...</article>
</body>
```
**Example pass:**
```html
<body style="background: #111; color: #f3f3f3">
  <article>Long-form content...</article>
</body>
```

### theme-mixed-light-dark-sections
**Category:** Color and Theme
**Severity:** warning
**Check:** Within one section, mix of light surfaces and dark surfaces without commitment — half-measure dark mode.
**Fix:** Commit to fully dark or fully light per section. Use full-bleed dark or full-bleed light, not interleaved.
**Example fail:**
```html
<section style="background: #fff">
  <div style="background: #111; color: #fff">Half-dark inside light section</div>
</section>
```
**Example pass:**
```html
<section style="background: #111; color: #fff">Fully committed dark section</section>
```

## Layout and Spacing

### all-sections-centered
**Category:** Layout and Spacing
**Severity:** warning
**Check:** Every top-level `<section>` uses `text-align: center` or centered flex/grid, producing monotonous rhythm.
**Fix:** Break symmetry at least once per page. Asymmetric hero, left-aligned editorial section, right-aligned testimonial, etc.
**Example fail:**
```html
<section style="text-align: center">...</section>
<section style="text-align: center">...</section>
<section style="text-align: center">...</section>
```
**Example pass:**
```html
<section style="text-align: left">...</section>
<section class="grid grid-cols-[1fr_2fr]">...</section>
<section style="text-align: center">...</section>
```

### nested-cards
**Category:** Layout and Spacing
**Severity:** warning
**Check:** A bordered/shadowed card contains another bordered/shadowed card inside it. Doubles the visual chrome without adding hierarchy.
**Fix:** Flatten inner card or remove the outer surround. Use spacing and typography for grouping, not nested boxes.
**Example fail:**
```html
<div class="border rounded-lg p-6 shadow">
  <div class="border rounded-md p-4 shadow-sm">Nested</div>
</div>
```
**Example pass:**
```html
<div class="border rounded-lg p-6 shadow">
  <div class="p-4">Flat content inside the card</div>
</div>
```

### uniform-gutter
**Category:** Layout and Spacing
**Severity:** warning
**Check:** Every gap, margin, and padding in the layout uses the same value (`gap-4`, `p-4`, `mt-4`). No spacing scale rhythm.
**Fix:** Apply the spacing scale tokens — section gaps larger, component gaps medium, inline gaps small. Vary at least three steps.
**Example fail:**
```html
<section class="p-4">
  <div class="gap-4">
    <p class="mt-4">Same spacing everywhere</p>
  </div>
</section>
```
**Example pass:**
```html
<section class="p-12">
  <div class="gap-3">
    <p class="mt-1">Hierarchical spacing</p>
  </div>
</section>
```

### hero-centered-stack-default
**Category:** Layout and Spacing
**Severity:** warning
**Check:** Hero is centered eyebrow + centered headline + centered subtext + centered single CTA. Generic AI default.
**Fix:** Anchor at least one element. Asymmetric image-text split, left-aligned headline with right-aligned CTA, or overlap a visual element across the grid boundary.
**Example fail:**
```html
<section class="text-center">
  <span>Eyebrow</span>
  <h1>Headline</h1>
  <p>Subtext</p>
  <button>CTA</button>
</section>
```
**Example pass:**
```html
<section class="grid grid-cols-[1fr_1fr] items-end">
  <div>
    <span>Eyebrow</span>
    <h1>Headline</h1>
    <button>CTA</button>
  </div>
  <img src="hero.jpg" alt="">
</section>
```

### cramped-throughout
**Category:** Layout and Spacing
**Severity:** warning
**Check:** Section vertical padding under `2rem`, content max-widths over `1200px`, line-heights under `1.4`. Reads as un-reviewed dump.
**Fix:** Either generous whitespace OR controlled density — the crime is the lukewarm middle. Section paddings 4-6rem on desktop minimum for editorial; constrain measure to 60-75 characters.
**Example fail:**
```html
<section style="padding: 0.5rem">
  <p style="max-width: 1400px; line-height: 1.2">Cramped wall of text</p>
</section>
```
**Example pass:**
```html
<section style="padding: 5rem 0">
  <p style="max-width: 60ch; line-height: 1.6">Breathable text</p>
</section>
```

### section-rhythm-flat
**Category:** Layout and Spacing
**Severity:** warning
**Check:** Consecutive sections use same background color, same spacing, same layout direction — no alternation.
**Fix:** Vary backgrounds (light/dark/accent), spacing density, or layout direction between sections to create rhythm.
**Example fail:**
```html
<section class="bg-white py-12">...</section>
<section class="bg-white py-12">...</section>
<section class="bg-white py-12">...</section>
```
**Example pass:**
```html
<section class="bg-white py-16">...</section>
<section class="bg-neutral-950 text-white py-24">...</section>
<section class="bg-white py-12">...</section>
```

## Decoration and Depth

### rounded-8px-everywhere
**Category:** Decoration and Depth
**Severity:** warning
**Check:** Every interactive element uses `border-radius: 8px` (or `rounded-lg`). No corner-language variation.
**Fix:** Pick a corner system: sharp (0-2px), subtle (4-6px), medium (8-12px), or pill (full). Use one corner style per role, varying by component class.
**Example fail:**
```html
<button class="rounded-lg">A</button>
<div class="rounded-lg">B</div>
<input class="rounded-lg">
```
**Example pass:**
```html
<button class="rounded-full">A</button>
<div class="rounded-sm">B</div>
<input class="rounded-md">
```

### stock-shadow
**Category:** Decoration and Depth
**Severity:** warning
**Check:** Shadow uses default `0 4px 6px rgba(0, 0, 0, 0.1)` or framework default (`shadow-md` everywhere). No elevation hierarchy.
**Fix:** Implement three shadow levels — subtle (cards at rest), medium (hover/raised), elevated (modals). Tint shadows toward the dominant hue when possible.
**Example fail:**
```html
<div class="shadow-md">A</div>
<div class="shadow-md">B</div>
<div class="shadow-md">C</div>
```
**Example pass:**
```html
<div class="shadow-sm">Resting card</div>
<div class="shadow-md hover:shadow-lg">Raised on hover</div>
<div class="shadow-2xl">Modal</div>
```

### gradient-border-stock
**Category:** Decoration and Depth
**Severity:** warning
**Check:** Decorative gradient border using mask hack with purple→pink or purple→blue stock palette.
**Fix:** Either drop the gradient border (solid accent does the same job) or use a brand-relevant gradient with intent.
**Example fail:**
```html
<div style="background: linear-gradient(#fff, #fff) padding-box, linear-gradient(135deg, #8b5cf6, #ec4899) border-box; border: 2px solid transparent">Card</div>
```
**Example pass:**
```html
<div style="border: 2px solid var(--accent)">Card</div>
```

### glass-without-fallback
**Category:** Decoration and Depth
**Severity:** warning
**Check:** Element uses `backdrop-filter: blur(...)` without a solid `background-color` fallback. Breaks in browsers without backdrop-filter support.
**Fix:** Always pair `backdrop-filter` with a translucent solid `background-color` that reads acceptably without blur.
**Example fail:**
```html
<nav style="backdrop-filter: blur(12px)">Nav</nav>
```
**Example pass:**
```html
<nav style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(12px)">Nav</nav>
```

### shadow-on-every-surface
**Category:** Decoration and Depth
**Severity:** warning
**Check:** Cards, buttons, sections, and inputs all carry shadows — no surfaces are flat. Erodes hierarchy.
**Fix:** Reserve shadows for elements that actually need to lift (interactive cards, modals). Keep most surfaces flat.
**Example fail:**
```html
<section class="shadow-lg">
  <div class="shadow-md">
    <button class="shadow-md">Click</button>
  </div>
</section>
```
**Example pass:**
```html
<section>
  <div class="shadow-md">
    <button>Click</button>
  </div>
</section>
```

## Component States

### missing-hover-states
**Category:** Component States
**Severity:** error
**Check:** Interactive element (`<a>`, `<button>`, `[role="button"]`, `[onClick]`) has no `:hover` styling — no color change, no transform, no shadow shift.
**Fix:** Combine color change with `transform` (slight scale or translate) and `box-shadow` shift for tactile feedback. Missing hover signals broken interactivity.
**Example fail:**
```html
<button class="bg-blue-500 text-white">Click</button>
```
**Example pass:**
```html
<button class="bg-blue-500 text-white hover:bg-blue-600 hover:-translate-y-0.5 hover:shadow-lg transition">Click</button>
```

### focus-state-removed
**Category:** Component States
**Severity:** error
**Check:** `outline: none` or `outline-none` applied without a `:focus-visible` replacement.
**Fix:** Add `focus-visible:ring-2 focus-visible:ring-offset-2` or visible outline replacement.
**Example fail:**
```html
<button class="outline-none">Click</button>
```
**Example pass:**
```html
<button class="outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500">Click</button>
```

### empty-state-blank
**Category:** Component States
**Severity:** warning
**Check:** Container that may render empty arrays/strings shows blank whitespace with no message, illustration, or CTA.
**Fix:** Always render an empty state: illustration or icon + descriptive message + optional CTA.
**Example fail:**
```html
<ul>{items.map(item => <li>{item}</li>)}</ul>
```
**Example pass:**
```html
{items.length === 0 ? <div><p>No items yet</p><button>Add one</button></div> : <ul>...</ul>}
```

### icon-floating-no-anchor
**Category:** Component States
**Severity:** warning
**Check:** Small monochrome icon (`<svg>`, `<iconify-icon>`) rendered without container, label, or border — visually disappears.
**Fix:** Anchor every icon with a colored container, text label, or both.
**Example fail:**
```html
<iconify-icon icon="lucide:search"></iconify-icon>
```
**Example pass:**
```html
<button class="p-2 rounded-md bg-neutral-100" aria-label="Search">
  <iconify-icon icon="lucide:search"></iconify-icon>
</button>
```

### button-stock-blue
**Category:** Component States
**Severity:** warning
**Check:** Primary button uses default framework blue (`#3b82f6`, `bg-blue-500`) without being mapped to a brand token.
**Fix:** Map primary button to `bg-primary` resolved from DESIGN.md `colors.primary`.
**Example fail:**
```html
<button class="bg-blue-500 text-white">Submit</button>
```
**Example pass:**
```html
<button class="bg-primary text-primary-foreground">Submit</button>
```

## Motion and Interaction

### ease-default-no-intention
**Category:** Motion and Interaction
**Severity:** warning
**Check:** Transitions/animations use bare `ease` or `ease-in-out` without an intentional `cubic-bezier` matching the project tone.
**Fix:** Pick a curve per tone — snappy (`cubic-bezier(0.22, 1, 0.36, 1)`) for tech, gentle (`cubic-bezier(0.25, 0.1, 0.25, 1)`) for editorial, bouncy (`cubic-bezier(0.34, 1.56, 0.64, 1)`) for playful.
**Example fail:**
```html
<button style="transition: all 200ms ease">A</button>
```
**Example pass:**
```html
<button style="transition: transform 200ms cubic-bezier(0.22, 1, 0.36, 1)">A</button>
```

### transition-all
**Category:** Motion and Interaction
**Severity:** error
**Check:** `transition: all` or `transition-all` Tailwind class. Animates unintended properties (font-size, color) and causes layout thrash.
**Fix:** List properties explicitly: `transition: transform 200ms, opacity 200ms`.
**Example fail:**
```html
<div class="transition-all hover:scale-105">A</div>
```
**Example pass:**
```html
<div class="transition-transform hover:scale-105">A</div>
```

### animation-without-stagger
**Category:** Motion and Interaction
**Severity:** warning
**Check:** Multiple elements animate in simultaneously on page load instead of staggered orchestration.
**Fix:** Apply `animation-delay` per child to stagger entrance (50-100ms increments). One choreographed moment beats scattered micro-animations.
**Example fail:**
```html
<div class="fade-in">A</div>
<div class="fade-in">B</div>
<div class="fade-in">C</div>
```
**Example pass:**
```html
<div class="fade-in" style="animation-delay: 0ms">A</div>
<div class="fade-in" style="animation-delay: 80ms">B</div>
<div class="fade-in" style="animation-delay: 160ms">C</div>
```

### motion-no-reduced-variant
**Category:** Motion and Interaction
**Severity:** error
**Check:** Animations defined without `@media (prefers-reduced-motion: reduce)` override.
**Fix:** Provide reduced variant (zero-duration or disabled animation) for users with motion sensitivity.
**Example fail:**
```html
<style>.fade-in { animation: fade 600ms ease-out }</style>
```
**Example pass:**
```html
<style>
.fade-in { animation: fade 600ms ease-out }
@media (prefers-reduced-motion: reduce) { .fade-in { animation: none } }
</style>
```

## Accessibility

### div-onclick-for-action
**Category:** Accessibility
**Severity:** error
**Check:** `<div onClick>` or `<span onClick>` used for an actionable element instead of `<button>` or `<a>`.
**Fix:** Use `<button>` for actions, `<a>`/`<Link>` for navigation. Native elements come with keyboard, focus, and ARIA semantics for free.
**Example fail:**
```html
<div onClick={handleClick}>Submit</div>
```
**Example pass:**
```html
<button onClick={handleClick}>Submit</button>
```

### icon-button-no-aria-label
**Category:** Accessibility
**Severity:** error
**Check:** Button containing only an icon (no visible text) without `aria-label`.
**Fix:** Add `aria-label` describing the action, and `aria-hidden="true"` on the decorative icon.
**Example fail:**
```html
<button><iconify-icon icon="lucide:x"></iconify-icon></button>
```
**Example pass:**
```html
<button aria-label="Close"><iconify-icon icon="lucide:x" aria-hidden="true"></iconify-icon></button>
```

### form-input-no-label
**Category:** Accessibility
**Severity:** error
**Check:** `<input>`, `<select>`, or `<textarea>` without an associated `<label>` (via `htmlFor`/`for`) or `aria-label`.
**Fix:** Wrap with `<label>` or add `htmlFor`/`for` pointing to the input id. Floating placeholders are not a substitute.
**Example fail:**
```html
<input type="email" placeholder="Email">
```
**Example pass:**
```html
<label for="email">Email</label>
<input id="email" type="email">
```

### user-scalable-disabled
**Category:** Accessibility
**Severity:** error
**Check:** Viewport meta uses `user-scalable=no` or `maximum-scale=1`. Disables pinch-zoom for users who need it.
**Fix:** Remove `user-scalable=no` and `maximum-scale=1`. Never disable pinch zoom.
**Example fail:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
```
**Example pass:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### heading-level-skipped
**Category:** Accessibility
**Severity:** error
**Check:** Heading hierarchy skips levels (e.g., `<h1>` followed by `<h3>` with no `<h2>`).
**Fix:** Maintain ordered hierarchy `<h1>` → `<h2>` → `<h3>`. Use CSS for visual size, never skip semantic levels.
**Example fail:**
```html
<h1>Title</h1>
<h3>Subsection</h3>
```
**Example pass:**
```html
<h1>Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

### image-no-alt
**Category:** Accessibility
**Severity:** error
**Check:** `<img>` without `alt` attribute. Decorative images must use `alt=""` explicitly.
**Fix:** Add descriptive `alt` for meaningful images, `alt=""` for decorative.
**Example fail:**
```html
<img src="hero.jpg">
```
**Example pass:**
```html
<img src="hero.jpg" alt="Two designers reviewing wireframes">
```

### autofocus-on-mobile
**Category:** Accessibility
**Severity:** warning
**Check:** `autoFocus` applied to inputs on mobile-app or screen-based project types. Forces keyboard open immediately, jumps the viewport.
**Fix:** Reserve `autoFocus` for desktop primary input only. Even on desktop, use sparingly.
**Example fail:**
```html
<input type="text" autoFocus>
```
**Example pass:**
```html
<input type="text">
```

### paste-blocked
**Category:** Accessibility
**Severity:** error
**Check:** `onPaste` handler with `preventDefault()`. Breaks password managers, autofill, accessibility tools.
**Fix:** Never block paste. Validate after paste if needed.
**Example fail:**
```html
<input onPaste={e => e.preventDefault()}>
```
**Example pass:**
```html
<input onPaste={e => validateAfterPaste(e.target.value)}>
```

## Performance

### image-no-dimensions
**Category:** Performance
**Severity:** error
**Check:** `<img>` without explicit `width` and `height` attributes. Causes cumulative layout shift (CLS).
**Fix:** Always set `width` and `height` (intrinsic ratio) or `aspect-ratio` container.
**Example fail:**
```html
<img src="hero.jpg" alt="">
```
**Example pass:**
```html
<img src="hero.jpg" alt="" width="1200" height="800">
```

### large-list-no-virtualization
**Category:** Performance
**Severity:** warning
**Check:** `.map()` over array of 50+ items rendered as DOM nodes without virtualization or `content-visibility: auto`.
**Fix:** Virtualize with `virtua`, `react-window`, `@tanstack/react-virtual`, or apply `content-visibility: auto`.
**Example fail:**
```html
<ul>{thousands.map(item => <li>{item}</li>)}</ul>
```
**Example pass:**
```html
<Virtualizer items={thousands} renderItem={item => <li>{item}</li>} />
```

### below-fold-image-eager
**Category:** Performance
**Severity:** warning
**Check:** Below-fold image without `loading="lazy"`. Wastes bandwidth and main-thread parse time.
**Fix:** Add `loading="lazy"` to below-fold images. Reserve `fetchpriority="high"` / `priority` for the LCP candidate only.
**Example fail:**
```html
<img src="footer.jpg" alt="" width="800" height="400">
```
**Example pass:**
```html
<img src="footer.jpg" alt="" width="800" height="400" loading="lazy">
```

### hardcoded-date-format
**Category:** Performance
**Severity:** warning
**Check:** Date or number rendered with hardcoded string format instead of `Intl.DateTimeFormat` / `Intl.NumberFormat`.
**Fix:** Use `Intl.*` formatters so locale, calendar, and number conventions follow the user's environment.
**Example fail:**
```html
<time>{`${month}/${day}/${year}`}</time>
```
**Example pass:**
```html
<time>{new Intl.DateTimeFormat(locale).format(date)}</time>
```

### critical-font-no-preload
**Category:** Performance
**Severity:** warning
**Check:** Critical above-fold font loaded via CSS `@font-face` only, without `<link rel="preload" as="font" crossorigin>` and `font-display: swap`.
**Fix:** Preload the critical font in `<head>` and use `font-display: swap`.
**Example fail:**
```html
<style>@font-face { font-family: Display; src: url(/fonts/display.woff2) }</style>
```
**Example pass:**
```html
<link rel="preload" href="/fonts/display.woff2" as="font" type="font/woff2" crossorigin>
<style>@font-face { font-family: Display; src: url(/fonts/display.woff2); font-display: swap }</style>
```

## Hydration and SSR

### controlled-input-no-onchange
**Category:** Hydration and SSR
**Severity:** error
**Check:** React `<input>` with `value` prop but no `onChange` handler. React warns and the input becomes read-only.
**Fix:** Either add `onChange` (controlled) or use `defaultValue` (uncontrolled).
**Example fail:**
```html
<input value={text}>
```
**Example pass:**
```html
<input value={text} onChange={e => setText(e.target.value)}>
```

### date-render-ssr-mismatch
**Category:** Hydration and SSR
**Severity:** error
**Check:** Date/time rendered inline during SSR (`new Date().toLocaleString()`) without guard. Causes hydration mismatch.
**Fix:** Defer to `useEffect` for client-only rendering, or pass server timestamp as prop and format on client mount.
**Example fail:**
```html
<span>{new Date().toLocaleString()}</span>
```
**Example pass:**
```html
const [now, setNow] = useState(null)
useEffect(() => setNow(new Date().toLocaleString()), [])
<span>{now}</span>
```

### suppress-hydration-blanket
**Category:** Hydration and SSR
**Severity:** warning
**Check:** `suppressHydrationWarning` applied to a root or wide-scope element as a blanket fix instead of the smallest scope that mismatches.
**Fix:** Scope `suppressHydrationWarning` to the exact node that legitimately differs (e.g., a timestamp span). Never on `<body>` or layout wrappers.
**Example fail:**
```html
<html suppressHydrationWarning>...</html>
```
**Example pass:**
```html
<time suppressHydrationWarning>{formattedDate}</time>
```

## Drift

### inline-hex-not-in-tokens
**Category:** Drift
**Severity:** error
**Check:** Rendered HTML contains an inline color hex (`style="color: #abc123"` or class `bg-[#abc123]`) that is not present in DESIGN.md `colors` frontmatter.
**Fix:** Either add the color to DESIGN.md as a token and reference it via `bg-{name}` / `var(--{name})`, or replace with the nearest existing token.
**Example fail:**
```html
<div style="background: #7d3aed">Hero</div>
```
**Example pass:**
```html
<div class="bg-primary">Hero</div>
```

### inline-style-bypass-tokens
**Category:** Drift
**Severity:** warning
**Check:** Inline `style="padding: 12px"`, `style="border-radius: 9px"`, or `class="p-[15px]"` used for properties that have token equivalents in DESIGN.md `spacing` / `rounded` / `elevation`.
**Fix:** Replace inline literal with the nearest token (`p-4`, `rounded-md`, or `var(--spacing-4)`).
**Example fail:**
```html
<div style="padding: 12px; border-radius: 9px">A</div>
```
**Example pass:**
```html
<div class="p-3 rounded-md">A</div>
```

### font-family-not-in-tokens
**Category:** Drift
**Severity:** error
**Check:** Rendered HTML uses a font-family not declared in DESIGN.md `typography.*.fontFamily`.
**Fix:** Either declare the font in DESIGN.md as a token role and reference it, or swap to an existing token role.
**Example fail:**
```html
<h1 style="font-family: Playfair Display">Title</h1>
```
**Example pass:**
```html
<h1 style="font-family: var(--font-display)">Title</h1>
```

### arbitrary-tailwind-value-repeated
**Category:** Drift
**Severity:** warning
**Check:** Same arbitrary Tailwind value (`w-[317px]`, `bg-[#abc123]`, `mt-[7px]`) appears 2+ times in the same variant.
**Fix:** Promote to `@theme` in the inline `<style type="text/tailwindcss">` block once, then reference everywhere as a named utility.
**Example fail:**
```html
<div class="bg-[#abc123]">A</div>
<div class="bg-[#abc123]">B</div>
```
**Example pass:**
```html
<style type="text/tailwindcss">@theme { --color-brand: #abc123; }</style>
<div class="bg-brand">A</div>
<div class="bg-brand">B</div>
```

### copy-string-in-design-md
**Category:** Drift
**Severity:** warning
**Check:** DESIGN.md prose (Section 1 Overview, Section 7 Components, Section 11 Agent Prompt Guide) contains literal product copy — real headlines, CTAs, feature names, or product pitches.
**Fix:** Move every product string to `copy.yaml`. Keep DESIGN.md content-agnostic; use placeholders like `[Headline]`, `[CTA Label]` in Section 11 prompts.
**Example fail:**
```markdown
## 11. Agent Prompt Guide
- Use the hero pattern: "Ship Faster With Acme — Start Free Today"
```
**Example pass:**
```markdown
## 11. Agent Prompt Guide
- Use the hero pattern: "[Eyebrow] — [Headline] — [CTA Label]"
```
