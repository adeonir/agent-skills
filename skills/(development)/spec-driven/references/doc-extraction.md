# Documentation Extraction

Extract rules, constraints, and requirements from referenced documentation files.

## When to Use

- User provides `@path` to PRD, TDD, or documentation
- Need to map external requirements to spec format

## Process

### Step 1: List Files

If path is a directory, list all files:

```bash
find {path} -type f -name "*.md"
```

### Step 2: Read Each File

Read files completely to extract:

| Pattern | What to Extract | Examples |
|---------|-----------------|----------|
| Rules | "must", "cannot", "always", "never", "required", "shall" | "Users must verify email before login" |
| Constraints | "only if", "when", "unless", "if...then" | "Only if user is admin" |
| Examples | Code blocks, diagrams, sample data | API response examples |

### Step 3: Map to Specification

For each item extracted, ask: "Is this relevant to the feature?"

**If relevant:**
- Map to Functional Requirement (FR-xxx)
- Map to Acceptance Criteria (AC-xxx)
- Or add to Notes

**If skipped:**
- Note WHY in Notes section

### Step 4: Document Extraction

Output extraction summary before generating spec:

```markdown
## Extracted from Documentation

| Source | Item | Relevant | Mapped To |
|--------|------|----------|-----------|
| prd.md | Users must verify email | Yes | FR-001 |
| prd.md | SMS verification optional | No | Skipped: out of scope |
```

## Mapping Guidelines

### Rules → Functional Requirements

```markdown
Source: "Users must be able to reset password via email"
→ FR-001: System must allow users to request password reset via email
```

### Constraints → Business Rules or AC

```markdown
Source: "Reset link expires after 24 hours"
→ AC-001: Reset link must expire after 24 hours
→ OR Business Rule: Reset tokens valid for 24 hours only
```

### Examples → Notes or AC

```markdown
Source: Example API response { status: "sent" }
→ Notes: API returns { status } where status can be "sent", "failed", "pending"
→ OR AC-002: Email endpoint returns status field
```

## Template Integration

After extraction, populate spec.md sections:

```markdown
# Feature: {name}

## Overview
{Brief description from user input + docs context}

## User Stories
{Derived from who needs what in docs}

## Functional Requirements
- [ ] FR-001: {Rule from docs}
- [ ] FR-002: {Rule from docs}

## Acceptance Criteria
- [ ] AC-001: {Constraint from docs}
- [ ] AC-002: {Example validation from docs}

## Notes
- Extracted from: {file paths}
- Skipped items: {reasons}
```

## Error Handling

- **File not found**: Inform user, ask for correct path
- **Directory empty**: Inform user no .md files found
- **No relevant items**: Note in spec that docs were reviewed but no applicable requirements
- **Conflicting requirements**: Add to "Open Questions" section in spec.md

## Examples

**PRD Input:**
```
initialize feature @docs/prd.md
```

**Extraction Process:**
1. Read docs/prd.md
2. Find: "Users must verify email before accessing dashboard"
3. Find: "Verification link expires in 1 hour"
4. Map to spec:
   - FR-001: System must require email verification before dashboard access
   - AC-001: Verification link must expire after 1 hour

**Spec Output:**
```markdown
## Functional Requirements
- [ ] FR-001: System must require email verification before dashboard access

## Acceptance Criteria  
- [ ] AC-001: Verification link must expire after 1 hour

## Notes
Extracted from: docs/prd.md
```
