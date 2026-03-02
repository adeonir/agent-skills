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

Load [codebase-exploration.md](codebase-exploration.md).

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
