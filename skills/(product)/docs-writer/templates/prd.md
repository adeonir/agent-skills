---
name: {{document-name}}
created: {{YYYY-MM-DD}}
---

# PRD

## 1. Problem Statement

{{Describe the problem being solved. What pain point exists? Who is affected? What evidence supports this?}}

## 2. Goals & Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| {{goal}} | {{how it will be measured}} | {{concrete number or threshold}} |

## 3. User Personas

### {{Persona Name}}

- **Role:** {{role or job title}}
- **Pain Point:** {{primary frustration or problem}}
- **Goal:** {{what they want to achieve with this product}}

## 4. Scope Definition

### Must Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-001 | {{core capability required for launch}} | |
| FR-002 | {{another core capability}} | |

### Should Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-003 | {{important but not launch-blocking}} | |

### Could Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-004 | {{nice-to-have for future iteration}} | |

### Won't Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-XXX | {{feature considered and explicitly excluded}} | {{reason for exclusion}} |

### Non-Goals

- {{What is explicitly out of scope and why}}

## 5. User Journeys

### {{Journey Name}}

**Actor:** {{persona}}
**Goal:** {{what the user is trying to accomplish}}

**Pre-conditions:**
- {{what must be true before this journey starts}}

**Main Flow:**
1. {{user action}} → {{system behavior}}
2. {{user action}} → {{system behavior}}
3. {{user action}} → {{system behavior}}

**Alternative Flows:**
- {{step}}a. {{condition}} → {{what happens instead}}

**Post-conditions:**
- {{what is true after the journey completes}}

## 6. Business Rules

| ID | Rule | Scope |
|----|------|-------|
| BR-001 | {{functional constraint that applies across features}} | {{which features/journeys it affects}} |
| BR-002 | {{another business rule}} | {{scope}} |

## 7. Edge Cases

| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-001 | {{what goes wrong or what unusual situation occurs}} | {{how the product should respond}} |
| EC-002 | {{another exception scenario}} | {{expected behavior}} |

## 8. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NFR-001 | Performance | {{e.g., page load < 2s}} |
| NFR-002 | Accessibility | {{e.g., WCAG 2.1 AA}} |

## 9. Milestones

| Milestone | Deliverables |
|-----------|-------------|
| {{milestone_1}} | {{key features and capabilities included}} |
| {{milestone_2}} | {{key features and capabilities included}} |

## 10. Assumptions

- {{Assumption that, if wrong, would change the plan}}

## 11. Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| {{what could go wrong}} | High | Medium | {{how to address}} |

## 12. Hypotheses to Validate

- [ ] {{Hypothesis to be tested and validated with data or user research}}

## 13. Unknowns

- [ ] TBD: {{Question that needs answering before implementation}}

## 14. References

- {{Link to designs, research, prior art, or related documents}}
