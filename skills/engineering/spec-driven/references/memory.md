# Memory and Handoff

The two cross-cutting memory files: `CONTEXT.md` (persistent, cross-feature) and `STATE.md` (session handoff for the active feature). Their formats, when each is read and written, and how conflicts resolve.

## When to Use

At the load-context step of every phase (read), and whenever a phase discovers a durable fact or ends a session with unfinished work (write).

## The two files

| File | Scope | Updated | Read |
|------|-------|---------|------|
| `.artifacts/CONTEXT.md` | cross-feature, persistent, append-only | when design/implement/audit find a cross-feature lesson | every phase |
| `.artifacts/STATE.md` | active feature/session | every phase, if the session ends with unfinished work | every phase, to resume |

`CONTEXT.md` is append-only and cross-feature. `STATE.md` is overwritten on each pause — it holds only the current state — and is cleared only after merge (during archive), never when the audit passes.

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
## Handoff

- **Feature:** {slug}
- **Phase:** specify | design | tasks | implement | audit | validate
- **Next action:** {T-3, run gate X, etc.}
- **Blockers:** {none | ...}
- **Uncommitted files:** {list}
- **Branch:** {name}
- **Last updated:** {YYYY-MM-DD HH:MM}

## Notes

- {feature-local observations, e.g. a design gap found during implement}
```

Written when a session will end with unfinished work; read at the start of any phase to resume.

## Conflicts with `CONTEXT.md`

Read `CONTEXT.md` before any design decision. A decision that conflicts with it is either **conformed** to or **explicitly superseded** (documenting why) — never silently ignored.
