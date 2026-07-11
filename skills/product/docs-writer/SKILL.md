---
name: docs-writer
description: >-
  Generates structured product and technical documents through guided
  discovery: PRDs, product positioning docs, Design Docs, and architecture
  decision records. Use when defining product requirements, capturing product
  strategy or positioning, weighing architecture and trade-offs, or recording
  an architecture decision. Not for visual or UI design, feature specs tied to
  implementation, or meeting and session notes.
---

# Docs Writer

Generates structured product and technical documents through guided discovery. 4 document types, each with its own workflow depth.

## Quick start

```text
trigger → detect type → load reference → check disk → drafting
  artifact exists → reconcile (light discovery on the delta)
  artifact absent → full discovery
  ADR → append-only, always a new numbered record (never reconciled)
```

Detect document type from the trigger. If ambiguous, ask the user.

| Type | Reference |
|------|-----------|
| PRD — product requirements | [prd.md](references/prd.md) |
| PRODUCT — strategic positioning and identity | [product.md](references/product.md) |
| Design Doc — lean technical design and trade-offs | [design.md](references/design.md) |
| ADR — single accepted decision record | [adr.md](references/adr.md) |

Auto-loaded (no direct triggers):

- `discovery.md` — by the product-doc flow, Design Doc, ADR at start of discovery
- `quality.md` — before writing any document
- `reconcile.md` — by PRD, PRODUCT, or Design Doc when the artifact already exists on disk. ADR is append-only — a new numbered record each time, never reconciled
- `product.md` — by `prd.md` when resolving PRODUCT (reconcile if `PRODUCT.md` exists, discovery if absent; the PRODUCT row above is the same flow)

## Document Boundaries

- **PRD** — product only: problem, users, scope, journeys, rules, metrics. No implementation, architecture, tech stack, UI, or API.
- **PRODUCT** — strategic positioning and identity: register, audience posture, brand personality, anti-references, design principles. Prose, not requirements. Part of the product-doc pair; resolved by whether `PRODUCT.md` exists — discovery if absent, reconcile if present. The PRD owns what the product does; PRODUCT owns what it is. Keep three zones clean — audience as relationship (not the PRD's job to be done), refused aesthetics (not the PRD's out-of-scope features), and differentiation (not the PRD's problem statement).
- **Design Doc** — lean technical design: the context, the design, and the trade-offs behind it (Google-style). Context recaps the project in 1-2 paragraphs and links to the PRD; never duplicates product prose. Not visual or UI design, and not an exhaustive technical spec.
- **ADR** — single architecture decision (1-2 pages). Numbered, immutable once committed; superseded by new ADRs, not edited in place — reopened to `proposed` only on an explicit, justified user request. Use when lifting decisions from a PRD/Design Doc or recording retrospectively. When extracted from a Design Doc Alternatives row, the design doc row's `Record` column is updated to the ADR ID and the ADR's References link back to the design doc section anchor.

## Guidelines

- Complete discovery when the artifact is absent, or reconcile the delta when it exists — never draft blind
- Run the quality gates before writing (load `quality.md`)
- Write the document to its path directly, then report a brief prose summary in chat (up to 2-3 paragraphs) — the path, type, and what it contains; never paste the full document
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Keep each document within its domain (PRD / PRODUCT = product, Design Doc / ADR = technical)

## Anti-Pattern: Yes-Man Discovery

Discovery is not a formality. When a problem statement is vague, evidence is thin, scope keeps expanding, or the user jumps to solution before naming the problem, push back. Ask for evidence, narrow scope, challenge weak ideas, and flag a fragile direction — reopened upstream for a product doc, weighed in place for a Design Doc, never rubber-stamped. Gate advancement on understanding, not on willingness to move on. The same posture governs reconcile: a change to an existing doc earns the same scrutiny as a fresh idea, scoped to the delta — question the rationale, resist silent scope creep, never overwrite an evidenced decision without cause.

## Anti-Pattern: ADR as Design Doc

ADR records *one* decision after it's been made — context, decision, consequences, alternatives. The design doc carries the design and the trade-offs behind it. Writing a long ADR that weighs several open options is a design doc in disguise; writing a design doc that captures a single accepted choice is an ADR padded with prose. If the decision is still in motion, leave it in the design doc's Alternatives Considered table with `Record = —`. Once recorded, extract it into an ADR, update the design doc row's `Record` column to `ADR-NNN`, and link the ADR's References back to the design doc's Alternatives Considered section.

## Anti-Pattern: Vague Requirements

"Search should be fast", "easy to use", "intuitive interface" are not requirements — they're aspirations. Requirements must be measurable: "Search returns results within 200ms", "new users complete onboarding in under 2 minutes", "task completion rate above 90% without help text". If a requirement can't be measured, it can't be verified.

## Anti-Pattern: Technical Detail in PRD

A PRD describes the product: problem, users, scope, journeys, business rules, success metrics. It does not specify architecture, tech stack, APIs, UI components, or any "how it is built" detail. Discussions of microservices vs monolith, SQL vs NoSQL, REST vs GraphQL, framework choice, or deployment topology belong in the Design Doc. If a PRD section reads like it could be implemented in two ways and the reviewer is asked to choose, that section is a technical decision in disguise — extract it to the Design Doc or ADR and leave a link in its place.
