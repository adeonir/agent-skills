# Tasks

Turn `spec.md` and `design.md` into a `tasks.md` — atomic steps, dependencies, per-task tests, gates, and commit boundaries. Answers WHEN / ORDER.

## When to Use

When breaking a change into tasks or product slices, or producing the task breakdown for a designed feature. Runs for every feature that produced a `design.md`.

## Workflow

1. **Resolve feature** — resolve `.artifacts/specs/<slug>/` per [memory.md](../references/memory.md) and read its `STATE.md ## Progress` before loading `design.md`. If `Phase` points to `specify` or `design`, stop and report that phase whatever `Findings` names — a report routed back to the contract or the design is corrected in that artifact, never with a task. If `Phase` points to `tasks` and `Findings` names `validate` or `audit`, triage that report before loading downstream artifacts. Require `spec.md` and `design.md` at `status: ready`; if either phase is not ready, stop and run that phase. Otherwise resolve `design.md` and continue.
2. **Load context** — read the feature's `STATE.md`, the spec, the design, and the root `CONTEXT.md`. When `Phase` points to `tasks` and `Findings` names `validate`, read `validate.md`; when it names `audit`, read `audit.md`. Verify each reported finding before adding or adjusting a correction task. These are context only: upstream prose never crosses into `tasks.md` (the template's MUST-NOT names it) — tasks reference `AC-N.M` in `Covers`, never restate its text.
3. **Build the task list** — when editing an existing `tasks.md`, set its status to `draft` before writing, keep every ticked task ticked, give a new task the next unused number, and never renumber. If `Findings` names a report, create or adjust tasks for verified findings. Otherwise break into atomic tasks in execution order (top-to-bottom). Cut a task at the smallest change that leaves the tree green on its own: build, types, linter, formatter, and tests pass at the end of it, and its commit stands without the next task. Name one outcome per task; two outcomes joined by "and" are two tasks. The commit boundary bounds the cut from below: tasks that would land as one commit under one slice are one task, so ask of every adjacent pair whether a reviewer would read them as one change before writing them as two. What stays separate defaults to 1 task = 1 commit; record in `## Commit Boundary Notes` the split, and the grouping that no single task can carry because its tasks serve different slices — the fact only, no long justification. A task may touch several files when the changes are mechanical and dependent. Never write as a task what the repository already does on its own — formatting, a commit hook, a generated client — or an activity spread across the whole feature, such as writing the tests or adding the types. Generate `Builds` from the approved design: name every component whose purpose the task creates or changes, using its exact component heading. Separate multiple names with commas when an atomic change crosses components. Use `Builds: none` only for groundwork that creates or changes no component. Do not copy component, interface, or endpoint contracts into `tasks.md`. Use `Depends on` as the only dependency source; declare dependencies before the dependent task, reject self-dependencies and cycles, then derive `## Sequence` as graph waves. Group tasks under the product slice they serve, contiguously. A groundwork task uses `Slice: none`. A slice is `S-N` from the spec, not a tracker story. When a slice's tasks reveal it is not one vertical slice ([slicing.md](../references/slicing.md)) — it carries two benefits, or it carries the same benefit as another slice reaching a different consumer, which shows up as slices whose whole delivery is one task each — set `STATE.md` to `Phase: specify` and `Next: specify`; never split its task list at an arbitrary index to compensate.
4. **Assign contract coverage** — assign every AC to exactly one task through `Covers`, and name the runner-level test case that proves the complete scenario. A task covers several criteria only when they sit under one slice and one indivisible change closes them all, with no commit among them standing alone in review. `Slice` names one `S-N`, so criteria under different slices stay separate tasks however close their code sits — the commit boundary is what ships them together. Criteria that each land on their own stay separate tasks, whatever file they touch. Every covered criterion carries its own `Test` line, in the order `Covers` names them. A `Scenario Outline` test covers every row in its `Examples` table. Before naming a case, confirm the project has a runner that reaches the outcome. Where none does — a visual result, an external service, a timing no suite exercises — write `Test: none — [what no runner reaches]` rather than a case that will not exist; on a `user-facing` feature `validate` settles that criterion, and on any other the outcome has no observable this system owns, so set `STATE.md` to `Phase: specify` and `Next: specify`. A task with no AC is groundwork and may omit `Covers` and `Test`.
5. **Self-check** — read for what no script can settle: boundaries hold — nothing from spec or design leaked in, per the template's MUST-NOT ([discriminator.md](../references/discriminator.md)); no task introduces a decision instead of sequencing one — set `STATE.md` to `Phase: design` and `Next: design` when the design has not made the decision; every design component appears in at least one `Builds` field; every non-groundwork task names one or more exact component headings, and `Builds: none` appears only on groundwork; `Depends on` is the only dependency source; every task appears exactly once in `Sequence`, and each wave matches the derived graph; when the linter reports a canonical sequence, copy that projection instead of repairing waves by intuition; every AC has exactly one `Covers` owner, and either a named test case that proves its complete scenario or a `Test: none` that names what no runner reaches; surface every `Test: none` as a pendency at the approval gate; a task covering several criteria closes them in one indivisible change under one slice; every verified report finding has a correction task or a triage entry in `## Findings Triage` naming its report number and one of `resolved by task`, `not actionable`, or `routed to specify/design`; tests are co-located with the code they cover, never deferred.

   Then run `python3 <this-skill>/scripts/lint_artifact.py tasks .artifacts/specs/<slug>` over the text the reading produced — it settles structure, presence, the dependency graph, and cross-file references, and it reads last because the pass above edits the breakdown. Fix every error and run it again, up to three passes; after the third, stop, record the standing error in `STATE.md ## Blockers`, and leave `tasks.md` at `draft`. A warning never blocks — act on it, or keep what it names as deliberate and say which at the approval gate.
6. **Approval gate** — present the path of `tasks.md`, the task count, the commit count the boundaries produce, the wave sequence derived by the linter, and every `Test: none` pendency. The user may reorder only tasks that preserve the dependency graph. Then ask *"Move to implement?"* Name anything the run wrote that the project does not ignore and suggest the commit — see [memory.md](../references/memory.md).
7. **Update the feature's `STATE.md ## Progress`** at the approval gate — phase and next step. When report findings were processed, clear the consumed source from `Findings`; keep any other source. Set `tasks.md` to `status: ready`. If `.artifacts/` is ignored, these artifact updates are local state and are not part of an implementation commit. See [memory.md](../references/memory.md).

## Template: `tasks.md`

ALWAYS use this exact template structure. Conditional sections appear only when their trigger is met.

```markdown
---
name: <slug>
spec: .artifacts/specs/<slug>/spec.md
design: .artifacts/specs/<slug>/design.md
status: draft
---

# Tasks: [Feature]

## Scope
[In-scope / out-of-scope for this tasks.md — one paragraph.]

## Sequence

| Wave | Tasks |
|------|-------|
| W-1 | T-1, T-2 |
| W-2 | T-3 |

## Task List

### [ ] T-1: [title]
- **Slice:** S-N — [title] <!-- use `none` for groundwork -->
- **Description:** [what to do]
- **Builds:** [exact component name, or comma-separated names] <!-- use `none` only for groundwork that changes no component -->
- **Depends on:** T-N, T-M (none if first)
- **Covers:** `AC-N.M` <!-- comma-separated ids when one indivisible change closes several criteria of this task's slice; conditional: omit for groundwork tasks -->
- **Test:** `[file]` — `[runner test case]` <!-- one line per id in Covers, same order; `none — [what no runner reaches]` when the project has no runner for the outcome -->
- **Gate:** [command] | [descriptive check when no command exists]
- **Done when:** [observable result]

### [ ] T-2: ...

## Findings Triage <!-- conditional: when validate or audit findings were processed -->
- Report #1 — [resolved by task | not actionable | routed to specify/design] — [task id or concrete reason]

## Commit Boundary Notes <!-- conditional: when 1 task ≠ 1 commit -->
- T-1 + T-2 → single commit "scaffold checkout module"
- T-7 → split into 2 commits for review: backend + frontend
```

MUST NOT contain: new architecture (it belongs in design.md), observable behavior or acceptance criteria (they belong in spec.md), or component design. Tasks sequence and verify existing decisions; they never introduce them. `Builds` carries only exact component names from `design.md`, separated by commas when a task changes more than one component, or `none` for groundwork that changes no component. Component, interface, and endpoint contracts remain in `design.md`. `Depends on` is the only normative ordering field. `Sequence` is a checked projection of that dependency graph, not a second source of truth. `Covers` carries only AC identifiers of the task's own slice, separated by commas when one indivisible change closes several criteria; the scenario and its expected outcome remain in `spec.md`. `Test` names the runner-level case that proves the complete scenario, or `none` with what no runner reaches, one line per covered criterion; discrimination is checked by `audit`, not by a task field.
