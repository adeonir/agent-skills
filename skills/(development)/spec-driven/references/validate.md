# Validate

Validate artifacts and implementation.

## Modes

Detected automatically based on artifacts:

| Artifacts | Mode | Validates |
|-----------|------|-----------|
| spec only | Spec | Structure |
| spec+plan | Plan | + documentation compliance |
| spec+plan+tasks | Tasks | + requirements coverage |
| all + code | Full | + implementation |

## Process

### Step 1: Resolve Feature

1. If ID provided -> use `.specs/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Detect Mode

Check which files exist in `.specs/features/{ID}-{name}/`.

### Step 3: Run Validation

**Spec Mode:**
- Structure complete
- No clarifications pending

**Plan Mode:**
- + Documentation compliance

**Tasks Mode:**
- + Requirements coverage
- + Task dependencies valid

**Full Mode:**
- + Git diff comparison with plan.md
- + Pattern compliance check
- + Code implements spec
- + Acceptance criteria pass
- + Only report findings with confidence >= 80

### Step 4: Determine Outcome

**If valid:**
- Update status:
  - Spec mode: `ready` → suggest `plan`
  - Plan mode: stay `ready` → suggest `tasks`
  - Tasks mode: stay `ready` → suggest `implement`
  - Full mode: `to-review` → `done` → suggest `archive`

**If issues:**
- List what needs fixing
- Suggest appropriate command

## Validation Checklists

### Spec Validation

- [ ] Has overview
- [ ] Has user stories
- [ ] Has functional requirements (FR-xxx)
- [ ] Has acceptance criteria (AC-xxx)
- [ ] No [NEEDS CLARIFICATION] markers
- [ ] For brownfield: has baseline section

### Plan Validation

- [ ] References spec requirements
- [ ] Has architecture section
- [ ] Has implementation approach
- [ ] Lists files to create/modify
- [ ] Documents key decisions
- [ ] Follows codebase conventions

### Tasks Validation

- [ ] All FRs covered by tasks
- [ ] All ACs addressed
- [ ] Tasks are atomic and testable
- [ ] Dependencies are valid [P] or [B:Txxx]
- [ ] Has quality gates defined

### Full Validation (Code)

- [ ] All tasks implemented
- [ ] Acceptance criteria pass
- [ ] Follows plan architecture
- [ ] Quality gates pass (lint, typecheck, tests)
- [ ] No TODO/FIXME comments
- [ ] Edge cases handled

## Output Formats

### Spec Mode Output

```markdown
## Validation: {ID}-{feature}

### Mode: Spec

### Structure Check

| Check | Status |
|-------|--------|
| Overview | ✅ |
| User Stories | ✅ |
| Functional Requirements | ✅ |
| Acceptance Criteria | ✅ |

### Clarifications

- [ ] None found, ready for planning
- [x] 2 items need clarification (run `clarify`)

### Summary

- Status: **Ready for plan** or **Needs clarification**
```

### Plan Mode Output

```markdown
## Validation: {ID}-{feature}

### Mode: Plan

### Documentation Compliance

| Guideline | Status | Issue |
|-----------|--------|-------|
| Architecture documented | ✅ | - |
| Files listed | ⚠️ | Missing entry points |

### Summary

- Status: **Ready for tasks** or **Needs corrections**
```

### Tasks Mode Output

```markdown
## Validation: {ID}-{feature}

### Mode: Tasks

### Coverage

| Requirement | Tasks | Status |
|-------------|-------|--------|
| FR-001 | T001, T002 | ✅ Covered |
| FR-002 | T003 | ⚠️ Partial |

### Dependencies

- ✅ All valid [P] or [B:Txxx]
- ⚠️ T005 blocks non-existent task

### Summary

- Status: **Ready for implement** or **Needs fixes**
```

### Full Mode Output

```markdown
## Validation: {ID}-{feature}

### Mode: Full

### Implementation Coverage

| Planned | Status | Issue |
|---------|--------|-------|
| src/api.ts | Modified | - |
| src/utils.ts | NOT MODIFIED | **GAP** |

### Requirements

| Req | Status | Evidence | Issue |
|-----|--------|----------|-------|
| FR-001 | Implemented | src/api.ts:45 | - |
| FR-002 | Partial | src/service.ts:23 | Missing error handling |
| FR-003 | **Missing** | - | **No implementation** |

### Acceptance Criteria

| AC | Status | Test | Issue |
|----|--------|------|-------|
| AC-001 | Satisfied | src/test.ts:34 | - |
| AC-002 | **Missing** | - | **No test found** |

### Pattern Compliance

| Expected | Found | Status |
|----------|-------|--------|
| Custom Error class | Raw throw | **VIOLATION** |
| API wrapper with retry | Direct fetch | **VIOLATION** |

### Gaps Found

1. **Missing File Modifications**
   - `src/utils.ts` - Planned but not modified

2. **Missing Requirements**
   - FR-003: User validation not implemented

3. **Missing Tests**
   - AC-002: No error scenario test

4. **Pattern Violations**
   - Using raw throw instead of custom Error class (see src/service.ts:23)

### Summary

- Status: **Needs fixes** (5 issues found)
- Confidence: Only findings >= 80 reported
- Suggested: Run `implement` to fix gaps
```

## Error Handling

- No artifacts: Suggest `initialize`
- Issues found: List with severity
