# Responsive

Adapting a design across screen sizes, devices, and contexts. The trap is
treating adaptation as scaling — the job is rethinking the experience for the new
context (input method, screen, usage), not shrinking pixels.

## When to Use

Composed by `render.md` (apply while generating), and by `critique.md` /
`audit.md` (judge a rendered surface against it). Not a direct trigger.

## Register

- **Brand** — fluid spacing/type that breathes across viewports; the hero may be
  re-art-directed per breakpoint. See [brand.md](brand.md).
- **Product** — responsive behavior is structural (collapse sidebar, responsive
  table, breakpoint-driven columns), not fluid typography; one information
  architecture across contexts. See [product.md](product.md).

## Mobile-first

Base styles for mobile, layer complexity with `min-width` queries. Desktop-first
(`max-width`) makes mobile load unnecessary styles first.

## Breakpoints: content-driven

Let content tell you where to break — start narrow, stretch until the design
breaks, add the breakpoint there. Three usually suffice (~640, 768, 1024px); use
`clamp()` for fluid values without breakpoints.

## Detect input method, not just screen size

Screen size doesn't tell you the input (a laptop with touchscreen, a tablet with
keyboard). Use pointer/hover queries:

```css
@media (pointer: coarse) { .button { padding: 12px 20px; } }  /* touch */
@media (hover: hover)    { .card:hover { transform: translateY(-2px); } }
@media (hover: none)     { /* use :active, not hover, for functionality */ }
```

Never rely on hover for functionality — touch users can't hover.

## Adaptation by context (rethink, don't scale)

- **Desktop → mobile** — single column, vertical stacking, full-width
  components, bottom nav; touch targets 44×44px, more spacing; progressive
  disclosure (primary content first); larger/shorter text.
- **Tablet** — two-column / master-detail; support both touch and pointer;
  adapt by orientation.
- **Mobile → desktop** — multi-column, persistent side nav, hover affordances,
  keyboard shortcuts; fixed widths with `max-width` (don't stretch to 4K); show
  more upfront (less progressive disclosure).
- **Print** — page breaks at logical points; remove nav/interactive; expand
  shortened content; page numbers.
- **Email** — ≤600px, single column, inline CSS, table layouts; large button
  CTAs, no hover; deep-link to the web app for complex interactions.

Never hide core functionality on mobile, use a different IA per context, or
forget landscape.

## Touch

44×44px minimum targets, more spacing between them, remove hover-dependent
interactions, add touch feedback. Respect thumb zones (bottom is easier to reach
than top).

## Safe areas (the notch)

```css
.footer { padding-bottom: max(1rem, env(safe-area-inset-bottom)); }
```

Enable it: `<meta name="viewport" content="width=device-width, initial-scale=1,
viewport-fit=cover">`.

## Responsive images

- **`srcset` + `sizes`** for resolution: list widths (`hero-800.jpg 800w`), tell
  the browser the displayed width (`sizes="(max-width: 768px) 100vw, 50vw"`);
  the browser picks by viewport × DPR.
- **`<picture>`** for art direction — different crops/compositions, not just
  resolutions.

## Layout adaptation patterns

- **Navigation** — three stages: hamburger/drawer on mobile, compact horizontal
  on tablet, full-with-labels on desktop.
- **Tables → cards** on mobile (`display: block` + `data-label`).
- **Progressive disclosure** via `<details>`/`<summary>` for collapsible content.

## Testing

DevTools emulation catches layout but misses real touch, CPU/memory, latency,
font rendering, and keyboard chrome. Test on at least one real iPhone, one real
Android, a tablet if relevant — cheap Android phones reveal perf issues
simulators hide.

## Responsive anti-defaults

- Desktop-first; device detection instead of feature detection; separate
  mobile/desktop codebases; hiding core functionality on mobile; ignoring tablet
  and landscape; generic breakpoints applied blindly.
