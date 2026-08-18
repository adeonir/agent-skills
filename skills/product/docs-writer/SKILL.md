---
name: docs-writer
description: "Generates structured product and technical documents through guided discovery: PRDs, product positioning docs, Design Docs, and architecture decision records. Use when defining product requirements, capturing product strategy or positioning, weighing architecture and trade-offs, or recording an architecture decision. Not for visual or UI design, feature specs tied to implementation, or meeting and session notes."
---

# Docs Writer

## Quick start

```text
trigger → detect type → load reference → check disk → drafting
  document exists → update the requested parts
  document absent → full discovery
  ADR → create a numbered record or update the requested record
```

Detect document type from the trigger. If ambiguous, ask the user.

| Type | Reference |
|------|-----------|
| PRD — product requirements | [prd.md](references/prd.md) |
| PRODUCT — strategic positioning and identity | [product.md](references/product.md) |
| Design Doc — lean technical design and trade-offs | [design.md](references/design.md) |
| ADR — single architecture decision record | [adr.md](references/adr.md) |

Auto-loaded (no direct triggers):

- `discovery.md` — by the product-doc flow, Design Doc, ADR at start of discovery
- `quality.md` — before writing any document
- `reconcile.md` — by PRD, PRODUCT, or Design Doc when updating an existing document
- `product.md` — by `prd.md` when handling PRODUCT; discover it if absent or update it if present

Resolve copyable document templates from the directory containing this `SKILL.md` as `<this-skill>/assets/<document-type>.template.md`. Read only the template selected by the document type.

## Document Boundaries

- **PRD** — product only: problem, users, scope, journeys, rules, metrics. No implementation, architecture, tech stack, UI, or API.
- **PRODUCT** — strategic positioning and identity: register, audience relationship, brand personality, anti-references, and design principles. Write prose, not requirements. If `PRODUCT.md` does not exist, discover its content. If it exists, update only the requested parts. The PRD records what the product does; PRODUCT records what it is. Keep three boundaries clear: audience relationship is not the user's job to be done, refused aesthetics are not excluded features, and differentiation is not the problem statement.
- **Design Doc** — lean technical design: the context, the design, and the trade-offs behind it (Google-style). Context recaps the project in 1-2 paragraphs and links to the PRD; never duplicates product prose. Not visual or UI design, and not an exhaustive technical spec.
- **ADR** — single architecture decision with its status, context, decision, consequences, and references. Use when turning a decision from a PRD or Design Doc into an ADR, recording an earlier decision, or updating an existing ADR. When an ADR records a Design Doc Alternatives row, set that row's `Record` to the ADR ID and link the ADR back to the Design Doc section.

## Guidelines

- Complete discovery for a new document. For an existing document, update only the requested parts. Never write without reading the available context.
- Run the quality checks before writing (load `quality.md`)
- Write the document to its path directly, then report a brief prose summary in chat (up to 2-3 paragraphs) — the path, type, and what it contains; never paste the full document
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Keep each document within its domain (PRD / PRODUCT = product, Design Doc / ADR = technical)

## Anti-Pattern: Uncritical Discovery

Challenge weak claims during discovery. Ask for evidence when the problem is vague or poorly supported. Narrow the work when the scope grows without agreement. If the proposed direction is fragile, ask the user to reconsider it before writing a product document or examine the trade-offs in the Design Doc. Apply the same review to changes in an existing document. Do not replace a supported decision without evidence that its basis has changed.

## Anti-Pattern: ADR as Design Doc

Record one decision in each ADR: status, context, decision, consequences, and references. Keep the full design and its trade-offs in the Design Doc. If several options remain open, keep the decision in the Design Doc with `Record = —`. When the decision is final, create an ADR, set the Design Doc's `Record` to `ADR-NNN`, and link the ADR back to that Design Doc section.

## Anti-Pattern: Vague Requirements

"Search should be fast", "easy to use", "intuitive interface" are not requirements — they're aspirations. Requirements must be measurable: "Search returns results within 200ms", "new users complete onboarding in under 2 minutes", "task completion rate above 90% without help text". If a requirement can't be measured, it can't be verified.

## Anti-Pattern: Technical Detail in PRD

A PRD describes the product: problem, users, scope, journeys, business rules, success metrics. It does not specify architecture, tech stack, APIs, UI components, or any "how it is built" detail. Discussions of microservices vs monolith, SQL vs NoSQL, REST vs GraphQL, framework choice, or deployment topology belong in the Design Doc. If a PRD section reads like it could be implemented in two ways and the reviewer is asked to choose, that section is a technical decision in disguise — extract it to the Design Doc or ADR and leave a link in its place.
