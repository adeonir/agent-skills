---
name: wireframe-sketch
allowed-tools: Read Write Edit WebFetch
description: >-
  Plans the layout structure a design consumes — a region tree plus
  screen flow that arranges surfaces before any visual identity — then
  draws it as a low-fi wireframe, greyscale and content-blind, like a
  Figma sketch. Structure only, composable under any design. Use when
  planning information architecture, page composition, screen
  inventory, or screen flow; arranging surfaces, blocks, or
  navigation; wireframing, rendering, or drawing a low-fi wireframe,
  ASCII sketch, or screen flow; validating a wireframe or reconciling
  its plan; drafting a layout plan from a brief or conversation. Not
  for visual identity or design tokens, copy or content.
---

# Wireframe Sketch

Owns `WIREFRAME.md` — the structural layout plan a design consumes: a YAML frontmatter holds the region tree, and a markdown body narrates it with a screen map and per-surface rationale. From that plan the skill draws a **low-fi wireframe** — greyscale, content-blind, the kind you sketch before visual design. Arrangement is orthogonal to visual identity: the same plan holds under any design, so this skill plans structure only — information architecture, region layout, and screen flow — never colors, fonts, or tokens.

## Quick start

Operations:

- **create** — author or patch the layout plan from conversation (surfaces, blocks, shapes, flow). → [create.md](instructions/create.md)
- **render** — draw the plan as a low-fi wireframe — an HTML page or an ASCII sketch — or a Mermaid screen-flow. → [render.md](instructions/render.md)
- **validate** — check a wireframe or plan for coherence and reconcile the plan in natural language when it should change. → [validate.md](instructions/validate.md)

## Discovery

`discovery.md` runs before every operation — never skipped, never invoked directly. It checks existing context (an existing `WIREFRAME.md`, the conversation, any brief the user provides) and routes by intent — author a plan, draw one, or check one. See [discovery.md](instructions/discovery.md).

## Artifact

Produces and owns `docs/design/WIREFRAME.md` and its drawn view `docs/design/wireframe.html` — a low-fi wireframe. The **frontmatter** region tree is the plan the render draws from; the **body** is for humans. The render is **generative**: it reads the plan and draws the page with judgment, guided by the bundled glyph kit (`assets/wireframe.css`) and rubric ([drawing.md](references/drawing.md)) so runs stay consistent in style — not a byte-identical projection. The full template and the shape vocabulary live in [create.md](instructions/create.md).

## Register and surface

Two axes, set before arranging:

- **register** — the posture: **brand** (the surface communicates — landing, campaign, portfolio) or **product** (the surface serves a task — dashboard, form, settings). Biases the arrangement, never gates it. Read the matching [brand.md](references/brand.md) / [product.md](references/product.md) first.
- **surface** — the granular type, named by context. A surface sits under a register; surfaces come from the conversation, never a fixed set. Storefronts straddle — the marketing shell is brand, the checkout / account flow is product.

## Inputs

Plan from the conversation. Beyond that, the only inputs are what the user provides — a brief, a PRD, a description, a reference URL, or existing material they point to; nothing is auto-loaded. If the user hands over existing content or a prior plan, arrange against it; otherwise plan from intent.

## Guidelines

- Plan structure only — never embed visual decisions (colors, fonts, spacing, tokens), copy strings, or requirement IDs (`fr-1`, `m1`, `j1`, `us-3`).
- Derive surfaces and topics from the conversation; no fixed project types.
- Name the register (brand or product) per surface; it biases the arrangement, never gates the shape.
- Plan each surface for real conditions — its reflow on narrow viewports and its content volume (none/typical/many) — as structural intent in the narration, never pixels or breakpoints.
- Draw a low-fi wireframe — glyphs stand in for content; the plan stays greyscale and content-blind so it holds under any design.
- Patch the frontmatter region tree first, then the body that narrates it, so the two stay in sync.
