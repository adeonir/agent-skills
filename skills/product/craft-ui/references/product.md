# Product register

When design SERVES the product: app UIs, admin dashboards, settings panels, data tables, tools, authenticated surfaces — anything where the user is in a task.

## When to Use

Read by `critique.md` and `audit.md` when the surface is product — to set the judging posture — and by `render.md` to lean a variant toward this register. Name the register first, then read only the matching file: product here, or [brand.md](brand.md) when design is the deliverable. Not a direct trigger.

## Posture of judgment

| | Product |
|---|---|
| Question | "Would a fluent user pause at every subtly-off component?" |
| Bar | Earned familiarity — trust and consistency |
| Failure | Invented affordances, mismatched controls, gratuitous motion |
| Permission | Density, standard patterns, restraint; delight saved for moments |

Familiarity is a feature here. The consistency that reads as timid on brand is a virtue in product. A move that is voice on a brand surface is noise on this one.

## The product slop test

Not "would someone say AI made this" — familiarity is often the point. The test is: would a user fluent in the category's best tools (Linear, Figma, Notion, Raycast, Stripe) sit down and trust this interface, or pause at every subtly-off component?

Product UI's failure mode isn't flatness, it's **strangeness without purpose**: over-decorated buttons, mismatched form controls, gratuitous motion, display fonts where labels should be, invented affordances for standard tasks. The bar is earned familiarity — the tool disappears into the task.

## Typography

- **One family is often right.** Product UIs don't need display/body pairing; a well-tuned sans carries headings, buttons, labels, body, data.
- **Fixed rem scale, not fluid.** Clamp-sized headings don't serve product UI; a fluid h1 that shrinks in a sidebar looks worse, not better.
- **Tighter ratio** (1.125–1.2). More type elements here than on brand surfaces; exaggerated contrast creates noise.
- Line length still applies for prose (65–75ch); data and compact UI run denser.

## Color

Product defaults to **Restrained**. A single surface can earn Committed (a dashboard where one category color carries a report, a drenched onboarding welcome), but Restrained is the floor.

- State-rich semantic vocabulary: hover, focus, active, disabled, selected, loading, error, warning, success, info. Standardize these.
- Accent used for primary actions, current selection, and state — not decoration.
- A second neutral layer for sidebars, toolbars, and panels.

## Layout

Responsive behavior is structural (collapse sidebar, responsive table, breakpoint-driven columns), not fluid typography.

## Components

Every interactive component has default, hover, focus, active, disabled, loading, error. Don't ship with half of these.

- Skeleton states for loading, not spinners in the middle of content.
- Empty states that teach the interface, not "nothing here."
- Consistent affordances across the surface — same button shape, same form-control vocabulary, same icon style.

## Motion

- 150–250 ms on most transitions. Users are in flow; don't make them wait.
- Motion conveys state, not decoration — state change, feedback, loading, reveal.
- No orchestrated page-load sequences. Product loads into a task.

## Product bans (on top of the shared [anti-patterns.md](anti-patterns.md))

- Decorative motion that doesn't convey state.
- Inconsistent component vocabulary across screens — if "save" looks different in two places, one is wrong.
- Display fonts in UI labels, buttons, data.
- Reinventing standard affordances for flavor (custom scrollbars, weird form controls, non-standard modals).
- Heavy color or full-saturation accents on inactive states.
- Modal as first thought. Modals are usually laziness; exhaust inline / progressive alternatives first.

## Product permissions

Product can afford things brand can't.

- System fonts and familiar sans defaults (Inter, SF Pro, system-ui stacks).
- Standard navigation: top bar + side nav, breadcrumbs, tabs, command palettes.
- Density — tables with many rows, panels with many labels, when users need it.
- Consistency over surprise. Delight is saved for moments, not pages.

## Register is not surface

**Register** (brand vs product) is the posture — two values. **Surface** is the granular type the work actually is (dashboard, settings, data-table, onboarding, empty-state…). A surface sits under a register, but the register is not a finer surface list. Surfaces under this register:

**Product surfaces** — dashboard, settings, form / wizard, data-table, onboarding, empty-state, checkout / account, authenticated tools. Storefronts straddle: the checkout / account flow is Product, the marketing / catalog shell is Brand (see [brand.md](brand.md)).
