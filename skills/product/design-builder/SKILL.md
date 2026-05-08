---
name: design-builder
description: >-
  Greenfield design pipeline for any digital product (landing pages,
  websites, web apps, mobile apps): extract content, author a single-file
  visual identity in .agents/design/ (DESIGN.md, tokens plus
  rationale), define layout or screen flow, preview and refine designs,
  push to an external design tool when available. Use when building
  pages or app screens from references, images, briefs, or an existing
  codebase; defining layout or screen flow; previewing and tuning
  designs; authoring or refreshing DESIGN.md from a source. Triggers:
  "extract copy", "extract design", "extract from codebase", "web
  capture", "wireframe", "screen flow", "layout the page", "preview the
  design", "creative variants", "tune design", "mockup", "redesign this
  app", "modernize this app", "brand refresh", "validate DESIGN.md",
  "refresh design tokens", "push design to external tool", "generate
  hero banner", "create product image". Not for feature implementation
  spec, system architecture, or PR/code review.
---

# Design Builder

Greenfield design pipeline for any digital product: discover, extract
content, author `DESIGN.md`, define layout or screen flow, preview,
refine.

## Workflow

```
discovery --> copy --> inputs --> structure --> preview --> assets --> final
                                                  ^__|  (tune / comment / apply-across loop)
```

Each step is independent. Can run isolated or chained (`discovery.md`
pre-loads before every operation). Assets is optional: auto-invoked
after preview approval, or triggered directly. design-builder is
greenfield-first — codebase path inside `inputs.md` is an alternative
for redesign or migration, not the primary flow. Final design can be
served as HTML, pushed to an external design tool when the matching MCP
is available, or handed to the implementation phase.

## Triggers

- **Copy extraction** ("extract copy", "copy from URL", "web capture",
  "content from website", "brief document") →
  [copy.md](references/copy.md)
- **Visual identity (DESIGN.md authoring)** ("extract design tokens",
  "author DESIGN.md", "refresh design tokens", "extract design from
  images / codebase / design tool") → [inputs.md](references/inputs.md)
- **Layout / screen flow** ("create a wireframe", "layout the page",
  "structure the content", "screen flow", "validate this wireframe") →
  [structure.md](references/structure.md)
- **Preview / variants** ("preview the design", "visual mockup", "tune
  the design", "creative variants", "pivot the design", "apply across
  variants", "push to design tool") → [preview.md](references/preview.md)
- **Validation** ("validate DESIGN.md", "check DESIGN.md", "audit
  design tokens", "lint the design system") →
  [validate.md](references/validate.md)
- **Redesign** ("redesign this app", "modernize this interface", "brand
  refresh", "change the vibe") → [redesign.md](references/redesign.md)
- **Asset generation** ("generate hero banner", "create product image",
  "generate OG card", "image prompts") →
  [assets.md](references/assets.md)

`discovery.md` is auto-loaded before every operation — never skipped.

`aesthetics.md` and `web-standards.md` are auto-loaded by `preview.md`.

`validate.md` is both directly callable and auto-loaded by `inputs.md`
Step 5 as the gate before declaring done.

`assets.md` is both directly callable and an optional sub-phase
auto-invoked by `preview.md` after variant approval.

## Guidelines

- Ask one question at a time when gathering context from the user
- Treat `.agents/design/DESIGN.md` as the source of truth
  for visual identity
- Patch DESIGN.md section by section so each phase preserves the
  others' work
- Route preset and decision sets by project type (landing-page,
  website, web-app, mobile-app)
- Auto-load `aesthetics.md` and `web-standards.md` for every preview run
- Treat external design-tool files as user-owned — read or push only
  when the user asks and the matching MCP is available

## Anti-Pattern: Whole-File Rewrite on Section Edit

Rewriting the entire `DESIGN.md` when only `## Layout` or
`## Components` changed clobbers other sections that other phases own.
Patch section by section: `inputs.md` owns frontmatter + most prose,
`structure.md` owns `## Layout` and `## Screen Flow`, `copy.md` owns
content payload (in `copy.yaml`).

## Anti-Pattern: Creating External Tool Files

External design-tool files (Pencil, Paper, Figma) are user-owned. The
skill never creates them — it pulls when the file already exists and
the matching MCP is available, and pushes when the user explicitly
asks. Creating files in someone else's tool surprises them and risks
naming collisions.

## Anti-Pattern: Skipping Discovery

Discovery loads before every operation, even when the user hands you
images, briefs, or a codebase. Without discovery, the skill misroutes —
running landing-page presets on a mobile app, or pulling tokens from a
codebase the user wants to leave alone. The 30 seconds discovery costs
saves the alternative of redoing the whole flow.
