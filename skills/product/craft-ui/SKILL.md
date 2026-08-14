---
name: craft-ui
allowed-tools: Bash(bun:*) Read Write Edit Grep Glob WebFetch
description: "Explores the visual direction of a UI by building it. Use when planning the layout structure as a region tree and screen flow, generating design variants, previewing a page or screen, tuning a look, exploring a redesign of a page that already exists, or working from a reference page or screenshot. Covers landing pages, marketing sites, dashboards, product UI, and app screens, across information architecture, color, typography, layout, motion, interaction, and responsive behavior. Non-mutating — it writes throwaway HTML variants and never edits production code, tokens, or copy. Not for authoring the visual identity, writing copy, single-component design, judging or auditing a built UI, or source-code review."
---

# Craft UI

craft-ui builds the interface to decide how it should look — resolving the layout structure (a named page shape per surface, seeding a region tree plus screen flow), then composing it with DESIGN.md (identity) and copy.yaml (content) into full-page HTML variants to compare side by side. One mode, **render**: plan the structure, then construct the real UI in several visual directions to decide one. One invariant: **non-mutating end to end** — it writes only to `.artifacts/`, the throwaway session artifacts (`structure.yaml` and variant HTML) plus the `VARIANTS.md` log and the chosen `final.html`. It never edits tokens, copy, or production code, and it builds variants to decide a direction, not production components.

## Quick start

- [render.md](instructions/render.md) — resolve the layout structure, generate N variants, serve, tune direction, comment, switch viewport.

"Plan the layout / map the screen flow / arrange the screens / generate / compare / preview / tune" all enter here — no need to ask which. The structure phase can stop at the plan, before any variant exists.

The instructions write a bundled script as `<this-skill>/scripts/<name>`. Resolve `<this-skill>` to the directory this `SKILL.md` was read from before running the command.

## References

render composes the references its job needs:

- [brand.md](references/brand.md) / [product.md](references/product.md) — brand vs product posture and structural arrangement (read the matching one, first)
- [macrostructures.md](references/macrostructures.md) — named page-shape presets per register, with knobs and exclusions
- [archetypes.md](references/archetypes.md) — region set plus chrome and close compositions, reflex entries marked
- [structure.md](references/structure.md) — region tree, shape vocabulary, reflow, structural self-check
- [design-thinking.md](references/design-thinking.md) — Four Questions, color strategy, slop test, density/variance dials
- [visual-laws.md](references/visual-laws.md) — Gestalt, hierarchy, balance, reading patterns
- [color.md](references/color.md) — OKLCH, palette, contrast, dark mode
- [typography.md](references/typography.md) — scale, pairing, loading
- [layout.md](references/layout.md) — spacing, grid, hierarchy, hero composition, depth
- [motion.md](references/motion.md) — the animate gate, timing, easing, materials
- [overdrive.md](references/overdrive.md) — the ambitious-tier motion tune (brand only)
- [interaction.md](references/interaction.md) — states, focus, overlays
- [responsive.md](references/responsive.md) — breakpoints, input, safe areas
- [tune.md](references/tune.md) — the tune directions (bolder, quieter, distill, delight, harden)
- [anti-patterns.md](references/anti-patterns.md) — failure modes with fail/pass examples
- [web-standards.md](references/web-standards.md) — technical rules applied to every variant

## Inputs

render resolves the layout structure itself and reads the product posture (`PRODUCT.md`), the tokens (`DESIGN.md`), the content (`copy.yaml`), and its own variant log — each optional, plus a reference page or screenshot when the user offers one. Any missing input falls back to a composed seed so a variant always renders. This is the **integrator**: the one place that resolves structure, tokens, and content together. It caches `structure.yaml` and variant HTML to `.artifacts/`, appends each variant to `VARIANTS.md` so a later session neither repeats a spent direction nor re-rolls a surface's arrangement, and writes no `docs/` source.

## Non-mutating invariant

render reads, never writes a source artifact or production code. It emits `structure.yaml`, variant HTML, the `VARIANTS.md` log, and the chosen `final.html` to `.artifacts/` — never a `docs/` source. To make a direction permanent, the user invokes the owning skill (visual identity, copy).

## Anti-Pattern: Writing a Source Artifact

render resolves structure and reads DESIGN.md and copy.yaml together — precisely because it writes no `docs/` source. Its `structure.yaml` is a session cache in `.artifacts/`, not a committed layout artifact; treating it as a `docs/` source would break the integrator boundary. When a tuned style should become permanent, redirect to DESIGN.md authoring.

## Anti-Pattern: Hard-Gating on Missing Inputs

Refusing to render until DESIGN.md and copy.yaml exist defeats the purpose — render shows the product at any stage, and the structure phase composes a layout when none is given. A missing input is a fallback, not a blocker: compose a seed, follow anti-patterns, render the best coherent page, and flag what is illustrative.

## Guidelines

- Name the register before building — the bar differs for brand vs product
- Resolve inputs via the fallback rule — never hard-gate on a missing one
- Vary the direction per variant; never converge on a house style
- Tune the visual direction by re-rendering — never edit tokens or write a source artifact
- Write only `.artifacts/`; the variants are a decision aid, not a handoff
