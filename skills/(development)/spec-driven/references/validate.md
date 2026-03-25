# Interactive UAT

User acceptance testing where the user manually verifies behavior. On-demand -- the user requests it when they want to test.

## When to Use

- User explicitly requests UAT or manual testing
- After implementation is complete and verify has passed
- Any scope -- not restricted to Complex

## When to Skip

- User does not request it
- Feature has no user-facing behavior (purely backend/infrastructure)

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Pre-UAT Check

Verify that implementation is complete:
- All tasks marked done (or all inline steps completed)
- Quality gates pass
- Verify has passed (design and pattern adherence)

If not complete, inform user and suggest finishing implementation first.

### Step 3: Build Test Scenarios

From spec.md, extract testable scenarios:

1. For each P1 user story: create a step-by-step test
2. For P2/P3 stories: create key scenario tests (not exhaustive)
3. Include edge cases from spec.md that are user-facing

Present the test plan to the user before starting.

### Step 4: Run Interactive UAT

Walk the user through each scenario:

1. Describe the steps to perform
2. Ask user to verify the expected behavior
3. Record pass/fail with observations

### Step 5: Determine Outcome

**If all pass:**
- Confirm feature is validated
- Suggest commit if not already committed

**If issues found:**
- List what needs fixing with severity
- Suggest specific areas to re-implement
- User decides whether to fix now or defer

## Guidelines

**DO:**
- Let the user drive -- they decide when to run UAT
- Focus on behavior, not code quality (verify handles that)
- Prioritize P1 stories in test scenarios
- Keep test steps concrete and actionable

**DON'T:**
- Run UAT automatically without user request
- Report code style or pattern issues (that's verify's job)
- Make UAT exhaustive for non-P1 stories
- Block completion on minor P3 issues

## Error Handling

- No spec.md: suggest running specify first
- Implementation not complete: redirect to implement
- No user-facing behavior: inform user UAT is not applicable
