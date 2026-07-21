---
name: design-brief
allowed-tools: Bash(bun:*) Bash(python3:*) Read Write Edit Grep Glob WebFetch
description: >-
  Greenfield design pipeline for any digital product: explore a visual
  direction when no reference exists, then author and refine the visual
  identity in DESIGN.md. Use when designing a landing page, marketing
  site, web or mobile app, dashboard, or e-commerce store; exploring or
  deciding a mood or visual direction from scratch with no reference or
  moodboard; authoring a design system, extracting design tokens,
  building or refreshing DESIGN.md from references, images, briefs, or a
  codebase; applying named tones to the identity; redesigning,
  modernizing, or refreshing the brand identity; previewing and tuning
  the design tokens as a visual styleguide then committing tuned
  values back; syncing DESIGN.md from implementation drift; evolving
  the identity against a product's stated intent from a PRD or
  PRODUCT.md. Not for rendering page variants, feature implementation
  spec, technical design docs, system architecture, or PR/code review.
---

# Design Brief

Greenfield design pipeline for any digital product: discover, author `DESIGN.md` with a YAML frontmatter holding the authoritative design tokens plus prose sections that narrate them, and refine that identity. DESIGN.md is the primary artifact this skill authors and owns; `docs/design/styleguide.html` is its rendered styleguide.

## Quick start

| Operation | File |
| --------- | ---- |
| Explore and lock a visual direction when no reference exists | [direction.md](instructions/direction.md) |
| Author, refresh, or drift-sync DESIGN.md from images, codebase, URL, brand, design-tool file | [design.md](instructions/design.md) |
| Preview DESIGN.md tokens as a styleguide and tune them live, committing tuned values back | [preview.md](instructions/preview.md) |
| Audit DESIGN.md tokens, contrast, references, hierarchy | [validate.md](instructions/validate.md) |

## Workflow

```text
direction → design → preview (optional)
  |          |          |
  v          v          v
moodboard.md DESIGN.md  styleguide.html
               ^          |
               |__________|
        tuned values commit back
```

Arrows show the suggested greenfield order. `direction` auto-skips when a visual direction is already given (reference images, URL, codebase, text description); it runs only when the direction is absent, exploring a mood into `moodboard.md` that `design` then authors tokens from. `preview` is optional and runs after `design` — it renders the tokens as a specimen sheet, tunes them live, and commits tuned values straight back into DESIGN.md. Each step is invokable standalone — call them in any order, skip any of them, or run only the one you need. Brownfield drift after handoff → `design.md`'s `sync` sub-mode.

DESIGN.md holds the visual identity as a YAML frontmatter carrying the normative design tokens (`colors`, `typography`, `rounded`, `borderWidth`, `spacing`, `components`, `elevation`, `duration`, `easing`, `breakpoints`) plus prose sections that narrate them, following the `design.md` spec order (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Motion & Interaction, Responsive Behavior, Do's and Don'ts, Agent Prompt Guide). Token references use `{path.to.token}` syntax. The frontmatter is the authoritative state; the prose narrates it. Layout and content are separate concerns, not part of DESIGN.md.

## Fields

Discovery classifies every engagement by field, then routes:

- **Greenfield** — no existing identity. Author `DESIGN.md` from raw inputs (URL, images, brief, codebase, design-tool file). Default path; runs `direction` first when no visual reference exists (mood explored into `moodboard.md`), then `design`.
- **Brownfield** — an existing identity to inherit, refresh, rebrand from a new reference, evolve against stated intent (`PRODUCT.md` / PRD), or sync from a drifted implementation. Handled by [design.md](instructions/design.md); discovery picks the sub-mode by intent.

## Loading

`discovery.md` auto-loads before every operation — never skipped, never invoked directly. It reads the surfaces, source, and entry mode so downstream phases route correctly. `aesthetics.md` and the register files (`brand.md` / `product.md`) auto-load inside `direction.md`; `aesthetics.md` and the matching register file also auto-load inside `design.md` for token-authoring principles; `anti-patterns.md` auto-loads inside `preview.md`, which serves the styleguide through `scripts/preview-server.ts`. `design.md` and `validate.md` compute WCAG contrast through `scripts/check-contrast.py` — ratios are computed, never estimated. `validate.md` is both directly callable and auto-loaded as a gate by `design.md`, and runs at the close of a `preview.md` tuning session — DESIGN.md is never declared done with validation errors.

## Guidelines

- Ask one question at a time when gathering context from the user
- Treat `docs/design/DESIGN.md` as the source of truth for visual identity
- Patch DESIGN.md frontmatter group by group and prose section by section so each phase preserves the others' work; patch the YAML authoritative layer first, prose follows
- Route by the surfaces the project has, named by context — registers and the straddle cases are defined in `references/brand.md` / `references/product.md`; surfaces spanning both registers load both
- Treat external design-tool files as user-owned — read only when the user asks and the matching MCP is available

## Anti-Pattern: Whole-File Rewrite on Section Edit

Rewriting the entire `DESIGN.md` when only one slice changed clobbers other slices. Patch the YAML frontmatter group first, then the prose bullets that cite the patched tokens. DESIGN.md has two writers under the same surgical rules: `design.md` owns authoring, refresh, and drift sync; `preview.md` commits tuned deltas.

## Anti-Pattern: Creating External Tool Files

External design-tool files are user-owned. The skill never creates them — it pulls when the file already exists and the matching MCP is available. Creating files in someone else's tool surprises them and risks naming collisions.

## Anti-Pattern: Copy Leakage into DESIGN.md

DESIGN.md is content-agnostic by design. The same tokens and brand prose must render *any* copy — placeholder, marketing, editorial, or per-locale — without rewrites. Leaks happen when the Overview section reads like a product pitch, when the Components section names components by product-specific labels, or when the Agent Prompt Guide section bakes real headlines, CTAs, or feature names into example prompts. The fix: keep brand voice in DESIGN.md, keep every product string out of it, and use placeholders (`[Headline]`, `[Body Lorem]`, `[CTA Label]`, `[Nav Label]`) inside the Agent Prompt Guide prompts. Treat content and design as orthogonal — one DESIGN.md must survive any content swap.

## Anti-Pattern: Skipping Discovery

Discovery loads before every operation, even when the user hands you images, briefs, or a codebase. Without discovery, the skill misroutes — authoring brand-register tokens for a product app, or pulling tokens from a codebase the user wants to leave alone. The 30 seconds discovery costs saves the alternative of redoing the whole flow.
