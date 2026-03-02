---
status: draft
date: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
---

# TDD - {{Product Name}}

## 1. Overview

{{What is being built, why it exists, and the problem it solves. Include relevant context and history. 1-2 paragraphs max.}}

## 2. Goals / Non-Goals

### Goals

- **{{Goal name}}:** {{Measurable technical objective}}
- **{{Goal name}}:** {{Measurable technical objective}}

### Non-Goals

- {{What this design explicitly does not address}}
- {{Another explicit exclusion}}

## 3. Tech Stack

### Frontend

| Category | Choice |
|----------|--------|
| {{e.g., Framework}} | {{e.g., Next.js}} |
| {{e.g., Styling}} | {{e.g., Tailwind CSS}} |

### Backend

| Category | Choice |
|----------|--------|
| {{e.g., Framework}} | {{e.g., NestJS}} |
| {{e.g., Database}} | {{e.g., PostgreSQL}} |

### Shared

| Category | Choice |
|----------|--------|
| {{e.g., Validation}} | {{e.g., Zod}} |

## 4. Architecture

### High-Level Design

```mermaid
{{flowchart showing the system architecture at a high level}}
```

### System Context

```mermaid
{{diagram showing the system within existing infrastructure and external services}}
```

### Data Flow

```mermaid
{{sequenceDiagram showing how data moves through the system for key scenarios}}
```

## 5. Security & Compliance

- {{Security concern and how it is addressed}}
- {{Auth/authz approach}}
- {{Data protection strategy}}
- **Compliance:**
  - {{Regulatory requirements and how they are met}}
  - {{Data handling policies}}

## 6. Testing

| Type | Coverage | Tools |
|------|----------|-------|
| {{e.g., Unit}} | {{what is covered}} | {{e.g., Vitest}} |
| {{e.g., E2E}} | {{what is covered}} | {{e.g., Playwright}} |

## 7. Alternatives Considered

| Decision | Choice | Over | Why |
|----------|--------|------|-----|
| {{what was decided}} | {{what was chosen}} | {{what was rejected}} | {{reasoning}} |

## 8. Open Questions

- [ ] {{Question requiring further investigation}}
- [ ] {{Decision that can be deferred}}

## 9. References

- {{Link to relevant documentation or prior art}}
- {{Link to related ADRs, RFCs, or PRDs}}
