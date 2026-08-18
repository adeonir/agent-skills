<!--
PRD skeleton. Delete every comment and replace every square-bracket slot before writing the file.

ALWAYS use this exact template structure.
-->
---
name: [document-name]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
status: draft
sources: []
---

# PRD: [Product Name]

## 1. Executive Summary

[One short paragraph for a quick scan of the spec: the problem, who it is for, the must-have scope, and the primary success metric. Requirements digest only — positioning (what the product is and stands for) lives in PRODUCT, never here.]

## 2. Problem Statement

[Describe the problem being solved. What pain point exists? Who is affected? What evidence supports this?]

## 3. Goals & Non-Goals

| Goal | Metric | Target |
|------|--------|--------|
| [goal] | [how it will be measured] | [concrete number or threshold, or TBD] |

### Non-Goals

- [An outcome this product deliberately does not pursue. Distinct from a cut feature — that goes to Scope → Won't Have.]

## 4. User Personas

### [Persona Name]

- **Role:** [role or job title]
- **Pain Point:** [primary frustration or problem]
- **Goal:** [what they want to achieve with this product]

## 5. User Journeys

### [Journey Name]

**Actor:** [persona]
**Goal:** [what the user is trying to accomplish]

**Pre-conditions:**

- [what must be true before this journey starts]

**Main Flow:**

1. [user action] → [system behavior]
2. [user action] → [system behavior]
3. [user action] → [system behavior]

**Alternative Flows:**

- [step]a. [condition] → [what happens instead]

**Post-conditions:**

- [what is true after the journey completes]

## 6. Scope

### Must Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-1 | [core capability required for launch] | |
| FR-2 | [another core capability] | |

### Should Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-3 | [important but not launch-blocking] | |

### Could Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-4 | [nice-to-have for future iteration] | |

### Won't Have

| ID | Requirement | Reason for exclusion |
|----|------------|----------------------|
| FR-N | [feature considered and cut from this release] | [why it is out of scope now — informs future revisit] |

## 7. Business Rules

| ID | Rule | Scope |
|----|------|-------|
| BR-1 | [functional constraint that applies across features] | [which features/journeys it affects] |
| BR-2 | [another business rule] | [scope] |

## 8. Edge Cases (optional)

[Include only when exception scenarios are material to the product.]

| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-1 | [what goes wrong or what unusual situation occurs] | [how the product should respond] |
| EC-2 | [another exception scenario] | [expected behavior] |

## 9. Non-Functional Requirements

Non-functional requirements state measurable targets without prescribing the mechanism.

| ID | Requirement | Target |
|----|------------|--------|
| NFR-1 | Performance | [for example, page load < 2s] |
| NFR-2 | Accessibility | [applicable WCAG conformance level] |

Examples:
- "Use Redis caching" (prescribes mechanism)
- "Search returns results within 200ms" (states measurable target)

## 10. Definition of Done

[Product-level criteria that tell us this is ready to ship. Independent of any calendar; applies whenever launch happens.]

| Criterion | How verified |
|-----------|--------------|
| [for example, all Must Have requirements implemented and validated] | [test/validation method] |
| [for example, primary success metric meeting target for 7 days] | [measurement source] |
| [for example, no critical or blocker defects open] | [issue tracker state] |

## 11. External Dependencies

[Dependencies outside the product team that can block or shape delivery.]

| ID | Dependency | Impact if blocked | Owner / Status |
|----|-----------|-------------------|----------------|
| DEP-1 | [for example, legal approval on terms of use] | [blocks launch] | [Owner — pending] |

## 12. Risks (optional)

[Include only when there are material risks worth tracking.]

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [what could go wrong] | High | Medium | [how to address] |

## 13. Open Questions & Assumptions

### Assumptions

- [Assumption that, if wrong, would change the plan]

### Open Questions

- [ ] [Hypothesis to validate with data or user research, or unknown to resolve before implementation (mark TBD)]

## 14. References

Durable pointers to related documents. Use typed labels so a fresh session knows where to recover context.

- **PRODUCT:** [link to docs/product/PRODUCT.md or "None"]
- **PRD:** [link to this PRD or upstream PRD]
- **Design Doc:** [link to docs/tech/design-doc.md or "None"]
- **Research:** [link to research, interviews, data — or "None"]
- **ADRs:** [link to relevant ADRs or "None"]

MUST NOT contain: architecture, tech stack, framework or deployment choices, API contracts, database schema, or UI components — those belong to the Design Doc or ADR; nor strategic positioning (brand personality, anti-references) — that lives in PRODUCT.
