# Memory and Progress

The two cross-cutting memory files: `CONTEXT.md` (persistent, cross-feature) and `STATE.md` (progress of the active feature). Their formats, when each is read and written, and how conflicts resolve.

## When to Use

At the load-context step of every phase (read), and whenever a phase discovers a durable fact (`CONTEXT.md`) or reaches an approval gate or finishes a task (`STATE.md`).

## The two files

| File | Scope | Updated | Read |
|------|-------|---------|------|
| `.artifacts/CONTEXT.md` | cross-feature, persistent, append-only | when design/implement/audit find a cross-feature lesson | every phase |
| `.artifacts/STATE.md` | active feature | at each approval gate, after each task in implement; cleared at `status: done` | at each phase's load step, and before each task in implement |

`CONTEXT.md` is append-only and cross-feature. `STATE.md` is overwritten at each boundary — it holds only the feature's current progress — and is cleared when the spec reaches `status: done`: at audit PASS, or after UAT approval for user-facing features. Clearing means emptying the whole file — before doing so, promote any still-durable `## Notes` item to `CONTEXT.md ## Gotchas`; the rest dies with the feature. Done is the last boundary this skill owns; pull request and merge happen outside it.

## `CONTEXT.md` format

Here is a sensible default format, but use your best judgment:

```markdown
## Decisions
- {decision} — {rationale}; source: {file:line/doc}; scope: {context}

## Gotchas
- {gotcha} — {context}

## Conventions
- {convention} — {where it applies / why}
```

No mandatory date. No rigid routing rules. Routing by intent: a project-level decision a future feature must follow → `## Decisions`; a real trap found in the code → `## Gotchas`; a normative codebase pattern → `## Conventions`.

MUST NOT contain: feature-local state, progress, or notes — `CONTEXT.md` is knowledge shared across features; the active feature's status lives in `STATE.md`.

## `STATE.md` format

ALWAYS use this exact template structure — other phases clear `## Progress` and write to `## Notes` by name:

```markdown
## Progress

- **Feature:** {slug}
- **Phase:** specify | design | tasks | implement
- **Next:** {the next task or step, e.g. T-3, run audit}
- **Blockers:** {none | ...}

## Notes

- {feature-local observations, e.g. a design gap found during implement}
```

Task-level done/remaining lives in the `tasks.md` heading checkboxes; `STATE.md` is the coarse pointer to phase and next step. Written at each approval gate and after each task; read before the next task to see what is done and what remains.

`Blockers` records why a run stopped, and nothing else writes that fact to disk. A task that halts writes the blocker and leaves `Next` on the halted task, so a resume sees both where the run stopped and why. `none` therefore asserts that the last write completed cleanly — a resuming agent that finds `Next` on a task whose checkbox is already flipped is reading a run that died mid-task, not a clean handoff.

MUST NOT contain: cross-feature knowledge (decisions, gotchas, conventions — `CONTEXT.md` owns them). `STATE.md` is the current spec's status and is cleared after the audit passes, so nothing durable may live here.

## Conflicts with `CONTEXT.md`

Read `CONTEXT.md` before any design decision. A decision that conflicts with it is either **conformed** to or **explicitly superseded** (documenting why) — never silently ignored.
