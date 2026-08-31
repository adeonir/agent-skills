# Direction

Explore and lock a named visual direction without authoring tokens.

## Load first

Read [discovery.md](../references/discovery.md) before starting — it settles the available context, the field, the brownfield intent, and the surfaces and register this operation must respect. Load [brand.md](../references/brand.md) or [product.md](../references/product.md) for the register the surfaces carry.

## Inputs

Read product documents as claims to check, not authority. Use purpose, audience, usage conditions, stated register, taste, anti-references, and hard constraints. Strip document IDs, feature names, milestones, and roadmap language from the moodboard.

Load [aesthetics.md](../references/aesthetics.md), the matching register file, [style-directions.md](../references/style-directions.md), and [anti-slop.md](../references/anti-slop.md). Keep the work text-only: no token maps, color values, or rendered HTML.

## Workflow

1. Gather only missing inputs that change the choice: what the product is, who uses it under what conditions, the desired first-second feeling, light/dark needs, hard constraints, anti-references, and visual work the user already likes.
2. Shortlist three named catalog directions unless the user requests another count. Choose directions that fit the product, surfaces, and register; never present a random sample.
3. Present each direction with its lineage, visual rules, fit, failure condition, explicit trade-off, and one signature move. Explain its Style Axes mapping without reducing the direction to the axes.
4. Support exactly three convergence operations:
   - **pick** — lock one direction.
   - **blend** — combine two directions while naming the dominant point of view and the trade-off that survives. Do not blend three directions.
   - **refine** — produce another focused round around one direction without changing its thesis silently.
5. Pressure-test the leaning direction against purpose, constraints, register, anti-references, and the anti-slop checklist. A legitimate exception records its reason.
6. Continue until the user locks the direction.
7. Write `docs/design/moodboard.md`. This record is additional context for design, not an intermediary gate. Direction ends without authoring tokens.

ALWAYS use this exact template structure:

```markdown
---
direction: [locked name]
status: locked
operation: pick | blend | refine
sources:
  - [catalog direction]
---

# Moodboard — [locked name]

## Point of View

[The visual thesis, dominant direction, and the sacrifice it accepts.]

## Visual Rules

- **Structure:** [rule]
- **Texture and Depth:** [rule]
- **Atmosphere:** [rule]
- **Color and Contrast:** [rule]
- **Typography:** [rule]

## Signature

[One memorable identity move.]

## Fit and Failure

- **Fits because:** [reason tied to purpose, conditions, surface, or register]
- **Fails if:** [condition that would invalidate the direction]

## Touchstones

- [real reference]

## Constraints

- [hard constraint or None]
```

MUST NOT contain: tokens, color values, rendered HTML, product copy, feature names, requirement IDs, milestones, roadmap language, or page arrangement.

## Error Handling

- If the user supplies a concrete visual reference, stop direction and route to design.
- If no choice survives pressure-testing, widen the shortlist across a different catalog lineage instead of producing small variations.
