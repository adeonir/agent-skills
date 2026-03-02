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

Perform a **deep analysis** of the entire codebase. This is NOT feature-specific -- the goal is to understand the project as a whole.

**Critical rule**: Don't just list or find files -- READ them and extract concrete patterns. Every convention documented must have evidence from actual code.

#### Phase 1: Project Discovery

1. **Read Project Metadata**

   Read package.json, tsconfig.json, pyproject.toml, go.mod, or equivalent. Extract:
   - Framework and runtime versions
   - All meaningful dependencies and their purpose
   - Scripts/commands available (build, test, lint, dev)
   - Configuration choices (module system, target, strict mode)

2. **Read Documentation**

   Read README.md, CLAUDE.md, CONTRIBUTING.md, or similar docs. Extract:
   - Project purpose and scope
   - Architecture decisions already documented
   - Coding standards and conventions
   - Setup and development workflow

3. **Map Directory Structure**

   Explore the full directory tree to understand the project, but only document the top-level directories and key subdirectories that define the architecture. Omit generated, vendored, or obvious directories.

#### Phase 2: Deep Code Analysis

4. **Read Representative Source Files**

   Select and READ 5-8 source files that represent different areas of the codebase (not just entry points -- pick files from different directories and layers). For each file, extract:
   - Naming conventions (functions, classes, variables, files)
   - Import/export patterns and module organization
   - Error handling approach (try/catch, Result types, error boundaries)
   - Type definitions style (interfaces vs types, inline vs shared)
   - Code organization within files (ordering, grouping)

5. **Map Module Dependencies**

   For key modules/directories, identify:
   - What they import (dependencies)
   - What imports from them (dependents)
   - Circular dependency patterns if any
   - Shared utilities, constants, or types used across modules

6. **Trace Data Flows**

   Follow 2-3 complete flows from entry to output:
   - Input: where data enters (API route, CLI arg, event handler, UI action)
   - Validation: how input is validated/parsed
   - Processing: business logic transformation
   - Persistence: how data is stored/retrieved
   - Output: how results are returned/rendered

   Document each step as a pattern, not with specific file references.

#### Phase 3: Testing & Integrations

7. **Analyze Testing Setup**

   READ 2-3 actual test files (not just find them). Extract:
   - Test framework and runner
   - Test file naming and location conventions
   - describe/it structure and nesting patterns
   - Mocking approach (what's mocked, how)
   - Fixture and helper patterns
   - Setup/teardown patterns

8. **Identify External Integrations**

   Search for and document all external touchpoints:
   - API calls (HTTP clients, SDK usage)
   - Database connections and ORM patterns
   - Third-party services (auth, payments, analytics)
   - Environment variables and configuration
   - File system operations

#### Phase 4: Convention Extraction

9. **Synthesize Patterns**

   Cross-reference findings from all files read. For each convention, provide:
   - What the project uses (with evidence from multiple files)
   - What to avoid (anti-patterns observed or implied)
   - Edge cases or inconsistencies found

   Cover at minimum: naming, imports, error handling, types, state management, async patterns, logging.

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
- {description}: {how it works}

## Layers

| Layer | Responsibility | Directory |
|-------|---------------|-----------|
| {Presentation/Business/Data/External} | {what it does} | {directory} |

## Data Flow
1. **Entry**: {description}
2. **Processing**: {description}
3. **Output**: {description}

## Key Decisions
| Decision | Rationale |
|----------|-----------|
```

**CONVENTIONS.md**
```markdown
# Conventions

| Aspect | Project Uses | Avoid |
|--------|-------------|-------|
| Naming | {convention} | {anti-pattern} |
| Error handling | {approach} | {anti-pattern} |
| Imports | {pattern} | {anti-pattern} |
| Types | {style} | {anti-pattern} |
| API calls | {pattern} | {anti-pattern} |
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
