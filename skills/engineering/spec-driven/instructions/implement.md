# Implement

Execute the tasks in `tasks.md` per `design.md` and `spec.md`. No dedicated artifact — progress lives in `tasks.md`, session state in `STATE.md`.

## When to Use

When implementing a named task, range, or user story, or executing a whole feature. Medium and up run in an isolated subagent; Small runs inline from the one-liner.

## Workflow

1. **Resolve feature** — find the active `.artifacts/specs/{date}-{slug}/` and load `spec.md`, `design.md`, `tasks.md`, `discuss.md` (if present), `.artifacts/CONTEXT.md`, `.artifacts/STATE.md`, and `AGENTS.md` / `CLAUDE.md`.
2. **Create branch** — from the spec's `branch:` field: `git switch -c {branch} 2>/dev/null || git switch {branch}`. Skip if already on it or on `main`/`master`.
3. **Update status** — if `status` is `draft`, set it to `in-progress` in `spec.md`.
4. **Run each task sequentially** — Before / During / After below.
5. **After the last task** — run the full-feature gates, then present the approval gate: tasks done, commits, a coverage summary, then ask *"Move to audit?"* Audit runs automatically after approval; UAT runs if `user-facing: true`.

Small ends inline after the one-liner — no approval gate, no audit prompt; the inline verify is the check. If the change turns out to need formal visual validation, the safety valve raises it to Medium and the full pipeline applies.

### Per task — Before

1. Read the task and confirm its `Depends on:` are complete.
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
5. **Commit** if 1 task = 1 commit, per [commit-conventions.md](../references/commit-conventions.md).
6. Announce: *"T-N done. Committing — stop me to review."*
7. Update `STATE.md ## Handoff` if the session is ending.

## Commits

1 task = 1 commit by default; follow `## Commit Boundary Notes` when it groups or splits. Fixes are always a new commit — never `git commit --amend`, never `--no-verify`. Message format in [commit-conventions.md](../references/commit-conventions.md).

## Subagent dispatch

Medium/Large/Complex run in a subagent handed a narrow selection (a task, a range `[T-1..T-5]`, a story, or `--all`) with no conversation history. It runs the tasks sequentially, one commit each, and returns a compact summary: tasks done, commits, gates, blockers. The main agent resumes for the approval gate.

## Design-gap recovery

When a task is correct per `design.md` but the design itself is wrong (contract, default, wiring, assumption):

| Gap size | Action |
|----------|--------|
| Small (isolated, does not invalidate a prior commit) | Fix in place, new commit |
| Large (invalidates a prior commit's premise) | `git reset --soft` to that commit, re-commit corrected |

Record it: feature-local → a `## Design Gaps Discovered During Implementation` section in `design.md`; durable cross-feature fact → `.artifacts/CONTEXT.md
## Gotchas`. If the gap breaks the scope, apply the safety valve
([sizing.md](../references/sizing.md)) — stop and raise the level, never push through.
