---
name: craft-ui
allowed-tools: Bash(bun:*) Read Write Edit Grep Glob WebFetch
description: "Decides how a UI is arranged and how it looks, by building it in two phases. Use when planning a layout, arranging the regions of a page or screen, mapping a screen flow, comparing wireframes, generating design directions, previewing a page, exploring a redesign, or working from a reference page or screenshot. Covers landing pages, marketing sites, dashboards, product UI, and app screens, across information architecture, color, typography, layout, motion, interaction, and responsive behavior. Writes lo-fi wireframes and full-page mockups to compare, and the chosen mockup to docs/design/. Not for authoring the visual identity, writing copy, single-component design, judging or auditing a built UI, or source-code review."
---

# Craft UI

craft-ui builds the interface to decide it — first the **arrangement**, then the **look**. The wireframe phase interviews for what the artifacts leave open and renders lo-fi arrangements to compare; the mockup phase renders the settled arrangement in several visual directions to pick one. `structure.yaml` is the contract between them: the wireframe writes it, the mockup reads it and never re-plans it.

## Quick start

- [wireframes.md](instructions/wireframes.md) — interview, render the arrangements lo-fi, settle `structure.yaml`.
- [mockups.md](instructions/mockups.md) — render that arrangement in N visual directions, pick one, deliver it.

"Plan the layout / map the screen flow / arrange the screens" enter at wireframes. "Generate / compare / preview / try a direction" enter at mockups, which reads `.artifacts/design/structure.yaml`; when that file is absent the run starts at wireframes and returns.

The instructions run a bundled script as `<this-skill>/scripts/<name>`. Resolve `<this-skill>` to the directory this `SKILL.md` was read from before running the command.

## References

Each phase composes only the references its job needs.

Wireframe:

- [structure.md](references/structure.md) — region tree, shape vocabulary, reflow, volume, structural self-check

Mockup:

- [brand.md](references/brand.md) / [product.md](references/product.md) — the register's permissions and bans (read the one the surface carries)
- [design-thinking.md](references/design-thinking.md) — Four Questions, style axes, color strategy, slop test, density and variance dials
- [visual-laws.md](references/visual-laws.md) — Gestalt, hierarchy, balance, reading patterns
- [color.md](references/color.md) — OKLCH, palette, contrast, dark mode
- [typography.md](references/typography.md) — scale, pairing, loading
- [layout.md](references/layout.md) — spacing, grid, hierarchy, hero composition, depth
- [motion.md](references/motion.md) — the animate gate, timing, easing, materials
- [interaction.md](references/interaction.md) — states, focus, overlays
- [responsive.md](references/responsive.md) — breakpoints, input, safe areas
- [anti-patterns.md](references/anti-patterns.md) — failure modes with fail/pass examples
- [web-standards.md](references/web-standards.md) — technical rules applied to every mockup

## Inputs

The wireframe reads the product posture (`PRODUCT.md`) and the content (`copy.yaml`). The mockup reads `structure.yaml`, the tokens (`DESIGN.md`), the content, and its own log of spent directions. Each is optional except `structure.yaml`, and a reference page or screenshot enters either phase when the user offers one. The mockup phase is the **integrator**: the one place that renders an arrangement, tokens, and content together.

## Boundary

craft-ui writes its own artifacts and nothing else: the wireframes, the mockups, `structure.yaml`, and the log under `.artifacts/design/`, plus the chosen mockup at `docs/design/mockup.html`. It never writes `DESIGN.md`, `copy.yaml`, `PRODUCT.md`, or production code, and it builds pages to decide a direction, not production components.

## Anti-Pattern: Editing Someone Else's Source

A comment on a served page names something to change in the rendered page, not in an artifact. Re-render the wireframe or the mockup with the change applied; a look worth keeping is authored in the tokens, and wording worth keeping is authored in the content — neither happens here.

## Anti-Pattern: Hard-Gating on Missing Inputs

Refusing to render until `PRODUCT.md`, `DESIGN.md`, and `copy.yaml` exist defeats the purpose — craft-ui shows the product at any stage. A missing one of those is a fallback, not a blocker: interview for it, compose a seed, follow the anti-patterns, render the best coherent page, and flag what is illustrative. The one thing a phase does wait on is `structure.yaml`, and that is a phase order, not an input: the run goes and settles the arrangement, then comes back.

## Anti-Pattern: Redeciding the Arrangement in a Mockup

Every mockup renders the same arrangement so the comparison is about the look alone. Moving a block, dropping a region, or changing a block's shape to make a direction work turns the round into a comparison of different pages, and the user picks a look while agreeing to a structure nobody decided. Change `structure.yaml` and re-render from it instead.

Taking one direction's header and another's hero is not this trap — the arrangement is untouched and only the treatment of each region moves. That verdict is a composite, and it is the useful one to get.

## Guidelines

- Settle the arrangement before any look exists — the wireframe carries no palette and no font pick
- Resolve every other input via the fallback rule; never hard-gate on a missing one
- Vary the direction per mockup; never converge on a house style
- Resolve every `{path.to.token}` reference when emitting CSS custom properties
- Carry what the project already wears — fonts, palette, and the components it ships — as the incumbent direction, never as a constraint on the others
- Take a verdict that spans directions and render it whole as a new one; never paste two directions into one page
- Adjust a chosen mockup by re-rendering it, never by editing an artifact it read
