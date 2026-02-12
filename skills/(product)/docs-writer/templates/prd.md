---
name: {{project-name}}
status: draft
created: {{YYYY-MM-DD}}
last_updated: {{YYYY-MM-DD}}
author: {{author}}
stakeholders: {{stakeholders}}
---

# PRD: {{Title}}

## 1. Problem Statement

{{Describe the problem being solved. What pain point exists? Who is affected?}}

## 2. Goals & Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| {{goal}} | {{how it will be measured}} | {{concrete number or threshold}} |

### Non-Goals

- {{What is explicitly out of scope and why}}

## 3. Value Proposition

**Headline:**
{{Main benefit in 1 line}}

**Subheadline:**
{{Supporting text explaining the value}}

**Key Benefits:**
- {{Benefit 1}}
- {{Benefit 2}}
- {{Benefit 3}}

## 4. User Personas

### {{Persona Name}}

- **Role:** {{role or job title}}
- **Pain Point:** {{primary frustration or problem}}
- **Goal:** {{what they want to achieve with this product}}

## 5. User Stories

| ID | As a... | I want to... | So that... | Priority |
|----|---------|--------------|------------|----------|
| US-001 | {{persona}} | {{action}} | {{benefit}} | Must Have |
| US-002 | {{persona}} | {{action}} | {{benefit}} | Should Have |

## 6. Requirements

### Functional Requirements

| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| FR-001 | {{what the system must do}} | Must Have | |
| FR-002 | {{another capability}} | Should Have | |

### Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NFR-001 | Performance | {{e.g., page load < 2s}} |
| NFR-002 | Accessibility | {{e.g., WCAG 2.1 AA}} |

## 7. Technical Specifications

### Architecture Overview

{{High-level system design}}

### Integration Points

| System | Purpose | Details |
|--------|---------|---------|
| {{API/DB/Service}} | {{what it does}} | {{endpoint/format}} |

### Security & Privacy

- {{Security requirement}}
- {{Privacy constraint}}

## 8. Milestones

| Milestone | Features | Target Date | Status |
|-----------|----------|-------------|--------|
| {{milestone_1}} | {{key features included}} | {{YYYY-MM-DD}} | Not Started |
| {{milestone_2}} | {{key features included}} | {{YYYY-MM-DD}} | Not Started |

## 9. Risks & Assumptions

### Assumptions

- {{Assumption that, if wrong, would change the plan}}

### Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| {{what could go wrong}} | High | Medium | {{how to address}} |

### Unknowns

- [ ] TBD: {{Question that needs answering before implementation}}
- [ ] TBD: {{Another open item requiring investigation}}

## 10. References

- {{Link to designs, research, prior art, or related documents}}
