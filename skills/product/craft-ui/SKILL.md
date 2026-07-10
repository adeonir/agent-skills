---
name: craft-ui
allowed-tools: Bash(bun:*) Read Write Edit Grep Glob WebFetch
description: >-
  Explores and judges the visual direction of a UI. Use when exploring,
  comparing, or deciding a visual direction for a UI —
  generating design variants, previewing a page or screen, tuning a look —
  or when judging design quality: critiquing a design, checking whether it
  reads as AI slop, scoring usability, or auditing a built UI for
  accessibility, performance, responsiveness, and theming before release.
  Covers landing pages, marketing sites, dashboards, product UI, app
  screens, and components, across color, typography, layout, motion,
  interaction, responsive behavior, anti-patterns, and visual hierarchy.
  Non-mutating — produces design directions and reviews, never edits
  production code, tokens, layout, or copy. Not for authoring the visual
  identity, planning layout structure, writing copy, or source-code / PR
  review.
---

# Craft UI

craft-ui builds the interface — composing DESIGN.md (identity), WIREFRAME.md (structure), and copy.yaml (content) into full-page HTML variants — and pressure-tests it, without touching production. Its core mode is **render**: construct the real UI in several visual directions to decide one. Two judging modes follow: **critique** (a chosen variant, pre-impl) and **audit** (a built UI, pre-release). The three share one rubric (register, design-thinking, heuristics, the craft dimensions, anti-patterns, web standards, scoring) and one invariant: **non-mutating end to end** — render writes only throwaway variant HTML to `.artifacts/`; critique and audit only report. It never edits tokens, layout, copy, or production code, and it builds variants to decide a direction, not production components.

## Modes

| Mode | Verb | Target | Moment | Output |
| ---- | ---- | ------ | ------ | ------ |
| **render** | integrate / tune | DESIGN.md + WIREFRAME.md + copy.yaml → variant HTML | pre-impl | variants side by side (decision aid) |
| **critique** | evaluate | the chosen variant | pre-impl | direction verdict + refinements |
| **audit** | evaluate | a running production UI | post-impl | P0–P3 quality report |

- [render.md](instructions/render.md) — generate N variants, serve, tune direction, comment, switch viewport.
- [critique.md](instructions/critique.md) — judge a chosen variant; loops back into render's tune verbs.
- [audit.md](instructions/audit.md) — judge a running UI for quality defects; independent of render, works on any build.

Pick the mode from the request — no need to ask. "Generate / compare / preview / tune" → render. "Critique / is this slop / score this variant" → critique. "Audit / is this production-ready / a11y or perf pass" → audit. critique is coupled to render (it judges a variant); audit stands alone (it judges a shipped UI).

## Shared rubric

Each mode composes the references its job needs from this shared set, so judgment and generation stay aligned:

- [brand.md](references/brand.md) / [product.md](references/product.md) — brand vs product posture (read the matching one, first)
- [design-thinking.md](references/design-thinking.md) — Four Questions, color strategy, slop test, density/variance dials
- [heuristics.md](references/heuristics.md) — Nielsen heuristics + 0–4 scoring + visual laws
- [cognitive-load.md](references/cognitive-load.md) — load checklist + working-memory rule
- [personas.md](references/personas.md) — five archetypes to test through
- [color.md](references/color.md) — OKLCH, palette, contrast, dark mode
- [typography.md](references/typography.md) — scale, pairing, loading
- [layout.md](references/layout.md) — spacing, grid, hierarchy, hero composition, depth
- [motion.md](references/motion.md) — the animate gate, timing, easing, materials
- [overdrive.md](references/overdrive.md) — the ambitious-tier motion tune (brand only)
- [interaction.md](references/interaction.md) — states, focus, overlays
- [responsive.md](references/responsive.md) — breakpoints, input, safe areas
- [tune.md](references/tune.md) — render/critique tune directions (bolder, quieter, distill, delight, harden)
- [anti-patterns.md](references/anti-patterns.md) — failure modes with fail/pass examples
- [web-standards.md](references/web-standards.md) — technical rules (render) and audit rubric
- [performance.md](references/performance.md) — loading, rendering, network, Core Web Vitals
- [scoring.md](references/scoring.md) — severity, score bands, report template

## Inputs

- **render** reads three upstream artifacts, each optional — `DESIGN.md` (tokens), `WIREFRAME.md` (layout), `copy.yaml` (content). Any missing input falls back to a composed seed so a variant always renders. This is the **integrator**: the one place that reads all three together. It writes none.
- **critique** reads the chosen variant HTML in `.artifacts/` (render's output).
- **audit** reads a running UI (required) plus optional source; inputs degrade gracefully.

## Non-mutating invariant

Each mode reads, never writes a source artifact or production code. render emits variant HTML to `.artifacts/`; critique and audit emit a judgment. To make a direction permanent, the user invokes the owning skill (layout, visual identity, copy). A reported audit defect is fixed in implementation, not here.

## Anti-Pattern: Writing a Source Artifact

render is the one place allowed to read DESIGN.md, WIREFRAME.md, and copy.yaml together — precisely because it writes none of them. Writing a source artifact here would give it two owners and break the integrator boundary. When a tuned direction should become permanent, redirect to the owning skill; when an audit finds a defect, report it for implementation to fix. Every mode here explores or judges — none edits.

## Anti-Pattern: Hard-Gating on Missing Inputs

Refusing to render until DESIGN.md, WIREFRAME.md, and copy.yaml all exist defeats the purpose — render shows the product at any stage. A missing input is a fallback, not a blocker: compose a seed, follow anti-patterns, render the best coherent page, and flag what is illustrative. Likewise audit needs only a running UI; missing source narrows the checks, it does not block them.

## Guidelines

- Name the register before judging — the bar differs for brand vs product
- render writes only `.artifacts/`; critique and audit write only a judgment
- Resolve render inputs via the fallback rule — never hard-gate on a missing one
- critique loops with render's tune verbs; audit stands alone on any build
- audit is quality-only — it does not flag token or design-system drift
- Lead evaluations with the verdict; let the score support it, not replace it
