---
name: copywriting
allowed-tools: Read Write Edit Grep Glob WebFetch
description: >-
  Authors copy.yaml, the content payload a design consumes: write fresh
  marketing or product copy from intent, or extract and structure existing
  content from a URL, brief, codebase, or screenshot — content only,
  composable under any design. Use when writing headlines, value
  propositions, landing-page or CTA copy; extracting, structuring,
  tightening, or revoicing content; capturing copy from a screenshot;
  or preparing copy.yaml for design work. Not for visual identity or
  design tokens, page layout or screen flow, or standalone social bios.
---

# Copywriting

Owns `copy.yaml` — the structured content payload a design consumes. Content
is orthogonal to design: the same `copy.yaml` must drop into any visual
identity, so this skill carries words only, never design decisions.

## Quick start

Produces `copy.yaml`, the content payload a design consumes. Operations:

- **write** — author fresh copy from intent (headlines, body, CTAs).
  → [write.md](instructions/write.md)
- **extract** — structure existing content from a source (URL, brief,
  codebase, screenshot), preserving tone. → [extract.md](instructions/extract.md)
- **refresh** — tighten existing copy in the same voice (editing passes).
  → [refresh.md](instructions/refresh.md)
- **revoice** — rewrite existing copy in a new voice, keeping the message.
  → [revoice.md](instructions/revoice.md)
- **reconcile** — sync `copy.yaml` from a drifted implementation.
  → [reconcile.md](instructions/reconcile.md)

## Discovery

`discovery.md` runs before every operation — never skipped, never invoked
directly. It checks existing context (`copy.yaml`, source, upstream intent),
classifies the field (greenfield / brownfield), and routes to the matching
operation. See [discovery.md](instructions/discovery.md).

## Artifact

Produces and owns `docs/design/copy.yaml` — a context-named content tree
(surfaces → parts → headline, body, cta, images), named to mirror the source.
Before saving, self-check: the tree is well-formed and carries no design
decisions — no colors, fonts, or layout, content only. The content stays
swappable: any `copy.yaml` must work independent of visual styling.

## References

Loaded on demand by the workflows:

- `references/copy-frameworks.md` — headline formulas, content-part types, page shapes, CTA patterns
- `references/voice.md` — voice axes, proof hierarchy, dead words and structures to strip
- `references/editing-sweeps.md` — Seven Sweeps, quick-pass checks, plain-English

## Guidelines

- When writing, be specific and keep proof outward — a number, name, or
  example beats an adjective.
- Preserve the source's tone when extracting — structure content, do not
  rewrite it.
- Keep `copy.yaml` content-only; never embed visual decisions.
- Scope output to what was captured — a region produces a region, not a
  full-surface tree.
- Name surfaces and parts by context; mirror the source's own structure.
