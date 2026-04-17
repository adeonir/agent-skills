# Task Decomposition

Break design into implementable tasks.

## When to Use

- Scope is **Large** or **Complex** (check `scope:` in spec.md frontmatter)
- design.md is complete
- Ready to define implementation steps

## When to Skip

- Scope is **Medium**: ≤3 obvious steps, tasks are implicit in Implement
- When skipped, implement lists steps inline before starting (see [implement.md](implement.md))
- **Safety valve**: If implement's inline listing reveals >5 steps or complex dependencies, it redirects back here

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load Context

Read:
- `spec.md` (requirements)
- `design.md` (architecture)
- `decisions.md` (if exists, for resolved gray areas)

### Step 3: Detect Quality Gates

Read `package.json`:
- Lint script
- Typecheck script
- Test script

### Step 4: Decompose Tasks

Generate tasks following natural order:
1. Setup (config, deps)
2. Types (interfaces)
3. Implementation (core logic)
4. Integration (connect)
5. Tests

Each task should be:
- **Atomic**: Completable in one session
- **Testable**: Has verifiable outcome
- **Independent**: Minimal dependencies
- **Traceable**: Maps to requirements

**Task ID format:** `T001, T002, T003...` -- sequential, zero-padded, never reused.

**Task description format:**
```
- [ ] T001 [P] {verb} {what}
  - **Done when:** {verifiable outcome}
```

Each task has a "Done when" line -- a concrete, verifiable condition that marks the task as complete.

### Step 5: Create Execution Plan

Before writing tasks, create an ASCII diagram showing the execution flow:
- Sequential dependencies as arrows (`-->`)
- Parallel tasks as branches (`├-->`, `└-->`)
- Convergence points where branches merge

This gives an overview of parallelism and critical path before the detailed
breakdown. The diagram also serves as a sub-agent dispatch map -- parallel
branches identify tasks that can be delegated to independent sub-agents
during implementation.

### Step 6: Generate tasks.md

**LOAD ORDER:** Load this template before reading any existing tasks.md in `.artifacts/features/`. Existing task breakdowns may be stale -- template wins on structure.

**USE TEMPLATE:** `templates/tasks.md`

Generate tasks following the template structure:
- Summary (total count)
- Execution Plan (ASCII diagram of task flow)
- Quality Gates (lint, typecheck, test commands)
- Tasks grouped by commit boundary (T001 [P] for parallel, T002 [B:T001] for dependent), each with "Done when"
- Requirements Coverage (mapping ACs to tasks)

### Step 7: Report

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

## Dependency Markers

| Marker | Meaning |
|--------|---------|
| [P] | Parallel-safe, no dependencies |
| [B:T001] | Blocked by T001 |
| [B:T001,T002] | Blocked by multiple |

## Guidelines

**DO:**
- Keep tasks atomic -- single, clear action per task
- Respect dependencies -- same component = sequential
- Mark independent tasks as [P] to enable parallelization
- Group by commit boundary -- each group forms one atomic commit
- Cover all ACs -- every AC-xxx has at least one task
- Run quality gates after each task, not as separate tasks

**DON'T:**
- Add Files:/Reference:/Commit: metadata lines in task descriptions
- Create tasks that span multiple unrelated concerns
- Leave AC-xxx requirements without corresponding tasks
- Bundle quality gates as tasks in the breakdown

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

- Design not found: Suggest `design` (or skip if Medium scope)
- No clear components: Ask for clarification
