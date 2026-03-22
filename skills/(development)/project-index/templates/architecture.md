---
project: {{project-name}}
created: {{YYYY-MM-DD}}
---

# Architecture

## Structure

```
{{directory tree -- top-level and key subdirectories only}}
```

## System Overview

Use mermaid diagrams to show the high-level architecture. Include the main
components, their relationships, and external services.

```mermaid
graph TB
    {{nodes and edges showing system architecture}}
```

## Patterns

Document each architectural pattern with evidence from code.

### {{Pattern Name}}

{{Description of the pattern and where it is used}}

```{{lang}}
// Source: {{file-path}}
{{code example showing the pattern}}
```

{{Repeat for each significant pattern observed}}

## Entry Points

| Entry Point | File | Purpose |
|-------------|------|---------|
| {{description}} | {{file-path}} | {{what it does}} |

## Layers

| Layer | Responsibility | Directory | Key Files |
|-------|---------------|-----------|-----------|
| {{layer}} | {{what it does}} | {{directory}} | {{representative files}} |

## Component Map

Group components by domain/feature area. This helps agents understand where
to add new components and which existing ones to reuse.

```mermaid
graph TB
    subgraph "{{Domain Name}}"
        {{ComponentA}}
        {{ComponentB}}
    end
    {{Repeat for each domain}}
```

### {{Domain Name}} (`{{directory}}`)

{{Brief description of the domain and its components}}

| Component | Purpose |
|-----------|---------|
| {{component}} | {{what it does}} |

{{Repeat for each domain}}

## Data Flows

Trace complete flows from entry to output. Use mermaid sequence or flowchart
diagrams for complex flows, ASCII arrows for simple ones.

### {{Flow Name}}

```mermaid
flowchart LR
    {{step-a}} --> {{step-b}} --> {{step-c}}
```

1. **Entry**: {{description}} (`{{file-path}}`)
2. **Validation**: {{description}} (`{{file-path}}`)
3. **Processing**: {{description}} (`{{file-path}}`)
4. **Persistence**: {{description}} (`{{file-path}}`)
5. **Output**: {{description}} (`{{file-path}}`)

{{Repeat for each core flow}}

## Interfaces and APIs

Document all external service interfaces and internal API routes.

### External Services

| Service | Protocol | Client File | Endpoint |
|---------|----------|-------------|----------|
| {{service}} | {{REST/GraphQL/gRPC}} | {{file-path}} | {{base URL or env var}} |

### Internal API Routes

| Route | File | Purpose |
|-------|------|---------|
| {{route}} | {{file-path}} | {{what it does}} |

## Module Dependencies

| Module | Depends On | Depended By |
|--------|-----------|-------------|
| {{module}} | {{dependencies}} | {{dependents}} |

## Key Decisions

| Decision | Rationale | Evidence |
|----------|-----------|----------|
| {{decision}} | {{why}} | {{file or pattern that shows this}} |
