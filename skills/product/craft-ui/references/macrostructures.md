# Macrostructures

Named presets for the region tree — the page-level shapes a surface can take, one level above the block-level shape vocabulary.

## When to Use

Composed by `render.md` in its structure phase (pick a preset, then walk what it leaves open) and by `critique.md` when it questions the arrangement behind a chosen variant. Not a direct trigger.

## How a preset is used

A macrostructure is a seed for the region tree, not a finished tree. It fixes which blocks exist, in what order, and at what shape; everything the preset leaves open — nesting, notes, reflow, volume — is still walked one decision at a time.

- **One preset per surface.** A multi-surface product picks one per surface; different surfaces may take different presets.
- **The register picks the half.** Brand surfaces choose from the brand presets, product surfaces from the product presets. A surface that straddles takes the preset matching the job that surface actually does ([brand.md](brand.md) / [product.md](product.md)).
- **Not for is the reject test.** Every entry carries what it is wrong for. Read it before committing; a preset chosen without clearing its own exclusion was not chosen.
- **The knob varies within the preset.** Where an entry has one, it changes the preset's character without changing which preset it is. Two surfaces on the same preset with the same knob value are the same page twice.
- **Naming the category is not picking.** "It is a SaaS landing, so Feature Stack" is the category reflex ([design-thinking.md](design-thinking.md)) wearing a preset name. Name the two presets rejected alongside the one taken.

Presets carry no color, type, token, or copy — the arrangement is orthogonal to the look. Block notation below is `label:shape` from the fixed shape vocabulary in [structure.md](structure.md).

## Brand presets

### Lead-and-support

One thing owns the fold; everything after qualifies it.

- **Blocks** — `hero:full-width` → `support:stack` → `detail:grid-3` → `close:full-width`
- **Knob** — what leads: statement · number · quote · image
- **Not for** — a surface carrying several equal-weight offers; the fold holds one idea.

### Bento Grid

An irregular modular grid where size variation carries the rhythm.

- **Blocks** — `hero:full-width` → `bento:grid-4` (children at mixed spans) → `close:full-width`
- **Knob** — tile economy: few large · many small · mixed spans
- **Not for** — content that reads in sequence; a grid states parallel items, not an argument.

### Long Document

Continuous prose with inline heads. The page is writing about the product.

- **Blocks** — `intro:stack` → `body:stack` → `close:stack`
- **Not for** — comparison or scanning; prose hides the differences a table shows.

### Manifesto

A sequence of declarations. States what to believe before what to buy.

- **Blocks** — `statement:full-width` (repeated) → `close:full-width`
- **Not for** — a surface whose job is explaining mechanics or comparing plans.

### Q&A

Question and answer pairs are the page, not an appendix to it.

- **Blocks** — `premise:stack` → `qa:stack` → `close:full-width`
- **Knob** — disclosure: all open · accordion
- **Not for** — a first-touch surface where the visitor has no questions yet.

### Catalogue

A uniform grid of same-kind items. The page is an index of inventory.

- **Blocks** — `header:stack` → `filter:full-width` → `items:grid-N` → `close:full-width`
- **Knob** — item weight: image-led · text-led
- **Not for** — a small set, where a grid reads as padding around six things.

### Index

The page is a list. Dense rows, one line per item.

- **Blocks** — `header:stack` → `list:stack` → `close:stack`
- **Not for** — items that need an image to be told apart.

### Narrative Workflow

Ordered stages. The sequence is the content.

- **Blocks** — `premise:full-width` → `stages:stack` → `close:full-width`
- **Knob** — stage orientation: vertical steps · horizontal track
- **Not for** — capabilities with no order between them.

### Guided Tour

Product captures are the primary content; the page walks the interface.

- **Blocks** — `hero:split` → `steps:stack` (capture plus note per step) → `close:full-width`
- **Knob** — pacing: one capture per section · a single capture that changes
- **Not for** — a product with nothing to show yet.

### Map/Diagram

Spatial arrangement carries the meaning; position is information.

- **Blocks** — `premise:stack` → `diagram:full-width` → `legend:grid-N` → `close:full-width`
- **Not for** — relationships a list expresses just as well.

### Feature Stack

The conventional marketing sequence. It is in the catalog so it can be named and rejected — a preset reached for because nothing else came to mind was not picked.

- **Blocks** — `hero:full-width` → `logos:full-width` → `features:grid-3` → `testimonial:stack` → `pricing:grid-3` → `faq:stack` → `close:full-width`
- **Not for** — any surface another entry fits. Take it when the audience genuinely expects the sequence, such as a comparison-shopped B2B buyer working through several vendors.

## Product presets

These describe the work surface. The persistent chrome around it — navigation the user orients by — is planned as blocks in the tree per [product.md](product.md), not chosen from this catalog.

### Master-detail

A collection on one side, the selected item on the other; selection drives the surface.

- **Blocks** — `list:sidebar` alongside `detail:full-width`
- **Knob** — collection type: list · queue · tree
- **Not for** — items read one at a time with no comparison between them.

### Dashboard grid

Tiles of metrics and charts, arranged to be scanned.

- **Blocks** — `header:full-width` → `tiles:grid-N`
- **Knob** — tile mix: uniform metrics · mixed metric and chart
- **Not for** — a single number; one metric is a page, not a grid.

### Table-first

A dense table is the screen; filters, search, and bulk actions surround it.

- **Blocks** — `toolbar:full-width` → `table:full-width` → `detail:overlay` (optional)
- **Knob** — row action: inline · drawer · route
- **Not for** — a handful of rows, where a table is scaffolding around a list.

### Canvas + inspector

A spatial work area with a contextual panel that follows selection.

- **Blocks** — `canvas:full-width` alongside `inspector:sidebar`, with `toolbar:overlay`
- **Not for** — linear tasks; a canvas invites exploration a form does not want.

### Editor

A single authoring surface with chrome around it.

- **Blocks** — `toolbar:full-width` → `document:full-width`, with `outline:sidebar` when the document is long
- **Not for** — work spanning many records at once.

### Wizard steps

One decision per screen, progress visible, order enforced.

- **Blocks** — `progress:full-width` → `step:stack` → `actions:full-width`
- **Knob** — reversibility: free navigation · forward-only
- **Not for** — settings the user revisits; a wizard is for a first pass.

### Feed

A reverse-chronological stream, unbounded.

- **Blocks** — `composer:full-width` (optional) → `stream:stack`
- **Not for** — content the user needs to find again.

### Form-stack

Sectioned forms and grouped preferences; the user arrives knowing what to change.

- **Blocks** — `sections:sidebar` alongside `fields:stack`
- **Knob** — navigation: sidebar sections · single scroll with anchors
- **Not for** — first-run setup, which is a wizard.
