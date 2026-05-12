# Conventions

Generate `.agents/codebase/conventions.md` — observed patterns with code snippets, project abstractions, and inconsistencies.

## When to Use

- Sub-agent dispatched during codebase summary fan-out
- User explicitly asks to refresh `conventions.md` after pattern shifts

## Scope

Naming, imports, error handling, types, styling, state management, async patterns, and project-specific abstractions (custom hooks, components, helpers, tokens). Every pattern must have evidence from actual source files.

## Reading Priorities

1. Config files (framework config, theme files, style tokens, env.example) — actual choices, not framework defaults
2. Custom hooks (all hooks in `hooks/` or equivalent)
3. Business logic files (services, use cases, domain modules)
4. UI components if applicable
5. Utilities (helpers, constants, shared types)
6. **Stop when** new files reveal no new patterns

Prefer AST-aware tooling (e.g., `smart-explore`) over full `Read` when scanning source files larger than 300 lines — same structural signal at a fraction of the tokens.

## Source Boundary

Document conventions as **observed**, not as prescribed. Never document patterns based on dependency names alone — read actual config and usage. Projects often override or extend framework defaults.

Project-specific abstractions are high priority. When a project wraps framework primitives (custom components, variables, tokens, helpers, hooks), agents need to know they exist and use them instead of underlying primitives.

## Output

Save to `.agents/codebase/conventions.md`. On re-run, follow [merge-policy.md](merge-policy.md).

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

# Conventions

## Naming

{{Description of naming conventions observed}}

```{{lang}}
// Source: {{file-path}}
{{code example showing the naming pattern}}
```

**Avoid:** {{anti-pattern observed or implied, with evidence}}

## Error Handling

{{Description of error handling approach}}

```{{lang}}
// Source: {{file-path}}
{{code example showing error handling pattern}}
```

**Avoid:** {{anti-pattern}}

## Imports

{{Import ordering and grouping conventions}}

```{{lang}}
// Source: {{file-path}}
{{code example showing import pattern}}
```

**Avoid:** {{anti-pattern}}

## Types

{{Type definition style: interfaces vs types, inline vs shared, strictness}}

```{{lang}}
// Source: {{file-path}}
{{code example showing type pattern}}
```

**Avoid:** {{anti-pattern}}

## Styling (if applicable)

{{CSS approach, preprocessor, custom properties, design tokens, theme structure}}

```{{lang}}
// Source: {{file-path}}
{{code example showing styling pattern}}
```

**Avoid:** {{anti-pattern}}

## Project Abstractions

Document reusable abstractions the project defines on top of frameworks or
libraries (components, hooks, helpers, variables, tokens). Agents MUST use
these instead of the underlying primitives.

| Abstraction | Import Path | Use Instead Of |
|-------------|-------------|---------------|
| {{name}} | {{import path}} | {{what it replaces}} |

```{{lang}}
// Source: {{file-path}}
{{code example showing usage}}
```

## Custom Hooks

Document all custom hooks the project defines. These encapsulate reusable
logic that agents should use instead of reimplementing.

| Hook | Import Path | Purpose |
|------|-------------|---------|
| {{hook name}} | {{import path}} | {{what it does}} |

```{{lang}}
// Source: {{file-path}}
{{code example showing hook signature and return type}}
```

```{{lang}}
// Source: {{file-path showing usage}}
{{code example showing how a component uses the hook}}
```

## State Management

{{Local state, global state, server state patterns}}

```{{lang}}
// Source: {{file-path}}
{{code example showing state pattern}}
```

**Avoid:** {{anti-pattern}}

## Async Patterns

{{Promises, async/await, error handling in async code}}

```{{lang}}
// Source: {{file-path}}
{{code example showing async pattern}}
```

**Avoid:** {{anti-pattern}}

## Components (if applicable)

{{File structure, props patterns, composition patterns (if UI project)}}

```{{lang}}
// Source: {{file-path}}
{{code example showing component pattern}}
```

**Avoid:** {{anti-pattern}}

## Inconsistencies

{{Patterns that are implemented differently across the codebase. List each
with the files where divergence was observed — useful for agents to know
which pattern to follow.}}
````

## Guidelines

- Every pattern must have a code snippet from a real source file
- Note inconsistencies when the same pattern is implemented differently
- "Avoid" entries describe anti-patterns observed or implied, never theoretical
- Document project abstractions with import paths and usage examples
- Populate `sources:` with every file actually read; empty list is not acceptable
