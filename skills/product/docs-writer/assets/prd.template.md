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

## 1. Problem

[The pain, who is affected, the evidence behind it (or an explicit hypothesis), and why it is worth solving now.]

## 2. Audience

- **[User profile]:** [context and main use cases]

## 3. Goals & Metrics

| Goal | Metric | Target |
|------|--------|--------|
| [goal] | [how it will be measured] | [a number the user supplied, the target in words, or TBD] |

Primary metric: [the one metric that defines success].

## 4. Scope

### Must Have

- FR-1 [core capability required for launch]

### Should Have

- FR-2 [important but not launch-blocking]

### Could Have

- FR-3 [nice-to-have for a later iteration]

### Won't Have

- FR-4 [capability considered and cut] — [why it is out now]

### Out of Scope

- [An outcome this product deliberately does not pursue.]

## 5. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NFR-1 | [quality the product needs: performance, security, accessibility, privacy] | [the requirement in words, or a number the user supplied] |

## 6. Phases

| Phase | Delivery | Criterion to advance |
|-------|----------|----------------------|
| MVP | [what ships first] | [what must hold before the next phase] |
| [Next phase] | [what follows] | [criterion] |

## 7. Assumptions & Risks

- **Assumption:** [what is taken as true; if wrong, the plan changes]
- **Risk:** [what could invalidate the project] — [mitigation]

## 8. Open Questions

- [ ] [Question with no safe default]

## 9. References

- [Typed reference to a related document that exists, such as the Design Doc, an ADR, or research.]

MUST NOT contain: architecture, tech stack, framework or deployment choices, API contracts, database schema, or UI components — those belong to the Design Doc or ADR; nor strategic positioning (brand personality, anti-references) — that lives in PRODUCT; nor conversation narrative ("as discussed", "we agreed", "the user confirmed").
