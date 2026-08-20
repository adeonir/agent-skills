---
name: craft-ui
allowed-tools: Bash(bun:*) Bash(python3:*) Read Write Edit Grep Glob WebFetch
description: "Decides how a UI is arranged and how it looks, using optional lo-fi wireframes and full-page mockups. Use when planning a layout, arranging the regions of a page or screen, mapping a screen flow, comparing wireframes, generating design directions, previewing a page, exploring a redesign, or working from a reference page or screenshot. Covers landing pages, marketing sites, dashboards, product UI, and app screens, across information architecture, color, typography, layout, motion, interaction, and responsive behavior. Writes the chosen mockup to docs/design/. Not for authoring the visual identity, writing copy, single-component design, judging or auditing a built UI, or source-code review."
---

# Craft UI

craft-ui starts from the brief and other supplied inputs. The wireframe phase is optional: when used, it renders lo-fi arrangements and passes the chosen arrangement to mockups through `structure.yaml`. Without a wireframe, each mockup direction may choose its own arrangement and look. Final copy comes after the mockup and is not an input to either phase.

## Quick start

- [wireframes.md](instructions/wireframes.md) — optionally interview, render arrangements lo-fi, and create the intermediate `structure.yaml` handoff.
- [mockups.md](instructions/mockups.md) — render visual directions, with or without the wireframe handoff, pick one, and deliver it.

"Plan the layout / map the screen flow / arrange the screens" enters at wireframes. "Generate / compare / preview / try a direction" enters at mockups. When `.artifacts/design/structure.yaml` exists, mockups read it; when it does not, each direction may choose its own arrangement.

The instructions run two bundled scripts as `<this-skill>/scripts/<name>` — `render-server.ts` serves a session, and `lint_structure.py` checks the optional `structure.yaml` handoff. Resolve `<this-skill>` to the directory this `SKILL.md` was read from before running either command.

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

The wireframe reads the brief, the product posture (`PRODUCT.md`), and any reference page or screenshot. The mockup reads the brief, any available tokens (`DESIGN.md`), its direction log, and `structure.yaml` when a wireframe created it. Each input is optional. The mockup phase renders a direction from the inputs it has and does not author final copy.

## Boundary

craft-ui writes its own artifacts and nothing else: optional wireframes, mockups, the optional intermediate `structure.yaml`, and the log under `.artifacts/design/`, plus the chosen mockup at `docs/design/mockup.html`. It never writes `DESIGN.md`, `copy.yaml`, `PRODUCT.md`, or production code, and it builds pages to decide a direction, not production components.

## Anti-Pattern: Editing Someone Else's Source

A comment on a served page names something to change in the rendered page, not in an artifact. Re-render the wireframe or the mockup with the change applied; a look worth keeping is authored in the tokens, and wording worth keeping is authored in the content — neither happens here.

## Anti-Pattern: Hard-Gating on Missing Inputs

Refusing to render until `PRODUCT.md`, `DESIGN.md`, or final copy exists defeats the purpose — craft-ui shows the product at any stage. A missing input is a fallback, not a blocker: infer what the brief leaves open, compose a seed, use neutral placeholders, follow the anti-patterns, render the best coherent page, and flag what is illustrative. `structure.yaml` is optional; when it is absent, each mockup direction may choose its own arrangement.

## Anti-Pattern: Redeciding a Settled Arrangement in a Mockup

When `structure.yaml` exists, every mockup renders the same arrangement so the comparison is about the look alone. Moving a block, dropping a region, or changing a block's shape to make a direction work turns the round into a comparison of different pages. Return to the wireframe path, update the arrangement, regenerate the handoff, and re-render. When `structure.yaml` is absent, each direction may choose its own arrangement.

When `structure.yaml` exists, taking one direction's header and another's hero is not this trap — the arrangement is untouched and only the treatment of each region moves. That verdict is a composite, and it is the useful one to get.

## Guidelines

- Use only the brief and supplied inputs to shape the arrangement; final copy comes later
- If a wireframe exists, pass its chosen arrangement through `structure.yaml`
- If no wireframe exists, let each mockup direction choose its own arrangement
- Resolve every other input via the fallback rule; never hard-gate on a missing one
- Vary the direction per mockup; never converge on a house style
- Resolve every `{path.to.token}` reference when emitting CSS custom properties
- Carry what the project already wears — fonts, palette, and the components it ships — as the incumbent direction, never as a constraint on the others
- Take a verdict that spans directions and render it whole as a new one; never paste two directions into one page
- Adjust a chosen mockup by re-rendering it, never by editing an artifact it read
