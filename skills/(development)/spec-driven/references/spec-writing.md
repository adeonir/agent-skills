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
[P1|P2|P3] As a {user}, I want {goal} so that {benefit}
```

Priority levels:
- **P1** (Must deliver): Core functionality, blocking requirements
- **P2** (Should have): Important but not blocking launch
- **P3** (Nice to have): Enhancements, can be deferred

Good:
```
[P1] As a user, I want to reset my password via email so that I can regain access
[P2] As a user, I want to see password strength feedback so that I choose a strong password
```

Bad:
```
As a user, I want a POST /reset-password endpoint (implementation detail)
As a user, I want to reset my password (no priority, no benefit)
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

Use WHEN/THEN format for verifiable conditions:

```markdown
- [ ] AC-001: WHEN user requests password reset THEN system sends email within 1 minute
- [ ] AC-002: WHEN user clicks reset link a second time THEN system rejects the request
```

Good:
```markdown
- [ ] AC-003: WHEN reset link is older than 24 hours THEN system SHALL display "Link expired" message
- [ ] AC-004: WHEN user submits new password THEN system SHALL enforce minimum 8 characters
```

Bad:
```markdown
- [ ] AC-005: Password reset works correctly (not testable)
- [ ] AC-006: System should handle errors (vague, no WHEN/THEN)
```

Rules:
- Must be testable (yes/no outcome)
- Use WHEN/THEN to define trigger and expected behavior
- Use SHALL for mandatory behavior
- Include edge cases
- Map to functional requirements

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
