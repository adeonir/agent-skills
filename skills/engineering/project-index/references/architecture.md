# Architecture

Generate `.agents/codebase/architecture.md` — system structure, patterns, layers, data flows, and interfaces.

## When to Use

- Sub-agent dispatched during codebase summary fan-out
- User explicitly asks to refresh `architecture.md` after major restructure

## Scope

Macro-level structure: how the codebase is organized, where logic lives, how data moves through the system. Not feature-specific implementation details.

## Reading Priorities

1. Project metadata (`package.json`, `tsconfig.json`, `pyproject.toml`, `go.mod`, etc.) — framework, runtime, scripts
2. Directory tree (top-level + key subdirectories)
3. Entry points (API routes, CLI commands, main files, layout files)
4. Layer boundaries — services, modules, packages, domain folders
5. Sample 2-3 representative files per identified layer to confirm responsibility

Prefer AST-aware tooling (e.g., `smart-explore`) over full `Read` when scanning source files larger than 300 lines — same structural signal at a fraction of the tokens.

## Source Boundary

Map only the observable current state of source code, config, and tooling. **Never** read `.artifacts/` (briefs, PRDs, design docs, epics, roadmaps) as a source of architecture facts. Forward-looking content (`(planned)`, `(TBD)`, milestone tags, feature IDs, "shipped through feature X") belongs to planning artifacts, not the codebase map.

If a module, route, or dependency is described in `.artifacts/` but absent from the filesystem right now, it does not exist and must not appear here.

## Output

Save to `.agents/codebase/architecture.md`. On re-run, follow [merge-policy.md](merge-policy.md).

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources:
  - {{file-path-actually-read}}
  - {{file-path-actually-read}}
---

# Architecture

## Structure

```
{{directory tree — top-level and key subdirectories only}}
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
```

### {{Domain Name}} (`{{directory}}`)

{{Brief description of the domain and its components}}

| Component | Purpose |
|-----------|---------|
| {{component}} | {{what it does}} |

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
````

## Guidelines

- Read entry points before mapping flows — flows trace from entries
- Document at least 2 data flows; complex projects warrant 5+
- Every pattern must cite a source file path as evidence
- Group components by domain, not by directory alone
- Populate `sources:` with every file actually read; empty list is not acceptable
