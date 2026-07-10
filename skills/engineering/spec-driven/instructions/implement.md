# Implement

Execute the tasks in `tasks.md` per `design.md` and `spec.md`. No dedicated artifact — task-level progress lives in `tasks.md` checkboxes, the coarse pointer in `STATE.md`.

## When to Use

When implementing a named task, range, or user story, or executing a whole feature. Medium and up run in an isolated subagent; Small runs inline from the one-liner.

## Workflow

Medium and up — Small has none of these artifacts; see [Small inline](#small-inline) below.

1. **Resolve feature** — find the active `.artifacts/specs/{slug}/` and load `spec.md`, `design.md`, `tasks.md`, `discuss.md` (if present), `.artifacts/CONTEXT.md`, and `AGENTS.md` / `CLAUDE.md`. `STATE.md ## Progress` is read per task in the Before step.
2. **Create branch** — from the spec's `branch:` field. Already on it → skip. On `main`/`master` → create: `git switch -c {branch} 2>/dev/null || git switch {branch}`. On an unrelated branch → stop and ask before branching, so the feature never carries foreign commits.
3. **Update status** — if `status` is `draft`, set it to `in-progress` in `spec.md`.
4. **Dispatch tasks** — hand the selection (a task, a range `[T-1..T-5]`, a story, or `--all`) to the isolated subagent per [Subagent dispatch](#subagent-dispatch); it runs each task through Before / During / After and returns the compact summary.
5. **After the last task** — run the whole test suite plus the project quality gates (lint, typecheck), then present the approval gate: tasks done, commits, a coverage summary, then ask *"Move to audit?"* Audit runs automatically after approval; UAT runs if `user-facing: true`.

### Small inline

No `spec.md` exists — work from the one-liner:

1. **Branch** — same rule as step 2, with a slug derived from the one-liner.
2. **Change** — make the edit; run the nearest gate (test, lint, or a described check).
3. **Commit** — per [commit-conventions.md](../references/commit-conventions.md).

No approval gate, no audit — the inline verify is the check. If the change turns out to need formal visual validation, the safety valve raises it to Medium and the full pipeline applies.

### Per task — Before

1. Read `STATE.md ## Progress` to see what is done and what remains, then read the task and confirm its `Depends on:` are complete.
2. Load the relevant slices of `spec.md` and `design.md`.
3. State the files to touch, the AC / `Done when` this task satisfies, and the main risks.

### Per task — During

1. Write or update the task's tests, derived from the spec, not the code.
2. Implement per `design.md` and `spec.md` — the minimum to satisfy `Done when`.
3. Out-of-scope discovery: cross-feature → `.artifacts/CONTEXT.md ## Gotchas`; feature-local → `STATE.md ## Notes`. See [memory.md](../references/memory.md).

### Per task — After

1. Run the task's **Gate** (command or descriptive check).
2. Run project quality gates (lint, typecheck) if fast.
3. Run **verify** (mental — no artifact): design adherence, AC coverage against the Coverage Matrix, pattern adherence, and the discrimination check when the task carries a `Discrimination:` field. Any "no" → fix before marking done.
4. Flip the task's heading checkbox in `tasks.md`: `### [ ] T-N:` → `### [x] T-N:`.
5. **Commit** — 1 task = 1 commit by default; follow `## Commit Boundary Notes` when it groups or splits. Fixes are always a new commit; message format and prohibitions in [commit-conventions.md](../references/commit-conventions.md).
6. Update `STATE.md ## Progress` — point `Next` at the following task, or at the audit after the last.

## Subagent dispatch

Medium/Large/Complex run in a subagent handed a narrow selection (a task, a range `[T-1..T-5]`, a story, or `--all`) with no conversation history. It runs the tasks sequentially, one commit each, and returns a compact summary: tasks done, commits, gates, blockers. The main agent resumes for the approval gate.

## Design-gap recovery

When a task is correct per `design.md` but the design itself is wrong (contract, default, wiring, assumption):

| Gap size | Action |
|----------|--------|
| Small (isolated, does not invalidate a prior commit) | Fix in place, new commit |
| Large (invalidates a prior commit's premise) | Stop the run and return it as a blocker. The main agent proposes the recovery — `git reset --soft` to that commit, re-commit corrected — and executes only with explicit user confirmation, only on the feature branch, never after push |

Record it: feature-local → a `## Design Gaps Discovered During Implementation` section in `design.md`; durable cross-feature fact → `.artifacts/CONTEXT.md ## Gotchas`. If the gap breaks the scope, apply the safety valve ([sizing.md](../references/sizing.md)) — stop and raise the level, never push through.
