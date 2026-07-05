# Memory and Progress

The two cross-cutting memory files: `CONTEXT.md` (persistent, cross-feature) and `STATE.md` (progress of the active feature). Their formats, when each is read and written, and how conflicts resolve.

## When to Use

At the load-context step of every phase (read), and whenever a phase discovers a durable fact (`CONTEXT.md`) or reaches an approval gate or finishes a task (`STATE.md`).

## The two files

| File | Scope | Updated | Read |
|------|-------|---------|------|
| `.artifacts/CONTEXT.md` | cross-feature, persistent, append-only | when design/implement/audit find a cross-feature lesson | every phase |
| `.artifacts/STATE.md` | active feature | at each approval gate, and after each task in implement | at each phase's load step, and before each task in implement |

`CONTEXT.md` is append-only and cross-feature. `STATE.md` is overwritten at each boundary — it holds only the feature's current progress — and is cleared only after merge (during archive), never when the audit passes.

## `CONTEXT.md` format

```markdown
## Decisions
- {decision} — {rationale}; source: {file:line/doc}; scope: {context}

## Gotchas
- {gotcha} — {context}

## Conventions
- {convention} — {where it applies / why}
```

No mandatory date. No rigid routing rules. Routing by intent: a project-level decision a future feature must follow → `## Decisions`; a real trap found in the code → `## Gotchas`; a normative codebase pattern → `## Conventions`.

## `STATE.md` format

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

## Conflicts with `CONTEXT.md`

Read `CONTEXT.md` before any design decision. A decision that conflicts with it is either **conformed** to or **explicitly superseded** (documenting why) — never silently ignored.
