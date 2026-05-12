---
name: docs-writer
description: >-
  Generates structured product and technical documents through guided
  discovery. 4 document types: PRD, Brief (1-page summary generated
  alongside PRD), Design Doc (informal trade-off discussion), TDD
  (prescriptive technical plan, sized core/medium/large). Use when
  defining products, designing systems, or when a structured document is
  needed for a project. Triggers: "create PRD", "create design doc",
  "create TDD", "technical design document", "create document", "write
  doc", "document this", "write requirements". Not for feature spec
  tied to implementation or meeting/session notes.
---

# Docs Writer

Generates structured documents through guided discovery. 4 document
types, each with its own workflow depth.

## Workflow

```
trigger --> detect type --> load reference --> discovery --> drafting
```

Detect document type from the trigger. If ambiguous, ask the user which
type they want.

## Triggers

- **PRD** ("create PRD", "define product", "product requirements",
  "write PRD") → [prd.md](references/prd.md)
- **Design Doc** ("create design doc", "design system") →
  [design.md](references/design.md)
- **TDD** ("create TDD", "technical design document",
  "technical design") → [tdd.md](references/tdd.md)
- **Generic doc** ("create document", "write doc") → ask user which type

`discovery.md`, `quality.md`, and `brief.md` are not direct triggers:

- `discovery.md` is loaded automatically by PRD, Design Doc, and TDD
  workflows at the start of the discovery phase
- `quality.md` is loaded automatically before presenting a document draft
- `brief.md` is loaded by `prd.md` during the drafting phase (the Brief
  is generated alongside the PRD, never independently)

## Document Boundaries

- **PRD**: product requirements only — problem, users, scope, journeys,
  business rules, success metrics. Never includes implementation,
  architecture, tech stack, UI components, or API specs.
- **Brief**: 1-page executive summary of the PRD. Generated automatically
  during PRD drafting from data already collected. No standalone trigger.
- **Design Doc**: informal trade-off discussion. When PRD exists, focuses
  on technical strategy; without PRD, covers both product context and
  technical design.
- **TDD**: prescriptive technical planning for specific components.
  Auto-sized (core/medium/large); sizing dimensions depth, never skips
  sections. A project can have both a Design Doc and TDDs.

## Guidelines

- Always complete discovery before drafting (for types that require it)
- Review the artifact before presenting (load `quality.md`)
- Present draft for user feedback before saving
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Keep each document within its domain (PRD = product, Design Doc / TDD = technical)

## Anti-Pattern: Yes-Man Discovery

Discovery is not a formality. When a problem statement is vague,
evidence is thin, scope keeps expanding, or the user jumps to solution
before naming the problem, push back. Ask for evidence, narrow scope,
challenge weak ideas, suggest pivots when the proposed approach is
fragile. Gate advancement on understanding, not on willingness to move
on.

## Anti-Pattern: Mixed Document Types

Including UI components or API specs in a PRD, or product requirements
in a TDD, makes both documents harder to consume and rotate out of date.
Each document has a domain — keep visual direction in design tooling,
technical implementation in Design Doc / TDD, and product requirements
in the PRD. When a section starts to belong elsewhere, link to the
correct document instead of inlining it.

## Anti-Pattern: Vague Requirements

"Search should be fast", "easy to use", "intuitive interface" are not
requirements — they're aspirations. Requirements must be measurable:
"Search returns results within 200ms", "new users complete onboarding
in under 2 minutes", "task completion rate above 90% without help text".
If a requirement can't be measured, it can't be verified.
