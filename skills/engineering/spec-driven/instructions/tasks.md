# Tasks

Turn `spec.md` and `design.md` into a `tasks.md` — atomic steps, dependencies, per-task tests, gates, and commit boundaries. Answers WHEN / ORDER.

## When to Use

When breaking a change into tasks or user stories, or producing the task breakdown for a designed feature. Runs at Medium and up; Small skips it.

## Workflow

1. **Resolve feature** — find the active `spec.md` and read the active feature's `STATE.md ## Progress` before loading `design.md`. If `Findings` names `validate` or `audit`, triage that report before loading downstream artifacts. Otherwise, if `Phase` points to `specify` or `design`, stop and report that phase. Require `spec.md` and `design.md` at `status: ready`; if either phase is not ready, stop and run that phase. Otherwise resolve `design.md` and continue.
2. **Load context** — read the active feature's `STATE.md`, the spec, the design, the root `CONTEXT.md`, `discuss.md` (if present), and `AGENTS.md` / `CLAUDE.md`. If `Findings` names `validate`, read `validate.md`; if it names `audit`, read `audit.md`. Verify each reported finding before adding or adjusting a correction task. These are context only: upstream prose never crosses into `tasks.md` (the template's MUST-NOT names it) — tasks reference `AC-N.M` by id in the Coverage Matrix, never restate its text.
3. **Build the task list** — when editing an existing `tasks.md`, set its status to `draft` before writing. If `Findings` names a report, preserve the existing `T-N` sequence and create or adjust tasks for verified findings. Otherwise break into atomic tasks in execution order (top-to-bottom). A task is atomic when it has one clear objective, is verifiable by one gate, and needs at most ~1 new design decision. It may touch several files if the changes are mechanical and dependent. Tasks group under the story they serve, contiguously, and stories appear in dependency order — no task depends on a task in a later story. Implement dispatches whole stories in that order, so this ordering is what makes a story safe to hand to one subagent. When a story's tasks reveal it is not one vertical slice ([slicing.md](../references/slicing.md)), set `STATE.md` to `Phase: specify` and `Next: specify`; never split its task list at an arbitrary index to compensate.
4. **Fill the Coverage Matrix** — map every AC to at least one task and test.
5. **Self-check** — run `python3 ${CLAUDE_SKILL_DIR}/scripts/lint_artifact.py tasks .artifacts/specs/{slug}` and fix every line it reports, then read for what it cannot: boundaries hold — nothing from spec or design leaked in, per the template's MUST-NOT ([discriminator.md](../references/discriminator.md)); no task introduces a decision instead of sequencing one — set `STATE.md` to `Phase: design` and `Next: design` when the design has not made the decision; every AC's task and test actually cover it; every verified report finding has a correction task or an explicit reason it needs no task; no task depends on a later task without a note; every task is one commit or is recorded in `## Commit Boundary Notes`; tests are co-located with the code they cover, never deferred. Watch for scope breaking the sizing — see the safety valve in [sizing.md](../references/sizing.md).
6. **Approval gate** — present the task count, a short execution order, 1-2 execution risks, then ask *"Move to implement?"*
7. **Update the active feature's `STATE.md ## Progress`** at the approval gate — phase and next step. When report findings were processed, clear the consumed source from `Findings`; keep any other source. Set `tasks.md` to `status: ready`. See [memory.md](../references/memory.md).

Default commit boundary is 1 task = 1 commit; document any grouping or split in `## Commit Boundary Notes` — the fact only, no long justification.

## Template: `tasks.md`

ALWAYS use this exact template structure. Conditional sections appear only when their trigger is met.

```markdown
---
name: {slug}
spec: .artifacts/specs/{slug}/spec.md
design: .artifacts/specs/{slug}/design.md
status: draft
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

## Commit Boundary Notes <!-- conditional: when 1 task ≠ 1 commit -->
- T-1 + T-2 → single commit "scaffold checkout module"
- T-7 → split into 2 commits for review: backend + frontend
```

MUST NOT contain: new architecture (it belongs in design.md), observable behavior or acceptance criteria (they belong in spec.md), or component design. Tasks sequence and verify existing decisions; they never introduce them. The `Discrimination:` field applies to conditionals, validations, calculations, and the ACs of a P-1 story — if the test would still pass with the logic removed, it is weak.
