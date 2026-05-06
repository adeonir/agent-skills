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

```mermaid
graph TB
    {{nodes and edges showing system architecture}}
```

## Patterns

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

## Component Map (if UI project)

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
