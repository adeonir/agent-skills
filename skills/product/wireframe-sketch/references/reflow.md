# Reflow

How an arrangement holds under real conditions — narrower viewports and real data
volumes. Structural intent only: which regions collapse, stack, or defer, and how
content volume drives the shape and states. Design-blind — no pixels, breakpoints,
or tokens; the patterns name structural moves, and a downstream design sizes them.

## When to Use

Composed by `create.md` when planning a surface's arrangement, and by
`validate.md` when checking one. Not a direct trigger. Reflow and volume live in
the per-surface narration (markdown body) and block `note`s — never as pixels or
breakpoints in the region tree, which stays the default arrangement.

## Responsive Reflow (collapsing strategy)

As the viewport narrows, the arrangement reorganizes — it does not just shrink.
Plan the move per surface, and keep the information architecture consistent across
contexts: the same surfaces and primary actions, rearranged — never a different IA
per device.

Common moves:

- **Columns → stack** — side-by-side regions (`split`, `grid-N`) stack vertically.
- **Sidebar → drawer** — a persistent rail collapses behind a toggle.
- **Top nav → bottom nav / menu** — primary navigation moves within thumb reach or
  behind a menu.
- **Table → cards** — a dense table or `grid` becomes a stacked list of cards.
- **Defer the secondary** — secondary regions move into tabs, accordions, or
  progressive disclosure rather than competing for the narrow view.
- **Primary action stays reachable** — the main task never collapses out of reach.

State the move in the surface's narration ("the sidebar collapses to a drawer when
narrow; the list grid becomes a single-column card stack"), and `note` a block when
its own reflow is non-obvious. No breakpoint values — "narrow / wide" or "phone /
tablet / desktop" is the right altitude; a design picks the pixels.

## Content Volume (ranges → states + shape)

The arrangement that works for typical data breaks at the extremes. For each data
region, plan the realistic range — roughly none / typical / many — because volume
drives both the states and the shape. Volume is structure, not copy: it is the
*amount*, never the words.

- **None** → the empty state is a planned block, not a blank region (acknowledge it,
  point to the primary action).
- **Typical** → the default shape; size the arrangement to read well here.
- **Many** → the shape that survives scale — a list or table with pagination or
  load-more, not an unbounded card grid; filtering or search where it earns it.
- A region whose range spans wildly (none to thousands) needs all three planned, not
  just the happy middle.

Capture the range and its consequences in the surface's narration and the block
`note`; the states it implies join the empty / loading / error set already planned.

## Guidelines

- Reflow reorganizes, never just scales — name the structural move per surface.
- Keep the IA consistent across contexts; never a different architecture per device.
- Altitude stays structural — "stack", "drawer", "cards", "narrow / wide"; never
  pixels, breakpoints, or tokens.
- Plan volume at none / typical / many; the extremes drive states and shape.
- Volume is an amount, not content — no copy strings cross into the plan.
