---
project: {{project-name}}
created: {{YYYY-MM-DD}}
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
