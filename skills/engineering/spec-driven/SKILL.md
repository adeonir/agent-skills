---
name: spec-driven
description: "Spec-driven feature development with auto-sized depth. Produces spec.md, design.md, tasks.md, audit.md, and validate.md with requirements traceability. Depth scales to scope — Small runs inline, Medium and up run the full pipeline. Use when planning or specing a feature, turning a PRD into a spec, breaking a change into tasks or product slices, designing a feature, implementing a named task or product slice, auditing goals at a commit boundary or before a PR, running UAT on a user-facing change, or discussing how to build a feature. Not for diagnosing unknown bugs, authoring standalone PRD/RFC/ADR/Design Doc documents, PR/commit mechanics, or PM backlog tracking."
argument-hint: "[T-N] | [T-N..T-M] | [S-N] | [S-N..S-M] | [W-N] | [W-N..W-M]"
allowed-tools: Bash(git:*) Bash(python3:*) Read Write Edit Grep Glob Task
---

# Spec-Driven Development

Feature development in phases, sized to the change. Light by default; weight only where the scope pays for it. Rigor comes from independent reading — the artifacts that settle decisions are checked by an agent that did not write them, and the diff by a final audit — never from heavy gates the author runs over its own work.

## Triggers

- **Specify** ("plan feature", "spec this", "from PRD", "modify feature", "discuss how to build") → [specify.md](instructions/specify.md)
- **Design** ("design this feature", "technical design", "plan the build") → [design.md](instructions/design.md)
- **Tasks** ("create tasks", "break into tasks", "task breakdown") → [tasks.md](instructions/tasks.md)
- **Implement** ("implement task T-1", "implement T-1 to T-4", "implement slice S-1", "implement wave W-1", "execute tasks", "implement everything") → [implement.md](instructions/implement.md)
- **Audit** ("audit feature", "validate goals", "verify before PR") → [audit.md](instructions/audit.md)
- **Validate / UAT** ("run UAT", "manual testing", "validate flows") → [validate.md](instructions/validate.md)
- **Archive** ("archive feature", "archive this spec") → [archive.md](instructions/archive.md)

## Workflow

```text
specify → design → tasks → implement → [validate] → [audit] → [archive]
   └────────┴────────┴──────────┴──────────┴ Small skips all of this: one-liner → branch → implement inline
```

Depth follows scope, not phase-skipping above Small — per-scope depth is owned by [sizing.md](references/sizing.md). Small is a one-liner straight to inline implement on its own branch — no `spec.md`, no audit. Verify is mental, per task, inside implement — never a user phase. Validate and audit are optional. Archive is manual housekeeping for a feature in any state — never automatic or suggested.

## References

Loaded on demand:

- [sizing.md](references/sizing.md) — the four scopes, scope table, safety valve
- [acceptance-criteria.md](references/acceptance-criteria.md) — the Gherkin form, `AC-N.M` identity, reshape vs author, `Serves` and `Satisfies`, case convention, calibration against the goal
- [discriminator.md](references/discriminator.md) — WHAT / HOW / WHEN boundaries and leak signals
- [slicing.md](references/slicing.md) — vertical slice vs horizontal, the two-benefit split
- [ordering.md](references/ordering.md) — task dependency graph, derived waves, and dispatch units
- [simplicity.md](references/simplicity.md) — the architecture ladder, chained necessity as the signal of a wrong root, verifying a simplification is real before it becomes a decision
- [research-cache.md](references/research-cache.md) — the cached-finding template, the basis that makes an entry falsifiable, the rule that voids a stale one
- [memory.md](references/memory.md) — root `CONTEXT.md`, per-feature `STATE.md`, and signal routing
- [lessons.md](references/lessons.md) — signal and lesson contracts (candidate → confirmed → quarantined)
- [commit-conventions.md](references/commit-conventions.md) — conventional commit message format
- [discovery.md](references/discovery.md) — adaptive discovery, when a gray area goes to the user, where a resolution lands
- `scripts/signals.py` — run to add, resolve, list, and normalize feature signals
- `scripts/lessons.py` — run to add, list, penalize, and normalize lessons
- `scripts/select_tasks.py` — run to select incomplete tasks by task, slice, or wave
- `scripts/lint_artifact.py` — run last in each phase's self-check to settle structure, presence, and cross-file references; an error blocks `ready`, a warning never does

## Artifacts

Every artifact's structure is canonical in the instruction or reference that owns it, inline and marked strict or flexible. Load the owning file before reading any existing file in `.artifacts/` — existing files are context, not structural reference. Templates win on divergence.

A feature lives in `.artifacts/specs/{slug}/` while active and moves to `.artifacts/archive/{created}-{slug}/` only when the user explicitly archives it. The date, taken from the spec's `created:`, is added at archive time, so active folders stay slug-only. Discovery never forages siblings or `archive/` for shape or decisions — the only cross-feature inputs a new feature reads are the root `CONTEXT.md` and confirmed lessons.

## Status

Artifact states are stored in the owning artifact:

- `spec.md`: `draft | ready`.
- `design.md`: `draft | ready`.
- `tasks.md`: `draft | ready | in-progress | done`.
- `validate.md`: `PASS | FAIL | BLOCKED`.
- `audit.md`: `PASS | FAIL | BLOCKED`.

`implement` uses the state in `tasks.md`; it never changes `spec.md`. The active feature's `STATE.md` stores phase progress, blockers, and the report routing that sends findings to task triage.

`STATE.md` is the phase router. Read `Phase` and `Next` before loading downstream artifacts; when it points to an earlier phase, stop and report that phase. Do not infer a new run from artifact differences or an old status.

## Guidelines

- Separate by purpose: spec = WHAT + WHY, design = HOW, tasks = WHEN.
- Size once, after discovery; default adversarial — when in doubt, size up.
- On a broken scope (a new load-bearing decision, inline steps past ~5), stop and raise a level; never push through in implement.
- 1 task = 1 commit by default; fixes are new commits, never `--amend`.
- Author ≠ auditor — `spec.md` and `design.md` are peer-checked by a subagent that did not write them, and the audit runs as an isolated subagent on the diff.
- Advance by default; ask only when the gray area is load-bearing — it changes Goals, ACs, or the approach.

## Anti-Pattern: Forced Full Depth

Running every scope at full depth is process tax. Auto-sizing scales depth, not phases: a mechanical fix is a one-liner, a canonical reapplication runs a light Medium, and only a novel or ambiguous change earns approaches and research. Forcing heavy grounding onto a routine change is the tax to avoid.

## Anti-Pattern: Deferred Verification

Implementing every task first and checking at the end loses the tie between code and its acceptance criteria. Verify is mental and runs after each task; the independent audit runs once at the end. A failed audit becomes fix tasks, not a silent pass.

## Anti-Pattern: Author Auditing Itself

The agent that wrote the code cannot be the one that clears it — it re-reads its own intent, not the behavior. The audit is a fresh subagent handed only the diff, the artifacts, and the tests; it flags gaps and never edits code. The same holds one phase at a time: `spec.md` and `design.md` are each peer-checked by a subagent handed the artifact and the inputs it was written from, never the author's reasoning about it. `tasks.md` earns no reader of its own — it settles nothing the code does not re-test.
