# Workflows

Generate `.agents/codebase/workflows.md` — user-facing flows and development workflows with step-by-step detail.

## When to Use

- Sub-agent dispatched during codebase summary fan-out
- User explicitly asks to refresh `workflows.md` after flow restructure

## Scope

Two categories:

- **User workflows**: core journeys through the application (auth, main feature flow, data submission). Trace from trigger to end state.
- **Development workflows**: how developers work with the codebase (local dev with mocks, feature flag flow, code generation flow, deploy).

## Reading Priorities

1. Entry points already mapped in architecture (API routes, CLI commands, UI pages)
2. Sample handlers or controllers per identified flow
3. Dev tooling scripts (`scripts/`, `bin/`, npm scripts) — for development workflows
4. CI config (deploy steps, environment promotions)

Prefer AST-aware tooling (e.g., `smart-explore`) over full `Read` when scanning handler or controller files larger than 300 lines.

## Source Boundary

Trace flows that exist in code today. A workflow described in `.artifacts/` (epic, story) but not yet wired must not appear here. Forward-looking content (`(planned)`, `(M5+)`, feature IDs) is excluded.

## Output

Save to `.agents/codebase/workflows.md`. On re-run, follow [merge-policy.md](merge-policy.md).

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

# Workflows

## User Workflows

### {{Flow Name}}

**Trigger**: {{what starts it}}

```mermaid
flowchart TD
    {{step-a}} --> {{step-b}} --> {{step-c}}
```

1. {{step}} (`{{file-path}}`)
2. {{step}} (`{{file-path}}`)
3. {{step}} (`{{file-path}}`)

**End state**: {{what the user sees}}

**Key code**:

```{{lang}}
// Source: {{file-path}}
{{code snippet showing the critical part of this flow}}
```

{{Repeat for each user workflow}}

## Development Workflows

### {{Workflow Name}}

**When**: {{when to use}}

```mermaid
flowchart LR
    {{step-a}} --> {{step-b}} --> {{step-c}}
```

1. {{step}}
2. {{step}}

**Key files**: {{relevant files with purpose}}

{{Repeat for each development workflow (local dev, testing, code generation, CI/CD, etc.)}}
````

## Guidelines

- 2-3 user workflows for simple CRUD apps; 5+ for complex/event-driven projects
- Each step cites a file path
- Each user workflow ends with the visible end state, not the last function call
- Development workflows include "When to use" so agents pick the right one
- Populate `sources:` with every file actually read; empty list is not acceptable
