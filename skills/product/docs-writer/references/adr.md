# ADR — Architecture Decision Record

Record one architecture decision with its status, context, decision, consequences, and references.

## When to Use

When a meaningful architecture decision has been made or needs an update that future engineers will need to understand: technology choice, integration pattern, data model shape, deprecation, or migration strategy. Keep one decision per ADR.

**Key principle:** ADRs capture the decision and why it was made, not the full exploration that led to it. If multiple decisions are still in play, keep them in the Design Doc until each decision is clear enough to record.

## When NOT to Write an ADR

- The decision is trivial
- Multiple decisions are bundled — split into separate ADRs or step back to a Design Doc
- The decision is still being explored
- The decision is implementation detail, not architecture (variable naming, file layout, formatting)

## Workflow

```text
context → validation → drafting
```

### Phase 1: Context

Load [discovery.md](discovery.md) for the shared interview method and critical review.

**Check Existing Context:**

Apply [discovery.md](discovery.md) `## Reading Project Files`, then read existing ADRs at `docs/adr/`. If the user identifies an existing ADR, read it and scope the requested update before discovery. Otherwise, use existing ADRs to exclude decisions already recorded. After the user selects a candidate, ask whether the new ADR supersedes an existing one.

Scan project documents for decisions that might need their own ADR:

| Source | Where decisions hide |
|--------|---------------------|
| `CODEBASE.md` | `## Decisions` entries not yet recorded as ADRs |
| `docs/tech/design-doc.md` | `## 4. Alternatives Considered & Trade-offs` rows (rows with `Record = —` are candidates for promotion) |
| `docs/product/PRD.md` | Constraints, NFR rationale, research notes |

Read `CODEBASE.md` only when it exists. Treat each entry as a claim to verify against the current codebase and existing ADRs, not as an approved ADR. Keep an entry as a candidate only when it meets **When to Use** and none of **When NOT to Write an ADR**. Report a contradiction instead of recording the entry.

List the unrecorded candidate decisions and ask the user which one this ADR records. Multiple decisions in a single source mean multiple ADRs — one per decision, not one ADR summarizing all of them.

**Discovery (1 topic):**

#### Topic: The Decision

**Opening questions:**

- What is the decision being recorded?
- What forces (technical, business, regulatory, team) made this decision necessary now?
- What alternatives or constraints explain why this response was chosen?
- What becomes easier or more difficult because of this decision?

**Ask follow-up when:**

- Multiple decisions appear → "These look like separate decisions. Should we split them?"
- The reason is unclear → "Which force or constraint made this response appropriate?"
- Consequences omit material costs → "What becomes harder or riskier because of this decision?"
- Decision is vague → "Stated as a positive imperative, what will we do? 'We will X' or 'We will not X'."

**Complete when:**

- One decision is clearly named
- Context forces are documented
- Material consequences are identified

### Phase 2: Validation

Before drafting, confirm that the ADR records exactly one decision, Context explains the forces behind it, Decision states the response, and Consequences names the material outcomes. Resolve missing information in discovery rather than drafting around it.

### Phase 3: Drafting

Use the template below. Follow the document-wide `sources` and References patterns. When the decision came from `CODEBASE.md`, add its path to both. Run the checks in [quality.md](quality.md) before writing, then write the ADR to `docs/adr/NNN-slug.md` and report a brief prose summary in chat (up to 2-3 paragraphs) — the ADR ID and the decision recorded. Do not paste the full document.

For a new ADR, write `Proposed` under Status. For an existing ADR, preserve its status unless the requested change includes a status change, and bump `updated`.

**Numbering:** Scan `docs/adr/` for existing files. Next ADR takes the next ID, zero-padded to three digits (`001`, `002`, ...). Filename and frontmatter `name` use bare ID (`001-slug`); document title heading uses prefix (`ADR-001`).

## ADR Template

ALWAYS use this exact template structure:

````markdown
---
name: [NNN-slug]
date: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
sources: []
---

# ADR-[NNN]: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-NNN]

## Context

[Describe the issue that motivates this decision and the forces that influence or constrain it. Include considered alternatives here when they help explain the response. Keep the language value-neutral.]

## Decision

[State the change that is proposed or agreed. Use active voice and a positive imperative such as "We will adopt X".]

## Consequences

[Describe what becomes easier or more difficult and the risks or constraints introduced by the decision. Include positive, negative, and neutral outcomes when they are material; do not force categories.]

## References

- [Related project documents, ADRs, external documentation, or prior art]
````

MUST NOT contain: more than one decision, still-open trade-offs, implementation planning, or product scope.

## ADR Schema

5 body sections matching the template:

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| Status | Current state of the decision | Existing record or user confirmation |
| Context | Issue and forces that motivate or constrain the decision | Opening and follow-up questions |
| Decision | Proposed or agreed response | Opening and follow-up questions |
| Consequences | Material outcomes, risks, and constraints | Opening and follow-up questions |
| References | Related project documents, ADRs, and external sources | All phases |

## Guidelines

- One decision per ADR — split or step back to a Design Doc if bundled
- State the decision as a positive imperative ("We will...")
- Keep context value-neutral — facts that force the decision, not arguments for the outcome
- Record the material consequences without forcing positive, negative, and neutral subsections
- Number ADRs sequentially, zero-padded to three digits — filename `001-slug.md`, heading `ADR-001`
- Link `ADR-NNN` to the replacement ADR when Status marks a decision as superseded
- When extracted from a Design Doc Alternatives row, the ADR's References section links back to the design doc section anchor; the Design Doc row's `Record` column is updated to this ADR's ID
- Title and slug name the decision with the same words — the slug and the heading Title stay in sync, never divergent terms
- Monitoring criteria, confirmation steps, and follow-up actions belong in the issue tracker, not in the ADR
- External facts (vendor pricing, provider capabilities) are dated and kept verifiable — for example "rates valid as of [Month YYYY]"

## Status Lifecycle

```text
Proposed → Accepted
Accepted → Deprecated | Superseded by ADR-NNN
```

- **Proposed**: Drafted and awaiting review.
- **Accepted**: Approved and in effect.
- **Deprecated**: No longer recommended but not replaced.
- **Superseded by ADR-NNN**: Replaced by the linked ADR.

Update an ADR when its record needs correction or clarification, and bump `updated`. When the decision itself is replaced, create a new ADR and mark the prior ADR as superseded by the replacement.

## Anti-Pattern: Bundled Decisions

An ADR titled "API and Database Decisions" or "Q2 Architecture Choices" bundles unrelated decisions, making each one harder to reference, supersede, or reason about. One decision per ADR. If the draft has multiple "We will..." statements covering distinct concerns, split into separate ADRs.

## Anti-Pattern: Advocacy or Narrative as Context

Context states the forces that make the decision necessary — directly, in the first sentence, value-neutral. It fails when it argues for the chosen outcome or re-introduces the product instead of naming the issue and constraints. State the forces and stop.

## Anti-Pattern: Planning or Scope in the Decision

The Decision states the choice — nothing else. It does not carry rationale, implementation planning ("automated via CI, pipeline TBD"), or product scope (feature lists, tier/plan allocation). Rationale belongs in Context, planning belongs in the tracker or design doc, and product scope belongs in the PRD. If the Decision reads like a build plan or a requirements table, lift that content out and leave only the decision.

## Output

Save to: `docs/adr/<NNN>-<slug>.md`

Create a new numbered ADR for a new decision. Update an existing ADR when the user asks to correct or clarify its record.
