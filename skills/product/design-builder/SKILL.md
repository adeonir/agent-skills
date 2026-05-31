---
name: design-builder
allowed-tools: Bash(bun:*) Read Write Edit Grep Glob WebFetch
description: >-
  Greenfield design pipeline for any digital product: author the
  visual identity, preview and refine variants. Use
  when designing a landing page, marketing site, web or mobile app,
  dashboard, or e-commerce store; authoring a design system, extracting
  design tokens, building or refreshing DESIGN.md, building pages,
  screens, or storefronts from references, images, briefs, or a
  codebase; previewing or tuning designs, generating creative variants,
  applying named tones; redesigning, modernizing, or refreshing the
  brand identity; reconciling design drift or syncing from
  implementation. Not for feature implementation spec, system
  architecture, or PR/code review.
---

# Design Builder

Greenfield design pipeline for any digital product: discover, author
`DESIGN.md` with a YAML frontmatter holding the authoritative design
tokens plus numbered prose sections that narrate them, preview, refine.
Content (`copy.yaml`) and arrangement (`blueprint.md`) come from
upstream — read here, never authored or owned by this skill.

## Workflow

```text
design --> preview
  |          ^__|
  |        (tune loop)
  v
DESIGN.md
(visual
identity)
```

Arrows show the suggested greenfield order. Each step is invokable
standalone — call them in any order, skip any of them, or run only the
one you need. Content (`copy.yaml`) and arrangement (`blueprint.md`)
are read as upstream inputs, not produced here. Brownfield drift after
handoff → `reconcile.md`.

> **Auto-load:** `discovery.md` runs before every operation — never
> skipped, never invoked directly. It reads the surfaces, source,
> and entry mode so downstream phases route correctly.

DESIGN.md holds the visual identity in two layers: a YAML frontmatter
carrying the normative design tokens (`colors`, `typography`, `rounded`,
`spacing`, `components`, `elevation`, `duration`, `easing`,
`breakpoints`) plus numbered prose sections that narrate them
(Visual Theme & Atmosphere, Color Palette & Roles, Typography Rules,
Component Stylings, Layout Principles, Shapes, Elevation & Depth,
Motion & Interaction, Responsive Behavior, Do's and Don'ts,
Agent Prompt Guide). Token references use `{path.to.token}` syntax.
preview parses the frontmatter at render time and resolves references
into CSS custom properties. Arrangement lives upstream in
`docs/design/blueprint.md` — read by preview, never part of DESIGN.md.

HTML preview is a visualization for decision-making — output that can
feed back into DESIGN.md via reconcile, not the final handoff artifact.

## Three Modes

- **Greenfield** — zero to `DESIGN.md` from raw inputs (URL, images,
  brief, codebase, design-tool file); content comes from `copy.yaml` and
  arrangement from `blueprint.md` upstream. Default path; runs
  design → preview.
- **Rebrand** — restyle an existing `DESIGN.md` from a new reference,
  patching the sections it drives. Handled by
  [design-brief.md](instructions/design-brief.md).
- **Reconcile** — sync DESIGN.md back from a drifted implementation.
  Brownfield-only. Lives in [reconcile.md](instructions/reconcile.md).

## Operations

| Operation | File |
| --------- | ---- |
| Author or refresh DESIGN.md from images, codebase, URL, brand, design-tool file | [design-brief.md](instructions/design-brief.md) |
| Generate variants, tune sliders, comment inline, commit back to DESIGN.md | [preview.md](instructions/preview.md) |
| Audit DESIGN.md tokens, contrast, references, hierarchy | [validate.md](instructions/validate.md) |
| Sync DESIGN.md from drifted implementation | [reconcile.md](instructions/reconcile.md) |

`discovery.md` auto-loads before every operation — never skipped, never
invoked directly. `aesthetics.md` and `web-standards.md` auto-load
inside `preview.md`. `validate.md` is both directly callable and
auto-loaded as a gate by `design-brief.md` and `reconcile.md`, so DESIGN.md
never lands invalid for downstream consumers (preview).

## Guidelines

- Ask one question at a time when gathering context from the user
- Treat `docs/design/DESIGN.md` as the source of truth for visual
  identity
- Read `docs/design/blueprint.md` as the upstream arrangement input;
  never author it here
- Patch DESIGN.md frontmatter group by group and prose section by
  section so each phase preserves the others' work; patch the YAML
  authoritative layer first, prose follows
- Route preset and decision sets by the surfaces the project has
  (marketing/content, app/dashboard, storefront/commerce)
- Auto-load `aesthetics.md` and `web-standards.md` for every preview run
- Treat external design-tool files as user-owned — read only when the
  user asks and the matching MCP is available

## Anti-Pattern: Whole-File Rewrite on Section Edit

Rewriting the entire `DESIGN.md` when only one slice changed clobbers
other slices. Patch the YAML frontmatter group first, then the prose
bullets that cite the patched tokens. `design-brief.md` owns the DESIGN.md
frontmatter and prose sections. `copy.yaml` (content) and `blueprint.md`
(arrangement) are authored upstream — read here, never written. `reconcile.md` patches DESIGN.md from a
drifted implementation following the same surgical rules.

## Anti-Pattern: Creating External Tool Files

External design-tool files are user-owned. The skill never creates
them — it pulls when the file already exists and the matching MCP is
available. Creating files in someone else's tool surprises them and
risks naming collisions.

## Anti-Pattern: Copy Leakage into DESIGN.md

DESIGN.md is content-agnostic by design. The same tokens and brand prose must render *any* copy — placeholder, marketing, editorial, or per-locale — without rewrites. Leaks happen when Section 1 (Visual Theme & Atmosphere) reads like a product pitch, when Section 4 (Component Stylings) names components by product-specific labels, or when Section 11 (Agent Prompt Guide) bakes real headlines, CTAs, or feature names into example prompts. The fix: keep brand voice in DESIGN.md, keep every product string out of it (those live in `copy.yaml`), and use placeholders (`[Headline]`, `[Body Lorem]`, `[CTA Label]`, `[Nav Label]`) inside Section 11 prompts. Treat copy and design as orthogonal — one DESIGN.md must survive any copy.yaml swap.

## Anti-Pattern: Skipping Discovery

Discovery loads before every operation, even when the user hands you
images, briefs, or a codebase. Without discovery, the skill misroutes —
running marketing-surface presets on an app, or pulling tokens from a
codebase the user wants to leave alone. The 30 seconds discovery costs
saves the alternative of redoing the whole flow.
