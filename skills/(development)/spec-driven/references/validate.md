# Validate

Validate artifacts and implementation.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) - Required for correct status management

## Adaptive Mode

Validation adapts automatically based on which artifacts exist. A single pass checks
everything available, from spec structure to code implementation.

## Process

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Detect Available Artifacts

Check which files exist in `.artifacts/features/{ID}-{name}/` and determine scope:

| Artifacts Found | Validation Scope |
|-----------------|------------------|
| spec only | Structure, completeness |
| spec + plan | + documentation compliance, data model |
| spec + plan + tasks | + requirements coverage, dependencies |
| all + code changes | + implementation, acceptance criteria, patterns |

### Step 3: Run Validation

#### Spec Checks

- [ ] Has overview section
- [ ] Has user stories with priority levels (P1/P2/P3)
- [ ] Has functional requirements (FR-xxx)
- [ ] Has acceptance criteria (AC-xxx) in WHEN/THEN format
- [ ] For brownfield: has baseline section
- [ ] Open questions are documented (not blocking)

#### Plan Checks (if plan.md exists)

- [ ] References spec requirements
- [ ] Has architecture decision with rationale
- [ ] Has data model (entities, relationships, API contracts)
- [ ] Lists files to create/modify
- [ ] Documents key decisions
- [ ] Follows codebase conventions

#### Tasks Checks (if tasks.md exists)

- [ ] All FRs covered by tasks
- [ ] All ACs addressed
- [ ] Tasks are atomic and testable
- [ ] Dependencies are valid [P] or [B:Txxx]
- [ ] Has quality gates defined

#### Code Checks (if implementation exists)

- [ ] All tasks implemented
- [ ] Acceptance criteria pass
- [ ] Follows plan architecture
- [ ] Quality gates pass (lint, typecheck, tests)
- [ ] No TODO/FIXME comments left
- [ ] Edge cases handled (see checklist below)

### Step 4: Edge Case Verification

When validating code, check for:

| Category | What to Verify |
|----------|---------------|
| Error states | Error paths return meaningful messages, no silent failures |
| Boundaries | Empty arrays, zero values, max lengths, off-by-one |
| Concurrency | Race conditions in async operations, state mutations |
| Permissions | Authorization checks on protected operations |
| Network | Timeout handling, retry logic, offline behavior |
| Invalid input | Null/undefined, wrong types, malformed data |

### Step 5: Determine Outcome

**If valid:**
- Update status based on scope:
  - Spec only: `ready` -> suggest `plan`
  - With plan: stay `ready` -> suggest `tasks`
  - With tasks: stay `ready` -> suggest `implement`
  - With code: `to-review` -> `done` -> suggest `archive`

**If issues:**
- List what needs fixing
- Suggest appropriate next step

## Output Format

```markdown
## Validation: {ID}-{feature}

### Checks

| Category | Check | Status | Issue |
|----------|-------|--------|-------|
| Spec | Overview present | ok | - |
| Spec | User stories with priorities | ok | - |
| Spec | Functional requirements | ok | - |
| Spec | Acceptance criteria (WHEN/THEN) | warning | AC-003 missing THEN clause |
| Plan | Architecture decision | ok | - |
| Plan | Data model defined | fail | No entities section |
| Tasks | All FRs covered | ok | - |
| Tasks | Dependencies valid | ok | - |
| Code | All tasks implemented | ok | - |
| Code | AC-001 satisfied | ok | src/api.ts:45 |
| Code | AC-002 satisfied | fail | No implementation found |
| Code | Edge case: error states | warning | Missing error handling in src/service.ts:23 |

### Edge Cases (code only)

| Category | Status | Detail |
|----------|--------|--------|
| Error states | warning | Empty catch block at src/service.ts:30 |
| Boundaries | ok | - |
| Invalid input | fail | No null check on user input at src/handler.ts:12 |

### Gaps Found

1. {description of gap with file:line reference}
2. {description of gap}

### Summary

- Status: **{Ready for plan | Ready for tasks | Ready for implement | Needs fixes | Done}**
- Issues: {count by severity}
- Confidence: Only findings >= 80 reported
- Next: {suggested action}
```

## Error Handling

- No artifacts: Suggest `initialize`
- Issues found: List with severity
