---
name: docs-writer
description: >-
  Generates structured product and technical documents through guided
  discovery. 5 document types: PRD, Brief (1-page summary generated
  alongside PRD), Design Doc (multi-decision trade-off discussion), ADR
  (single architecture decision record, append-only log), TDD
  (prescriptive technical plan, sized core/medium/large). Use when
  defining product requirements, drafting product specs, designing
  systems, recording architecture decisions, or writing technical
  design documents. Not for feature spec tied to implementation or
  meeting/session notes.
---

# Docs Writer

Generates structured product and technical documents through guided
discovery. 5 document types, each with its own workflow depth.

## Quick start

```text
trigger --> detect type --> load reference --> discovery --> drafting
```

Detect document type from the trigger. If ambiguous, ask the user.

| Type | Reference |
|------|-----------|
| PRD — product requirements | [prd.md](references/prd.md) |
| Design Doc — multi-decision trade-off discussion | [design.md](references/design.md) |
| ADR — single accepted decision record | [adr.md](references/adr.md) |
| TDD — prescriptive technical plan | [tdd.md](references/tdd.md) |

Auto-loaded (no direct triggers):

- `discovery.md` — by PRD, Design Doc, ADR, TDD at start of discovery
- `quality.md` — before presenting any draft
- `brief.md` — by `prd.md` during drafting (Brief is generated alongside
  the PRD, never independently)

## Document Boundaries

- **PRD** — product only: problem, users, scope, journeys, rules, metrics.
  No implementation, architecture, tech stack, UI, or API.
- **Brief** — 1-page narrative summary of the PRD. Generated alongside,
  no standalone trigger.
- **Design Doc** — informal multi-decision trade-off discussion. With PRD:
  technical strategy. Without PRD: covers both product and technical.
- **ADR** — single architecture decision (1-2 pages). Numbered, immutable
  once accepted; superseded by new ADRs, never edited. Use when lifting
  decisions from a PRD/Design Doc or recording retrospectively.
- **TDD** — prescriptive technical plan for a component. Auto-sized
  (core/medium/large); sizing controls depth, never skips sections.
  A project can have both a Design Doc and TDDs.

## Guidelines

- Always complete discovery before drafting (for types that require it)
- Review the artifact before presenting (load `quality.md`)
- Present draft for user feedback before saving
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Keep each document within its domain (PRD = product, Design Doc / ADR / TDD = technical)
- One decision per ADR — never bundle multiple decisions into a single record

## Anti-Pattern: Yes-Man Discovery

Discovery is not a formality. When a problem statement is vague,
evidence is thin, scope keeps expanding, or the user jumps to solution
before naming the problem, push back. Ask for evidence, narrow scope,
challenge weak ideas, suggest pivots when the proposed approach is
fragile. Gate advancement on understanding, not on willingness to move
on.

## Anti-Pattern: ADR as Design Doc

ADR records *one* decision after it's been made — context, decision,
consequences, alternatives. Design Doc *explores* multiple decisions
and trade-offs before they're settled. Writing a long ADR that weighs
several open options is a Design Doc in disguise; writing a Design Doc
that captures a single accepted choice is an ADR padded with prose. If
the decision is still in motion, write a Design Doc. Once accepted,
extract each decision into its own ADR and link back from the Design
Doc's References section.

## Anti-Pattern: Vague Requirements

"Search should be fast", "easy to use", "intuitive interface" are not
requirements — they're aspirations. Requirements must be measurable:
"Search returns results within 200ms", "new users complete onboarding
in under 2 minutes", "task completion rate above 90% without help text".
If a requirement can't be measured, it can't be verified.
