---
name: {{document-name}}
size: {{core|medium|large}}
created: {{YYYY-MM-DD}}
---

# TDD: {{Component Name}}

<!-- Core sections (always included) -->

## 1. Overview

{{What is being built and why. Brief description of the component/service, its purpose, and the problem it solves.}}

---

## 2. Goals / Non-Goals

### Goals

- **{{Goal name}}:** {{Measurable objective this component must achieve}}
- **{{Goal name}}:** {{Measurable objective this component must achieve}}

### Non-Goals

- {{Explicit exclusion -- something that could reasonably be a goal but is deliberately not}}

---

## 3. Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| {{Language}} | {{e.g. TypeScript 5.x}} | {{Primary language}} |
| {{Framework}} | {{e.g. Next.js 14}} | {{Web framework}} |
| {{Database}} | {{e.g. PostgreSQL 16}} | {{Primary data store}} |
| {{Infrastructure}} | {{e.g. AWS ECS}} | {{Container orchestration}} |
| {{Other}} | {{e.g. Redis 7}} | {{Caching layer}} |

---

## 4. Architecture

### High-Level Design

```mermaid
{{Component diagram showing internal modules and their relationships}}
```

### System Context

```mermaid
{{System-context diagram showing this component within the broader system landscape}}
```

### Component Interactions

{{How internal modules interact, key flows, request/response patterns.}}

---

## 5. Testing

| Type | Scope | Tools | Coverage Target |
|------|-------|-------|-----------------|
| {{Unit}} | {{Business logic, utilities}} | {{e.g. Vitest}} | {{e.g. 80%}} |
| {{Integration}} | {{API endpoints, DB queries}} | {{e.g. Vitest + Testcontainers}} | {{e.g. key paths}} |
| {{E2E}} | {{Critical user flows}} | {{e.g. Playwright}} | {{e.g. happy paths}} |

---

## 6. Monitoring & Observability

### Metrics

- {{Key metric and what it measures}}
- {{Key metric and what it measures}}

### Logging

- {{Logging strategy, structured logging format, log levels}}

### Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| {{Alert name}} | {{Trigger condition}} | {{critical/warning/info}} |

---

## 7. References

- {{Link to PRD, if exists}}
- {{Link to Design Doc, if exists}}
- {{Link to relevant ADRs}}
- {{Link to external documentation}}

---

<!-- Medium sections (include for medium and large projects) -->

## 8. Scope

### In Scope

- {{Feature or responsibility this TDD covers}}
- {{Feature or responsibility this TDD covers}}

### Out of Scope

- {{What is explicitly excluded and why}}
- {{What is explicitly excluded and why}}

---

## 9. Data Model

### Schema

```mermaid
erDiagram
    {{Entity relationships and key fields}}
```

### Storage

- **Engine:** {{e.g. PostgreSQL 16}}
- **Access patterns:** {{Read-heavy, write-heavy, mixed}}
- **Retention:** {{Data lifecycle and retention policy}}

---

## 10. APIs / Interfaces

### Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| {{GET}} | {{/api/resource}} | {{List resources}} | {{required}} |
| {{POST}} | {{/api/resource}} | {{Create resource}} | {{required}} |

### Contracts

{{Key request/response shapes, error formats, pagination strategy.}}

---

## 11. Security & Compliance

### Authentication & Authorization

- {{Auth mechanism (e.g. JWT, OAuth2, API keys)}}
- {{Authorization model (e.g. RBAC, ABAC)}}

### Data Protection

- {{Encryption at rest and in transit}}
- {{PII handling and data classification}}

### Regulatory

- {{Applicable regulations (LGPD, GDPR, HIPAA, PCI-DSS)}}
- {{How compliance is achieved}}

---

## 12. Alternatives Considered

| Decision | Chosen | Rejected | Reasoning |
|----------|--------|----------|-----------|
| {{what was decided}} | {{what was chosen}} | {{what was rejected}} | {{why this choice}} |
| {{what was decided}} | {{what was chosen}} | {{what was rejected}} | {{why this choice}} |

---

<!-- Large sections (include for large projects only) -->

## 13. Deployment & Rollback

### CI/CD

- {{Pipeline description and stages}}
- {{Build and artifact strategy}}

### Release Strategy

- {{Phased rollout, canary, blue-green, or big-bang}}
- {{Feature flags if applicable}}

### Rollback Plan

- {{How to roll back if deployment fails}}
- {{Database migration rollback strategy}}
- {{Rollback triggers (what conditions trigger rollback)}}

---

## 14. Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| {{Risk description}} | {{high/medium/low}} | {{high/medium/low}} | {{Mitigation strategy}} |
| {{Risk description}} | {{high/medium/low}} | {{high/medium/low}} | {{Mitigation strategy}} |

---

## 15. Open Questions

- [ ] {{Question or uncertainty that needs resolution}}
- [ ] {{Question or uncertainty that needs resolution}}
- [ ] {{Decision pending input from another team or stakeholder}}
