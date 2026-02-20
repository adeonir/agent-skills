# Implement Tasks

Execute tasks from task list.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) - Required for correct status management

## Arguments

- `[T001]` - Single task
- `[T001-T005]` - Range
- `[--all]` - All pending
- Empty - Next pending task

## Process

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load Context

Read:
- `spec.md` (acceptance criteria)
- `plan.md` (critical files, patterns, conventions)
- `tasks.md` (task list)

### Step 3: Validate Dependencies

For each task to execute:
- Check [P] (parallel) - proceed
- Check [B:Txxx] - verify Txxx is done

### Step 4: Update Status

If status is `ready`:
- Set `status: in-progress`

### Step 5: Execute Tasks

For each task, follow the 3-phase process:

#### Before (Preparation)

- Load [coding-principles.md](coding-principles.md)
- Read the relevant reference files from plan.md (patterns to follow)
- Check the conventions table (naming, imports, error handling)
- Run pre-implementation checklist:

**Pre-Implementation Checklist:**

| Check | Question |
|-------|----------|
| Assumptions | What am I assuming about the existing code? Verify. |
| Files | Which files will I touch? Are they listed in the plan? |
| Success criteria | What acceptance criteria does this task satisfy? |
| Risk | Could this change break existing functionality? |

- Understand the scope: what files to create/modify
- Note specific patterns to match

#### During (Implementation)

- Follow plan.md architecture precisely
- Match patterns from reference files exactly
- Use project's error handling approach
- Follow naming conventions documented
- Apply research findings if applicable

#### After (Validation)

- Validate against AC from spec.md
- Verify follows project patterns (naming, imports, error handling)
- Run quality gates

### Step 6: Run Quality Gates

After each task or range:

```bash
# Use --fix flags when available
{lint command} --fix
{typecheck command}
{test command}
```

Fix errors before marking task complete.

### Step 7: Update Progress

Mark completed tasks:
```markdown
- [x] T001 [P] {description}
```

Update task counters in tasks.md header.

### Step 8: Check Completion

If all tasks done:
- Set `status: to-review`
- Inform: ready for validation

### Step 9: Report

Show:
- Tasks completed
- Files modified
- Quality gate results
- Remaining tasks (if any)
- Suggested commit message

## Commit Suggestion Format

```
feat: {description of what was implemented}

- {key change 1}
- {key change 2}
```

Suggest atomic, logical commits at natural checkpoints.

## Error Handling

- Tasks not found: Suggest `tasks`
- Dependency blocked: List prerequisites
- Quality gate failed: Fix before marking done
