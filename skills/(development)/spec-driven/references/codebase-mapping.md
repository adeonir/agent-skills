# Codebase Mapping

Analyze existing codebase for brownfield development.

## When to Use

- Starting work on existing project
- Need general codebase understanding
- Creating first brownfield feature
- `.artifacts/codebase/` doesn't exist yet

## Scope

**Macro-level analysis** - Understanding the whole codebase:
- Technology stack
- Architecture patterns
- Project conventions
- Testing approach
- External integrations

For **feature-specific exploration**, see [codebase-exploration.md](codebase-exploration.md) (used during planning).

## Workflow

### Step 1: Check Existing Mapping

If `.artifacts/codebase/` exists:
- Check age of files
- Ask if refresh needed

### Step 2: Explore Codebase

Perform a **macro-level analysis** of the entire codebase. This is NOT feature-specific -- the goal is to understand the project as a whole.

#### Phase 1: Project Discovery

1. **Read Project Metadata**

   Read package.json, tsconfig.json, pyproject.toml, go.mod, or equivalent to understand stack and dependencies.

2. **Read Documentation**

   Read README.md, CLAUDE.md, CONTRIBUTING.md, or similar docs to understand project purpose and conventions.

3. **Map Directory Structure**

   List the top-level directory structure and key subdirectories to understand project organization.

#### Phase 2: Architecture Analysis

4. **Identify Entry Points**

   Find main entry points: API routes, CLI commands, app bootstrapping, event handlers.

5. **Trace Architecture Layers**

   Map layers: Presentation, Business logic, Data access, External services. Identify which directories/files belong to each.

6. **Read Reference Files**

   Read 3-5 representative files across different layers to extract:
   - Naming conventions (functions, classes, variables, files)
   - Import/export patterns
   - Error handling approach
   - Type definitions style

#### Phase 3: Testing & Integrations

7. **Analyze Testing Setup**

   Find test files, identify test framework, understand test organization and patterns.

8. **Identify External Integrations**

   Find API calls, database connections, third-party services, environment variables.

#### Phase 4: Consolidation

9. **Document Patterns**

   For each convention found, include a file:line reference as evidence:
   ```
   Pattern: Function naming
   - Project uses: camelCase for functions
   - Example: src/utils/helpers.ts:15
   ```

Generate:

**STACK.md**
```markdown
# Stack

## Framework
- {name}: {version}

## Key Dependencies
- {package}: {purpose}

## Dev Tools
- {tool}: {purpose}
```

**ARCHITECTURE.md**
```markdown
# Architecture

## Patterns
- {pattern}: {usage}

## Entry Points

| File | Line | Purpose |
|------|------|---------|
| {path} | {line} | {description} |

## Layers

| Layer | Responsibility | Key Files |
|-------|---------------|-----------|
| {Presentation/Business/Data/External} | {what it does} | {paths} |

## Data Flow

1. **Entry**: {file:line} - {description}
2. **Transform**: {file:line} - {description}
3. **Output**: {file:line} - {description}

## Key Decisions
| Decision | Rationale |
|----------|-----------|
```

**CONVENTIONS.md**
```markdown
# Conventions

| Aspect | Project Uses | Avoid | Reference |
|--------|-------------|-------|-----------|
| Naming | {convention} | {anti-pattern} | {file:line} |
| Error handling | {approach} | {anti-pattern} | {file:line} |
| Imports | {pattern} | {anti-pattern} | {file:line} |
| Types | {style} | {anti-pattern} | {file:line} |
| API calls | {pattern} | {anti-pattern} | {file:line} |
```

**STRUCTURE.md**
```markdown
# Structure

```
{tree}
```
```

**TESTING.md**
```markdown
# Testing

## Infrastructure

| Aspect | Detail |
|--------|--------|
| Framework | {jest/vitest/etc} |
| Command | {npm test/etc} |
| Location | {test directory pattern} |

## Patterns
- {describe/it structure, mocking approach, fixtures}

## Reference Tests

| File | What It Tests |
|------|---------------|
| {existing test} | {pattern to follow} |
```

**INTEGRATIONS.md**
```markdown
# Integrations

| Service | Purpose | Location |
|---------|---------|----------|
| | | |
```

### Step 3: Save

Create `.artifacts/codebase/` with generated docs.

### Step 4: Report

Inform user:
- Mapped 6 areas
- Next: Create feature with baseline context

## Guidelines

- Don't overwrite existing codebase/ mapping without user confirmation
- Focus on architecture-relevant patterns, not implementation details
- Keep mapping files concise and scannable
- Document conventions as observed, not as prescribed

## Error Handling

- No codebase: Inform this is for existing projects
- Empty project: Treat as greenfield
