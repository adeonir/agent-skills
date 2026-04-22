# Spec Writing Guidelines

Guidelines for writing clear specifications.

## When to Use

Auto-loaded as a guideline for writing feature specs. Not a direct trigger.

## Content Separation

| File | Purpose |
|------|---------|
| spec.md | WHAT to build |
| design.md | HOW to build |
| tasks.md | WHEN to build |

## Behavior vs Symbol

Every line in spec.md describes user-observable behavior. Never reference code-level symbols -- not in ACs, not in Edge Cases, not in Out of Scope, not in Notes, not in Baseline.

| Symbol leak | Behavioral rewrite |
|-------------|--------------------|
| WHEN user opens drawer in `mode: 'create'` | WHEN admin opens the drawer to create a new client |
| Server rejects with `reason: 'validation_error'` + `fieldErrors` | Server rejects the submission with per-field validation errors |
| `discountType === 'fixed'` shows currency input | When the discount is a fixed amount, the form shows a currency input |
| `plan.value × 1` | The plan's total value |
| `frozenBilling` rows show disabled state | Rows representing frozen billing records appear disabled |
| Uses `TanStack Form` with `shadcn` drawer | (remove -- belongs in design.md) |
| `ClientFormDrawer` renders the form | The client form is presented in a side drawer |

If a behavior only makes sense by naming a code symbol, the spec is leaking design. Either rewrite in behavioral terms or move the content to design.md.

## Goals

Measurable outcomes that define what success looks like at the feature level.

```markdown
## Goals

- [ ] Users can reset their password without contacting support
- [ ] Reset flow completes in under 2 minutes end-to-end
```

Rules:
- 2-4 goals per feature (more signals scope creep)
- Goals drive Success Criteria -- every goal should map to at least one SC

## Out of Scope

Explicit exclusions to prevent scope creep. Use a table with reasons.

```markdown
## Out of Scope

| Feature | Reason |
|---------|--------|
| SMS verification | Separate feature, different integration |
| Admin password override | Security concern, needs separate spec |
```

Rules:
- Always include at least one item (forces the conversation)
- Include the reason -- prevents re-discussion later

## User Stories

Format:
```
### Sxxx [P1|P2|P3] {Story Title}
As a {user}, I want {goal} so that {benefit}
```

All stories in a spec WILL be implemented. Priorities define **implementation order**, not whether something ships.

Story ID rules:
- Sequential across the spec: S001, S002, S003...
- Never reused, never recycled
- Story IDs survive spec edits -- adding a story at the end, never renumbering

Priority levels:
- **P1** (Core): Implement first. The feature works with only P1 stories done. Must be vertical slices -- complete, demo-able end-to-end (not just backend or frontend). Each P1 story includes an Independent Test.
- **P2** (Increment): Implement after P1. Adds important capability on top of the core.
- **P3** (Polish): Implement last. Refinements and enhancements that improve the experience.

Each story includes **Why Px** to justify its priority and **Acceptance Criteria** inline with AC-xxx IDs.

Good:
```markdown
### S001 [P1] Password Reset

- As a user, I want to reset my password via email so that I can regain access
- **Why P1:** Core account recovery -- users locked out without this
- **Independent Test:** Can demo by clicking "Forgot password", receiving email, clicking link, and setting new password

**Acceptance Criteria:**

- [ ] AC-001: WHEN user requests password reset THEN system SHALL send email within 1 minute
- [ ] AC-002: WHEN reset link is older than 24 hours THEN system SHALL display "Link expired"
- [ ] AC-003: WHEN user submits new password THEN system SHALL enforce minimum 8 characters
```

Bad:
```
As a user, I want a POST /reset-password endpoint (implementation detail)
As a user, I want to reset my password (no priority, no benefit, no ACs)
```

## Acceptance Criteria Format

Use WHEN/THEN/SHALL format for verifiable conditions. ACs live inline within each story, not as a separate section.

Rules:
- Must be testable (yes/no outcome)
- Use WHEN/THEN to define trigger and expected behavior
- Use SHALL for mandatory behavior
- AC-xxx IDs are sequential across the entire spec (not per story)
- Happy paths go in ACs, boundary conditions go in Edge Cases

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

## Notes

Free-form context that doesn't fit other sections -- evidence sources, stakeholder input, deadlines, dependencies on other features, non-functional constraints stated behaviorally.

Rules:
- Same Behavior vs Symbol filter as the rest of the spec -- no libraries, no paths, no component or hook names
- Anything HOW-flavored goes to design.md, not here
- Omit the section entirely if there's nothing behavioral to capture beyond what the other sections already cover

## Brownfield Baseline

For changes to existing code:
```markdown
## Baseline

### Current Behavior
- Password reset sends permanent link

### Gaps
- Links never expire (security risk)
```

**Important:** Describe BEHAVIOR, not implementation. No file paths, no component/hook/function names, no code identifiers. Describe what the user observes, not what the code is called.
