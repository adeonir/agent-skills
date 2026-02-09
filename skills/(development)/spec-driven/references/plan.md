# Technical Planning

Create technical plan from specification.

## When to Use

- Spec is complete (no [NEEDS CLARIFICATION])
- Ready to define HOW to build

## Process

### Step 1: Resolve Feature

1. If ID provided -> use `.specs/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load Spec

Read `.specs/features/{ID}-{name}/spec.md`.

If clarifications pending:
- List items
- Suggest `clarify` first
- Exit

### Step 3: Research Phase

Check for new technologies in spec:

- APIs mentioned
- Libraries not in codebase
- External services

For each new tech:
- Check `.specs/research/{topic}.md`
- If exists: use cached research
- If not: research and create cache

### Step 4: Codebase Exploration

Load [codebase-exploration.md](codebase-exploration.md).

Focus areas:
- Similar existing features
- Reusable components
- Patterns to follow
- Integration points

### Step 4b: MCP Strategy

**If serena MCP available:**
- Use `find_symbol` for precise symbol location
- Use `find_referencing_symbols` for impact analysis

**If NOT available (fallback):**
- Use grep to find symbol references
- Use glob to find files
- Use read to analyze code

### Step 5: Generate plan.md

**Structure:**

```markdown
# Technical Plan: {Feature}

## Context

- Feature: {ID}-{feature}
- Created: {date}
- Spec: .specs/features/{ID}-{feature}/spec.md

## Research Summary

(If external research done)

> From .specs/research/{topic}.md

- {key finding 1}
- {key finding 2}

## Critical Files

### Reference Files

| File | Purpose |
|------|---------|
| {path} | {why relevant} |

### Files to Modify

| File | Reason |
|------|--------|
| {path} | {what changes} |

### Files to Create

| File | Purpose |
|------|---------|
| {path} | {responsibility} |

## Codebase Patterns

| Pattern | Project Uses | Avoid | Reference |
|---------|-------------|-------|-----------|
| Naming | {convention} | {anti-pattern} | {file:line} |
| Error handling | {approach} | {anti-pattern} | {file:line} |
| API calls | {pattern} | {anti-pattern} | {file:line} |

## Architecture Decision

{chosen approach with rationale - be decisive, pick ONE approach}

## Component Design

| Component | File | Responsibility |
|-----------|------|----------------|
| {name} | {path} | {what} |

## Data Flow

1. {Entry point}
2. {Transform}
3. {Output}

## Requirements Traceability

| Requirement | Component | File | Status |
|-------------|-----------|------|--------|
| FR-001 | {comp} | {path} | Planned |
| FR-002 | {comp} | {path} | Planned |

## Test Strategy

### Infrastructure

| Aspect | Detail |
|--------|--------|
| Framework | {jest/vitest/etc} |
| Command | {npm test/etc} |
| Location | {test directory pattern} |

### Reference Tests

| File | What It Tests |
|------|---------------|
| {existing test} | {pattern to follow} |

### New Tests

| Component | Test File | Scenarios |
|-----------|-----------|-----------|
| {comp} | {path} | {what to test} |

## Considerations

### Error Handling

- {approach matching project patterns}

### Security

- {concerns if applicable}

## Decisions

| Decision | Rationale |
|----------|-----------|
| | |

## Open Questions

- [ ] {question}
```

### Step 6: Update Status

Set spec.md frontmatter: `status: ready`

### Step 7: Report

Inform user:
- Created: `plan.md`
- Research cached: {topics}
- Key decisions: {count}
- Next: Run `tasks`

## Error Handling

- Spec not found: Suggest `initialize`
- Clarifications found: Suggest `clarify`
- Codebase unclear: Ask for guidance
