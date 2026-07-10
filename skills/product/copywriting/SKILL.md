---
name: copywriting
allowed-tools: Read Write Edit Grep Glob WebFetch Bash(python3:*)
description: >-
  Authors and judges copy.yaml, the content payload a design consumes:
  write fresh brand or product copy from intent, or extract and structure
  existing content from a URL, brief, codebase, or screenshot — content
  only, composable under any design — then critique or audit it before it
  ships. Use when writing headlines, value propositions, landing-page or
  CTA copy; extracting, structuring, tightening, or revoicing content;
  capturing copy from a screenshot; syncing copy.yaml from a drifted
  implementation; critiquing copy or checking whether it reads as AI slop;
  scoring copy on voice and proof; or auditing copy for readability,
  claims, and microcopy before handoff. Not for visual identity or design
  tokens, page layout or screen flow, or standalone social bios.
---

# Copywriting

Owns `copy.yaml` — the structured content payload a design consumes. Content is orthogonal to design: the same `copy.yaml` must drop into any visual identity, so this skill carries words only, never design decisions. It both **authors** copy and **judges** it; the judging modes are non-mutating — they report, the authoring modes apply.

## Quick start

Produces and judges `copy.yaml`, the content payload a design consumes.

**Author** — produce or change copy:

- **write** — author fresh copy from intent (headlines, body, CTAs). → [write.md](instructions/write.md)
- **extract** — structure existing content from a source (URL, brief, codebase, screenshot), preserving tone. → [extract.md](instructions/extract.md)
- **refresh** — tighten existing copy in the same voice (editing passes). → [refresh.md](instructions/refresh.md)
- **revoice** — rewrite existing copy in a new voice, keeping the message. → [revoice.md](instructions/revoice.md)
- **reconcile** — sync `copy.yaml` from a drifted implementation. → [reconcile.md](instructions/reconcile.md)

**Judge** — a non-mutating verdict on existing copy:

- **critique** — quality and slop verdict on a draft; scores the seven sweeps, loops back to refresh. → [critique.md](instructions/critique.md)
- **audit** — ship-readiness defect report on `copy.yaml`, P0–P3, before handoff. → [audit.md](instructions/audit.md)

## Discovery

`discovery.md` runs before every operation — never skipped, never invoked directly. It checks existing context (`copy.yaml`, source, upstream intent), classifies the request (author vs judge, then greenfield vs brownfield for authoring), and routes to the matching operation. See [discovery.md](instructions/discovery.md).

## Artifact

Produces and owns `docs/design/copy.yaml` — a context-named content tree (surfaces → parts — headline, body, cta, labels, states, images — named by context), mirroring the source. Before saving, self-check: the tree is well-formed and carries no design decisions — no colors, fonts, or layout, content only. The content stays swappable: any `copy.yaml` must work independent of visual styling.

## Register and surface

Two axes, set before writing:

- **register** — the posture: **brand** (the words are the product) or **product** (the words serve the task). Sets the voice. Read the matching [brand.md](references/brand.md) / [product.md](references/product.md) first.
- **surface** — the granular type the copy serves, named by context (landing, dashboard, form, empty-state…). A surface sits under a register; the content tree is named by context, never forced into a fixed list. Storefronts straddle — catalog copy is brand, checkout / account copy is product.

## References

Loaded on demand by the workflows:

- `references/brand.md` / `references/product.md` — register (brand vs product) posture; read the matching one first
- `references/copy-frameworks.md` — headline formulas, content-part types, page shapes, CTA patterns
- `references/voice.md` — how register sets the voice, voice axes, proof hierarchy
- `references/editing-sweeps.md` — Seven Sweeps, quick-pass checks, plain-English
- `references/ux-writing.md` — clarity craft: the assess→plan→improve→verify method, clarity principles, microcopy (errors, labels, states), a11y/i18n/terminology
- `references/anti-patterns.md` — copy slop catalog: dead words, dead structures, AI tells, proof failures; composed by both author and judge modes
- `references/scoring.md` — shared severity, score bands, and report template for critique and audit
- `scripts/slop_scan.py` — run for the deterministic slop tally (dead words, em-dash density, openers) that critique and audit consume
- `scripts/validate_copy.py` — run after any write/patch for the deterministic well-formedness and design-leakage scan the authoring self-checks rely on

## Non-mutating judgment

critique and audit read and report — they never patch `copy.yaml`. To apply a verdict, run the matching authoring operation: a weak critique axis loops to `refresh`, an off-register voice to `revoice`, a missing part to `write` — each confirmed before write. The judging modes produce the verdict; the authoring modes own the change.

## Guidelines

- When writing, be specific and keep proof outward — a number, name, or example beats an adjective.
- Preserve the source's tone when extracting — structure content, do not rewrite it.
- Keep `copy.yaml` content-only; never embed visual decisions.
- When judging, name the register first and lead with the slop verdict; let the score support it, not replace it.
- Scope output to what was captured — a region produces a region, not a full-surface tree.
- Name surfaces and parts by context; mirror the source's own structure.
