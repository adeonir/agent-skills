---
name: design-brief
allowed-tools: Bash(bun:*) Bash(npx:*) Bash(python3:*) Read Write Edit Grep Glob WebFetch
description: "Visual identity development and validation through the official `DESIGN.md` schema and CLI. Use when creating, refreshing, syncing, previewing, exporting, or diffing design tokens. Not for page layout, rendered variants, product copy, feature specs, production code, or code review."
---

# Design Brief

Develops and validates the visual identity carried by the root `DESIGN.md`.

## Triggers

| Vocabulary or state | Load |
|---|---|
| no visual reference, explore, find a look, not sure how it should feel | [direction.md](instructions/direction.md) |
| assess, audit current identity, what is consistent or drifted | [identity-assessment.md](instructions/identity-assessment.md) |
| author, create, extract, codify, refresh, rebrand, evolve, sync | [design.md](instructions/design.md) |
| preview, tune, comment, inspect visually | [preview.md](instructions/preview.md) |
| validate, lint, check `DESIGN.md` | [validate.md](instructions/validate.md) |
| export tokens | [export.md](instructions/export.md) |
| compare versions, token diff, regressions | [diff.md](instructions/diff.md) |

Load one operation at a time. Preview, validate, export, and diff enter directly; brownfield authoring passes through the identity assessment first.

## Workflow

```text
greenfield, direction absent → direction → design → validate → preview
greenfield, direction given  ───────────→ design → validate → preview
brownfield → identity-assessment → confirmed intent → design → validate
```

Every operation starts by loading discovery. A brownfield assessment may end after presenting its findings when the user asked for an audit only.
