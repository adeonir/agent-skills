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

Track each step as it completes — mark it done before moving to the next.
In Claude Code, create a task list at phase start (TaskCreate) and update
each step as it completes (TaskUpdate).

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

**Story order is fixed.** Emit stories in the exact order they appear in spec.md: S001 first, then S002, then S003, and so on. Do not reorder stories by technical dependency, risk, or setup-first instinct -- the user reads and commits stories in the order the spec declares them.

**Task IDs are assigned top-to-bottom, in document order.** The first task listed in tasks.md is `T001`. The second is `T002`. Numbering is monotonic as the reader scrolls down. This means:

- All of S001's tasks are listed first and get IDs `T001..T00k`
- S002's tasks follow and get `T00k+1..T00m`
- S003 continues from there, and so on

Never assign a low ID (e.g. `T001`) to a task that appears later in the document than a higher ID. A reader scanning top-to-bottom must see ascending IDs.

**Commit boundary: each story is independently shippable.** The user must be able to execute and commit only S001's tasks without pulling in work from S002 or later stories. This forbids **forward dependencies**:

- Allowed: `T005 [B:T002]` inside S002 blocking on T002 inside S001 (backward dep)
- Forbidden: `T002 [B:T005]` inside S001 blocking on T005 inside S002 (forward dep)

If a task seems to need something from a later story, the dependency is a signal the stories are wrong -- either merge them, reorder them in spec.md (then reflect here), or pull the shared prerequisite into the earlier story.

**Shared infrastructure tasks** (test tooling, lint config, base types used by every story) belong to the first story that needs them -- typically S001. Do not invent a "Phase 0" or "Setup" section outside the story structure. A story exists precisely because it delivers user value; setup that serves one story lives in that story.

Within each story group, generate tasks following natural order:
1. Setup (config, deps) -- only if not already done in an earlier story
2. Types (interfaces)
3. Implementation (core logic, tests included per task)
4. Integration (connect)

Each task should be:
- **Atomic**: Completable in one session
- **Testable**: Has verifiable outcome
- **Independent**: Minimal dependencies
- **Traceable**: Maps to requirements

**Task ID format:** `T001, T002, T003...` -- sequential across the entire tasks.md in document order, zero-padded, never reused.

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

Run all four checks before writing tasks.md. Display the result of each check explicitly —
`[pass]` or `[fail]` per item. Fix all `[fail]` items before writing. Do not run
these checks silently. Exception: the Commit-Boundary Viability Check (last) is
reasoned about internally and not echoed into the artifact — the artifact stays
focused on tasks, not process logs.

#### Story Order and ID Monotonicity Check

Verify the document order enforces the commit-boundary contract.

- `[pass|fail]` Stories appear in spec.md order (S001 first, then S002, ...)
- `[pass|fail]` Task IDs are monotonic top-to-bottom (first listed task = T001)
- `[pass|fail]` Each story's tasks are contiguous -- no story is split across non-adjacent sections
- `[pass|fail]` No forward dependencies -- no task blocks on a task with a higher ID
- `[pass|fail]` Shared setup (test infra, types) lives inside the first story that needs it, not in a separate "Phase 0"

If any fail: re-emit stories in spec.md order, reassign IDs top-to-bottom, and move or rewrite any forward-dependent task.

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

#### Commit-Boundary Viability Check (implicit)

Reason about this silently. Do not print `[pass]` lines for this check into
tasks.md -- the artifact should not contain a compile/test log per prefix.

For each story prefix (S001, then S001+S002, then S001+S002+S003, ...), the
codebase state after applying those tasks in order must stand alone:

- Compiles, lint and typecheck pass, tests (if present) pass
- No unresolved reference to a primitive owned by a later story
- No task in an earlier story silently depends on a symbol, function, or
  module that a later story defines

If an intermediate state would fail, the problem is a hidden forward
dependency the `[B:Txxx]` markers did not surface. Resolve it before writing
the artifact -- pick one:

- Restructure: have the earlier story ship an inline implementation that the
  later story refactors into a shared primitive, and add a `[B:Txxx]`
  refactor marker
- Reorder stories in spec.md so the primitive is owned by an earlier story
  (keep IDs monotonic after the reorder)
- Escalate to design.md: relocate component ownership and update the
  Requirements Traceability table, then regenerate tasks.md against the new
  design

Do not ship a tasks.md whose commits do not stand alone. "Compiles only at
the end" is not an acceptable execution plan.

### Step 8: Approval Gate

Present a summary and wait for approval:

```
Tasks ready: `.artifacts/features/{ID}-{name}/tasks.md`
Tasks: {count} | Components: {list}

Approve to proceed, or describe changes.
```

- If changes: update tasks.md, re-run pre-approval checks, re-present gate.
- If approved: run `implement`.

Do not suggest `implement` until approved.

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
