# Task Decomposition

Break plan into implementable tasks.

## When to Use

- Plan.md is complete
- Ready to define implementation steps

## Process

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load Context

Read:
- `spec.md` (requirements)
- `plan.md` (architecture)

### Step 3: Detect Quality Gates

Read `package.json`:
- Lint script
- Typecheck script
- Test script

### Step 4: Decompose Tasks

Load [task-decomposition.md](task-decomposition.md) guidelines.

Generate tasks following natural order:
1. Setup (config, deps)
2. Types (interfaces)
3. Implementation (core logic)
4. Integration (connect)
5. Tests

### Step 5: Generate tasks.md

**USE TEMPLATE:** `templates/tasks.md`

Generate tasks following the template structure:
- Summary (total count)
- Tasks grouped by component (T001 [P] for parallel, T002 [B:T001] for dependent)
- Requirements Coverage (mapping FRs to tasks)
- Quality Gates (lint, typecheck, test commands)

### Step 6: Report

Inform user:
- Created: {count} tasks
- Components: {list}
- Next: Run `implement`

## Task Size Guidelines

| Size | Description | Example |
|------|-------------|---------|
| Small | Single file, simple change | "Add type export" |
| Medium | 1-3 files, moderate logic | "Create API endpoint" |
| Large | 3+ files, complex integration | "Implement auth flow" - consider splitting |

Prefer Small and Medium tasks. If a task feels Large, split it.

## Rules

1. **Be atomic** - Single, clear action per task
2. **No metadata** - No Files:/Reference:/Commit: lines in task descriptions
3. **Respect dependencies** - Same component = sequential
4. **Enable parallelization** - Mark independent tasks as [P]
5. **Group by commit boundary** - Each group of tasks must form a complete, self-contained unit of work that results in one atomic commit
6. **Cover all FRs** - Every FR-xxx has task(s)
7. **Quality gates separate** - Not tasks, run after each task

## Commit Boundary Grouping

Tasks are grouped so each group = one atomic commit. A group must be:
- **Self-contained**: The codebase compiles and works after the group is done
- **Logically cohesive**: All tasks in the group serve the same purpose
- **Minimal but complete**: No half-implemented features left behind

### Dependencies

Never create a dedicated "install all dependencies" task. Each dependency is installed in the task that first needs it, as part of its implementation. This keeps each commit group self-contained with only the deps it actually uses.

Example:
```markdown
### Authentication Setup

- [ ] T001 [P] Create auth types in types/auth.ts
- [ ] T002 [B:T001] Implement AuthService in services/auth.ts

### Auth Middleware

- [ ] T003 [B:T002] Add auth middleware in middleware.ts
- [ ] T004 [B:T003] Protect routes with auth middleware
```

After completing all tasks in a group, the code is in a stable, committable state.

## Error Handling

- Plan not found: Suggest `plan`
- No clear components: Ask for clarification
