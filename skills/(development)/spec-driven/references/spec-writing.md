# Spec Writing Guidelines

Guidelines for writing clear specifications.

## Content Separation

| File | Purpose |
|------|---------|
| spec.md | WHAT to build |
| plan.md | HOW to build |
| tasks.md | WHEN to build |

## User Stories

Format:
```
As a {user}, I want {goal} so that {benefit}
```

Good:
```
As a user, I want to reset my password via email so that I can regain access
```

Bad:
```
As a user, I want a POST /reset-password endpoint (implementation detail)
```

## Functional Requirements

Use checkboxes:
```markdown
- [ ] FR-001: System must allow password reset
- [ ] FR-002: Reset link expires after 24 hours
```

Rules:
- Start with "System must..." or "User must..."
- Be specific and measurable
- No implementation details

## Acceptance Criteria

Verifiable conditions:
```markdown
- [ ] AC-001: User receives email within 1 minute
- [ ] AC-002: Reset link works only once
```

Rules:
- Must be testable (yes/no)
- Include edge cases
- Map to functional requirements

## Handling Ambiguity

Mark unclear items:
```markdown
- [ ] FR-004: [NEEDS CLARIFICATION: Should reset require verification?]
```

## Brownfield Baseline

For changes to existing code:
```markdown
## Baseline

### Current Behavior
- Password reset sends permanent link

### Gaps
- Links never expire (security risk)
```

**Important:** Describe BEHAVIOR, not implementation. No file paths, no code.
