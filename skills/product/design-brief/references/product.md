# Product register

When design SERVES the product: app UIs, admin dashboards, settings panels, data tables, tools, authenticated surfaces — anything where the user is in a task.

## When to Use

Read by `direction.md` to bias a mood toward this register, and by `design.md` to bias token choices when authoring DESIGN.md. Name the register first, then read the matching file: product here, or [brand.md](brand.md) when design is the deliverable — or both, when the project's surfaces span the two registers (a storefront's checkout is product, its marketing shell brand). Not a direct trigger.

## Posture

| | Product |
|---|---|
| Question | "Would a fluent user pause at every subtly-off component?" |
| Bar | Earned familiarity — trust and consistency |
| Failure | Invented affordances, mismatched controls, gratuitous motion |
| Permission | Density, standard patterns, restraint; delight saved for moments |

Familiarity is a feature here. The consistency that reads as timid on brand is a virtue in product. A move that is voice on a brand surface is noise on this one.

## The product slop test

Not "would someone say AI made this" — familiarity is often the point. The test: would a user fluent in the category's best tools (Linear, Figma, Notion, Stripe) trust this interface, or pause at every subtly-off component? The failure mode is strangeness without purpose — over-decorated controls, display fonts where labels belong, invented affordances for standard tasks.

## Token permissions

What product should author:

- **Color** — Restrained is the floor; a single surface can earn Committed (one category color carrying a report, a drenched onboarding welcome). State-rich semantic vocabulary: hover, focus, active, disabled, selected, loading, error, warning, success, info.
- **Typography** — one well-tuned sans often carries headings, labels, body, and data; fixed rem scale (not fluid); tighter ratio (1.125–1.2). System stacks are acceptable. Typical roles: `heading`, `subheading`, `label`, `button` — functional UI roles — on top of the shared core `body` / `small` / `caption` / `code`; `label` names a form-field label, distinct from `button` (action text). The pool is open, not exclusive: a product surface may reach for `display` or `lead` (onboarding, empty-state), a functional variant is a suffixed entry (`-emphasis` / `-muted`), and a role with size variants may carry the size in its key (`button-sm`), additive to the vocabulary.
- **Motion** — 150–250 ms; motion conveys state, not decoration. No orchestrated page-load — users load into a task.
- **Components** — every interactive state defined (default / hover / focus / active / disabled / loading / error); consistent affordances across the surface.

## Product bans (on top of the shared [anti-patterns.md](anti-patterns.md))

- Display fonts in UI labels, buttons, or data.
- Decorative motion that doesn't convey state.
- Reinventing standard affordances for flavor (custom scrollbars, weird form controls).
- Heavy or full-saturation accents on inactive states.

## Register is not surface

**Register** (brand vs product) is the posture — two values. **Surface** is the granular type the work actually is (dashboard, settings, data-table, onboarding, empty-state…). A surface sits under a register, but the register is not a finer surface list. Surfaces under this register:

**Product surfaces** — dashboard, settings, form / wizard, data-table, onboarding, empty-state, checkout / account, authenticated tools. Storefronts straddle: the checkout / account flow is Product, the marketing / catalog shell is Brand (see [brand.md](brand.md)).
