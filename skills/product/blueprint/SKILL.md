---
name: blueprint
allowed-tools: Read Write Edit Grep Glob WebFetch
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

Produces `blueprint.md`, the layout plan a design consumes. Operations:

- **create** — author a fresh layout plan from conversation (surfaces,
  blocks, shapes, flow). → [create.md](references/create.md)
- **validate** — check a wireframe or existing plan for IA, flow, and
  intent coherence. → [validate.md](references/validate.md)

## Discovery

`discovery.md` runs before every operation — never skipped, never invoked
directly. It checks existing context (an existing `blueprint.md`, the
conversation, any brief the user provides) and routes by intent — author a
plan, or check one. See [discovery.md](references/discovery.md).

## Operations

| Operation | File |
| --------- | ---- |
| Author a fresh layout plan into blueprint.md | [create.md](references/create.md) |
| Check a wireframe or plan for coherence | [validate.md](references/validate.md) |

## Artifact

Produces and owns `docs/design/blueprint.md`. A **YAML frontmatter** carries
the normative region tree (surfaces → blocks with shape hints) plus optional
screen flow — what a downstream renderer parses to draw the low-fi wireframe. A
**markdown body** narrates it: a screen map and the per-surface rationale a
tree alone cannot hold. Block labels come from the conversation; shape hints
come from a fixed set. Patch the frontmatter first, then the prose that
describes it, so the two stay in sync. Before
saving, self-check: the tree is well-formed and carries structure only — no
colors, fonts, spacing, or tokens, and no copy. It plans arrangement, nothing
else.

## Inputs

Plan from the conversation. Beyond that, the only inputs are what the user
provides — a brief, a PRD, a description, or existing material they point to;
nothing is auto-loaded. If the user hands over existing content or a prior
plan, arrange against it; otherwise plan from intent.

## Guidelines

- Plan structure only — never embed colors, fonts, spacing, or tokens.
- Derive surfaces and topics from the conversation; no fixed project types.
- Use free block labels; pick shape hints from the fixed set so the plan
  stays renderable.
- Patch the frontmatter region tree first, then the body that narrates it,
  so the two stay in sync.
- Ask one decision at a time when walking surfaces, blocks, and flow.
- Keep content out — plan structure, never author copy here.
