---
project: {{project-name}}
created: {{YYYY-MM-DD}}
---

# Conventions

Document each convention with evidence from actual code. Include code snippets
showing the pattern in use and reference the file where it was observed.

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

## Styling

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

## Components

{{File structure, props patterns, composition patterns (if UI project)}}

```{{lang}}
// Source: {{file-path}}
{{code example showing component pattern}}
```

**Avoid:** {{anti-pattern}}

## Inconsistencies

{{Patterns that are implemented differently across the codebase. List each
with the files where divergence was observed -- useful for agents to know
which pattern to follow.}}
