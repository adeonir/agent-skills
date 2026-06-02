---
name: design-brief
allowed-tools: Bash(bun:*) Read Write Edit Grep Glob WebFetch
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
  the design tokens as a visual specimen sheet then committing tuned
  values back; reconciling design drift or syncing from implementation.
  Not for rendering page variants, feature implementation spec, system
  architecture, or PR/code review.
---

# Design Brief

Greenfield design pipeline for any digital product: discover, author
`DESIGN.md` with a YAML frontmatter holding the authoritative design
tokens plus numbered prose sections that narrate them, and refine that
identity. DESIGN.md is the single artifact this skill authors and owns.

## Workflow

```text
direction --> design --> preview (optional)
  |             |           |
  v             v           v
moodboard.md  DESIGN.md   styleguide.html (tune live)
                  ^___________|
                  reconcile commits tuned deltas back
```

Arrows show the suggested greenfield order. `direction` auto-skips when a
visual direction is already given (reference images, URL, codebase, text
description); it runs only when the direction is absent, exploring a mood
into `moodboard.md` that `design` then authors tokens from. `preview` is
optional and runs after `design` — it renders the tokens as a specimen
sheet and tunes them live; tuned deltas commit back through `reconcile.md`,
the sole patcher. Each step is invokable standalone — call them in any
order, skip any of them, or run only the one you need. Brownfield drift
after handoff → `reconcile.md`.

> **Auto-load:** `discovery.md` runs before every operation — never
> skipped, never invoked directly. It reads the surfaces, source,
> and entry mode so downstream phases route correctly.

DESIGN.md holds the visual identity as a YAML frontmatter
carrying the normative design tokens (`colors`, `typography`, `rounded`,
`borderWidth`, `spacing`, `components`, `elevation`, `duration`,
`easing`, `breakpoints`) plus numbered prose sections that narrate them
(Visual Theme & Atmosphere, Color Palette & Roles, Typography Rules,
Component Stylings, Layout Principles, Shapes, Elevation & Depth,
Motion & Interaction, Responsive Behavior, Do's and Don'ts,
Agent Prompt Guide). Token references use `{path.to.token}` syntax. The
frontmatter is the authoritative state; the prose narrates it. Layout and
content are separate concerns, not part of DESIGN.md.

## Three Modes

- **Greenfield** — zero to `DESIGN.md` from raw inputs (URL, images,
  brief, codebase, design-tool file). Default path; runs `direction`
  (when no visual reference exists, mood explored into `moodboard.md`
  first) → design.
- **Rebrand** — restyle an existing `DESIGN.md` from a new reference,
  patching the sections it drives. Handled by
  [design.md](instructions/design.md).
- **Reconcile** — patch DESIGN.md from a drifted implementation, or
  apply tuned token deltas handed over by `preview`. Lives in
  [reconcile.md](instructions/reconcile.md).

## Operations

| Operation | File |
| --------- | ---- |
| Explore and lock a visual direction when no reference exists | [direction.md](instructions/direction.md) |
| Author or refresh DESIGN.md from images, codebase, URL, brand, design-tool file | [design.md](instructions/design.md) |
| Preview DESIGN.md tokens as a specimen sheet and tune them live | [preview.md](instructions/preview.md) |
| Audit DESIGN.md tokens, contrast, references, hierarchy | [validate.md](instructions/validate.md) |
| Patch DESIGN.md from drifted implementation or tuned deltas | [reconcile.md](instructions/reconcile.md) |

`discovery.md` auto-loads before every operation — never skipped, never
invoked directly. `aesthetics.md` and `presets.md` auto-load inside
`direction.md`; `aesthetics.md` and `anti-patterns.md` auto-load inside
`preview.md`, which serves the specimen sheet through
`scripts/preview-server.ts`. `validate.md` is both directly callable and
auto-loaded as a gate by `design.md` and `reconcile.md`, so
DESIGN.md never lands invalid.

## Guidelines

- Ask one question at a time when gathering context from the user
- Treat `docs/design/DESIGN.md` as the source of truth for visual
  identity
- Patch DESIGN.md frontmatter group by group and prose section by
  section so each phase preserves the others' work; patch the YAML
  authoritative layer first, prose follows
- Route preset and decision sets by the surfaces the project has
  (marketing/content, app/dashboard, storefront/commerce)
- Treat external design-tool files as user-owned — read only when the
  user asks and the matching MCP is available

## Anti-Pattern: Whole-File Rewrite on Section Edit

Rewriting the entire `DESIGN.md` when only one slice changed clobbers
other slices. Patch the YAML frontmatter group first, then the prose
bullets that cite the patched tokens. `design.md` owns the DESIGN.md
frontmatter and prose sections. `reconcile.md` patches DESIGN.md from a
drifted implementation or from tuned deltas, following the same surgical
rules. `preview.md` produces tuned deltas but never writes DESIGN.md —
`reconcile.md` applies them.

## Anti-Pattern: Creating External Tool Files

External design-tool files are user-owned. The skill never creates
them — it pulls when the file already exists and the matching MCP is
available. Creating files in someone else's tool surprises them and
risks naming collisions.

## Anti-Pattern: Copy Leakage into DESIGN.md

DESIGN.md is content-agnostic by design. The same tokens and brand prose must render *any* copy — placeholder, marketing, editorial, or per-locale — without rewrites. Leaks happen when Section 1 (Visual Theme & Atmosphere) reads like a product pitch, when Section 4 (Component Stylings) names components by product-specific labels, or when Section 11 (Agent Prompt Guide) bakes real headlines, CTAs, or feature names into example prompts. The fix: keep brand voice in DESIGN.md, keep every product string out of it, and use placeholders (`[Headline]`, `[Body Lorem]`, `[CTA Label]`, `[Nav Label]`) inside Section 11 prompts. Treat content and design as orthogonal — one DESIGN.md must survive any content swap.

## Anti-Pattern: Skipping Discovery

Discovery loads before every operation, even when the user hands you
images, briefs, or a codebase. Without discovery, the skill misroutes —
running marketing-surface presets on an app, or pulling tokens from a
codebase the user wants to leave alone. The 30 seconds discovery costs
saves the alternative of redoing the whole flow.
