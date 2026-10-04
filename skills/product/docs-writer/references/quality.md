# Quality Standards

Quality checks for requirements and document integrity before writing any document to disk.

## When to Use

Load during the Drafting phase, before writing any document to disk, and again after writing it.

## Requirements Quality

Requirements must be concrete and measurable across all document types.

| Bad | Good |
|-----|------|
| "Search should be fast" | "Search returns results within 200ms" |
| "Easy to use" | "New users complete onboarding in under 2 minutes" |
| "Intuitive interface" | "Task completion rate above 90% without help text" |

## Declare, Don't Narrate

What produced a document is not what the document says. The conversation is input; the document states standing facts in present tense.

A resolved decision enters as fact (`Reset links expire in 15 minutes`), never as its history (`we discussed 24 hours but the user preferred 15 minutes`). Strip conversation narrative — "as discussed", "the user confirmed", "we agreed", "you chose" — and decision history. An updated document states the new state, never the change. An ADR Decision keeps its "We will..." form.

A section that keeps alternatives — Alternatives Considered, a Rejected column, the alternatives in an ADR Context — records each rejected option and why it fails, never the exchange that rejected it.

## Review Checklist

Before writing any document to disk, verify:

- [ ] No contradictions: read each statement that excludes or limits (an Out item, a Non-Goal, a Business Rule) against each statement that requires (a Goal, an In item, a Journey step, an Edge Case). A pair that cannot both hold is a contradiction — resolve it with the user.
- [ ] No unresolved TBDs that block the document's purpose
- [ ] Scope is focused (one document, one purpose)
- [ ] Cross-references to other docs are valid
- [ ] Requirements are concrete and measurable (no vague adjectives)
- [ ] The document declares and does not narrate, per `## Declare, Don't Narrate`

**If any check fails, fix the document, run that check again, and write only after it passes.** Apply all checks to both new and updated documents.

Mark an unknown as TBD rather than inventing a constraint to fill the slot.

## Writing and Reporting

Write the document to its path directly, and reread it per `## Reread`. Then report the path, what the document holds in one to three sentences — what changed, on an update — and any open question or TBD it carries. Never paste the document.

## Reread

After writing, read the written file whole and run the Review Checklist and the gates for its type over it. When a check finds a contradiction or a gap the document cannot settle on its own, interview the user about it, one question at a time, and fix the file from the answer. Read the file again until every check passes; report only after that.

## ADR-Specific Gates

When the document is an ADR, additionally verify:

- [ ] Exactly one decision is recorded (not bundled with others)
- [ ] Decision stated as a positive imperative ("We will...")
- [ ] Context is value-neutral (states forces, does not advocate)
- [ ] Consequences capture the material outcomes of the decision
- [ ] Frontmatter contains `name`, `status`, `date`, `updated`, and `sources`
- [ ] References follow the document reference pattern
- [ ] Numbering is sequential and zero-padded (no gaps, no duplicates)
- [ ] When superseding, the prior ADR's `status` names its replacement

## Document Boundaries

Apply these boundaries to the PRD and Design Doc. Keep each subject in its owning document and link to it from related documents.

**When the document is a PRD, verify:**

- [ ] No architecture, tech stack, framework choices, or deployment topology — those belong to the Design Doc
- [ ] No API contracts, endpoint paths, request/response shapes, or database schema details
- [ ] No UI component names, library references, or styling instructions
- [ ] Journeys describe actor goals and product behavior, not implementation steps ("user submits the form" not "POST /orders with payload X")
- [ ] NFRs state measurable targets without prescribing the mechanism ("p95 latency under 200ms" not "use Redis caching")
- [ ] Executive Summary is a requirements digest (problem, scope, metric) — no positioning (What/Why/Who, personality, anti-references), which lives in PRODUCT

**When the document is a Design Doc, verify:**

- [ ] Sections 1-2 carry no copy-paste from PRD — Context recaps in 1-2 paragraphs and links to PRD; does not duplicate Problem Statement, Personas, or Journeys
- [ ] Section 2 Goals are technical (p99 latency, throughput, SLAs, zero-downtime, isolation guarantees) — not product (DAU, conversion, NPS, retention)
- [ ] Business rules referenced from PRD via link, not restated
- [ ] No product framing prose ("users will love...", "this drives engagement...") in any section

## Design Doc-Specific Gates

When the document is a Design Doc, additionally verify:

- [ ] Every significant decision in Alternatives Considered carries its chosen / rejected / reasoning — the doc reasons, it does not just prescribe
- [ ] Alternatives Considered Record column populated where an ADR exists
- [ ] Context recaps in 1-2 paragraphs and links the PRD — no restated Problem Statement, Personas, or Journeys
- [ ] Cross-cutting concerns appear only where they shape the design — no exhaustive coverage of axes with no decision behind them
