# Tasks

Turn `spec.md` and `design.md` into a `tasks.md` — atomic steps, dependencies, per-task tests, gates, and commit boundaries. Answers WHEN / ORDER.

## When to Use

When breaking a change into tasks or product slices, or producing the task breakdown for a designed feature. Runs for every feature that produced a `design.md`.

Resolve `<this-skill>` to the directory this `SKILL.md` was read from before running any bundled script below.

## Workflow

1. **Resolve feature** — resolve `.artifacts/specs/<slug>/` per [memory.md](../references/memory.md) and read its `STATE.md ## Progress` before loading `design.md`. If `Phase` points to `specify` or `design`, stop and report that phase whatever `Findings` names — a report routed back to the contract or the design is corrected in that artifact, never with a task. If `Phase` points to `tasks` and `Findings` names `validate`, triage that report before loading downstream artifacts. Require `spec.md` and `design.md` at `status: ready`; if either phase is not ready, stop and run that phase. Otherwise resolve `design.md` and continue.
2. **Load context** — read the feature's `STATE.md`, the spec, the design, and the root `PROJECT.md`. When `Phase` points to `tasks` and `Findings` names `validate`, read `validate.md`. Verify each reported finding before adding or adjusting a correction task. These are context only: upstream prose never crosses into `tasks.md` (the template's MUST-NOT names it) — tasks reference `AC-N.M` in `Covers`, never restate its text.
3. **Build the task list** — when editing an existing `tasks.md`, set its status to `draft` before writing, keep every ticked task ticked, and rebuild every `Slice` and `Covers` reference from the current spec. Until a task is ticked, renumber tasks from `T-1` to close any gap. From the first ticked task on, never renumber: give a new task the next unused number, and mark a removed task in place as `### [-] T-N: ~~[title]~~ removed` with a `Reason:` line under it. If `Findings` names a report, create or adjust tasks for verified findings. Otherwise break into atomic tasks in execution order (top-to-bottom). Cut a task at the smallest change that leaves the tree green on its own: build, types, linter, formatter, and tests pass at the end of it, and its commit stands without the next task. Name one outcome per task; two outcomes joined by "and" are two tasks. The commit boundary bounds the cut from below: tasks that would land as one commit under one slice are one task, so ask of every adjacent pair whether a reviewer would read them as one change before writing them as two. What stays separate defaults to 1 task = 1 commit; record in `## Commit Boundary Notes` the split, and the grouping that no single task can carry because its tasks serve different slices — the fact only, no long justification. A task may touch several files when the changes are mechanical and dependent. Never write as a task what the repository already does on its own — formatting, a commit hook, a generated client — or an activity spread across the whole feature, such as writing the tests or adding the types. Generate `Builds` from the approved design: name every component whose purpose the task creates or changes, using its exact component heading. Separate multiple names with commas when an atomic change crosses components. Use `Builds: none` only for groundwork that creates or changes no component. Do not copy component, interface, or endpoint contracts into `tasks.md`. Use `Depends on` as the only dependency source; declare dependencies before the dependent task, reject self-dependencies and cycles — load [ordering.md](../references/ordering.md) for the dependency graph and the dispatch units. Group tasks under the product slice they serve, contiguously. A groundwork task uses `Slice: none` and comes before every slice task, unless it depends on one. A slice is `S-N` from the spec, not a tracker story. When a slice's tasks reveal it is not one vertical slice ([slicing.md](../references/slicing.md)) — it carries two benefits, it carries the same benefit as another slice reaching a different consumer, which shows up as slices whose whole delivery is one task each, or one change closes criteria of two slices — set `STATE.md` to `Phase: specify` and `Next: specify`; never split its task list at an arbitrary index to compensate.
4. **Assign contract coverage** — assign every AC to exactly one task through `Covers`, and name the runner-level test case that proves the complete scenario. A task covers several criteria only when they sit under one slice and one indivisible change closes them all, with no commit among them standing alone in review. `Slice` names one `S-N`, so criteria under different slices stay separate tasks however close their code sits — the commit boundary is what ships them together. Criteria that each land on their own stay separate tasks, whatever file they touch. A criterion goes only to a task whose change closes it; when that change sits in another slice's task, the cut is wrong — set `STATE.md` to `Phase: specify` and `Next: specify`. Before naming a case, confirm the project's test runner and record it once in `## Scope` as `Runner:` — its command, or `none — [why the project has none]`. With a runner, every covered criterion carries its own `Test` line, in the order `Covers` names them. A `Scenario Outline` test covers every row in its `Examples` table; when the rows land in several tasks, the task that completes the last row covers the criterion. Where the runner does not reach an outcome — a visual result, an external service, a timing no suite exercises — write `Test: none — [what the runner does not reach]` rather than a case that will not exist. With `Runner: none`, tasks carry no `Test` line. An outcome no runner reaches, for either reason, is checked by hand on a `user-facing` feature, through the task's `Gate` or `Done when`; on any other feature it has no observable this system owns, so set `STATE.md` to `Phase: specify` and `Next: specify`. A task with no AC is groundwork and may omit `Covers` and `Test`.
5. **Self-check** — read for what no script can settle: boundaries hold — nothing from spec or design leaked in, per the template's MUST-NOT ([discriminator.md](../references/discriminator.md)); no task introduces a decision instead of sequencing one — set `STATE.md` to `Phase: design` and `Next: design` when the design has not made the decision; every design component appears in at least one `Builds` field; every non-groundwork task names one or more exact component headings, and `Builds: none` appears only on groundwork; `Depends on` is the only dependency source; every AC has exactly one `Covers` owner and, unless `Runner: none`, either a named test case that proves its complete scenario or a `Test: none` that names what the runner does not reach; on a `user-facing` feature an outcome no runner reaches is not a pendency: its task's `Gate` or `Done when` names the check that replaces the runner; a task covering several criteria closes them in one indivisible change under one slice; every verified report finding has a correction task or a triage entry in `## Findings Triage` naming its report number and one of `resolved by task`, `not actionable`, or `routed to specify/design`; tests are co-located with the code they cover, never deferred.

   Then run `python3 <this-skill>/scripts/lint_artifact.py tasks .artifacts/specs/<slug>` over the text the reading produced — it settles structure, presence, the dependency graph, and cross-file references, and it reads last because the pass above edits the breakdown. Fix every error and run it again, up to three passes; after the third, stop, record the standing error in `STATE.md ## Blockers`, and leave `tasks.md` at `draft`. A warning never blocks — act on it, or keep what it names as deliberate and say which at the approval gate.
6. **Approval gate** — present the path of `tasks.md`, the task count, and the commit count the boundaries produce. The user may reorder only tasks that preserve the dependency graph. Then ask *"Move to implement?"* Name anything the run wrote that the project does not ignore and suggest the commit — see [memory.md](../references/memory.md).
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

**Runner:** `[command that runs the project's tests]` <!-- `none — [why the project has none]` when the project has no test runner -->

## Task List

### [ ] T-1: [title]
- **Slice:** S-N — [title] <!-- use `none` for groundwork -->
- **Description:** [what to do]
- **Builds:** [exact component name, or comma-separated names] <!-- use `none` only for groundwork that changes no component -->
- **Depends on:** T-N, T-M (none if first)
- **Covers:** `AC-N.M` <!-- comma-separated ids when one indivisible change closes several criteria of this task's slice; conditional: omit for groundwork tasks -->
- **Test:** `[file]` — `[runner test case]` <!-- one line per id in Covers, same order; `none — [what the runner does not reach]` for an outcome the runner misses; omit under `Runner: none` -->
- **Gate:** [command] | [descriptive check when no command exists]
- **Done when:** [observable result]

### [ ] T-2: ...

## Findings Triage <!-- conditional: when validate findings were processed -->
- Report #1 — [resolved by task | not actionable | routed to specify/design] — [task id or concrete reason]

## Commit Boundary Notes <!-- conditional: when 1 task ≠ 1 commit -->
- T-1 + T-2 → single commit "scaffold checkout module"
- T-7 → split into 2 commits for review: backend + frontend
```

MUST NOT contain: new architecture (it belongs in design.md), observable behavior or acceptance criteria (they belong in spec.md), or component design. Tasks sequence and verify existing decisions; they never introduce them. `Builds` carries only exact component names from `design.md`, separated by commas when a task changes more than one component, or `none` for groundwork that changes no component. Component, interface, and endpoint contracts remain in `design.md`. `Depends on` is the only normative ordering field. `Covers` carries only AC identifiers of the task's own slice, separated by commas when one indivisible change closes several criteria; the scenario and its expected outcome remain in `spec.md`. `Runner` states the project's test runner once. `Test` names the runner-level case that proves the complete scenario, or `none` with what the runner does not reach, one line per covered criterion, and is absent under `Runner: none`.
