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

## Process

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

## Data Flow
1. {step}

## Key Decisions
| Decision | Rationale |
```

**CONVENTIONS.md**
```markdown
# Conventions

## Naming
- Files: {pattern}
- Functions: {pattern}

## Code Style
- {convention}
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

## Framework
- {name}

## Patterns
- {pattern}
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

## Error Handling

- No codebase: Inform this is for existing projects
- Empty project: Treat as greenfield
