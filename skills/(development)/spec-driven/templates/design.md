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

### Reused Component Contracts

Required when the feature reuses a shared component (UI component, service, module, class, hook, etc.) in an execution context or input shape that differs from existing consumers. One row per reused component. Fields sourced by reading the component, not by trusting the name.

| Component | Runtime Preconditions | Inputs Exercised | Defaults Activated for This Input Shape | Source (file:line) |
|-----------|----------------------|------------------|-----------------------------------------|--------------------|
| {{name}} | {{must run inside X / requires Y to be initialized / must be invoked from environment Z}} | {{inputs this feature passes -- props, args, config, params}} | {{defaults that activate when called this way}} | {{file:line}} |

### Reused Utility Contracts

Required for every shared utility the feature reuses. One row per utility. Internal rules sourced by reading the utility, never inferred from the name.

| Utility | Inputs | Outputs | Internal Rules (transforms, edge cases, output constraints) | Source (file:line) |
|---------|--------|---------|-------------------------------------------------------------|--------------------|
| {{name}} | {{shape}} | {{shape}} | {{rules that shape the output -- caps, multipliers, exclusions, branching, etc.}} | {{file:line}} |

### Integration Points

| System | Integration Method |
|--------|--------------------|
| {{existing API / service / DB / auth}} | {{how the feature connects}} |

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
| {{AC-N}} | {{fieldName}} | {{path:line or "none"}} | {{yes / no}} | {{none / must add / must map}} |

## Decisions

{Non-obvious decisions only. If the choice is self-evident from the spec, omit it.}

| Decision | Choice | Worst-Case Consumer (file:line) | Rationale |
|----------|--------|---------------------------------|-----------|
| {{what was decided}} | {{what was chosen}} | {{file:line of largest realistic consumer the value must satisfy, or `n/a` for non-numeric decisions}} | {{why this over alternatives -- when the choice fixes a numeric default, cap, or implicit upper bound, the rationale must show the value derives from the worst-case consumer}} |

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

### Cross-Task Value Trace

Required when more than one task produces a value another task consumes. One row per hop. A reader must be able to reconstruct the value at every consumer without reading code.

| Hop | Producer Task | Value Shape Out | Consumer Task | Transformation Applied at Consumer | Final Value Shape |
|-----|---------------|-----------------|---------------|------------------------------------|-------------------|
| 1 | {{T-X}} | {{shape produced}} | {{T-Y}} | {{what the consumer applies on top}} | {{shape after consumer}} |

## Requirements Traceability

> **Granularity rule:** If an acceptance criterion enumerates N fields, expand it into N rows -- one per field, each with its own Source `file:line`. Coarse AC-level rows hide individual field gaps.

| Requirement | Component | File | Status |
|-------------|-----------|------|--------|
| AC-1 | {{comp}} | {{path}} | Planned |
| AC-2 | {{comp}} | {{path}} | Planned |

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

- {{error scenario}}: {{how handled}}. User sees: {{user-visible impact or "none"}}.

### Security

- {{concerns if applicable}}

## Open Questions

- [ ] {{question}}
