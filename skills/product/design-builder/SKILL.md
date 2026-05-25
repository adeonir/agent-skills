---
name: design-builder
allowed-tools: Bash(bun:*) Read Write Edit Grep Glob WebFetch
description: >-
  Greenfield design pipeline for any digital product (landing pages,
  websites, web apps, mobile apps, e-commerce storefronts): extract
  content, author the visual identity, define page composition, screen
  flow, or commerce surfaces, preview and refine variants. Not for
  feature implementation spec, system architecture, or PR/code review.
when_to_use: >-
  Use when building pages, app screens, or storefronts from references,
  images, briefs, or a codebase; defining layout or screen flow;
  previewing and tuning designs; authoring or refreshing the visual
  identity from a source; or syncing design artifacts back from a
  drifted implementation. Trigger phrases: "extract copy", "extract
  design tokens", "extract from codebase", "web capture", "create a
  wireframe", "screen flow", "layout the page", "preview the design",
  "creative variants", "tune the design", "visual mockup", "redesign
  this app", "modernize this app", "brand refresh", "validate the
  design", "refresh DESIGN.md from design-tool file", "sync design from
  implementation", "update DESIGN.md from code", "reconcile drift",
  "refresh design tokens from this codebase".
---

# Design Builder

Greenfield design pipeline for any digital product: discover, extract
content, author `DESIGN.md` with a YAML frontmatter holding the
authoritative design tokens plus numbered prose sections that narrate
them, define page composition or screen flow in a separate structure
artifact, preview, refine.

## Workflow

```text
copy --> identity --> structure --> preview
            |            |             ^__|
            |            |           (tune loop)
            v            v
      DESIGN.md     .agents/design/structure.md
      (visual       (page composition, screen flow,
      identity)      or commerce surfaces)
```

Arrows show the suggested greenfield order. Each step is invokable
standalone — call them in any order, skip any of them, or run only the
one you need. Brownfield drift after handoff → `reconcile.md`.
`discovery.md` is auto-loaded before every operation — never skipped,
never a step the user invokes directly.

DESIGN.md holds the visual identity in two layers: a YAML frontmatter
carrying the normative design tokens (`colors`, `typography`, `rounded`,
`spacing`, `components`, `elevation`, `duration`, `easing`,
`breakpoints`) plus numbered prose sections that narrate them
(Overview, Colors, Typography, Layout, Elevation & Depth, Shapes,
Components, Do's and Don'ts, Motion & Interaction, Responsive Behavior,
Agent Prompt Guide). Token references use `{path.to.token}` syntax.
`structure.md` writes a parallel artifact at `.agents/design/structure.md`
and never touches DESIGN.md. preview parses the frontmatter at render
time and resolves references into CSS custom properties.

design-builder is greenfield-first. For brownfield drift after handoff,
`reconcile.md` patches DESIGN.md and copy.yaml back from the
implementation. HTML preview is a visualization for decision-making —
output that can feed back into DESIGN.md or copy.yaml via reconcile, not
the final handoff artifact.

## Triggers

- **Copy extraction** ("extract copy", "copy from URL", "web capture",
  "content from website", "brief document") →
  [copy.md](instructions/copy.md)
- **Visual identity (DESIGN.md authoring)** ("extract design tokens",
  "author DESIGN.md", "extract from images", "extract from codebase",
  "extract from URL", "extract from design tool", "refresh DESIGN.md
  from design-tool file") →
  [identity.md](instructions/identity.md)
- **Layout / screen flow / commerce surfaces** ("create a wireframe",
  "layout the page", "structure the content", "screen flow", "PLP",
  "PDP", "cart", "checkout", "validate this wireframe") →
  [structure.md](instructions/structure.md)
- **Preview / variants** ("preview the design", "visual mockup", "tune
  the design", "creative variants", "pivot the design") →
  [preview.md](instructions/preview.md)
- **Validation** ("validate DESIGN.md", "validate the design", "check
  DESIGN.md", "audit design tokens", "lint the design system") →
  [validate.md](instructions/validate.md)
- **Redesign (anchor + new reference)** ("redesign this app", "modernize
  this app", "brand refresh", "change the vibe") →
  [redesign.md](instructions/redesign.md)
- **Reconcile (brownfield drift sync)** ("sync design from
  implementation", "update DESIGN.md from code", "reconcile drift",
  "refresh design tokens from this codebase"; not for: applying a new
  reference or vibe — see redesign) →
  [reconcile.md](instructions/reconcile.md)

`discovery.md` is auto-loaded before every operation — never skipped.

`aesthetics.md` and `web-standards.md` are auto-loaded by `preview.md`.

`validate.md` is both directly callable and auto-loaded as a gate by
`identity.md` and `reconcile.md` — so DESIGN.md never lands invalid for
downstream consumers (preview, structure, redesign).

## Guidelines

- Ask one question at a time when gathering context from the user
- Treat `.agents/design/DESIGN.md` as the source of truth for visual
  identity
- Treat `.agents/design/structure.md` as the source of truth for
  page composition or screen flow
- Patch DESIGN.md frontmatter group by group and prose section by
  section so each phase preserves the others' work; patch the YAML
  authoritative layer first, prose follows
- Route preset and decision sets by project type (landing-page,
  website, web-app, mobile-app, e-commerce)
- Auto-load `aesthetics.md` and `web-standards.md` for every preview run
- Treat external design-tool files as user-owned — read only when the
  user asks and the matching MCP is available

## Anti-Pattern: Whole-File Rewrite on Section Edit

Rewriting the entire `DESIGN.md` when only one slice changed clobbers
other slices. Patch the YAML frontmatter group first, then the prose
bullets that cite the patched tokens. `identity.md` owns the DESIGN.md
frontmatter and prose sections, `structure.md` owns its own artifact at
`.agents/design/structure.md`, `copy.md` owns content payload in
`copy.yaml`. `reconcile.md` patches DESIGN.md and copy.yaml from a
drifted implementation following the same surgical rules.

## Anti-Pattern: Creating External Tool Files

External design-tool files are user-owned. The skill never creates
them — it pulls when the file already exists and the matching MCP is
available. Creating files in someone else's tool surprises them and
risks naming collisions.

## Anti-Pattern: Copy Leakage into DESIGN.md

DESIGN.md is content-agnostic by design. The same tokens and brand prose must render *any* copy — placeholder, marketing, editorial, or per-locale — without rewrites. Leaks happen when Section 1 (Overview) reads like a product pitch, when Section 7 (Components) names components by product-specific labels, or when Section 11 (Agent Prompt Guide) bakes real headlines, CTAs, or feature names into example prompts. The fix: keep brand voice in DESIGN.md, route every product string into `copy.yaml`, and use placeholders (`[Headline]`, `[Body Lorem]`, `[CTA Label]`, `[Nav Label]`) inside Section 11 prompts. Treat copy and design as orthogonal — one DESIGN.md must survive any copy.yaml swap.

## Anti-Pattern: Skipping Discovery

Discovery loads before every operation, even when the user hands you
images, briefs, or a codebase. Without discovery, the skill misroutes —
running landing-page presets on a mobile app, or pulling tokens from a
codebase the user wants to leave alone. The 30 seconds discovery costs
saves the alternative of redoing the whole flow.
