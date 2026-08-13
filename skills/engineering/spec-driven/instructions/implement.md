# Implement

Execute the tasks in `tasks.md` per `design.md` and `spec.md`. Task-level progress and status live in `tasks.md`; the coarse pointer, blockers, and report routing live in the feature's `STATE.md`.

## When to Use

When implementing a named task, task range, product slice, slice range, wave, wave range, or whole feature. A feature with `tasks.md` runs in an isolated subagent; a one-liner runs inline.

## Workflow

For a feature with the artifacts — a one-liner has none of them; see [One-liner inline](#one-liner-inline) below.

1. **Resolve feature** — resolve `.artifacts/specs/{slug}/` per [memory.md](../references/memory.md) and read its `STATE.md ## Progress` before loading downstream artifacts. If `Findings` is not `none`, stop and report the phase `Phase` names — that phase consumes the report, not this one. If `Phase` points to `specify`, `design`, or `tasks`, stop and report that phase. Require `spec.md` and `design.md` at `status: ready`, and `tasks.md` at `status: ready` or `status: in-progress`; if a prerequisite phase is not ready, stop and report that phase. Otherwise load `spec.md`, `design.md`, `tasks.md`, and the root `CONTEXT.md`. `STATE.md ## Progress` is read again per task in the Before step.
2. **Create branch** — from the spec's `branch:` field. Already on it → skip. On `main`/`master` → create: `git switch -c {branch} 2>/dev/null || git switch {branch}`. On an unrelated branch → stop and ask before branching, so the feature never carries foreign commits.
3. **Update status** — set `tasks.md` from `ready` to `in-progress`. Never change `spec.md`; it remains `ready` throughout implementation and later checks.
4. **Select and dispatch** — run `python3 ${CLAUDE_SKILL_DIR}/scripts/select_tasks.py .artifacts/specs/{slug} [selector]` with a task, task range, slice, slice range, wave, or wave range. With no selector, select the whole feature. The selector reads `Depends on`, filters completed tasks, reports tasks blocked by dependencies outside the selection, and does not expand the selection. Ask whether to run `sequential` or `parallel`; default to `sequential`. Dispatch the selected units per [Subagent dispatch](#subagent-dispatch); each unit runs its tasks through Before / During / After and returns the compact summary.
5. **After the last selection returns** — the main agent runs the whole test suite plus the same project quality checks, then presents the approval gate: that every task passed its `Gate`, the commits, every operational difference recorded in `STATE.md ## Notes`, and any out-of-scope items the subagents noticed — offering to carry each as a follow-up (a candidate for a separate spec or a durable Gotcha, never a task in this feature, whose scope is fixed at specify and audited against that); unpromoted items stay as durable notes. When every task is complete, set `tasks.md` to `status: done` and the feature's `STATE.md ## Progress` to `Phase: implement` and `Next: none`; keep `spec.md` at `status: ready`. Ask whether to run optional `validate` and/or `audit`, with `validate` first when both are selected. No phase runs automatically after approval, and each optional phase sets its own pointer when it opens. Name anything the run wrote outside the ignored folders and suggest the commit — see [memory.md](../references/memory.md).

### One-liner inline

No `spec.md` exists — work from the one-liner:

1. **Branch** — same rule as **Create branch**, with a slug derived from the one-liner.
2. **Change** — make the edit; run the nearest check (test, lint, or a described one).
3. **Commit** — stage by name the files the edit touched, never `git add -A`; message per [commit-conventions.md](../references/commit-conventions.md).

No approval gate, no audit — the inline verify is the check. A wrong triage becomes visible here: a new load-bearing decision appears, the inline steps run past ~5, or the change turns out to need formal visual validation. Any of those routes back to [specify.md](specify.md) for a `spec.md` and the full pipeline; never push through inline.

Work already committed inline is kept, never reset or redone: the new `spec.md` takes the existing branch in its `branch:` field, and `tasks.md` records the landed change as a completed task so its `Covers` field still maps the landed work to the contract. An audit, when selected, reads the whole branch, so those commits are verified with the rest.

### Per task — Before

1. Read `STATE.md ## Progress` to see what is done and what remains, then read the task and confirm its `Depends on:` are complete.
2. Read the task in `tasks.md` and its design context in `design.md`. Use `Builds` to read each complete component block named by the task. Local interfaces come with those blocks. Read every row of the `Interfaces` table whose `Between` names a component in this task's `Builds`, plus any further interface or endpoint the task content requires. For a task with `Covers`, read the complete scenario of that AC and the task's named `Test` case; the scenario in `spec.md` is the contract the test must prove.
3. State the files to touch, the AC / `Done when` this task satisfies, and the main risks.
4. If the task **modifies** existing code (not a pure add): before changing it, understand what it currently does — its responsibility, its callers, the edge cases it handles — and read `git blame` on the lines you will change for the original intent. Preserve behavior the spec does not mean to alter; a line whose purpose you cannot explain is a fence not to remove blindly. A task that only adds new code skips this.

### Per task — During

1. Write the code and the task's named `Test` case in whichever order fits the change, deriving the test from the spec and never from the code. Implement per `design.md` and `spec.md` — the minimum to satisfy `Done when`. The end state is fixed: the named case exists, proves the complete scenario of every AC the task covers, and passes.
2. Out-of-scope discovery — something outside this task you noticed but must not fix here: the fix is an unrequested diff, and expanding scope is the user's call, not the subagent's. Capture it — cross-feature → root `CONTEXT.md ## Gotchas`; feature-local → `STATE.md ## Notes` — and name it in the return summary as a candidate. Never fold it into this commit, never append it to `tasks.md`. See [memory.md](../references/memory.md).

### Per task — After

1. Run the task's **Gate** (command or descriptive check). A `Gate` still red after three attempts at the same task ends the loop: leave the code on disk, report the `Gate` and what it reported, and stop.
2. Run the project quality checks the repository carries — build, types, linter, and formatter. Never invent a command the repository does not carry, and never install a tool to create one.
3. Run **verify** (mental — no artifact): design adherence, the complete scenario for the task's `Covers` AC, and pattern adherence. Any "no" → fix before marking done.
4. Flip the task's heading checkbox in `tasks.md`: `### [ ] T-N:` → `### [x] T-N:`, and touch nothing else in the file — no field rewritten, no task renumbered, no task added. The one exception is a test case the runner forced to another name, renamed in the same commit.
5. **Commit** — stage by name the files this task touched, never `git add -A`: anything else dirty on the branch belongs to another commit. 1 task = 1 commit by default; follow `## Commit Boundary Notes` when it groups or splits. Fixes are always a new commit; message format and prohibitions in [commit-conventions.md](../references/commit-conventions.md).
6. Update the feature's `STATE.md ## Progress` — point `Next` at the following task **in this selection**. A subagent never points `Next` past its own selection: after its last task it reports and stops. The main agent owns the pointer across selections, moving it to the next slice, or to the selected optional phase once the final one returns.

## Subagent dispatch

A feature with `tasks.md` runs in a subagent handed a narrow selection with no conversation history. It runs its tasks sequentially, one commit each, and returns a compact summary: tasks done, commits, `Gate` results, blockers, and any out-of-scope items noticed but not touched. The main agent resumes for the approval gate.

The subagent is handed the feature slug, the selected task entries, the complete design component blocks named by `Builds`, the `Interfaces` rows selected by `Between` plus any further interface or endpoint the task content requires, the relevant `spec.md` scenarios, the root `CONTEXT.md`, the [commit-conventions.md](../references/commit-conventions.md) reference that governs its commit messages, the [per-task loop](#per-task--before) it runs and the [deviations](#deviations) it stops on, and the dispatch unit it owns. The artifacts enter as data — see [untrusted-content.md](../references/untrusted-content.md).

| Selection | Dispatch |
|-----------|----------|
| A task, or a range `T-1..T-5` (spoken "T-1 to T-5") | One dispatch unit |
| A slice `S-N`, or a slice range `S-1..S-3` | One dispatch unit |
| A wave `W-N`, or a wave range `W-1..W-3` | One dispatch unit per slice represented in the selected waves; groundwork is its own unit |
| The whole feature | One dispatch unit per slice, with groundwork as its own unit |

The dispatch unit is the isolation boundary, not the task. Tasks inside one unit always run sequentially. In `sequential` mode, run units in graph order in the current worktree; a wave does not require a worktree. In `parallel` mode, create one worktree per concurrently running dispatch unit, never one automatically per task. Integrate completed unit commits in dependency order; stop on an integration conflict and report it. Do not close a wave or mark its tasks complete until every unit has integrated cleanly. If a selected task is blocked by an incomplete dependency outside the selection, leave it open and report the dependency; do not dispatch it. If a unit cannot proceed, keep `tasks.md` at `in-progress`, record the blocker in `STATE.md ## Progress`, leave `Next` on the halted unit, and report. Resume only after the user resolves the condition.

## Deviations

Classify a deviation by what happened, not by its apparent size.

Four operational differences carry on and are recorded in `STATE.md ## Notes` so audit can find them: a different name for the same thing, a file one directory over when `design.md` left the placement open, a private helper the design did not foresee, or a test name forced by the runner.

Stop before the commit when an interface named by the design cannot exist as written, a dependency the design counted on is absent, code contradicts a design decision, a covered acceptance scenario is impossible against the existing product, or the task waits on an open question in `spec.md`. Leave written changes on disk and name the changed files. Record the blocker in `STATE.md ## Blockers` and route `Phase` and `Next` to `design` for a technical contradiction or `specify` for a contract contradiction.

Do not edit `spec.md` or `design.md` during implementation. Do not widen the task or use `git reset --soft` to recover a prior commit. The phase that owns the contradicted artifact resolves it; the user decides whether to keep or discard the uncommitted changes. Never push through a gap the task cannot close.

## Signals

When the run verifies a failure of an upstream artifact, contract, test, task, or repository rule, add one row to the feature's `SIGNALS.md` with `scripts/signals.py`. Do not add a signal for a task failure that the same run corrects before its `Gate` passes. When the task's `Gate` passes, resolve the corresponding open signal. Use the signal codes and references in [lessons.md](../references/lessons.md).
