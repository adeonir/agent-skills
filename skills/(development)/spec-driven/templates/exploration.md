---
id: {{ID}}
feature: {{name}}
created: {{YYYY-MM-DD}}
---

## Documentation Findings

| File | Purpose |
|------|---------|
| `{{path/to/README.md}}` | {{Brief description}} |

## Entry Points

| File | Line | Purpose |
|------|------|---------|
| `{{src/api/routes.ts}}` | {{45}} | {{API endpoint definitions}} |

## Code Flow

1. **Entry**: `{{file.ts:line}}` - {{Description}}
2. **Transform**: `{{file.ts:line}}` - {{Description}}
3. **Output**: `{{file.ts:line}}` - {{Description}}

## Architecture

- **Pattern**: {{MVC/Clean/Hexagonal/etc}}
- **Layers**: {{list}}
- **Key Abstractions**: {{wrappers used}}

## Touched Types -- Member Enumeration

Every entity, projection, contract, or type the feature reads or writes. All exposed members listed -- no sampling. Every "no change needed" claim anchored to `file:line`.

| Type / Entity | Member | file:line | Notes (feature reads? writes? nullable?) |
|---------------|--------|-----------|------------------------------------------|
| {{EntityOrContract}} | {{memberName}} | {{path:line}} | {{notes}} |

### Absence Claims

Claims that an existing type already covers the feature's needs -- each must cite the member that backs the claim.

| Claim | Anchor (file:line) |
|-------|--------------------|
| {{e.g. "response shape already exposes field X"}} | {{path:line}} |

## Conventions

| Aspect | Project Uses | Avoid | Reference |
|--------|-------------|-------|-----------|
| {{Env vars}} | {{t3-env}} | {{process.env}} | {{src/env.ts:10}} |
| {{Function naming}} | {{camelCase}} | {{snake_case}} | {{src/utils.ts:23}} |
| {{Error handling}} | {{Custom Error classes}} | {{Raw throws}} | {{src/errors.ts:15}} |
| {{API calls}} | {{Wrapper with retry}} | {{Direct fetch}} | {{src/lib/api.ts:45}} |
| {{Types}} | {{Interface + type}} | {{Any}} | {{src/types/index.ts:8}} |

## Test Infrastructure

- **Framework**: {{jest/vitest/etc}}
- **Location**: {{test directory pattern}}
- **Command**: {{npm test/etc}}
- **Patterns**: {{describe/it structure, mocking approach}}

## Essential Files

### Reference Files (patterns to follow)

1. `{{src/core/feature.ts}}` - {{Core implementation pattern}}
2. `{{src/types/feature.ts}}` - {{Type definition pattern}}

### Files to Modify

1. `{{src/api/routes.ts}}` - {{Add new endpoint}}
2. `{{src/services/index.ts}}` - {{Register new service}}

### Dependencies

1. `{{src/lib/db.ts}}` - {{Database connection}}
2. `{{src/utils/validation.ts}}` - {{Input validation}}
