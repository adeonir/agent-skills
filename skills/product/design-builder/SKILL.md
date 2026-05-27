---
name: design-builder
allowed-tools: Bash(bun:*) Read Write Edit Grep Glob WebFetch
description: >-
  Greenfield design pipeline for any digital product (landing pages,
  websites, web apps, mobile apps, e-commerce storefronts): extract
  content, author the visual identity, define page composition, screen
  flow, or commerce surfaces, preview and refine variants. Use when
  authoring a design system, extracting design tokens, building or
  refreshing DESIGN.md, building pages, app screens, or storefronts
  from references, images, briefs, or a codebase; creating wireframes,
  defining screen flows or layouts; previewing or tuning designs,
  generating creative variants, applying named tones; redesigning,
  modernizing, or refreshing the brand identity; reconciling design
  drift or syncing from implementation. Not for feature implementation spec, system
  architecture, or PR/code review.
---

# Design Builder

Greenfield design pipeline for any digital product: discover, extract
content, author `DESIGN.md` with a YAML frontmatter holding the
authoritative design tokens plus numbered prose sections that narrate
them, define page composition or screen flow in a separate structure
artifact, preview, refine.

## Workflow

```text
copy --> design --> structure --> preview
            |            |             ^__|
            |            |           (tune loop)
            v            v
      DESIGN.md     docs/design/structure.md
      (visual       (page composition, screen flow,
      identity)      or commerce surfaces)
```

Arrows show the suggested greenfield order. Each step is invokable
standalone — call them in any order, skip any of them, or run only the
one you need. Brownfield drift after handoff → `reconcile.md`.

> **Auto-load:** `discovery.md` runs before every operation — never
> skipped, never invoked directly. It classifies project type, source,
> and entry mode so downstream phases route correctly.

DESIGN.md holds the visual identity in two layers: a YAML frontmatter
carrying the normative design tokens (`colors`, `typography`, `rounded`,
`spacing`, `components`, `elevation`, `duration`, `easing`,
`breakpoints`) plus numbered prose sections that narrate them
(Overview, Colors, Typography, Layout, Elevation & Depth, Shapes,
Components, Do's and Don'ts, Motion & Interaction, Responsive Behavior,
Agent Prompt Guide). Token references use `{path.to.token}` syntax.
`structure.md` writes a parallel artifact at `docs/design/structure.md`
and never touches DESIGN.md. preview parses the frontmatter at render
time and resolves references into CSS custom properties.

HTML preview is a visualization for decision-making — output that can
feed back into DESIGN.md or copy.yaml via reconcile, not the final
handoff artifact.

## Three Modes

- **Greenfield** — zero to `DESIGN.md` + `structure.md` + `copy.yaml`
  from raw inputs (URL, images, brief, codebase, design-tool file).
  Default path; runs copy → design → structure → preview.
- **Redesign** — anchor an existing app, ingest a new external
  reference, map slices to DESIGN.md sections, generate variants.
  Lives in [redesign.md](instructions/redesign.md).
- **Reconcile** — sync DESIGN.md and copy.yaml back from a drifted
  implementation. Brownfield-only. Lives in
  [reconcile.md](instructions/reconcile.md).

## Operations

| Operation | File |
| --------- | ---- |
| Extract copy from URLs, captures, briefs | [copy.md](instructions/copy.md) |
| Author or refresh DESIGN.md from images, codebase, URL, brand, design-tool file | [design.md](instructions/design.md) |
| Define page composition, screen flow, or commerce surfaces | [structure.md](instructions/structure.md) |
| Generate variants, tune sliders, comment inline, commit back to DESIGN.md | [preview.md](instructions/preview.md) |
| Audit DESIGN.md tokens, contrast, references, hierarchy | [validate.md](instructions/validate.md) |
| Anchor existing app + apply new reference | [redesign.md](instructions/redesign.md) |
| Sync DESIGN.md + copy.yaml from drifted implementation | [reconcile.md](instructions/reconcile.md) |

`discovery.md` auto-loads before every operation — never skipped, never
invoked directly. `aesthetics.md` and `web-standards.md` auto-load
inside `preview.md`. `validate.md` is both directly callable and
auto-loaded as a gate by `design.md` and `reconcile.md`, so DESIGN.md
never lands invalid for downstream consumers (preview, structure,
redesign).

## Guidelines

- Ask one question at a time when gathering context from the user
- Treat `docs/design/DESIGN.md` as the source of truth for visual
  identity
- Treat `docs/design/structure.md` as the source of truth for
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
bullets that cite the patched tokens. `design.md` owns the DESIGN.md
frontmatter and prose sections, `structure.md` owns its own artifact at
`docs/design/structure.md`, `copy.md` owns content payload in
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
