# Archetypes

Named compositions for the blocks where the agent has a reflex to correct — the chrome regions and the conversion ask.

## When to Use

Composed by `render.md` in its structure phase, after the macrostructure seeds the tree. Not a direct trigger.

## How an archetype is used

- **The region set comes first.** Decide which chrome regions the surface carries, then compose each one. The set is largely a register question; the reflex lives in the composition.
- **The catalog covers four blocks.** `header`, `rail`, and `footer` for chrome, `close` for the conversion ask. Every other block carries its intent in the tree's `note` — a named catalog earns its load only where a reflex exists to correct.
- **Reflex marked, not banned.** An entry marked **reflex** is the one reached for without deciding. It is often still the right answer; take it when its own "not for" clears, and record that it was chosen rather than fallen into.
- **Not for is the reject test.** Every entry carries what it is wrong for. An archetype committed without clearing its exclusion was not chosen.
- **Chrome keeps its structural shape.** `header:full-width`, `rail:stack`, `footer:full-width`. An archetype composes a region; it never re-shapes one. Where a composition layers over the content instead of sitting in flow, it is a separate `overlay` block alongside the region, not the region wearing a different shape.

Archetypes carry no color, type, token, or copy. Blocks and shapes are the vocabulary in [structure.md](structure.md); the preset that seeds them is in [macrostructures.md](macrostructures.md).

## Region set

Which chrome regions the surface carries. The preset seeds the common answer; this decision confirms it or drops a region.

**Brand** — read [brand.md](brand.md).

- `header` + `footer` — navigation across the top, closing chrome at the bottom. Right for most brand surfaces.
- `rail` + `footer` — navigation down a side, persisting while a narrow content column scrolls. Fits an index or a body of work where the list stays in view.
- `footer` only — no persistent navigation; the surface is one argument read top to bottom.

**Product** — read [product.md](product.md). This is where the product register spends its structural decision; the compositions below are conventional on purpose.

- `header` — a top bar alone. Few destinations, or one surface deep.
- `rail` — side navigation alone. Many destinations the user moves between constantly.
- `header` + `rail` — the rail carries destinations, the header carries account, search, and global context. The convention for dense tools.
- neither — the task owns the screen. A wizard, a full-screen editor, a first-run step.

A product surface takes a `footer` only where it genuinely closes — an account or settings surface signing off with version, status, and support. A tool the user works inside all day does not end, so it carries none.

## Header

### Minimal bar — **reflex**

Wordmark plus one or two links.

- **Register** — brand
- **Not for** — a surface with more than three destinations, where it reads as a template that ran out of content.

### Three-section bar — **reflex**

Wordmark left, a link cluster centre, actions right.

- **Register** — brand
- **Knob** — cluster behaviour: flat links · dropdowns · full-width panel
- **Not for** — a surface with two destinations, which leaves the centre empty and the balance false.

### Masthead

The wordmark is the header, set large, with navigation beneath or around it.

- **Register** — brand
- **Not for** — a visitor who already knows the brand and came for a destination.

### Floating

The header does not scroll with the document; it persists above the content.

- **Register** — brand
- **Knob** — on scroll: static · morph (narrows, gains a backdrop)
- **Not for** — a short surface, where persistence buys nothing and costs the fold.

### Edge-aligned

Items pushed to the two extremes with nothing between them; the emptiness is the composition.

- **Register** — brand
- **Not for** — more than four items, which turns the gap into a gap between crowds.

### Command-first

A search or command affordance is the primary element; navigation is secondary.

- **Register** — brand, product
- **Knob** — exposure: inline field · pill that opens a palette
- **Not for** — a surface whose content is not searchable.

### Context bar

Product mark, the current workspace or record, then search and account. Orientation, not persuasion.

- **Register** — product
- **Knob** — context element: breadcrumb · switcher · both
- **Not for** — a single-workspace tool with nothing to switch between.

## Rail

### Destination list — **reflex**

Destinations in one flat level, no grouping.

- **Register** — product
- **Knob** — density: icon-only · labelled · collapsible
- **Not for** — more than about seven destinations, where a flat list becomes a scroll with no landmarks in it.

### Grouped sections

Destinations under labelled groups, separated by rules.

- **Register** — product
- **Knob** — group marker: label · rule only
- **Not for** — a handful of destinations, where each group ends up labelling one item.

### Switcher-topped

A workspace or project switcher pinned at the top, destinations beneath it, account pinned at the bottom.

- **Register** — product
- **Not for** — a single-workspace tool with nothing to switch between.

### Flyout

A narrow icon column; selecting one opens a panel beside it holding that section's contents.

- **Register** — product
- **Knob** — opening: hover · click-pinned
- **Not for** — destinations whose icons do not tell each other apart without labels.

### Index rail

The surface's own contents — chapters, works, entries — down the side, tracking position while the content column scrolls.

- **Register** — brand
- **Not for** — a surface that reads as one continuous argument, with no entries to index.

## Footer

### Index columns — **reflex**

Three to five columns of links, a social row, a copyright line.

- **Register** — brand
- **Not for** — a surface with fewer than a dozen destinations, where the columns pad a sitemap that does not exist. Take it on a genuine hub or documentation root.

### Inline rule

A rule and one line: wordmark, a few links, copyright.

- **Register** — brand, product
- **Not for** — a surface that has to be navigable from the bottom.

### Mast-headed

The wordmark at scale with links beneath it; the page signs off.

- **Register** — brand
- **Not for** — a product surface, where a large sign-off reads as marketing inside a tool.

### Statement

A closing sentence at display size; links reduced to the minimum.

- **Register** — brand
- **Not for** — a surface whose footer carries real navigation load.

### Colophon

Small type, dense facts: what it is built with, who made it, when it last changed.

- **Register** — brand
- **Not for** — an audience with no interest in how it was made.

## Close

The conversion ask at the end of a brand surface. Product surfaces carry their primary action in the work surface, not in a closing block.

### Restated pitch plus button — **reflex**

A heading, a line of subtext, a filled button, centred.

- **Register** — brand
- **Not for** — a surface that already made the ask above the fold and gains nothing by repeating it.

### Inline form

The ask *is* the form — one field and a submit, so the conversion completes in place.

- **Register** — brand
- **Knob** — fields: one · one plus a qualifier
- **Not for** — a conversion that genuinely needs its own surface, such as pricing or scheduling.

### Typographic link

A word and an arrow. No box, no fill; the close is quiet on purpose.

- **Register** — brand
- **Not for** — a surface whose entire job is the conversion.

### Persistent bar

A bar fixed to a viewport edge holding the action and one line of reassurance. It layers over the content, so it is an `overlay` block alongside `close`, never the `close` block re-shaped.

- **Register** — brand
- **Not for** — an action that needs the surrounding content to make sense.
