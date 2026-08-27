---
name: copywriting
allowed-tools: Read Write Edit Grep Glob WebFetch Bash(python3:*)
description: "Creates and evaluates copy for brand, editorial, product, UX, conversion, and informational surfaces. Use when writing, extracting, editing, syncing, critiquing, or auditing copy. Not for visual identity, page layout, or standalone social bios."
---

# Copywriting

Owns `copy.yaml`, the structured content payload that design consumes. The same payload must work with any visual identity, so this skill carries words, not design decisions. It supports conversion, brand and editorial expression, product and UX guidance, and informational explanation. Authoring modes change copy. Judgment modes report on it.

## Quick start

**Author:** produce or change copy:

- **write:** author fresh or net-new copy from intent (headlines, body, CTAs). → [write.md](instructions/write.md)
- **extract:** structure existing content from a source (URL, brief, codebase, screenshot), preserving tone. → [extract.md](instructions/extract.md)
- **refresh:** tighten existing copy in the same voice (editing passes). → [refresh.md](instructions/refresh.md)
- **revoice:** rewrite existing copy in a new voice, keeping the message. → [revoice.md](instructions/revoice.md)
- **reconcile:** sync `copy.yaml` from a drifted implementation. → [reconcile.md](instructions/reconcile.md)

**Judge:** a non-mutating verdict on existing copy:

- **critique:** quality and slop verdict on a draft; scores the seven sweeps, loops back to refresh. → [critique.md](instructions/critique.md)
- **audit:** ship-readiness defect report on `copy.yaml`, P0–P3, before handoff. → [audit.md](instructions/audit.md)

## Discovery

Run `discovery.md` before every operation. It checks existing context, classifies the request, and routes to the matching operation. Do not invoke it directly. See [discovery.md](instructions/discovery.md).

## Artifact

Produces and owns `docs/design/copy.yaml`: a context-named content tree whose surfaces and parts mirror the source. It carries `intent` (purpose, reader goal, function, and functional constraints) and `voice` (the stylistic direction). Later operations read both before drafting or judging. Authoring operations change content only after the user confirms the proposed edits; they change intent or voice only after the user confirms a new intent or voice. Before saving, self-check that the tree is well-formed and carries no design decisions: no colors, fonts, or layout. The content stays swappable: any `copy.yaml` must work independent of visual styling.

## Function, register, and surface

Set the intent before choosing patterns. `intent.function` is the reader's job for that surface; classify it with [surface-functions.md](references/surface-functions.md). Intent also records the purpose, reader goal, and functional constraints, such as a ban on sales language. `voice` carries tone and style. Use one function per surface when possible. Mixed surfaces may override the root intent per surface or part.

Then set the register:

- **register:** the posture, either **brand** (the words are the product) or **product** (the words serve the task). It sets the voice. Read the matching [brand.md](references/brand.md) / [product.md](references/product.md) first.
- **surface:** the granular type the copy serves, named by context (landing, dashboard, form, empty-state…). A surface sits under a register; the content tree is named by context, never forced into a fixed list. Storefronts straddle: catalog copy is brand, checkout / account copy is product.

## References

Loaded on demand by the workflows:

- `references/brand.md` / `references/product.md`: register posture; read the matching one first
- `references/surface-functions.md`: reader job, function-specific patterns, and quality criteria
- `references/copy-frameworks.md`: headline formulas, content-part types, page shapes, CTA patterns
- `references/voice.md`: how register sets the voice, voice axes, proof hierarchy
- `references/editing-sweeps.md`: Seven Sweeps, quick-pass checks, plain-English
- `references/ux-writing.md`: clarity craft, including the assess→plan→improve→verify method and microcopy
- `references/anti-patterns.md`: copy slop catalog; dead words, dead structures, AI tells, proof failures
- `references/scoring.md`: shared severity, score bands, and report template for critique and audit
- `scripts/slop_scan.py`: run for the deterministic slop tally (dead words, em-dash density, openers) that critique and audit consume
- `scripts/validate_copy.py`: run after any write or patch for the well-formedness and design-leakage scan

The workflows write a bundled script as `<this-skill>/scripts/<name>`. Resolve `<this-skill>` to the directory this `SKILL.md` was read from before running the command.

## Non-mutating judgment

critique and audit read and report; they never patch `copy.yaml`. To apply a verdict, run the matching authoring operation: a weak critique axis loops to `refresh`, an off-register voice to `revoice`, and a missing part to `write`. Confirm each before writing. The judging modes produce the verdict; the authoring modes own the change.

## Guidelines

- When writing, support claims about capability, quality, or outcomes with proof; factual descriptions need accurate context.
- Treat the confirmed intent, including its constraints, as the first gate for every pattern, edit, and verdict.
- Select frameworks and quality criteria from the surface function before drafting.
- Preserve the source's tone when extracting: structure content, do not rewrite it.
- Keep `copy.yaml` content-only; never embed visual decisions.
- When judging, name the intent and register first, then lead with the slop verdict; let the score support it, not replace it.
- Scope output to what was captured: a region produces a region, not a full-surface tree.
- Name surfaces and parts by context; mirror the source's own structure.
