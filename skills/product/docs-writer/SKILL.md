---
name: docs-writer
description: >-
  Generates structured product and technical documents through guided
  discovery. 4 document types: PRD (product requirements), PRODUCT.md
  (strategic positioning and identity, generated alongside the PRD or
  standalone), Design Doc (single project-wide living technical document
  covering strategy through prescriptive plan), ADR (single architecture
  decision record, append-only log). Use when defining product
  requirements, drafting product specs, capturing product positioning,
  authoring the design doc, or writing ADRs. Not for feature spec tied to
  implementation or meeting/session notes.
---

# Docs Writer

Generates structured product and technical documents through guided
discovery. 4 document types, each with its own workflow depth.

## Quick start

```text
trigger → detect type → load reference → discovery → drafting
```

Detect document type from the trigger. If ambiguous, ask the user.

| Type | Reference |
|------|-----------|
| PRD — product requirements | [prd.md](references/prd.md) |
| PRODUCT.md — strategic positioning and identity | [product.md](references/product.md) |
| Design Doc — single project-wide living technical document | [design.md](references/design.md) |
| ADR — single accepted decision record | [adr.md](references/adr.md) |

Auto-loaded (no direct triggers):

- `discovery.md` — by PRD, Design Doc, ADR at start of discovery
- `quality.md` — before presenting any draft
- `product.md` — by `prd.md` during drafting (PRODUCT.md is generated
  alongside the PRD by default; it also has a standalone trigger above)

## Document Boundaries

- **PRD** — product only: problem, users, scope, journeys, rules, metrics.
  No implementation, architecture, tech stack, UI, or API.
- **PRODUCT.md** — strategic positioning and identity: register, audience
  posture, brand personality, anti-references, design principles. Prose,
  not requirements. Generated alongside the PRD by default; also authored
  standalone. The PRD owns what the product does; PRODUCT.md owns what it
  is. Keep three zones clean — audience as relationship (not the PRD's job
  to be done), refused aesthetics (not the PRD's out-of-scope features),
  and differentiation (not the PRD's problem statement).
- **Design Doc** — single project-wide living technical document.
  Covers strategy, trade-offs, and prescriptive plan (domain,
  conventions, architecture, security, observability, testing,
  deployment). Lifecycle tracked via frontmatter `status`: draft →
  accepted → in-progress → shipped → superseded. Context section
  recaps the project in 1-2 paragraphs and links to the PRD; never
  duplicates product prose.
- **ADR** — single architecture decision (1-2 pages). Numbered, immutable
  once accepted; superseded by new ADRs, never edited. Use when lifting
  decisions from a PRD/Design Doc or recording retrospectively. When
  extracted from a Design Doc Alternatives row, the design doc row's
  `Record` column is updated to the ADR ID and the ADR's References
  link back to the design doc section anchor.

## Guidelines

- Always complete discovery before drafting (for types that require it)
- Review the artifact before presenting (load `quality.md`)
- Present draft for user feedback before saving
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Keep each document within its domain (PRD = product, Design Doc / ADR = technical)
- One decision per ADR — never bundle multiple decisions into a single record
- One Design Doc per project — major rewrites spawn `design-doc-v2.md` and supersede the old via frontmatter

## Anti-Pattern: Yes-Man Discovery

Discovery is not a formality. When a problem statement is vague,
evidence is thin, scope keeps expanding, or the user jumps to solution
before naming the problem, push back. Ask for evidence, narrow scope,
challenge weak ideas, suggest pivots when the proposed approach is
fragile. Gate advancement on understanding, not on willingness to move
on.

## Anti-Pattern: ADR as Design Doc

ADR records *one* decision after it's been made — context, decision,
consequences, alternatives. Design Doc carries the living narrative
of trade-offs across the project. Writing a long ADR that weighs
several open options is a Design Doc in disguise; writing a Design
Doc that captures a single accepted choice is an ADR padded with
prose. If the decision is still in motion, leave it in the Design
Doc's Alternatives Considered table with `Record = —`. Once
accepted, extract it into an ADR, update the design doc row's
`Record` column to `ADR-NNNN`, and link the ADR's References back
to the design doc section anchor.

## Anti-Pattern: Vague Requirements

"Search should be fast", "easy to use", "intuitive interface" are not
requirements — they're aspirations. Requirements must be measurable:
"Search returns results within 200ms", "new users complete onboarding
in under 2 minutes", "task completion rate above 90% without help text".
If a requirement can't be measured, it can't be verified.

## Anti-Pattern: Product Prose in Technical Sections

A Design Doc's Context section recaps the project in 1-2 paragraphs
and links to the PRD. It does not restate Problem Statement, list
Personas, or walk through Journeys. Goals translate product NFRs
into technical targets (latency, throughput, isolation); they do
not echo product KPIs (DAU, conversion, NPS). If a reviewer cannot
tell whether they are reading the PRD or the Design Doc, the
Context is too long or the Goals are not technical. Cut and link.

## Anti-Pattern: Technical Detail in PRD

A PRD describes the product: problem, users, scope, journeys,
business rules, success metrics. It does not specify architecture,
tech stack, APIs, UI components, or any "how it is built" detail.
Discussions of microservices vs monolith, SQL vs NoSQL, REST vs
GraphQL, framework choice, or deployment topology belong in the
Design Doc. If a PRD section reads like it could be implemented in
two ways and the reviewer is asked to choose, that section is a
technical decision in disguise — extract it to the Design Doc or
ADR and leave a link in its place.
