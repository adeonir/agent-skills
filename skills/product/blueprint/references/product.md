# Product register

When the surface serves a task — the user is mid-work and the arrangement gets
them through it: dashboard, settings, data-table, form, onboarding, the checkout
/ account flow of a storefront. Structure follows the task, not a narrative.

## When to Use

Read by `create.md` and `validate.md` when the surface is product — to bias its
arrangement. Name the register first, then read only the matching file: product
here, or [brand.md](brand.md) when the surface communicates. Not a direct
trigger.

## Posture

| | Product |
|---|---|
| Question | "Can the user find and act without hunting?" |
| Bar | A familiar, navigable structure the user trusts |
| Failure | Invented navigation, a buried primary action, no state plan |
| Arrangement | Persistent nav, content plus actions, density, planned states |

## Arranging a product surface

- **Persistent navigation** — a nav or sidebar the user orients by; don't
  reinvent it.
- **Primary action reachable** — the main task is obvious, not buried.
- **Standard patterns** — list / detail, table plus toolbar, form plus summary;
  users expect them, and familiarity is a feature.
- **Plan the states** — empty, loading, error per data region; a box can't show
  these, so carry them in `note`.
- Flow is multi-surface (a nav graph): screen → screen, with entry and exit.

## Register is not surface

**Register** (brand vs product) is the posture — two values. **Surface** is the
granular type the plan arranges (dashboard, settings, data-table, onboarding…). A
surface sits under a register, but the register is not a finer surface list.
Surfaces under this register:

**Product surfaces** — dashboard, settings, form / wizard, data-table,
onboarding, empty-state, checkout / account, authenticated tools. Storefronts
straddle: the checkout / account flow is Product, the marketing / catalog shell
is Brand (see [brand.md](brand.md)).
