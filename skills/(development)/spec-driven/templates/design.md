---
id: {{ID}}
feature: {{name}}
created: {{YYYY-MM-DD}}
---

# Technical Design: {{Feature}}

## Scope

{{What is in scope and out of scope for this feature}}

## Research Summary

{{#if research}}
> From .artifacts/research/{{topic}}.md

- {{key finding 1}}
- {{key finding 2}}
{{/if}}

## Patterns & Reuse

### Conventions to Follow

| Pattern | Project Uses | Avoid | Reference |
|---------|-------------|-------|-----------|
| Naming | {{convention}} | {{anti-pattern}} | {{file:line}} |
| Error handling | {{approach}} | {{anti-pattern}} | {{file:line}} |
| API calls | {{pattern}} | {{anti-pattern}} | {{file:line}} |

### Existing Code to Reuse

| Component | Location | How to Use |
|-----------|----------|------------|
| {{existing component}} | {{file:line}} | {{extend/import/wrap}} |

## Data Model

### Entities

| Entity | Purpose |
|--------|---------|
| {{name}} | {{role in feature}} |

For each entity, enumerate the members the feature reads or writes:

#### {{Entity}}

- `{{memberName}}` ({{type}}) -- {{path:line}}

### Relationships

{{Describe entity relationships. Use a mermaid erDiagram when relationships are non-trivial.}}

### API Contracts

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| {{path}} | {{verb}} | {{shape}} | {{shape}} |

### Currently Exposed Fields

Required when any acceptance criterion enumerates output, display, response, or persisted fields. One row per AC-named field.

| AC ID | Field | Source (file:line) | Currently Exposed? | Gap? |
|-------|-------|--------------------|--------------------|------|
| {{AC-00N}} | {{fieldName}} | {{path:line or "none"}} | {{yes / no}} | {{none / must add / must map}} |

## Decisions

| Decision | Rationale |
|----------|-----------|
| {{architecture approach}} | {{why this over alternatives}} |
| {{decision}} | {{rationale}} |

## Component Design

| Component | File | Action | Responsibility |
|-----------|------|--------|----------------|
| {{name}} | {{path}} | {{new/modify}} | {{what}} |

{{#if designs}}
## Visual Design Considerations

{{#each designs}}
- **{{filename}}**: {{design_decisions_based_on_image}}
{{/each}}

Key UI/UX patterns to implement:
- {{layout_patterns}}
- {{component_styles}}
- {{interaction_behaviors}}
{{/if}}

## Data Flow

{{Use a mermaid sequenceDiagram or flowchart when the flow involves 3+ steps or multiple actors.}}

1. {{Entry point}}
2. {{Transform}}
3. {{Output}}

## Requirements Traceability

> **Granularity rule:** If an acceptance criterion enumerates N fields, expand it into N rows -- one per field, each with its own Source `file:line`. Coarse AC-level rows hide individual field gaps.

| Requirement | Component | File | Status |
|-------------|-----------|------|--------|
| AC-001 | {{comp}} | {{path}} | Planned |
| AC-002 | {{comp}} | {{path}} | Planned |

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

## Open Questions

- [ ] {{question}}
