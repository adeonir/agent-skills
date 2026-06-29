# Quality Standards

Quality gates for requirements and document integrity before presenting
any draft to the user.

## When to Use

Load during the Drafting phase, before presenting any document to the user.

## Requirements Quality

Requirements must be concrete and measurable across all document types.

| Bad | Good |
|-----|------|
| "Search should be fast" | "Search returns results within 200ms" |
| "Easy to use" | "New users complete onboarding in under 2 minutes" |
| "Intuitive interface" | "Task completion rate above 90% without help text" |

## Review Checklist

Before presenting any document to the user, verify:

- [ ] No contradictions between sections
- [ ] No unresolved TBDs that block the document's purpose
- [ ] Scope is focused (one document, one purpose)
- [ ] Cross-references to other docs are valid
- [ ] Requirements are concrete and measurable (no vague adjectives)

## ADR-Specific Gates

When the document is an ADR, additionally verify:

- [ ] Exactly one decision is recorded (not bundled with others)
- [ ] Decision stated as a positive imperative ("We will...")
- [ ] Context is value-neutral (states forces, does not advocate)
- [ ] Consequences include both positive AND negative outcomes
- [ ] At least one alternative is recorded with a rejection reason
- [ ] Numbering is sequential and zero-padded (no gaps, no duplicates)
- [ ] When superseding, frontmatter `supersedes` and prior ADR's
      `superseded-by` are both populated

## Document Boundaries

Applies to PRD and Design Doc. Each document stays in its lane;
cross-doc content links rather than duplicates.

**When the document is a PRD, verify:**

- [ ] No architecture, tech stack, framework choices, or deployment
      topology — those belong to the Design Doc
- [ ] No API contracts, endpoint paths, request/response shapes, or
      database schema details
- [ ] No UI component names, library references, or styling
      directives — those belong to the design artifact
- [ ] Journeys describe actor goals and product behavior, not
      implementation steps ("user submits the form" not "POST
      /orders with payload X")
- [ ] NFRs state measurable targets without prescribing the
      mechanism ("p95 latency under 200ms" not "use Redis caching")
- [ ] Executive Summary is a requirements digest (problem, scope,
      metric) — no positioning (What/Why/Who, personality,
      anti-references), which lives in PRODUCT

**When the document is a Design Doc, verify:**

- [ ] Sections 1-2 carry no copy-paste from PRD — Context recaps in
      1-2 paragraphs and links to PRD; does not duplicate Problem
      Statement, Personas, or Journeys
- [ ] Section 2 Goals are technical (p99 latency, throughput, SLAs,
      zero-downtime, isolation guarantees) — not product (DAU,
      conversion, NPS, retention)
- [ ] Business rules referenced from PRD via link, not restated
- [ ] No product framing prose ("users will love...", "this drives
      engagement...") in any section

## Design Doc-Specific Gates

When the document is a Design Doc, additionally verify:

- [ ] Every significant decision in Alternatives Considered carries its
      chosen / rejected / reasoning — the doc reasons, it does not just
      prescribe
- [ ] Alternatives Considered Record column populated where an ADR exists;
      rows with `ADR-NNNN` are frozen (reversals require a superseding ADR,
      not a row edit)
- [ ] Context recaps in 1-2 paragraphs and links the PRD — no restated
      Problem Statement, Personas, or Journeys
- [ ] Cross-cutting concerns appear only where they shape the design — no
      exhaustive coverage of axes with no decision behind them

If issues found: fix inline before presenting.
