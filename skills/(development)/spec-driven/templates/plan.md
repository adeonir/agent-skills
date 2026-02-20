---
id: {{ID}}
feature: {{name}}
created: {{YYYY-MM-DD}}
---

# Technical Plan: {{Feature}}

## Scope

{{What is in scope and out of scope for this feature}}

## Research Summary

{{#if research}}
> From .artifacts/research/{{topic}}.md

- {{key finding 1}}
- {{key finding 2}}
{{/if}}

## Critical Files

### Reference Files

| File | Purpose |
|------|---------|
| {{path}} | {{why relevant}} |

### Files to Modify

| File | Reason |
|------|--------|
| {{path}} | {{what changes}} |

### Files to Create

| File | Purpose |
|------|---------|
| {{path}} | {{responsibility}} |

## Codebase Patterns

| Pattern | Project Uses | Avoid | Reference |
|---------|-------------|-------|-----------|
| Naming | {{convention}} | {{anti-pattern}} | {{file:line}} |
| Error handling | {{approach}} | {{anti-pattern}} | {{file:line}} |
| API calls | {{pattern}} | {{anti-pattern}} | {{file:line}} |

## Data Model

### Entities

| Entity | Key Attributes | Purpose |
|--------|---------------|---------|
| {{name}} | {{attributes}} | {{role in feature}} |

### Relationships

{{Describe entity relationships. Use a mermaid erDiagram when relationships are non-trivial.}}

### API Contracts

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| {{path}} | {{verb}} | {{shape}} | {{shape}} |

## Architecture Decision

{{chosen approach with rationale - be decisive, pick ONE approach}}

## Component Design

| Component | File | Responsibility |
|-----------|------|----------------|
| {{name}} | {{path}} | {{what}} |

## Data Flow

{{Use a mermaid sequenceDiagram or flowchart when the flow involves 3+ steps or multiple actors.}}

1. {{Entry point}}
2. {{Transform}}
3. {{Output}}

## Requirements Traceability

| Requirement | Component | File | Status |
|-------------|-----------|------|--------|
| FR-001 | {{comp}} | {{path}} | Planned |
| FR-002 | {{comp}} | {{path}} | Planned |

## Test Strategy

### Infrastructure

| Aspect | Detail |
|--------|--------|
| Framework | {{jest/vitest/etc}} |
| Command | {{npm test/etc}} |
| Location | {{test directory pattern}} |

### Reference Tests

| File | What It Tests |
|------|---------------|
| {{existing test}} | {{pattern to follow}} |

### New Tests

| Component | Test File | Scenarios |
|-----------|-----------|-----------|
| {{comp}} | {{path}} | {{what to test}} |

## Considerations

### Error Handling

- {{approach matching project patterns}}

### Security

- {{concerns if applicable}}

## Decisions

| Decision | Rationale |
|----------|-----------|
| {{decision}} | {{rationale}} |

## Open Questions

- [ ] {{question}}
