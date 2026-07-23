---
name: craft-ui
allowed-tools: Bash(bun:*) Read Write Edit Grep Glob WebFetch
description: >-
  Explores and judges the visual direction of a UI. Use when exploring,
  comparing, or deciding a visual direction for a UI — planning the layout
  structure as a region tree and screen flow, generating design variants,
  previewing a page or screen, tuning a look — or when judging design
  quality: critiquing a design, checking whether it reads as AI slop,
  scoring usability, or auditing a built UI for accessibility, performance,
  responsiveness, and theming before release. Covers landing pages,
  marketing sites, dashboards, product UI, app screens, and components,
  across information architecture, color, typography, layout, motion,
  interaction, responsive behavior, anti-patterns, and visual hierarchy.
  Non-mutating — produces layout plans, design directions, and reviews,
  never edits production code, tokens, or copy. Not for authoring the
  visual identity, writing copy, or source-code / PR review.
---

# Craft UI

craft-ui builds the interface — resolving the layout structure (a region tree plus screen flow), then composing it with DESIGN.md (identity) and copy.yaml (content) into full-page HTML variants — and pressure-tests it, without touching production. Its core mode is **render**: plan the structure, then construct the real UI in several visual directions to decide one. Two judging modes follow: **critique** (a chosen variant, pre-impl) and **audit** (a built UI, pre-release). The three share one rubric (register, structure, design-thinking, heuristics, the craft dimensions, anti-patterns, web standards, scoring) and one invariant: **non-mutating end to end** — render writes only throwaway session artifacts (`structure.yaml` and variant HTML) to `.artifacts/`; critique and audit only report. It never edits tokens, copy, or production code, and it builds variants to decide a direction, not production components.

## Quick start

| Mode | Verb | Target | Moment | Output |
| ---- | ---- | ------ | ------ | ------ |
| **render** | plan / integrate / tune | structure (region tree + flow) + DESIGN.md + copy.yaml → variant HTML | pre-impl | variants side by side (decision aid) |
| **critique** | evaluate | the chosen variant | pre-impl | direction verdict + refinements |
| **audit** | evaluate | a running production UI | post-impl | P0–P3 quality report |

- [render.md](instructions/render.md) — resolve the layout structure, generate N variants, serve, tune direction, comment, switch viewport.
- [critique.md](instructions/critique.md) — judge a chosen variant; loops back into render's tune verbs.
- [audit.md](instructions/audit.md) — judge a running UI for quality defects; independent of render, works on any build.

Pick the mode from the request — no need to ask. "Plan the layout / map the screen flow / arrange the screens / generate / compare / preview / tune" → render (its structure phase can stop at the plan, before any variant). "Critique / is this slop / score this variant / does this arrangement hold" → critique. "Audit / is this production-ready / a11y or perf pass" → audit. critique is coupled to render (it judges a variant); audit stands alone (it judges a shipped UI).

## Shared rubric

Each mode composes the references its job needs from this shared set, so judgment and generation stay aligned:

- [brand.md](references/brand.md) / [product.md](references/product.md) — brand vs product posture and structural arrangement (read the matching one, first)
- [structure.md](references/structure.md) — region tree, shape vocabulary, reflow, structural self-check
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

- **render** resolves the layout structure itself and reads two upstream artifacts, each optional — `DESIGN.md` (tokens) and `copy.yaml` (content). Any missing input falls back to a composed seed so a variant always renders. This is the **integrator**: the one place that resolves structure, tokens, and content together. It caches `structure.yaml` and variant HTML to `.artifacts/`, and writes no `docs/` source.
- **critique** reads the chosen variant HTML in `.artifacts/` (render's output).
- **audit** reads a running UI (required) plus optional source; inputs degrade gracefully.

## Non-mutating invariant

Each mode reads, never writes a source artifact or production code. render emits `structure.yaml` and variant HTML to `.artifacts/` — session-internal, never a `docs/` source; critique and audit emit a judgment. To make a direction permanent, the user invokes the owning skill (visual identity, copy). A reported audit defect is fixed in implementation, not here.

## Anti-Pattern: Writing a Source Artifact

render resolves structure and reads DESIGN.md and copy.yaml together — precisely because it writes no `docs/` source. Its `structure.yaml` is a session cache in `.artifacts/`, not a committed layout artifact; treating it as a `docs/` source would break the integrator boundary. When a tuned style should become permanent, redirect to DESIGN.md authoring; when an audit finds a defect, report it for implementation to fix. Every mode here explores or judges — none edits a source.

## Anti-Pattern: Hard-Gating on Missing Inputs

Refusing to render until DESIGN.md and copy.yaml exist defeats the purpose — render shows the product at any stage, and the structure phase composes a layout when none is given. A missing input is a fallback, not a blocker: compose a seed, follow anti-patterns, render the best coherent page, and flag what is illustrative. Likewise audit needs only a running UI; missing source narrows the checks, it does not block them.

## Guidelines

- Name the register before judging — the bar differs for brand vs product
- render writes only `.artifacts/`; critique and audit write only a judgment
- Resolve render inputs via the fallback rule — never hard-gate on a missing one
- critique loops with render's tune verbs; audit stands alone on any build
- audit is quality-only — it does not flag token or design-system drift
- Lead evaluations with the verdict; let the score support it, not replace it
