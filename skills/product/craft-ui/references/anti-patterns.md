# Anti-Patterns

Anti-pattern catalog for rendered UI. Each rule documents a recognizable failure mode and the smallest sufficient fix.

Every rule is a failure a viewer can see or a user can hit on the rendered surface. Framework and runtime correctness — hydration mismatch, reconciliation keys, server-only APIs — is source-code review and belongs elsewhere; a rule whose failure has no rendered consequence does not enter the catalog.

## When to Use

Composed by `render.md` to avoid known failure shapes during generation. Not a direct trigger.

## Categories

Jump-table — each category links to its rule section below.

- [Typography](#typography) — fonts, weights, scale, pairing
- [Color and Theme](#color-and-theme) — palette, contrast, theme commitment
- [Layout and Spacing](#layout-and-spacing) — composition, density, alignment, rhythm
- [Decoration and Depth](#decoration-and-depth) — shadow, radius, glass, layering
- [Component States](#component-states) — hover, focus, disabled, loading, empty
- [Motion and Interaction](#motion-and-interaction) — easing, transitions, hover feedback
- [Accessibility](#accessibility) — keyboard nav, semantic HTML, ARIA, contrast ratios
- [Performance](#performance) — CDN abuse, layout shift, blocking renders
- [AI Scaffolding Tells](#ai-scaffolding-tells) — reflex section-grammar and template clichés
- [Fabricated Content](#fabricated-content) — invented proof and asserted evidence no input supplied
- [Drift](#drift) — HTML not aligned with DESIGN.md tokens

## Rule Template

ALWAYS use this exact template structure:

````markdown
### {rule-id-kebab-case}
**Category:** {category name from above} **Severity:** {error | warning} **Check:** {what to detect — one or two sentences} **Fix:** {what to do instead}
````

A **deterministic** rule adds a pair, and only a deterministic rule does. The pair carries the token the Check names and nothing else — no surrounding element, no filler content, no second utility along for the ride:

````markdown
**Example fail:**
```html
{the token that trips the rule}
```
**Example pass:**
```html
{the token that satisfies it}
```
````

A **perceptual** rule ships no pair. Its Check is a read of the whole surface, which three lines of markup cannot hold; a snippet there only gives the model a literal shape to hunt for instead of the page to look at.

Neither kind carries a fix recipe in the pass example — exact shadow layers, named easing curves, and property lists are the model's craft. State the move in **Fix** and stop.

## Two Kinds of Check

A rule's Check is one of two kinds:

- **Deterministic** — the Check reduces to a selector or a value: a property, a missing attribute, a ratio (`gradient-clip-text`, `image-no-alt`, `focus-state-removed`). It has a definite answer — verify it against the markup; it either fires or it does not.
- **Perceptual** — the Check needs a holistic read: sameness, reflex, "reads as a template" (`hero-metric-template`, `all-sections-centered`, the scaffolding tells). Weigh it by eye; reasonable reviewers can disagree at the margin.

Tell them apart from the Check itself: one expressible as a query or a measurement is deterministic; one that needs a look is perceptual. render avoids both kinds during generation.

## Typography

### inter-as-primary-font
**Category:** Typography **Severity:** warning **Check:** Primary font-family of headings or body is `Inter`, `Roboto`, `Arial`, or `Helvetica` on a marketing, content, or storefront surface. **Fix:** Run the font-selection procedure in [brand.md](brand.md) and carry its pick in the display role — its reflex-reject list names the families to look past, so a font drawn from memory here repeats the failure. System fonts are acceptable only on app and dashboard screens, not on marketing or editorial surfaces. **Example fail:**
```html
font-family: Inter, system-ui, sans-serif
```
**Example pass:**
```html
font-family: var(--font-display)
```

### system-font-stack-on-marketing
**Category:** Typography **Severity:** warning **Check:** `font-family: system-ui` or `-apple-system, ...` stack used on marketing/editorial pages where brand voice matters. **Fix:** Reserve system stacks for utility surfaces (admin, dashboards). On marketing, use a characterful display font and a refined body font. **Example fail:**
```html
font-family: system-ui, -apple-system, sans-serif
```
**Example pass:**
```html
font-family: var(--font-display)
```

### weight-range-flat
**Category:** Typography **Severity:** warning **Check:** All text on a brand surface uses weights between `400` and `700` only — no `100-200` for subtlety, no `800-900` for impact. A product surface holds the middle band on purpose, where exaggerated contrast reads as noise across many type elements. **Fix:** Push at least one role into the 100-200 or 800-900 range to create typographic drama.

### heading-body-ratio-shy
**Category:** Typography **Severity:** warning **Check:** Largest heading is less than `2.5x` the body font-size on a surface led by a display hero, flattening hierarchy. A surface built on inline heads inside running prose, on dense index rows, or on a product screen runs flatter by design. **Fix:** Target at least `3x` on desktop hero; ramp down gracefully on mobile, but never collapse below `2x`. **Example fail:**
```html
h1 { font-size: 24px } / body { font-size: 16px }
```
**Example pass:**
```html
h1 { font-size: 64px } / body { font-size: 16px }
```

### single-font-family-hierarchy
**Category:** Typography **Severity:** warning **Check:** Display, heading, and body share one font-family with nothing compensating for it — same weight band, shallow size ramp — so hierarchy rests on nothing. One well-chosen family is a legitimate choice; the failure is the flat execution of it, not the count. **Fix:** Either pair a display face with a refined body face, or commit to the single family with real weight and size contrast.

## Color and Theme

### purple-to-blue-gradient
**Category:** Color and Theme **Severity:** warning **Check:** Background or text uses `linear-gradient` from purple (`#a78bfa`, `#8b5cf6`, `#7c3aed`, etc.) to blue (`#3b82f6`, `#2563eb`, etc.). Most overused AI default. **Fix:** Pick a single committed accent OR pair two colors that aren't the purple→blue cliché (warm→cool, neon→neutral, brand→brand-shadow). **Example fail:**
```html
linear-gradient(135deg, #8b5cf6, #3b82f6)
```
**Example pass:**
```html
linear-gradient(135deg, var(--accent), var(--accent-shadow))
```

### gray-text-on-saturated-color
**Category:** Color and Theme **Severity:** error **Check:** Gray text (`#6b7280`, `#9ca3af`, `slate-500`, etc.) placed on saturated colored background fails WCAG AA 4.5:1 contrast. **Fix:** Use the foreground color paired with that background, or recompute contrast: white/near-white on saturated backgrounds, dark gray only on neutral backgrounds. **Example fail:**
```html
background: #3b82f6; color: #6b7280
```
**Example pass:**
```html
background: var(--primary); color: var(--primary-foreground)
```

### pure-saturated-accent
**Category:** Color and Theme **Severity:** warning **Check:** Accent color is pure saturated hex (`#ff0000`, `#00ff00`, `#0000ff`) without muted variant or oklch refinement. **Fix:** Emit the accent as an oklch value rather than raw hex. Soften with reduced chroma or shift toward a brand-specific hue. **Example fail:**
```html
color: #ff0000
```
**Example pass:**
```html
color: oklch(0.65 0.22 25)
```

### evenly-distributed-palette
**Category:** Color and Theme **Severity:** warning **Check:** Four or more brand colors used at roughly equal frequency across the page (25/25/25/25 distribution) — no hierarchy, no focal point. **Fix:** Apply 60-30-10 rule. 60% dominant surface, 30% secondary, 10% accent. Sharp accents on committed base outperform timid even distribution.

### dark-pure-black-body
**Category:** Color and Theme **Severity:** warning **Check:** Dark theme uses true `#000000` for entire body surface (not just OLED hero accents). Causes halation and harms long-form legibility. **Fix:** Use `#000000` only for OLED-punchy hero or accent surfaces. Soften body background to `#0a0a0a`/`#111111`/`oklch(0.15 0 0)`. **Example fail:**
```html
body { background: #000 }
```
**Example pass:**
```html
body { background: #111 }
```

### theme-mixed-light-dark-sections
**Category:** Color and Theme **Severity:** warning **Check:** Within one section, mix of light surfaces and dark surfaces without commitment — half-measure dark mode. **Fix:** Commit to fully dark or fully light per section. Use full-bleed dark or full-bleed light, not interleaved.

### orphan-accent-color
**Category:** Color and Theme **Severity:** warning **Check:** An accent — on a divider, icon, glyph, badge, or small decoration — whose hue is not part of the brand palette's hue family, or a third-party service color (messaging green, social blue) rendered raw. Two or more unrelated accents (a red divider beside a green icon) compound into an accidental clash. **Fix:** Pull every accent from the defined palette — the brand hue or a semantic token. Reconcile a borrowed service color toward the palette (tint or desaturate), or render the mark in a brand or neutral color. Decoration carries brand color, never an arbitrary hue.

## Layout and Spacing

### all-sections-centered
**Category:** Layout and Spacing **Severity:** warning **Check:** Every top-level `<section>` uses `text-align: center` or centered flex/grid, producing monotonous rhythm. Does not fire where a centered sequence is the arrangement itself — a surface of successive declarations, each holding the axis on purpose. **Fix:** Break symmetry at least once per page. Asymmetric hero, left-aligned editorial section, right-aligned testimonial, etc.

### nested-cards
**Category:** Layout and Spacing **Severity:** warning **Check:** A bordered/shadowed card contains another bordered/shadowed card inside it. Doubles the visual chrome without adding hierarchy. **Fix:** Flatten inner card or remove the outer surround. Use spacing and typography for grouping, not nested boxes. **Example fail:**
```html
<div class="border shadow"><div class="border shadow-sm">
```
**Example pass:**
```html
<div class="border shadow"><div class="p-4">
```

### uniform-gutter
**Category:** Layout and Spacing **Severity:** warning **Check:** Every gap, margin, and padding in the layout uses the same value (`gap-4`, `p-4`, `mt-4`). No spacing scale rhythm. **Fix:** Apply the spacing scale tokens — section gaps larger, component gaps medium, inline gaps small. Vary at least three steps.

### hero-centered-stack-default
**Category:** Layout and Spacing **Severity:** warning **Check:** Hero is centered eyebrow + centered headline + centered subtext + centered single CTA. Generic AI default. **Fix:** Anchor at least one element. Asymmetric image-text split, left-aligned headline with right-aligned CTA, or overlap a visual element across the grid boundary.

### cramped-throughout
**Category:** Layout and Spacing **Severity:** warning **Check:** Section vertical padding under `2rem`, content max-widths over `1200px`, line-heights under `1.4`. Reads as un-reviewed dump. **Fix:** Either generous whitespace OR controlled density — the crime is the lukewarm middle. Section paddings 4-6rem on desktop minimum for editorial; constrain measure to 60-75 characters. **Example fail:**
```html
padding: 0.5rem; max-width: 1400px; line-height: 1.2
```
**Example pass:**
```html
padding: 5rem 0; max-width: 60ch; line-height: 1.6
```

### section-rhythm-flat
**Category:** Layout and Spacing **Severity:** warning **Check:** Consecutive sections use same background color, same spacing, same layout direction — no alternation. Does not fire where uniformity is the arrangement's premise: a continuous document, a repeated declaration, or a grid or list of same-kind entries. **Fix:** Vary backgrounds (light/dark/accent), spacing density, or layout direction between sections to create rhythm.

## Decoration and Depth

### rounded-8px-everywhere
**Category:** Decoration and Depth **Severity:** warning **Check:** Every interactive element uses `border-radius: 8px` (or `rounded-lg`). No corner-language variation. **Fix:** Pick a corner system: sharp (0-2px), subtle (4-6px), medium (8-12px), or pill (full). Use one corner style per role, varying by component class.

### stock-shadow
**Category:** Decoration and Depth **Severity:** warning **Check:** Shadow uses default `0 4px 6px rgba(0, 0, 0, 0.1)` or framework default (`shadow-md` everywhere). No elevation hierarchy. **Fix:** Implement three shadow levels — subtle (cards at rest), medium (hover/raised), elevated (modals). Tint shadows toward the dominant hue when possible.

### gradient-border-stock
**Category:** Decoration and Depth **Severity:** warning **Check:** Decorative gradient border using mask hack with purple→pink or purple→blue stock palette. **Fix:** Either drop the gradient border (solid accent does the same job) or use a brand-relevant gradient with purpose. **Example fail:**
```html
linear-gradient(135deg, #8b5cf6, #ec4899) border-box; border: 2px solid transparent
```
**Example pass:**
```html
border: 2px solid var(--accent)
```

### glass-without-fallback
**Category:** Decoration and Depth **Severity:** warning **Check:** Element uses `backdrop-filter: blur(...)` without a solid `background-color` fallback. Breaks in browsers without backdrop-filter support. **Fix:** Always pair `backdrop-filter` with a translucent solid `background-color` that reads acceptably without blur. **Example fail:**
```html
backdrop-filter: blur(12px)
```
**Example pass:**
```html
background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(12px)
```

### shadow-on-every-surface
**Category:** Decoration and Depth **Severity:** warning **Check:** Cards, buttons, sections, and inputs all carry shadows — no surfaces are flat. Erodes hierarchy. **Fix:** Reserve shadows for elements that actually need to lift (interactive cards, modals). Keep most surfaces flat.

### cheap-vs-expensive-depth
**Category:** Decoration and Depth **Severity:** warning **Check:** Surfaces are separated by a hard, dark, opaque drop shadow (`rgba(0,0,0,0.3)`-class) or a default 1px solid grey border — the two tells of cheap depth. **Fix:** Separate by light, not by lines or hard shadow. A soft, diffused, low-opacity ambient shadow plus a translucent hairline (`rgba(0,0,0,0.05)`) and generous whitespace read premium. Use a border only where a shadow ring cannot define the surface — never as the default edge. Shadow *tiering* by elevation is `stock-shadow`; this rule owns the hard-vs-soft and border-vs-light choice.

## Component States

### missing-hover-states
**Category:** Component States **Severity:** error **Check:** Interactive element (`<a>`, `<button>`, `[role="button"]`, `[onclick]`) has no `:hover` styling — no color change, no transform, no shadow shift. **Fix:** Combine color change with `transform` (slight scale or translate) and `box-shadow` shift for tactile feedback. Missing hover signals broken interactivity. **Example fail:**
```html
<button class="bg-primary">
```
**Example pass:**
```html
<button class="bg-primary hover:bg-primary-hover">
```

### focus-state-removed
**Category:** Component States **Severity:** error **Check:** `outline: none` or `outline-none` applied without a `:focus-visible` replacement. **Fix:** Add `focus-visible:ring-2 focus-visible:ring-offset-2` or visible outline replacement. **Example fail:**
```html
<button class="outline-none">
```
**Example pass:**
```html
<button class="outline-none focus-visible:ring-2">
```

### empty-state-blank
**Category:** Component States **Severity:** warning **Check:** Container that may render empty arrays/strings shows blank whitespace with no message, illustration, or CTA. **Fix:** Always render an empty state: illustration or icon + descriptive message + optional CTA.

### icon-floating-no-anchor
**Category:** Component States **Severity:** warning **Check:** Small monochrome icon (`<svg>`, `<iconify-icon>`) rendered without container, label, or border — visually disappears. **Fix:** Anchor every icon with a colored container, text label, or both.

### button-stock-blue
**Category:** Component States **Severity:** warning **Check:** Primary button uses the framework default blue (`#3b82f6`, `bg-blue-500`) — a hue with no relation to the rest of the surface's palette. **Fix:** Draw the primary from the surface's own accent, referenced as a named utility rather than a raw value. **Example fail:**
```html
<button class="bg-blue-500">
```
**Example pass:**
```html
<button class="bg-primary">
```

## Motion and Interaction

### ease-default-no-intention
**Category:** Motion and Interaction **Severity:** warning **Check:** Transitions/animations use bare `ease` or `ease-in-out` without an intentional `cubic-bezier` matching the project tone — or a state change snaps with no transition at all. Both read as unconsidered. **Fix:** Pick a curve per tone — snappy (`cubic-bezier(0.22, 1, 0.36, 1)`) for tech, gentle (`cubic-bezier(0.25, 0.1, 0.25, 1)`) for editorial, decisive (`cubic-bezier(0.16, 1, 0.3, 1)`) for bold, never an overshoot/bounce curve — and interpolate every state change; an instant, un-interpolated jump reads cheaper than a considered 150ms. **Example fail:**
```html
transition: transform 200ms ease
```
**Example pass:**
```html
transition: transform 200ms var(--ease-out)
```

### transition-all
**Category:** Motion and Interaction **Severity:** error **Check:** `transition: all` or `transition-all` Tailwind class. Animates unintended properties (font-size, color) and causes layout thrash. **Fix:** List the properties explicitly. In Tailwind that is a single-property utility, or the bracket form when more than one property moves. **Example fail:**
```html
<div class="transition-all">
```
**Example pass:**
```html
<div class="transition-transform">
<div class="transition-[transform,color]">
```

### animation-without-stagger
**Category:** Motion and Interaction **Severity:** warning **Check:** Multiple elements animate in simultaneously on page load instead of staggered orchestration. **Fix:** Apply `animation-delay` per child to stagger entrance (50-100ms increments). One choreographed moment beats scattered micro-animations.

### motion-no-reduced-variant
**Category:** Motion and Interaction **Severity:** error **Check:** Animations defined without `@media (prefers-reduced-motion: reduce)` override. **Fix:** Provide reduced variant (zero-duration or disabled animation) for users with motion sensitivity. **Example fail:**
```html
.fade-in { animation: fade 600ms ease-out }
```
**Example pass:**
```html
@media (prefers-reduced-motion: reduce) { .fade-in { animation: none } }
```

### nothing-from-nothing
**Category:** Motion and Interaction **Severity:** warning **Check:** An element enters from `scale(0)`, or fades in from `opacity: 0` with no scale to anchor it — it materializes from nothing instead of settling into place. **Fix:** Enter from a near-resting state — `scale(0.95)` plus opacity — so the element appears to arrive, not spawn. Nothing in a considered interface pops out of the void. **Example fail:**
```html
from { transform: scale(0); opacity: 0 }
```
**Example pass:**
```html
from { transform: scale(0.95); opacity: 0 }
```

## Accessibility

### div-onclick-for-action
**Category:** Accessibility **Severity:** error **Check:** `<div onclick>` or `<span onclick>` used for an actionable element instead of `<button>` or `<a>`. **Fix:** Use `<button>` for actions, `<a>` for navigation. Native elements come with keyboard, focus, and ARIA semantics for free. **Example fail:**
```html
<div onclick="submit()">Submit</div>
```
**Example pass:**
```html
<button onclick="submit()">Submit</button>
```

### icon-button-no-aria-label
**Category:** Accessibility **Severity:** error **Check:** Button containing only an icon (no visible text) without `aria-label`. **Fix:** Add `aria-label` describing the action, and `aria-hidden="true"` on the decorative icon. **Example fail:**
```html
<button><iconify-icon icon="lucide:x"></iconify-icon></button>
```
**Example pass:**
```html
<button aria-label="Close"><iconify-icon icon="lucide:x" aria-hidden="true"></iconify-icon></button>
```

### form-input-no-label
**Category:** Accessibility **Severity:** error **Check:** `<input>`, `<select>`, or `<textarea>` without an associated `<label>` (via `for`) or `aria-label`. **Fix:** Wrap with `<label>` or add `for` pointing to the input id. Floating placeholders are not a substitute. **Example fail:**
```html
<input type="email" placeholder="Email">
```
**Example pass:**
```html
<label for="email">Email</label>
<input id="email" type="email">
```

### user-scalable-disabled
**Category:** Accessibility **Severity:** error **Check:** Viewport meta uses `user-scalable=no` or `maximum-scale=1`. Disables pinch-zoom for users who need it. **Fix:** Remove `user-scalable=no` and `maximum-scale=1`. Never disable pinch zoom. **Example fail:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
```
**Example pass:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### heading-level-skipped
**Category:** Accessibility **Severity:** error **Check:** Heading hierarchy skips levels (e.g., `<h1>` followed by `<h3>` with no `<h2>`). **Fix:** Maintain ordered hierarchy `<h1>` → `<h2>` → `<h3>`. Use CSS for visual size, never skip semantic levels. **Example fail:**
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
**Category:** Accessibility **Severity:** error **Check:** `<img>` without `alt` attribute. Decorative images must use `alt=""` explicitly. **Fix:** Add descriptive `alt` for meaningful images, `alt=""` for decorative. **Example fail:**
```html
<img src="hero.jpg">
```
**Example pass:**
```html
<img src="hero.jpg" alt="Two designers reviewing wireframes">
```

### autofocus-on-mobile
**Category:** Accessibility **Severity:** warning **Check:** `autofocus` applied to inputs on mobile app screens. Forces keyboard open immediately, jumps the viewport. **Fix:** Reserve `autofocus` for desktop primary input only. Even on desktop, use sparingly. **Example fail:**
```html
<input type="text" autofocus>
```
**Example pass:**
```html
<input type="text">
```

### paste-blocked
**Category:** Accessibility **Severity:** error **Check:** `onpaste` handler with `preventDefault()`. Breaks password managers, autofill, accessibility tools. **Fix:** Never block paste. Validate after paste if needed. **Example fail:**
```html
<input onpaste="event.preventDefault()">
```
**Example pass:**
```html
<input onpaste="validateAfterPaste(event)">
```

## Performance

### image-no-dimensions
**Category:** Performance **Severity:** error **Check:** `<img>` without explicit `width` and `height` attributes. Causes cumulative layout shift (CLS). **Fix:** Always set `width` and `height` (intrinsic ratio) or `aspect-ratio` container. **Example fail:**
```html
<img src="hero.jpg" alt="">
```
**Example pass:**
```html
<img src="hero.jpg" alt="" width="1200" height="800">
```

### large-list-no-virtualization
**Category:** Performance **Severity:** warning **Check:** A list or table of 50+ rows rendered as DOM nodes with no virtualization and no `content-visibility`. **Fix:** Apply `content-visibility: auto` with a `contain-intrinsic-size` estimate, or virtualize the list.

### below-fold-image-eager
**Category:** Performance **Severity:** warning **Check:** Below-fold image without `loading="lazy"`. Wastes bandwidth and main-thread parse time. **Fix:** Add `loading="lazy"` to below-fold images. Reserve `fetchpriority="high"` / `priority` for the LCP candidate only. **Example fail:**
```html
<img src="footer.jpg" alt="" width="800" height="400">
```
**Example pass:**
```html
<img src="footer.jpg" alt="" width="800" height="400" loading="lazy">
```

### critical-font-no-preload
**Category:** Performance **Severity:** warning **Check:** Critical above-fold font loaded via CSS `@font-face` only, without `<link rel="preload" as="font" crossorigin>` and `font-display: swap`. **Fix:** Preload the critical font in `<head>` and use `font-display: swap`. **Example fail:**
```html
@font-face { src: url(/fonts/display.woff2) }
```
**Example pass:**
```html
<link rel="preload" href="/fonts/display.woff2" as="font" crossorigin>
@font-face { src: url(/fonts/display.woff2); font-display: swap }
```

## AI Scaffolding Tells

Reflex section-grammar and template clichés — the moves an interface reaches for because "landing pages do this", not because the brief asked. Harvested as a family for render to avoid.

### side-stripe-accent-border
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** A `border-left` or `border-right` wider than 1px used as a colored accent on cards, list items, callouts, or alerts. **Fix:** Use a full border, a background tint, a leading icon or number, or nothing. The single colored side-stripe is never an intentional system. **Example fail:**
```html
<div class="border-l-4 border-accent">
```
**Example pass:**
```html
<div class="bg-accent-subtle">
```

### redrawn-ui-chrome
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** Browser, device, or editor furniture hand-built around content — a URL pill and traffic-light dots above a screenshot, a drawn phone bezel, a title bar wrapping a code block. The viewer is already looking through real chrome; a drawn copy of it is decoration standing in for context. Distinct from `fabricated-product-evidence`, which is about the content inside the frame rather than the frame. **Fix:** Put the capture in a plain `<figure>` with at most a hairline edge, or drop the frame and let the content carry itself.

### gradient-clip-text
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** `background-clip: text` (or `-webkit-background-clip: text`) over a gradient, turning text into a gradient fill. Decorative, never meaningful. **Fix:** Use a single solid color. Carry emphasis with weight or size, not a gradient wash. **Example fail:**
```html
<h1 class="bg-clip-text text-transparent">
```
**Example pass:**
```html
<h1 class="text-foreground">
```

### eyebrow-on-every-section
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** A tiny uppercase tracked label above the heading of most or every section ("ABOUT", "PROCESS", "PRICING"). One named kicker as a brand system is voice; an eyebrow on every section is grammar by reflex. **Fix:** Drop the repeated kicker. Keep at most one, and only when it carries a deliberate, named brand system.

### numbered-section-markers
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** Sequence numbers (`01 / 02 / 03`) prefixing section headings that are not an actual ordered sequence — scaffolding because "it looks structured", not because order carries meaning. The same tell wears a label: `00 / INDEX`, `002 · Featured` — a number stapled to a category name. **Fix:** Remove the numbers unless the section truly is a step in an ordered flow the reader must follow in order.

### hero-metric-template
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** The stock SaaS hero — one big number, a small label, a row of supporting stats, a gradient accent — reached for as the default hero shape. **Fix:** Lead with the actual value proposition. Use a metric only where a real, specific number earns the spotlight.

### identical-card-grid
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** Same-sized cards, each icon + heading + paragraph, repeated across the page as the default way to present any group of items. A grid of genuinely same-kind entries — products, works, index rows — is not this tell; the rule fires on varied content forced into equal cards. **Fix:** Vary the layout to the content — one item can lead and others support; some want prose, a list, or an asymmetric composition rather than another equal card.

### version-label-eyebrow
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** A fake version or status tag (`V0.6`, `BETA`, `v2.0`) set as a hero eyebrow on a marketing page, dressing the page as a product changelog it is not. **Fix:** Drop it. A version label belongs in an app chrome or a real release note, not above a headline where it only performs seriousness.

### pagination-index-static
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** A `01 / 4` counter or slash-index rendered on content that is not a paged or navigable sequence — pagination chrome as decoration. **Fix:** Remove it unless the counter tracks real position in a carousel or stepper the user moves through.

### middle-dot-separator-overuse
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** The middle dot (`·`) sprinkled through headings, eyebrows, and metadata rows more than once per line as a texture, not a separator. **Fix:** Ration it — at most one middle dot per line, and only where two peers genuinely need separating. Reach for space or a line break instead.

### floating-corner-paragraph
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** A small explainer paragraph floated into an otherwise empty corner of a section to fill space, unanchored to any element it describes. **Fix:** Anchor the text to what it explains, or cut it. Empty space is a composition choice, not a slot to backfill with prose.

### filled-progress-bar-marketing
**Category:** AI Scaffolding Tells **Severity:** warning **Check:** A filled-track progress or score bar (`72%`, a partial meter) on a marketing page where nothing is actually in progress — telemetry cosplay. **Fix:** Use a bar only for real, live state (upload, completion, capacity). On a marketing surface, state the number plainly or drop the meter.

## Fabricated Content

Claims the surface makes that no input supports. A variant is a decision aid and a shipped UI is a promise; either one carrying invented proof wins trust it did not earn. Representative imagery standing in for an asset that does not exist yet is not this family — the line is asserting a fact, not filling a picture.

### invented-proof
**Category:** Fabricated Content **Severity:** error **Check:** A metric, testimonial, customer logo, rating, or case count presented as real when no input supplied it. The tells are round marketing figures (`10,000+ teams`, `47% faster`), a testimonial under a generic name and title, and a wall of well-known logos unrelated to the product. **Fix:** Use the supplied figure; or hold the slot with a visibly unresolved placeholder and a label saying so; or take an arrangement that does not ask for proof.

### fabricated-product-evidence
**Category:** Fabricated Content **Severity:** error **Check:** A product screenshot, dashboard, chart, or data visualization depicting an interface or dataset that does not exist, rendered as the real thing. Photography standing in for a shoot is not this rule; the failure is asserting evidence. **Fix:** Show the real capture; or render the visual with data that reads as sample and label it; or take an arrangement that does not lead on product evidence.

## Drift

Drift fires against the **resolved token set** — the DESIGN.md frontmatter where it exists, the composed seed otherwise. A value outside that set is drift either way, so the rules below hold on a greenfield render as much as on one with an identity already authored.

### inline-hex-not-in-tokens
**Category:** Drift **Severity:** error **Check:** Rendered HTML contains an inline color hex (`style="color: #abc123"` or class `bg-[#abc123]`) that is not present in DESIGN.md `colors` frontmatter. **Fix:** Replace it with the nearest existing token, referenced via `bg-{name}` / `var(--{name})`. **Example fail:**
```html
<div style="background: #7d3aed">Hero</div>
```
**Example pass:**
```html
<div class="bg-primary">Hero</div>
```

### inline-style-bypass-tokens
**Category:** Drift **Severity:** warning **Check:** Inline `style="padding: 12px"`, `style="border-radius: 9px"`, or `class="p-[15px]"` used for properties that have token equivalents in DESIGN.md `spacing` / `rounded` / `elevation`. **Fix:** Replace inline literal with the nearest token (`p-4`, `rounded-md`, or `var(--space-md)`). **Example fail:**
```html
<div style="padding: 12px; border-radius: 9px">A</div>
```
**Example pass:**
```html
<div class="p-3 rounded-md">A</div>
```

### font-family-not-in-tokens
**Category:** Drift **Severity:** error **Check:** Rendered HTML uses a font-family not declared in DESIGN.md `typography.*.fontFamily`. **Fix:** Swap to an existing token role and reference it via `var(--font-{role})`. **Example fail:**
```html
<h1 style="font-family: Playfair Display">Title</h1>
```
**Example pass:**
```html
<h1 style="font-family: var(--font-display)">Title</h1>
```

### arbitrary-tailwind-value-repeated
**Category:** Drift **Severity:** warning **Check:** Same arbitrary Tailwind value (`w-[317px]`, `bg-[#abc123]`, `mt-[7px]`) appears 2+ times in the same variant. **Fix:** Promote to `@theme` in the inline `<style type="text/tailwindcss">` block once, then reference everywhere as a named utility. **Example fail:**
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
