# Direction

Explore and lock a named visual direction without authoring tokens.

## Load first

Read [discovery.md](../references/discovery.md) before starting — it settles the available context, the field, the brownfield intent, and the surfaces and register this operation must respect. Load [brand.md](../references/brand.md) or [product.md](../references/product.md) for the register the surfaces carry.

## Inputs

Read product documents as claims to check, not authority. Use purpose, audience, usage conditions, stated register, taste, anti-references, and hard constraints. Strip document IDs, feature names, milestones, and roadmap language from the moodboard.

Load [aesthetics.md](../references/aesthetics.md), the matching register file, [style-directions.md](../references/style-directions.md), and [anti-slop.md](../references/anti-slop.md). Keep the moodboard text-only: no token maps, color values, or rendered HTML. Image tiles are an optional companion to the moodboard, never its content.

## Workflow

1. Gather only missing inputs that change the choice: what the product is, who uses it under what conditions, the decision this direction must unblock, the desired first-second feeling, light/dark needs, hard constraints, anti-references, and visual work the user already likes. When the user cannot name the feeling, propose two or three candidate feelings tied to the product and let the user pick one.
2. Shortlist three named catalog directions unless the user requests another count. Choose directions that fit the product, surfaces, and register; never present a random sample. Each direction differs from the others in organizing principle, never only in palette: a reader with no design background can tell them apart from the descriptions alone.
3. Present each direction with its lineage, visual rules, fit, failure condition, explicit trade-off, one signature move, and a one-line `reads as` in plain language for a reader with no design background. Explain its Style Axes mapping without reducing the direction to the axes.
4. Recommend one direction, with the reason tied to the audience, the usage conditions, and the surface it must serve. Present the recommendation as a claim the user can reject.
5. Support exactly three convergence operations:
   - **pick** — lock one direction.
   - **blend** — combine two directions while naming the dominant point of view and the trade-off that survives. Do not blend three directions.
   - **refine** — produce another focused round around one direction without changing its thesis silently.
6. Pressure-test the leaning direction against purpose, constraints, register, anti-references, and the anti-slop checklist. A legitimate exception records its reason.
7. Mark every brand constraint the user did not state as an assumption. Assumptions land in `## Constraints` of the moodboard, labeled as such.
8. Continue until the user locks the direction.
9. Write `docs/design/moodboard.md`. This record is additional context for design, not an intermediary gate. Direction ends without authoring tokens.
10. **Report.** Report the path, what the moodboard holds in one to three sentences, and any open item it carries, such as an assumed constraint. Never paste the file.

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

## Reads As

[One or two sentences in plain language for a reader with no design background.]

## Visual Rules

- **Structure:** [rule]
- **Texture and Depth:** [rule]
- **Atmosphere:** [rule]
- **Color and Contrast:** [rule]
- **Typography:** [rule]
- **Imagery:** [photography, illustration, or none, and its posture]
- **Motion:** [feeling and pace, no values]

## Signature

[One memorable identity move.]

## Fit and Failure

- **Fits because:** [reason tied to purpose, conditions, surface, or register]
- **Fails if:** [condition that would invalidate the direction]

## Touchstones

- [real reference]

## Constraints

- [hard constraint, or an assumption labeled `assumed:`, or None]

## Tiles

- [prompt for one tile, or None]
```

MUST NOT contain: tokens, color values, rendered HTML, product copy, feature names, requirement IDs, milestones, roadmap language, page arrangement, conversation narrative ("as discussed", "the user picked", "we agreed"), or the history of the lock (the shortlist, the rounds, the directions not taken).

## Tiles

Tiles are optional generated images that show a direction before any token exists. Offer them when an image-generation tool is available in the session; detect the tool before offering and never name a specific tool or host in the moodboard.

When the user accepts:

1. Write four to six tile prompts per shortlisted direction into `## Tiles`. Vary the subject across tiles: one hero surface, one texture close-up, one product-in-context view, one type-in-situ view, one color study. Keep the prompt DNA of one direction consistent across its tiles so they read as one world, and distinct from every other direction.
2. Generate the tiles and save them to `docs/design/moodboard/<direction>/tile-<NN>.png`.
3. Present the tiles beside the text description of each direction. Tiles support the decision; the moodboard prose remains the locked record.
4. Keep only the locked direction's tiles when the direction is locked. Report the folders removed and ask before removing them.

Without an image-generation tool, write the prompts into `## Tiles` and tell the user where to generate them. Do not block the lock on missing tiles.

A tile is evidence of the direction, never a target for design: token values derive from the catalog anchors and the color and typography references, not from a generated image.

## Error Handling

- If the user supplies a concrete visual reference, stop direction and route to design.
- If no choice survives pressure-testing, widen the shortlist across a different catalog lineage instead of producing small variations.
- If tile generation fails, keep the prompts in the moodboard and continue with the text descriptions.
