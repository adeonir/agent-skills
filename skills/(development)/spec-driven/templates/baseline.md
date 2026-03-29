---
area: {{name}}
scope: {{directory-or-description}}
captured: {{YYYY-MM-DD}}
---

# Baseline: {{Area Name}}

## Scope

{{Description of what this baseline covers and its boundaries.}}

**Directories:** {{list of directories that define this area}}

## Current Behavior

### {{Concern 1}}

- {{What users/callers can currently do}}
- {{How the system behaves under normal conditions}}
- {{Behavioral contracts: what callers expect}}

### {{Concern 2}}

- {{Current capabilities}}
- {{Error states and edge cases}}

{Repeat for each major concern discovered.}

## Dependencies

### Depends On

| Dependency | Nature |
|------------|--------|
| {{internal module or external service}} | {{what it provides to this area}} |

### Depended On By

| Dependent | Nature |
|-----------|--------|
| {{module or service that uses this area}} | {{what it consumes}} |

## Configuration Surface

| Setting | Purpose | Current |
|---------|---------|---------|
| {{env var or config key}} | {{what it controls}} | {{current value or default}} |

## Gaps

- {{Missing functionality, incomplete features}}
- {{TODO/FIXME items observed}}

## Risks

- {{Security concerns}}
- {{Single points of failure}}
- {{Missing validation or error handling}}

## Tech Debt

- {{Inconsistent patterns}}
- {{Deprecated dependencies}}
- {{Dead code or missing tests}}

## Notes

{{Additional observations, historical context if discoverable, links to related baselines.}}
