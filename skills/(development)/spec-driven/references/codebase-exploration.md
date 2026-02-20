# Codebase Exploration Patterns

Patterns for analyzing existing code for a specific feature.

## When to Explore

- During planning (plan.md)
- Need to understand patterns for a specific feature
- Finding similar existing features
- Understanding integration points

## Scope

**Feature-specific analysis** - Focused on what you need for this feature:
- Similar existing features
- Reusable components
- Integration patterns
- Testing approaches

For **general codebase mapping**, see [codebase-mapping.md](codebase-mapping.md) (creates .artifacts/codebase/ docs).

## Tools

Use available semantic analysis, code search, and file reading tools to explore the codebase.
The agent discovers and uses whatever tools are available in the environment.

## Process

### Phase 1: Discovery

1. **Find Documentation**

   Look for README.md, CLAUDE.md, CONTRIBUTING.md, package.json, tsconfig.json in the project.

2. **Find Source Files**

   Find files related to the feature being built, plus test files.

3. **Read Documentation**

   Read 2-3 documentation files to understand project structure, architecture patterns, and coding conventions.

### Phase 2: Pattern Extraction

4. **Identify Reference Files**

   Find 2-3 existing features similar to what needs to be built. Check imports, exports, and file organization.

5. **Read Reference Files**

   Read 3-5 essential files and extract:
   - Naming conventions (functions, classes, variables)
   - Import/export patterns
   - Error handling approach
   - Type definitions style
   - Testing patterns

6. **Extract Code Patterns**

   Document specific patterns with file:line references:
   ```
   Pattern: Function naming
   - Project uses: camelCase for functions
   - Example: src/utils/helpers.ts:15

   Pattern: Error handling
   - Project uses: Custom error classes
   - Example: src/errors/index.ts:23
   ```

7. **Map Dependencies**

   For key files, identify imports (dependencies) and what imports from them (dependents).

### Phase 3: Architecture Analysis

8. **Trace Entry Points**

   Where would the feature integrate: API routes, UI components, CLI commands, event handlers.

9. **Follow Data Flow**

   Trace: Input validation -> Business logic -> Data transformation -> Output/response.

10. **Identify Layers**

    Map architecture layers: Presentation, Business logic, Data access, External services.

### Phase 4: Consolidation

11. **Summarize Conventions**

    Create comprehensive convention table with file:line references.

12. **List Essential Files**

    Categorize as: Reference (patterns to follow), Modify (existing files to change), Dependencies (files to import).

## Output Template

After exploration, document using this template:

```markdown
## Documentation Findings

| File | Purpose |
|------|---------|
| `path/to/README.md` | Brief description |

## Entry Points

| File | Line | Purpose |
|------|------|---------|
| `src/api/routes.ts` | 45 | API endpoint definitions |

## Code Flow

1. **Entry**: `file.ts:line` - Description
2. **Transform**: `file.ts:line` - Description
3. **Output**: `file.ts:line` - Description

## Architecture

- **Pattern**: {MVC/Clean/Hexagonal/etc}
- **Layers**: {list}
- **Key Abstractions**: {wrappers used}

## Conventions

| Aspect | Project Uses | Avoid | Reference |
|--------|-------------|-------|-----------|
| Env vars | `t3-env` | `process.env` | `src/env.ts:10` |
| Function naming | camelCase | snake_case | `src/utils.ts:23` |
| Error handling | Custom Error classes | Raw throws | `src/errors.ts:15` |
| API calls | Wrapper with retry | Direct fetch | `src/lib/api.ts:45` |
| Types | Interface + type | Any | `src/types/index.ts:8` |

## Test Infrastructure

- **Framework**: {jest/vitest/etc}
- **Location**: {test directory pattern}
- **Command**: {npm test/etc}
- **Patterns**: {describe/it structure, mocking approach}

## Essential Files

### Reference Files (patterns to follow)

1. `src/core/feature.ts` - Core implementation pattern
2. `src/types/feature.ts` - Type definition pattern

### Files to Modify

1. `src/api/routes.ts` - Add new endpoint
2. `src/services/index.ts` - Register new service

### Dependencies

1. `src/lib/db.ts` - Database connection
2. `src/utils/validation.ts` - Input validation
```

## Integration with Plan

Use findings in plan.md:
- Reference files to follow
- Patterns to use
- Code to reuse

## Rules

1. **Read content**: Don't just list files - READ them to extract actual patterns
2. **Be specific**: Always include file:line references for every pattern
3. **Be comprehensive**: Cover naming, imports, error handling, types, testing
4. **Follow template**: Use exact sections above
5. **Prioritize**: Focus on patterns most relevant to the feature being built
