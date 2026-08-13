# Tasks

Turn `spec.md` and `design.md` into a `tasks.md` — atomic steps, dependencies, per-task tests, gates, and commit boundaries. Answers WHEN / ORDER.

## When to Use

When breaking a change into tasks or product slices, or producing the task breakdown for a designed feature. Runs at Medium and up; Small skips it.

## Workflow

1. **Resolve feature** — find the active `spec.md` and read the active feature's `STATE.md ## Progress` before loading `design.md`. If `Phase` points to `specify` or `design`, stop and report that phase whatever `Findings` names — a report routed back to the contract or the design is corrected in that artifact, never with a task. If `Phase` points to `tasks` and `Findings` names `validate` or `audit`, triage that report before loading downstream artifacts. Require `spec.md` and `design.md` at `status: ready`; if either phase is not ready, stop and run that phase. Otherwise resolve `design.md` and continue.
2. **Load context** — read the active feature's `STATE.md`, the spec, the design, and the root `CONTEXT.md`. When `Phase` points to `tasks` and `Findings` names `validate`, read `validate.md`; when it names `audit`, read `audit.md`. Verify each reported finding before adding or adjusting a correction task. These are context only: upstream prose never crosses into `tasks.md` (the template's MUST-NOT names it) — tasks reference `AC-N.M` in `Covers`, never restate its text.
3. **Build the task list** — when editing an existing `tasks.md`, set its status to `draft` before writing. If `Findings` names a report, preserve the existing `T-N` sequence and create or adjust tasks for verified findings. Otherwise break into atomic tasks in execution order (top-to-bottom). A task is atomic when it has one clear objective, is verifiable by one gate, and needs at most ~1 new design decision. It may touch several files if the changes are mechanical and dependent. Generate `Builds` from the approved design: name every component whose responsibility the task creates or changes, using its exact component heading. Separate multiple names with commas when an atomic change crosses components. Use `Builds: none` only for groundwork that creates or changes no component. Do not copy component, interface, or endpoint contracts into `tasks.md`. Use `Depends on` as the only dependency source; declare dependencies before the dependent task, reject self-dependencies and cycles, then derive `## Sequence` as graph waves. Group tasks under the product slice they serve, contiguously. A groundwork task uses `Slice: none`. A slice is `S-N` from the spec, not a tracker story. When a slice's tasks reveal it is not one vertical slice ([slicing.md](../references/slicing.md)), set `STATE.md` to `Phase: specify` and `Next: specify`; never split its task list at an arbitrary index to compensate.
4. **Assign contract coverage** — assign every AC to exactly one task through `Covers`, and name the runner-level test case that proves the complete scenario. A `Scenario Outline` test covers every row in its `Examples` table. A task with no AC is groundwork and may omit `Covers` and `Test`.
5. **Self-check** — read for what no script can settle: boundaries hold — nothing from spec or design leaked in, per the template's MUST-NOT ([discriminator.md](../references/discriminator.md)); no task introduces a decision instead of sequencing one — set `STATE.md` to `Phase: design` and `Next: design` when the design has not made the decision; every design component appears in at least one `Builds` field; every non-groundwork task names one or more exact component headings, and `Builds: none` appears only on groundwork; `Depends on` is the only dependency source; every task appears exactly once in `Sequence`, and each wave matches the derived graph; every AC has exactly one `Covers` owner and a named test case that proves its complete scenario; every verified report finding has a correction task or an explicit reason it needs no task; every task is one commit or is recorded in `## Commit Boundary Notes`; tests are co-located with the code they cover, never deferred. Watch for scope breaking the sizing — see the safety valve in [sizing.md](../references/sizing.md).

   Then run `python3 ${CLAUDE_SKILL_DIR}/scripts/lint_artifact.py tasks .artifacts/specs/{slug}` over the text the reading produced — it settles structure, presence, the dependency graph, and cross-file references, and it reads last because the pass above edits the breakdown. Fix every error and run it again, up to three passes; after the third, stop, record the standing error in `STATE.md ## Blockers`, and leave `tasks.md` at `draft`. A warning never blocks — act on it, or keep what it names as deliberate and say which at the approval gate.
6. **Approval gate** — present the task count, a short execution order, 1-2 execution risks, then ask *"Move to implement?"* Name anything the run wrote outside the ignored folders and suggest the commit — see [memory.md](../references/memory.md).
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

## Sequence

| Wave | Tasks |
|------|-------|
| W-1 | T-1, T-2 |
| W-2 | T-3 |

## Task List

### [ ] T-1: {title}
- **Slice:** S-N — {title} <!-- use `none` for groundwork -->
- **Description:** {what to do}
- **Builds:** [exact component name, or comma-separated names] <!-- use `none` only for groundwork that changes no component -->
- **Depends on:** T-N, T-M (none if first)
- **Covers:** `AC-N.M` <!-- conditional: omit for groundwork tasks -->
- **Test:** `{file}` — `{runner test case}` <!-- required when Covers is present -->
- **Gate:** {command} | {descriptive check when no command exists}
- **Done when:** {observable result}

### [ ] T-2: ...

## Commit Boundary Notes <!-- conditional: when 1 task ≠ 1 commit -->
- T-1 + T-2 → single commit "scaffold checkout module"
- T-7 → split into 2 commits for review: backend + frontend
```

MUST NOT contain: new architecture (it belongs in design.md), observable behavior or acceptance criteria (they belong in spec.md), or component design. Tasks sequence and verify existing decisions; they never introduce them. `Builds` carries only exact component names from `design.md`, separated by commas when a task changes more than one component, or `none` for groundwork that changes no component. Component, interface, and endpoint contracts remain in `design.md`. `Depends on` is the only normative ordering field. `Sequence` is a checked projection of that dependency graph, not a second source of truth. `Covers` carries only the AC identifier; the scenario and its expected outcome remain in `spec.md`. `Test` names the runner-level case that proves the complete scenario; discrimination is checked by `audit`, not by a task field.
