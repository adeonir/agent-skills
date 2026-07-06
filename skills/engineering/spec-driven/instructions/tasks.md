# Tasks

Turn `spec.md` and `design.md` into a `tasks.md` — atomic steps, dependencies, per-task tests, gates, and commit boundaries. Answers WHEN / ORDER.

## When to Use

When breaking a change into tasks or user stories, or producing the task breakdown for a designed feature. Runs at Medium and up; Small skips it.

## Workflow

1. **Resolve feature** — find the active `spec.md` and `design.md`.
2. **Load context** — read `.artifacts/STATE.md` (if present), the spec, the design, `.artifacts/CONTEXT.md`, `discuss.md` (if present), and `AGENTS.md` / `CLAUDE.md`.
3. **Build the task list** — break into atomic tasks in execution order (top-to-bottom). A task is atomic when it has one clear objective, is verifiable by one gate, and needs at most ~1 new design decision. It may touch several files if the changes are mechanical and dependent.
4. **Fill the Coverage Matrix** — map every AC to at least one task and test.
5. **Self-check** — every AC in the matrix maps to a task/test; no task depends on a later task without a note; tests are co-located with the code they cover, never deferred. Watch for scope breaking the sizing — see the safety valve in [sizing.md](../references/sizing.md).
6. **Approval gate** — present the task count, a short execution order, tasks that can run in parallel (if any), 1-2 execution risks, then ask *"Move to implement?"*
7. **Update `STATE.md ## Progress`** at the approval gate — phase and next step. See [memory.md](../references/memory.md).

Default commit boundary is 1 task = 1 commit; document any grouping or split in `## Commit Boundary Notes` — the fact only, no long justification.

## Template: `tasks.md`

ALWAYS use this exact template structure. Conditional sections appear only when their trigger is met.

```markdown
---
spec: .artifacts/specs/{slug}/spec.md
design: .artifacts/specs/{slug}/design.md
---

# Tasks: {Feature}

## Scope
{In-scope / out-of-scope for this tasks.md — one paragraph.}

## Task List

### [ ] T-1: {title}
- **Story:** S-N — {title}
- **Description:** {what to do}
- **Depends on:** T-N, T-M (none if first)
- **Tests:** `{file}` — {short description}
- **Gate:** {command} | {descriptive check when no command exists}
- **Discrimination:** {does the test fail if X is removed/relaxed?} <!-- relevant tasks only -->
- **Done when:** {observable result}

### [ ] T-2: ...

## Coverage Matrix
| AC | Task | Test File | Notes |
|----|------|-----------|-------|

## Parallelism           <!-- conditional: Large/Complex -->
- T-2 and T-3 can run in parallel.

## Commit Boundary Notes <!-- conditional: when 1 task ≠ 1 commit -->
- T-1 + T-2 → single commit "scaffold checkout module"
- T-7 → split into 2 commits for review: backend + frontend
```

MUST NOT contain: new architecture (it belongs in design.md), observable behavior or acceptance criteria (they belong in spec.md), or component design. Tasks sequence and verify existing decisions; they never introduce them. The `Discrimination:` field applies to conditionals, validations, calculations, and P-1 ACs — if the test would still pass with the logic removed, it is weak.
