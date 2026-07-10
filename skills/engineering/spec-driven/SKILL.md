---
name: spec-driven
description: >-
  Spec-driven feature development with auto-sized depth. Produces
  spec.md, design.md, tasks.md, and validation.md with requirements
  traceability, and closes with an independent audit tied to Goals and
  acceptance criteria. Depth scales to scope — Small runs inline, Medium and
  up run the full pipeline. Use when planning or specing a feature, turning a
  PRD into a spec, breaking a change into tasks or user stories, designing a
  feature, implementing a named task or user story, auditing goals at a commit
  boundary or before a PR, running UAT on a user-facing change, or discussing
  how to build a feature. Not for diagnosing unknown bugs, authoring standalone
  PRD/RFC/ADR/Design Doc documents, PR/commit mechanics, or PM backlog tracking.
argument-hint: "[T-N] | [T-N..T-M] | [S-N]"
allowed-tools: Bash(git:*) Bash(python3:*) Read Write Edit Grep Glob Task
---

# Spec-Driven Development

Feature development in phases, sized to the change. Light by default; weight only where the scope pays for it. Rigor concentrates in a final independent audit, not in heavy intermediate gates.

## Triggers

- **Specify** ("plan feature", "spec this", "from PRD", "modify feature", "discuss how to build") → [specify.md](instructions/specify.md)
- **Design** ("design this feature", "technical design", "plan the build") → [design.md](instructions/design.md)
- **Tasks** ("create tasks", "break into tasks", "task breakdown") → [tasks.md](instructions/tasks.md)
- **Implement** ("implement task T-1", "implement T-1 to T-4", "implement story S-1", "execute tasks", "implement everything") → [implement.md](instructions/implement.md)
- **Audit** ("audit feature", "validate goals", "verify before PR") → [audit.md](instructions/audit.md)
- **Validate / UAT** ("run UAT", "manual testing", "validate flows") → [validate.md](instructions/validate.md)
- **Archive** ("archive feature", "archive this spec") → [archive.md](instructions/archive.md)

## Workflow

```text
specify → design → tasks → implement → audit → [validate] → done → [archive]
   │        │        │          │          │         │
   │        │        │          │          │         └ only user-facing
   └────────┴────────┴──────────┴──────────┴ Small skips all of this:
                                              one-liner → implement inline
```

Depth follows scope, not phase-skipping above Small — per-scope depth is owned by [sizing.md](references/sizing.md). Small is a one-liner straight to inline implement — no `spec.md`, no audit. Verify is mental, per task, inside implement — never a user phase. Archive is optional housekeeping for done specs — manual, never automatic, never suggested.

## References

Loaded on demand:

- [sizing.md](references/sizing.md) — the four scopes, scope table, safety valve
- [acceptance-criteria.md](references/acceptance-criteria.md) — EARS-lite shapes, `AC-N` tombstones, reshape vs author, `Satisfies`, case convention, calibration against the goal
- [discriminator.md](references/discriminator.md) — WHAT / HOW / WHEN boundaries and leak signals
- [memory.md](references/memory.md) — `CONTEXT.md` and `STATE.md` formats, routing, conflicts
- [lessons.md](references/lessons.md) — lessons layer mechanics (candidate → confirmed)
- [commit-conventions.md](references/commit-conventions.md) — conventional commit message format
- [discovery.md](references/discovery.md) — adaptive discovery, discuss trigger, `discuss.md` template
- `scripts/lessons.py` — run to add, list, promote, normalize, and render lessons

## Artifacts

Every artifact's structure is canonical in the instruction or reference that owns it, inline and marked strict or flexible. Load the owning file before reading any existing file in `.artifacts/` — existing files are context, not structural reference. Templates win on divergence.

A feature lives in `.artifacts/specs/{slug}/` while built and moves to `.artifacts/archive/{created}-{slug}/` only once at `status: done` — the date, taken from the spec's `created:`, is added at archive time, so active folders stay slug-only. Discovery never forages siblings or `archive/` for shape or decisions — the only cross-feature inputs a new feature reads are `.artifacts/CONTEXT.md` and confirmed lessons.

## Status

Minimal machine, single source in `spec.md` frontmatter:

- `draft` — specify/design/tasks created the artifacts.
- `in-progress` — implement started.
- `done` — audit passed (and UAT, if `user-facing`).

## Guidelines

- Separate by purpose: spec = WHAT + WHY, design = HOW, tasks = WHEN.
- Size once, after discovery; default adversarial — when in doubt, size up.
- On a broken scope (a new load-bearing decision, inline steps past ~5), stop and raise a level; never push through in implement.
- 1 task = 1 commit by default; fixes are new commits, never `--amend`.
- Author ≠ auditor — the audit runs as an isolated subagent on the diff.
- Advance by default; ask (discuss) only when the gray area is load-bearing — it changes Goals, ACs, or the approach.

## Anti-Pattern: Forced Full Depth

Running every scope at full depth is process tax. Auto-sizing scales depth, not phases: a mechanical fix is a one-liner, a canonical reapplication runs a light Medium, and only a novel or ambiguous change earns fresh-eyes, approaches, and research. Forcing heavy grounding onto a routine change is the tax to avoid.

## Anti-Pattern: Deferred Verification

Implementing every task first and checking at the end loses the tie between code and its acceptance criteria. Verify is mental and runs after each task; the independent audit runs once at the end. A failed audit becomes fix tasks, not a silent pass.

## Anti-Pattern: Author Auditing Itself

The agent that wrote the code cannot be the one that clears it — it re-reads its own intent, not the behavior. The audit is a fresh subagent handed only the diff, the artifacts, and the tests; it flags gaps and never edits code.
