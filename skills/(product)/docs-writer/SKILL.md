---
name: docs-writer
description: >-
  Generate structured product and technical documents through guided
  discovery. 4 document types (PRD, Brief, Design Doc, TDD).
  Use when defining products, designing systems, or when the user needs
  any structured document for a project.
when_to_use: >-
  Triggers on "create PRD", "create design doc", "create TDD",
  "technical design document", "create document", "write doc",
  "document this", "write requirements".
  Not for feature spec.md tied to implementation (use spec-driven),
  system architecture discovery (use system-design), or meeting/session
  notes in Obsidian (use session-notes).
effort: high
---

# Docs Writer

**Recommended effort:** high for PRD, Design Doc, and TDD (multi-phase discovery).

Generate structured documents through guided discovery. 4 document types, each
with its own workflow depth. Use ultrathink for PRD validation and Design Doc
trade-off analysis.

## Workflow

```
trigger --> detect type --> load reference --> discovery --> drafting
```

Detect document type from the trigger. If ambiguous, ask the user which type they want.

## Context Loading Strategy

Load the reference and template matching the detected document type. For types that require discovery, also load [discovery.md](references/discovery.md).

**Never simultaneous:**

- Multiple document type references
- Templates for different document types

## Triggers

| Trigger Pattern                                             | Type       | Reference                         |
| ----------------------------------------------------------- | ---------- | --------------------------------- |
| Create PRD, define product, product requirements, write PRD | PRD        | [prd.md](references/prd.md)       |
| Create design doc, design system                            | Design Doc | [design.md](references/design.md) |
| Create TDD, technical design document, technical design     | TDD        | [tdd.md](references/tdd.md)       |
| Create document, write doc                                  | Ask user   | --                                |

## Cross-References

```
PRD -------------> Design Doc     (PRD feeds requirements, context into Design Doc)
PRD -------------> TDD            (PRD feeds requirements into TDD)
PRD -------------> epic-tracker   (PRD milestones and FRs inform epic definition)
PRD -------------> design-builder (PRD + Brief inform copy and design extraction)
PRD -------------> spec-driven    (PRD milestones feed spec initialization)
```

Notes:

- **PRD**: Product requirements only -- problem, users, scope, journeys, business rules, success metrics. Never includes implementation, architecture, tech stack, UI components, or API specs. Those belong to Design Doc, TDD, or design-builder.
- **Brief**: 1-page executive summary of the PRD. Generated automatically during PRD drafting from data already collected; never has its own trigger or discovery phase.
- **Design Doc**: When PRD exists, the Design Doc focuses on technical strategy; without PRD, it covers both product context and technical design. Use Design Doc for informal trade-off discussion.
- **TDD**: Prescriptive technical planning for specific components. A project can have both a Design Doc (system-level decisions) and TDDs (component-level technical plans).
- **epic-tracker**: PRD milestones and functional requirements feed epic planning -- epics, stories, and bugs are managed by epic-tracker
- **design-builder**: PRD sections 1, 3-4 (problem, personas, scope) and Brief (value prop, market) inform copy extraction and design extraction
- **spec-driven**: PRD milestones feed feature initialization -- each milestone can generate a spec with its own tasks

## Document Types

| Type       | Workflow                                         | Reference                         | Template                         |
| ---------- | ------------------------------------------------ | --------------------------------- | -------------------------------- |
| PRD        | discovery -> validation -> synthesis -> drafting | [prd.md](references/prd.md)       | [prd.md](templates/prd.md)       |
| Brief      | generated with PRD (no separate trigger)         | [brief.md](references/brief.md)   | [brief.md](templates/brief.md)   |
| Design Doc | discovery -> analysis -> drafting                | [design.md](references/design.md) | [design.md](templates/design.md) |
| TDD        | discovery -> analysis -> drafting                | [tdd.md](references/tdd.md)       | [tdd.md](templates/tdd.md)       |

## Shared Discovery Patterns

**LOAD:** [discovery.md](references/discovery.md) before starting any type that requires discovery.

Discovery applies to: PRD, Design Doc, TDD.
Brief is generated as part of the PRD workflow (no standalone trigger).

## Quality Standards

Requirements must be concrete and measurable across all document types.

| Bad                     | Good                                               |
| ----------------------- | -------------------------------------------------- |
| "Search should be fast" | "Search returns results within 200ms"              |
| "Easy to use"           | "New users complete onboarding in under 2 minutes" |
| "Intuitive interface"   | "Task completion rate above 90% without help text" |

## Guidelines

**DO:**

- Always complete discovery before drafting (for types that require it)
- Review the artifact before presenting to user (see Review Checklist below)
- Present draft for user feedback before saving
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Use fixed filenames per type

**DON'T:**

- Skip discovery for types that require it
- Assume document type -- detect from trigger or ask
- Include visual/design direction (that belongs in design-builder)
- Use vague adjectives as requirements ("fast", "easy", "intuitive")
- Mix document types in a single file

## Review Checklist

Before presenting any document to the user, verify:

- [ ] No contradictions between sections
- [ ] No unresolved TBDs that block the document's purpose
- [ ] Scope is focused (one document, one purpose)
- [ ] Cross-references to other docs are valid
- [ ] Requirements are concrete and measurable (no vague adjectives)

If issues found: fix inline before presenting. Don't deliver a flawed artifact.

## Output

All documents save to `.artifacts/docs/`. Create the directory if it doesn't exist.

| Type       | Filename    |
| ---------- | ----------- |
| PRD        | `prd.md`    |
| Brief      | `brief.md`  |
| Design Doc | `design.md` |
| TDD        | `tdd.md`    |

## Error Handling

- No `.artifacts/docs/`: Create the directory
- Ambiguous trigger: Ask user which document type
- Missing context for discovery: Ask questions, never assume

## Compact Instructions

Preserve:

- Document type being written, current phase (discovery/validation/synthesis/drafting)
- All discovery topic answers collected so far
- Agreed scope, priorities, and open TBDs
- User confirmations received

Drop:

- Raw question-and-answer transcript
- Intermediate analysis scratch work
