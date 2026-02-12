---
name: {{tdd-name}}
status: draft
author: {{author}}
created: {{YYYY-MM-DD}}
last_updated: {{YYYY-MM-DD}}
prd_reference: {{link to PRD, or "None"}}
reviewers: {{reviewers}}
---

# TDD: {{Title}}

## 1. Overview

{{Brief summary of what is being built and why. 2-3 sentences max.}}

## 2. Context & Background

{{What existing system or situation motivates this design? Include relevant history.}}

## 3. Goals

- {{Technical goal this design achieves}}
- {{Another measurable objective}}

### Non-Goals

- {{What this design explicitly does not address}}

## 4. Architecture

### High-Level Design

```mermaid
{{flowchart or graph showing the system architecture at a high level}}
```

### Component Diagram

```mermaid
{{flowchart showing components and their relationships}}
```

### Components

| Component | Responsibility |
|-----------|---------------|
| {{name}} | {{what it does and why it exists}} |
| {{name}} | {{what it does and why it exists}} |

### Data Flow

```mermaid
{{sequenceDiagram or flowchart showing how data moves through the system}}
```

## 5. Technical Design

### Data Model

```typescript
// {{Describe key types, interfaces, or schemas}}
interface Example {
  id: string;
  name: string;
  createdAt: Date;
}
```

### API Design

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| {{GET/POST/etc}} | {{/api/resource}} | {{what it does}} | {{request shape or "-"}} | {{response shape}} |

### State Management

{{Describe how state is managed -- React state, context, stores, URL params, etc.}}

### Key Algorithms / Logic

{{Describe any non-trivial logic, business rules, or algorithms that need special attention}}

## 6. Tech Stack & Dependencies

| Category | Choice | Justification |
|----------|--------|---------------|
| {{e.g., Framework}} | {{e.g., Next.js 15}} | {{why this choice}} |
| {{e.g., Database}} | {{e.g., PostgreSQL}} | {{why this choice}} |
| {{e.g., New Dependency}} | {{package name}} | {{why needed}} |

## 7. Error Handling

| Scenario | Handling Strategy | User Impact |
|----------|------------------|-------------|
| {{what can go wrong}} | {{how the system responds}} | {{what the user sees}} |
| {{another failure mode}} | {{recovery strategy}} | {{degraded experience description}} |

## 8. Performance Considerations

- {{Performance concern and mitigation strategy, e.g., lazy loading for large lists}}
- {{Caching approach, e.g., stale-while-revalidate for API responses}}
- {{Bundle size impact, e.g., tree-shaking strategy for new dependency}}

## 9. Security Considerations

- {{Security concern and how it is addressed, e.g., input validation on all user-facing endpoints}}
- {{Auth/authz approach, e.g., role-based access control for admin features}}

## 10. Testing Strategy

| Type | Coverage | Tools |
|------|----------|-------|
| Unit | {{what is covered}} | {{e.g., Vitest}} |
| Integration | {{what is covered}} | {{e.g., Testing Library}} |
| E2E | {{what is covered}} | {{e.g., Playwright}} |

## 11. Migration / Rollout Plan

1. {{First step to ship this change safely}}
2. {{Next step in the rollout}}
3. {{Final step to complete the migration}}

### Feature Flags

| Flag | Purpose | Default |
|------|---------|---------|
| {{flag_name}} | {{what it gates}} | `false` |

### Rollback Strategy

{{How to revert if something goes wrong. What signals trigger a rollback?}}

## 12. Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| {{approach considered}} | {{advantages}} | {{disadvantages}} | {{reason it was not chosen}} |
| {{another approach}} | {{advantages}} | {{disadvantages}} | {{reason it was not chosen}} |

## 13. Open Questions

- [ ] {{Question requiring further investigation before or during implementation}}
- [ ] {{Decision that can be deferred to implementation phase}}

## 14. References

- {{Link to relevant documentation, prior art, or inspiration}}
- {{Link to related ADRs or RFCs}}
