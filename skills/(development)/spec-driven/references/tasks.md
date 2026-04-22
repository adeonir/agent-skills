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

Group tasks by story. Each story in spec.md becomes a `### Sxxx [Px] {Story Title}` section in tasks.md. Tasks within a group implement that story's acceptance criteria.

Within each story group, generate tasks following natural order:
1. Setup (config, deps)
2. Types (interfaces)
3. Implementation (core logic, tests included per task)
4. Integration (connect)

Each task should be:
- **Atomic**: Completable in one session
- **Testable**: Has verifiable outcome
- **Independent**: Minimal dependencies
- **Traceable**: Maps to requirements

**Task ID format:** `T001, T002, T003...` -- sequential across the entire tasks.md, zero-padded, never reused.

**Task description format:**

Without test infrastructure:
```
- [ ] T001 [P] {verb} {what}
  - **Done when:** {verifiable outcome}
```

With test infrastructure (test script detected in Step 3):
```
- [ ] T001 [P] {verb} {what}
  - **Tests:** unit|integration|e2e|none
  - **Gate:** quick|full|build
  - **Done when:** {verifiable outcome}; gate passes, no tests deleted
```

`Tests` declares the test type written in this task. `Gate` declares which gate command to run.
`Done when` is a concrete, verifiable condition. When test infrastructure exists it must
confirm the gate passes and no tests were deleted (count after ≥ count before).

**Metadata split:** What/Where/Reuses live in design.md Component Design and Patterns & Reuse.
Do not duplicate them per task -- tasks own Tests, Gate, and Done when only.

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

After generating tasks.md, update spec.md: for each AC mapped to a task in Requirements Coverage,
change its status tag from `` `in-design` `` to `` `in-tasks` ``. For Medium scope (no design phase),
change from `` `pending` `` directly to `` `in-tasks` ``.

### Step 7: Pre-Approval Checks

Run both checks before presenting tasks to the user. If either fails, restructure and re-run.

#### Diagram-Definition Cross-Check

Verify the execution diagram arrows match every task's dependency markers.
These are written independently and can drift.

For each task, confirm:
- Every `[B:Txxx]` marker has a corresponding arrow in the diagram
- Every arrow in the diagram has a corresponding `[B:Txxx]` in the target task
- Tasks shown as parallel `[P]` do not depend on each other

If any mismatch: fix the diagram or the marker, not both arbitrarily.

#### Test Co-location Check

Only applies when a test script was detected in Step 3. Skip entirely if no test infrastructure.

For each task that creates or modifies a code layer:
- Tests for that layer must be included in the same task
- "Tested in T00X" or "tests added later" is a violation -- merge the tests into the task

If any task defers its tests: merge them in before proceeding.

### Step 8: Report

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
- Defer tests to a later task when test infrastructure exists (contrasts: include tests in the task that creates the code)
- Present tasks before running the pre-approval checks (contrasts: run checks first, restructure if needed)

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
