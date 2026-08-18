<!--
Design Doc skeleton. Delete every comment and replace every square-bracket slot before writing the file.

ALWAYS use this exact template structure.
-->
---
name: [document-name]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
sources: []
---

# Design Doc: [Project Name]

## 1. Context & Scope

[One or two paragraphs: what is being built, why it matters, and the surrounding system landscape. Keep it succinct — the reader follows the PRD link for product depth.]

> See PRD: `docs/product/PRD.md`

## 2. Goals & Non-Goals

### Goals

- **[Goal name]:** [Measurable technical objective — latency, throughput, isolation guarantee, zero-downtime target, etc.]

### Non-Goals

- [A choice deliberately excluded — for example "ACID compliance" considered and not pursued. Not a negated goal like "shouldn't crash".]

## 3. Design

[Describe the high-level architecture, the surrounding system, the key components and their responsibilities, and the data or interfaces the design depends on. Add Mermaid diagrams when they clarify the design. Include only the detail needed to explain the decisions.]

```mermaid
[System-context or component diagram]
```

## 4. Alternatives Considered & Trade-offs

| Decision | Chosen | Rejected | Reasoning | Record |
|----------|--------|----------|-----------|--------|
| [what was decided] | [what was chosen] | [what was rejected] | [trade-offs, why this choice] | [— or ADR-NNN] |

`—` = the design doc is the only record of this decision. `ADR-NNN` = the decision is formalized as an ADR.

## 5. Cross-cutting Concerns

[Brief prose on the concerns that shape this design — security/privacy, observability, operations, testing. Cover only what affects the design; leave the rest out.]

## 6. Open Questions

- [ ] [Question or uncertainty to resolve before implementation can proceed]

## 7. References

- [Link to PRD]
- [Links to ADRs that record extracted decisions]
- [External documentation, RFCs, prior art]

MUST NOT contain: product KPIs, personas, journey walkthroughs, requirement IDs, or restated PRD prose — recap in 1-2 lines and link the PRD instead.
