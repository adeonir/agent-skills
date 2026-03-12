---
name: docs-writer
description: >-
  Generate structured product and technical documents through guided
  discovery. 9 document types (PRD, Brief, Design Doc, TDD, Pitch, Scope, Bug,
  RFC, ADR). Use when defining products, designing systems, reporting bugs,
  planning tasks, writing stories, proposing changes, recording decisions. Also
  use when the user wants to document a feature idea, write requirements,
  formalize a decision, describe a bug they found, plan technical architecture,
  or needs any structured document for a project. Triggers on "create PRD",
  "create design doc", "design system", "create TDD", "technical design
  document", "technical design", "create pitch", "new feature", "feature
  request", "create scope", "report bug", "fix bug", "create RFC", "create
  ADR", "create document", "write doc", "document this", "need a spec",
  "write requirements".
metadata:
  author: Adeonir Kohl
---

# Docs Writer

Generate structured documents through guided discovery. 9 document types, each with its own workflow depth.

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

| Trigger Pattern | Type | Reference |
|-----------------|------|-----------|
| Create PRD, define product, product requirements, write PRD | PRD | [prd.md](references/prd.md) |
| Create pitch, new feature, feature request | Pitch | [pitch.md](references/pitch.md) |
| Create scope | Scope | [scope.md](references/scope.md) |
| Report bug, fix bug | Bug | [bug.md](references/bug.md) |
| Create RFC, propose change, request for comments | RFC | [rfc.md](references/rfc.md) |
| Create ADR, record decision, architecture decision | ADR | [adr.md](references/adr.md) |
| Create design doc, design system | Design Doc | [design.md](references/design.md) |
| Create TDD, technical design document, technical design | TDD | [tdd.md](references/tdd.md) |
| Create document, write doc | Ask user | -- |

## Cross-References

```
PRD -------------> Design Doc     (PRD feeds requirements, context into Design Doc)
PRD -------------> TDD            (PRD feeds requirements into TDD)
PRD -------------> Pitch          (PRD scope and journeys inform feature pitches)
PRD -------------> design-builder (PRD + Brief inform copy and design extraction)
PRD -------------> spec-driven    (PRD milestones feed spec initialization)
Pitch -----------> Scope          (pitch defines feature, scopes slice the work)
Design Doc ------> ADR            (design decisions generate ADRs)
TDD -------------> ADR            (TDD decisions generate ADRs)
RFC -------------> ADR            (accepted RFC generates ADR)
```

Notes:

- **design-builder**: PRD sections 1, 3-4 (problem, personas, scope) and Brief (value prop, market) inform copy extraction and design extraction
- **spec-driven**: PRD milestones feed feature initialization -- each milestone can generate a spec with its own tasks
- **Design Doc**: When PRD exists, the Design Doc focuses on technical strategy; without PRD, it covers both product context and technical design. Use Design Doc for informal trade-off discussion.
- **TDD**: Prescriptive technical planning for specific components. A project can have both a Design Doc (system-level decisions) and TDDs (component-level technical plans).
- **Pitch -> Scope**: A pitch defines the feature as a whole; scopes are technical slices within it. Scopes have no acceptance criteria -- validation happens at the pitch level.

## Document Types

| Type | Workflow | Reference | Template |
|------|----------|-----------|----------|
| PRD | discovery -> validation -> synthesis -> drafting | [prd.md](references/prd.md) | [prd.md](templates/prd.md) |
| Brief | generated with PRD (no separate trigger) | [brief.md](references/brief.md) | [brief.md](templates/brief.md) |
| Design Doc | discovery -> analysis -> drafting | [design.md](references/design.md) | [design.md](templates/design.md) |
| TDD | discovery -> analysis -> drafting | [tdd.md](references/tdd.md) | [tdd.md](templates/tdd.md) |
| Pitch | [clarification] -> drafting | [pitch.md](references/pitch.md) | [pitch.md](templates/pitch.md) |
| Scope | direct drafting | [scope.md](references/scope.md) | [scope.md](templates/scope.md) |
| Bug | structured collection -> drafting | [bug.md](references/bug.md) | [bug.md](templates/bug.md) |
| RFC | [clarification] -> analysis -> drafting | [rfc.md](references/rfc.md) | [rfc.md](templates/rfc.md) |
| ADR | [clarification] -> drafting | [adr.md](references/adr.md) | [adr.md](templates/adr.md) |

## Shared Discovery Patterns

**LOAD:** [discovery.md](references/discovery.md) before starting any type that requires discovery.

Discovery applies to: PRD, Design Doc, TDD.
Clarification (lightweight, only when input is incomplete) applies to: RFC, ADR, Pitch.
Neither applies to: Scope, Bug (uses structured collection instead), Brief (generated as part of PRD workflow).

## Quality Standards

Requirements must be concrete and measurable across all document types.

| Bad | Good |
|-----|------|
| "Search should be fast" | "Search returns results within 200ms" |
| "Easy to use" | "New users complete onboarding in under 2 minutes" |
| "Intuitive interface" | "Task completion rate above 90% without help text" |

## Guidelines

**DO:**
- Always complete discovery before drafting (for types that require it)
- Present draft for user feedback before saving
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Use fixed filenames per type (ADR and RFC keep `{number}-{name}` suffix in kebab-case)

**DON'T:**
- Skip discovery for types that require it
- Assume document type -- detect from trigger or ask
- Include visual/design direction (that belongs in design-builder)
- Use vague adjectives as requirements ("fast", "easy", "intuitive")
- Mix document types in a single file

## Output

All documents save to `.artifacts/docs/`. Create the directory if it doesn't exist.

| Type | Filename |
|------|----------|
| PRD | `prd.md` |
| Brief | `brief.md` |
| Design Doc | `design.md` |
| TDD | `tdd.md` |
| Pitch | `pitch.md` |
| Scope | `scope.md` |
| Bug | `bug.md` |
| RFC | `rfc/{number}-{name}.md` |
| ADR | `adr/{number}-{name}.md` |

For ADR and RFC, use kebab-case for `{name}` and auto-detect the next sequential number from existing files in the respective subdirectory.

## Error Handling

- No `.artifacts/docs/`: Create the directory
- Ambiguous trigger: Ask user which document type
- Missing context for discovery: Ask questions, never assume
- ADR/RFC numbering conflict: Scan existing files in subdirectory and use next available number
