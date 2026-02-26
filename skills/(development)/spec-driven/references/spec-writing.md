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

All stories in a spec WILL be implemented. Priorities define **implementation order**, not whether something ships.

Priority levels:
- **P1** (Core): Implement first. The feature works with only P1 stories done. Must be vertical slices -- complete, demo-able end-to-end (not just backend or frontend). Each P1 story includes an Independent Test.
- **P2** (Increment): Implement after P1. Adds important capability on top of the core.
- **P3** (Polish): Implement last. Refinements and enhancements that improve the experience.

Good:
```
### P1: Password Reset

- As a user, I want to reset my password via email so that I can regain access
- **Independent Test:** Can demo by clicking "Forgot password", receiving email, clicking link, and setting new password
```

Bad:
```
As a user, I want a POST /reset-password endpoint (implementation detail)
As a user, I want to reset my password (no priority, no benefit, no independent test)
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

## Edge Cases

Boundary conditions, error scenarios, and unexpected inputs. Use WHEN/THEN/SHALL format:

```markdown
- WHEN user submits empty form THEN system SHALL display validation errors for required fields
- WHEN reset link is clicked after expiry THEN system SHALL display "Link expired" and offer new reset
- WHEN user enters password shorter than 8 characters THEN system SHALL reject and show requirement
```

Rules:
- Separate from acceptance criteria (ACs define happy paths, edge cases define boundaries)
- Each edge case must be independently testable
- Cover: empty/null inputs, boundary values, error states, concurrent access

## Success Criteria

Measurable outcomes that define when the feature is successful. Not what the system does (that's ACs), but what the user achieves.

```markdown
- [ ] User can complete password reset in under 2 minutes
- [ ] Zero unhandled errors in reset flow during testing
- [ ] Reset email delivered within 60 seconds of request
```

Rules:
- Must be measurable (numbers, times, rates)
- Avoid vague adjectives ("fast", "easy", "intuitive")
- Focus on user outcomes, not implementation metrics

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
