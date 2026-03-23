# Interactive UAT

User acceptance testing for Complex scope features with user-facing behavior. Triggered within Implement, not a separate phase.

## When to Use

- Scope is **Complex** (check `scope:` in spec.md frontmatter)
- All tasks are implemented and verified
- Feature has user-facing behavior worth walking through
- User explicitly requests UAT or validation

## When to Skip

- Scope is **Medium** or **Large**: per-task verification in Implement is sufficient
- Feature is purely backend/infrastructure with no user-facing behavior

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Pre-UAT Check

Verify that Implement has completed:
- All tasks marked done in tasks.md
- Quality gates pass
- Per-task verification passed

If not complete, redirect back to Implement.

### Step 3: Run Interactive UAT

Walk the user through each P1 story's Independent Test:

1. For each P1 story:
   - Describe the steps to perform
   - Ask user to verify the expected behavior
   - Record pass/fail with any observations
2. For P2/P3 stories: verify key scenarios (not exhaustive)

**UAT output:**

```markdown
### UAT Results

| Story | Test | Result | Notes |
|-------|------|--------|-------|
| P1: Password Reset | Request, receive email, click link, set new password | Pass | - |
| P1: Login | Enter credentials, see dashboard | Pass | - |
| P2: Remember Me | Check box, close browser, reopen | Fail | Cookie not persisting |
```

### Step 4: Determine Outcome

**If all pass:**
- Confirm `status: done` (already set by Implement)
- Inform user: feature complete and validated

**If issues found:**
- List what needs fixing with severity
- Suggest specific tasks to re-execute
- Status stays `done` only if issues are minor (P3); otherwise revert to `in-progress`

## Artifact Validation Checks

When the user requests explicit validation of artifacts (not UAT), run these checks:

### Spec Checks

- [ ] Has overview section
- [ ] Has user stories with priority levels (P1/P2/P3)
- [ ] P1 stories have independent test descriptions
- [ ] Has functional requirements (FR-xxx)
- [ ] Has acceptance criteria (AC-xxx) in WHEN/THEN format
- [ ] Has edge cases (boundary conditions, error scenarios)
- [ ] Has success criteria (measurable outcomes)
- [ ] For brownfield: has baseline section
- [ ] Open questions are documented (not blocking)

### Design Checks (if design.md exists)

- [ ] References spec requirements
- [ ] Has architecture decision with rationale
- [ ] Has data model (entities, relationships, API contracts)
- [ ] Lists files to create/modify
- [ ] Documents key decisions
- [ ] Follows codebase conventions

### Tasks Checks (if tasks.md exists)

- [ ] All FRs covered by tasks
- [ ] All ACs addressed
- [ ] Tasks are atomic and testable
- [ ] Dependencies are valid [P] or [B:Txxx]
- [ ] Has quality gates defined

## Guidelines

**DO:**
- Reserve interactive UAT for Complex scope only
- Validate against spec requirements, not subjective quality
- Mark gaps as blocking only if they affect core functionality
- Focus on behavior, not code style

**DON'T:**
- Over-validate with interactive UAT on non-Complex scope
- Report code style issues during validation
- Mark non-critical gaps as blocking

## Error Handling

- No artifacts: Suggest `specify`
- Implement not complete: Redirect to Implement
- Issues found: List with severity
