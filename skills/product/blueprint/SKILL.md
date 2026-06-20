---
name: blueprint
allowed-tools: Read Write Edit WebFetch
description: >-
  Plans blueprint.md, the design-blind layout payload a design
  consumes: a region tree plus screen flow that arranges surfaces
  before any visual identity is styled — structure only, composable
  under any design. Use when planning information architecture, page
  composition, screen inventory, or screen flow; arranging surfaces,
  blocks, or navigation; wireframing or validating a wireframe;
  drafting a layout plan from a brief or conversation. Not for visual
  identity or design tokens, copy or content, or rendering HTML.
---

# Blueprint

Owns `blueprint.md` — the design-blind layout payload a design consumes: a
YAML frontmatter holds the renderable region tree, and a markdown body
narrates it with a screen map and per-surface rationale.
Arrangement is orthogonal to visual identity: the same `blueprint.md` must
hold under any design, so this skill plans structure only — information
architecture, region layout, and screen flow — never colors, fonts, or tokens.

## Quick start

Operations:

- **create** — author a fresh layout plan from conversation (surfaces,
  blocks, shapes, flow). → [create.md](instructions/create.md)
- **validate** — check a wireframe or existing plan for IA, flow, and
  intent coherence. → [validate.md](instructions/validate.md)

## Discovery

`discovery.md` runs before every operation — never skipped, never invoked
directly. It checks existing context (an existing `blueprint.md`, the
conversation, any brief the user provides) and routes by intent — author a
plan, or check one. See [discovery.md](instructions/discovery.md).

## Artifact

Produces and owns `docs/design/blueprint.md`. The **frontmatter** region tree
is normative — a downstream renderer parses it to draw the low-fi wireframe;
the **body** is for humans. The full template, the shape vocabulary, and the
pre-save self-check live in [create.md](instructions/create.md).

## Register and surface

Two axes, set before arranging:

- **register** — the posture: **brand** (the surface communicates — landing,
  campaign, portfolio) or **product** (the surface serves a task — dashboard,
  form, settings). Biases the arrangement, never gates it. Read the matching
  [brand.md](references/brand.md) / [product.md](references/product.md) first.
- **surface** — the granular type, named by context. A surface sits under a
  register; surfaces come from the conversation, never a fixed set. Storefronts
  straddle — the marketing shell is brand, the checkout / account flow is product.

## Inputs

Plan from the conversation. Beyond that, the only inputs are what the user
provides — a brief, a PRD, a description, a reference URL, or existing material
they point to; nothing is auto-loaded. If the user hands over existing content
or a prior plan, arrange against it; otherwise plan from intent.

## Guidelines

- Plan structure only — never embed visual decisions (colors, fonts, spacing,
  tokens), copy strings, or requirement IDs (`fr-1`, `m1`, `j1`, `us-3`).
- Derive surfaces and topics from the conversation; no fixed project types.
- Name the register (brand or product) per surface; it biases the arrangement, never gates the shape.
- Plan each surface for real conditions — its reflow on narrow viewports and its content volume (none/typical/many) — as structural intent in the narration, never pixels or breakpoints.
- Patch the frontmatter region tree first, then the body that narrates it,
  so the two stay in sync.
