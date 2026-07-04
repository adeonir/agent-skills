# Layout

Space is the most underused design tool. Recipes for spacing systems, rhythm,
the right layout tool, hierarchy, depth, and optical adjustment — fix the
structure, not the surface. Layout problems are often why an interface feels
"off" even when color and type are fine.

## When to Use

Composed by `render.md` (apply while generating), and by `critique.md`
(judge a rendered surface against it). Not a direct trigger.

## Register sets the composition

- **Brand** — asymmetric compositions, fluid `clamp()` spacing, intentional
  grid-breaking for emphasis; rhythm through contrast (tight groupings + generous
  separations). See [brand.md](brand.md).
- **Product** — predictable grids, consistent densities, familiar navigation;
  responsive behavior is structural (collapse sidebar, responsive table), not
  fluid type. Consistency IS an affordance. See [product.md](product.md).

## Spacing system

- Values come from a defined scale, never arbitrary. Prefer a **4pt base** (4, 8,
  12, 16, 24, 32, 48, 64, 96) over 8pt — 8pt is too coarse (you'll want 12
  between 8 and 16).
- Semantic token names (`--space-xs`…`--space-xl`), not `--spacing-8`.
- Use `gap` for sibling spacing, not margins (no margin-collapse hacks).
- `clamp()` for fluid spacing that breathes on larger screens.

## Visual rhythm

- Tight grouping for related elements (8–12px); generous separation between
  sections (48–96px); varied spacing within sections (not every row the same
  gap). Asymmetry is a deliberate choice when content invites it, not a default.

## The right layout tool

- **Flexbox for 1D** — nav bars, button groups, card internals, most components.
- **Grid for 2D** — page structure, dashboards, data-dense interfaces; named
  `grid-template-areas` for complex pages, redefined at breakpoints.
- **Container queries for components, viewport queries for pages** — a card in a
  narrow sidebar stays compact while the same card in main content expands:

```css
.card-container { container-type: inline-size; }
@container (min-width: 400px) { .card { grid-template-columns: 120px 1fr; } }
```

## Hierarchy

Use the fewest dimensions that work — space alone can carry it; generous
whitespace around an element draws the eye. The best hierarchy combines 2–3 at
once (larger + bolder + more space above = primary without trying).

Let spacing do the work — don't manufacture hierarchy with a gradient, a card
wrapper, a badge, or hero drama when space and weight would carry it. Decoration
reached for to signal importance usually means the spacing hierarchy is too flat.

| Tool | Strong | Weak |
|------|--------|------|
| Size | ≥3:1 | <2:1 |
| Weight | Bold vs Regular | Medium vs Regular |
| Color | high contrast | similar tones |
| Position | top/left | bottom/right |
| Space | surrounded by whitespace | crowded |

Squint test: blur your eyes — can you still identify primary, secondary, and the
groupings? Reorder weight until the survivors match the intended reading order.

## Hero composition

- The hero fits the initial viewport — the primary message and action are visible
  without scrolling.
- Headline ≤2 lines; a hero carries ≤4 text elements total (eyebrow, headline,
  subtext, CTA — rarely all four). More is a hero doing the whole page's job.
- A headline wrapping to four lines is a font-size error, not a copy problem —
  size it down before cutting words.
- Repeat the primary CTA only when it reduces friction (a long page where the top
  CTA has scrolled away), never as a default rhythm.

## Cards & monotony

- Don't default to card grids — spacing and alignment group naturally. Use cards
  only when content is truly distinct and actionable. **Never nest cards.**
- Vary card sizes, span columns, or mix cards with non-card content to break
  repetition.

## Depth & elevation

- Consistent shadow scale (sm → md → lg → xl), subtle; elevation reinforces
  hierarchy, not decoration. Semantic z-index scale (base < cards < dropdowns <
  modals < overlays), never arbitrary 999/9999.
- One border-radius scale locked page-wide (inputs/buttons small, cards medium,
  modals large) — sharp and soft corners mixed across peer elements read as no
  system.

## Optical adjustments

- Geometrically centered glyphs often look off-center — play icons shift right,
  arrows shift toward their direction. Nudge only when you're sure it looks
  wrong, never speculatively.
- Text at `margin-left: 0` looks indented from letterform whitespace; `-0.05em`
  optically aligns it.
- Touch targets 44×44px minimum even when the visual element is smaller — expand
  the hit area with padding or a pseudo-element (`inset: -10px`).

## Layout anti-defaults

- Arbitrary spacing outside the scale; all spacing equal (variety creates
  hierarchy).
- Wrapping everything in cards; nesting cards; identical card grids (icon +
  heading + text, repeated).
- The hero-metric template (big number, small label, stats, gradient) as a
  default — a prominent metric is fine only with real data.
