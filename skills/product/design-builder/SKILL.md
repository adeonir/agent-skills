---
name: design-builder
description: >-
  Greenfield design pipeline for any digital product (landing pages,
  websites, web apps, mobile apps, e-commerce storefronts): extract
  content, author the visual identity, define page composition, screen
  flow, or commerce surfaces, preview and refine variants. Use when
  building pages, app screens, or storefronts from references, images,
  briefs, or a codebase; defining layout or screen flow; previewing and
  tuning designs; authoring or refreshing the visual identity from a
  source. Triggers: "extract copy", "extract design", "extract from
  codebase", "web capture", "create a wireframe", "screen flow",
  "layout the page", "preview the design", "creative variants", "tune
  design", "visual mockup", "redesign this app", "modernize this app",
  "brand refresh", "validate the design", "refresh design tokens",
  "sync design from implementation", "reconcile drift". Not for feature
  implementation spec, system architecture, or PR/code review.
---

# Design Builder

Greenfield design pipeline for any digital product: discover, extract
content, author `DESIGN.md` with numbered prose sections, define page
composition or screen flow in a separate structure artifact, preview,
refine.

## Workflow

```
copy --> inputs --> structure --> preview --> final
            |          |             ^__|
            |          |           (tune loop)
            v          v
      DESIGN.md   .agents/design/structure.md
      (visual     (page composition, screen flow,
      identity)    or commerce surfaces)
```

Each step is independent. Can run isolated or chained. `discovery.md`
is auto-loaded before every operation — never skipped, never a step the
user invokes directly.

DESIGN.md holds the visual identity — numbered prose sections covering
atmosphere, color, typography, components, layout, depth, motion,
responsiveness, do's and don'ts, and an agent prompt guide.
`structure.md` writes a parallel artifact at `.agents/design/structure.md`
and never touches DESIGN.md. preview composes both at render time,
extracting tokens from DESIGN.md prose at generation time.

design-builder is greenfield-first. The codebase source inside
`inputs.md` doubles as the brownfield path: extracting tokens from an
existing project at the start, and reverse-syncing DESIGN.md after the
implementation has drifted. Final design is served as HTML and handed
to the implementation phase.

## Triggers

- **Copy extraction** ("extract copy", "copy from URL", "web capture",
  "content from website", "brief document") →
  [copy.md](references/copy.md)
- **Visual identity (DESIGN.md authoring)** ("extract design tokens",
  "author DESIGN.md", "refresh design tokens", "extract design from
  images / codebase / design tool", "sync design from implementation",
  "update DESIGN.md from code", "reconcile drift") →
  [inputs.md](references/inputs.md)
- **Layout / screen flow / commerce surfaces** ("create a wireframe",
  "layout the page", "structure the content", "screen flow", "PLP",
  "PDP", "cart", "checkout", "validate this wireframe") →
  [structure.md](references/structure.md)
- **Preview / variants** ("preview the design", "visual mockup", "tune
  the design", "creative variants", "pivot the design") →
  [preview.md](references/preview.md)
- **Validation** ("validate DESIGN.md", "check DESIGN.md", "audit
  design tokens", "lint the design system") →
  [validate.md](references/validate.md)
- **Redesign** ("redesign this app", "modernize this interface", "brand
  refresh", "change the vibe") → [redesign.md](references/redesign.md)

`discovery.md` is auto-loaded before every operation — never skipped.

`aesthetics.md` and `web-standards.md` are auto-loaded by `preview.md`.

`validate.md` is both directly callable and auto-loaded by `inputs.md`
Step 5 as the gate before declaring done.

## Guidelines

- Ask one question at a time when gathering context from the user
- Treat `.agents/design/DESIGN.md` as the source of truth for visual
  identity
- Treat `.agents/design/structure.md` as the source of truth for
  page composition or screen flow
- Patch DESIGN.md bullet by bullet or section by section so each phase
  preserves the others' work
- Route preset and decision sets by project type (landing-page,
  website, web-app, mobile-app, e-commerce)
- Auto-load `aesthetics.md` and `web-standards.md` for every preview run
- Treat external design-tool files as user-owned — read only when the
  user asks and the matching MCP is available

## Anti-Pattern: Whole-File Rewrite on Section Edit

Rewriting the entire `DESIGN.md` when only one section changed clobbers
other sections. Patch bullet by bullet within the affected heading.
`inputs.md` owns the DESIGN.md sections, `structure.md` owns its own
artifact at `.agents/design/structure.md`, `copy.md` owns content
payload in `copy.yaml`.

## Anti-Pattern: Creating External Tool Files

External design-tool files are user-owned. The skill never creates
them — it pulls when the file already exists and the matching MCP is
available. Creating files in someone else's tool surprises them and
risks naming collisions.

## Anti-Pattern: Skipping Discovery

Discovery loads before every operation, even when the user hands you
images, briefs, or a codebase. Without discovery, the skill misroutes —
running landing-page presets on a mobile app, or pulling tokens from a
codebase the user wants to leave alone. The 30 seconds discovery costs
saves the alternative of redoing the whole flow.
