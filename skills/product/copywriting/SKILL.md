---
name: copywriting
allowed-tools: Read Write Edit Grep Glob WebFetch
description: >-
  Extracts and structures content from references — URLs, briefs,
  codebases, screenshots — into copy.yaml, the content payload a design
  consumes, preserving the source's tone. Use when extracting copy or
  content from a page, brief, or codebase; structuring a content payload;
  capturing copy from a screenshot or selected region; or preparing
  copy.yaml for later design work. Not for visual identity or design
  tokens, page layout or screen flow, or standalone social bios.
---

# Copywriting

Owns `copy.yaml` — the structured content payload a design consumes. Content
is orthogonal to design: the same `copy.yaml` must drop into any visual
identity, so this skill carries words only, never design decisions.

## Quick start

Structures content into `copy.yaml`, the payload a design consumes. Two
operations:

- **extract** — structure content from a source (URL, brief, codebase,
  screenshot), or draft from a description; preserve the source's tone.
  → [extract.md](instructions/extract.md)
- **reconcile** — sync `copy.yaml` from a drifted implementation.
  → [reconcile.md](instructions/reconcile.md)

## Discovery

`discovery.md` runs before every operation — never skipped, never invoked
directly. It checks existing context (`copy.yaml`, source, upstream intent),
classifies the field (greenfield / brownfield), and routes to the matching
mode. See [discovery.md](instructions/discovery.md).

## Operations

| Operation | File |
| --------- | ---- |
| Extract and structure content into copy.yaml | [extract.md](instructions/extract.md) |
| Sync copy.yaml from a drifted implementation | [reconcile.md](instructions/reconcile.md) |

## Artifact

Produces and owns `docs/design/copy.yaml` — a context-named content tree
(surfaces → parts → headline, body, cta, images), named to mirror the source.
Before saving, self-check: the tree is well-formed and carries no design
decisions (no colors, fonts, or layout — those belong to `DESIGN.md`). The two
artifacts compose on disk: any `copy.yaml` must render under any `DESIGN.md`.

## Guidelines

- Preserve the source's tone when extracting — structure content, do not
  rewrite it.
- Keep `copy.yaml` content-only; never embed visual decisions.
- Scope output to what was captured — a region produces a region, not a
  full-surface tree.
- Name surfaces and parts by context; mirror the source's own structure.
