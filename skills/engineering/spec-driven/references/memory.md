# Memory and Progress

The two cross-cutting memory files: `CONTEXT.md` (persistent, cross-feature) and `STATE.md` (progress of the active feature). Their formats, when each is read and written, and how conflicts resolve.

## When to Use

At the load-context step of every phase (read), and whenever a phase discovers a durable fact (`CONTEXT.md`) or reaches an approval gate or finishes a task (`STATE.md`).

## The two files

| File | Scope | Updated | Read |
|------|-------|---------|------|
| `.artifacts/CONTEXT.md` | cross-feature, persistent, append-only | when design/implement/audit find a cross-feature lesson | every phase |
| `.artifacts/STATE.md` | active feature | at each approval gate, after each task in implement, and when a report creates or clears a finding signal | at each phase's load step, before each task in implement, and before tasks loads finding reports |

`CONTEXT.md` is append-only and cross-feature. `STATE.md` is overwritten at each boundary and holds the feature's current progress. No phase clears it — no artifact carries a terminal state, so the file persists until the next feature's specify overwrites it. Archive is manual and leaves `STATE.md` unchanged.

## `CONTEXT.md` format

Here is a sensible default format, but use your best judgment:

```markdown
## Stakes
- {what the product is}
- {surface} — {what a silent failure here costs}

## Decisions
- {decision} — {rationale}; source: {file:line/doc}; scope: {context}

## Gotchas
- {gotcha} — {context}

## Conventions
- {convention} — {where it applies / why}
```

No mandatory date. No rigid routing rules. Routing by intent: a project-level decision a future feature must follow → `## Decisions`; a real trap found in the code → `## Gotchas`; a normative codebase pattern → `## Conventions`.

`## Stakes` records the product and what a silent failure costs per surface: money, auth, user data, or persisted state on one side; a content or presentation surface — where a silent failure costs a wrong pixel or an inert link — on the other. It is what tells the audit's discrimination sensor whether a surviving mutant's failure is worth acting on. Unlike the append-only sections, it holds one current picture: specify writes it when absent and rewrites it — never appends — when a later feature's surface contradicts what it says.

MUST NOT contain: feature-local state, progress, or notes — `CONTEXT.md` is knowledge shared across features; the active feature's status lives in `STATE.md`.

## `STATE.md` format

ALWAYS use this exact template structure — other phases clear `## Progress` and write to `## Notes` by name:

```markdown
## Progress

- **Feature:** {slug}
- **Phase:** specify | design | tasks | implement | audit | validate
- **Next:** {the next task or step, e.g. T-3, run audit, or none}
- **Blockers:** {none | ...}
- **Findings:** {none | validate | audit | validate,audit}
- **Audit iteration:** {0 | 1 | 2 | 3}

## Notes

- {feature-local observations, e.g. a design gap found during implement}
```

Task-level done/remaining lives in the `tasks.md` heading checkboxes and its frontmatter status; `STATE.md` is the coarse pointer to phase and next step. Written at each approval gate, after each task, and when report findings need task triage; read before the next task to see what is done and what remains.

`Blockers` records why a run stopped, and nothing else writes that fact to disk. A task that halts writes the blocker and leaves `Next` on the halted task, so a resume sees both where the run stopped and why. `none` means no task halted — it does not mean the run finished. `implement` has no `BLOCKED` artifact state; its open task remains open and `tasks.md` remains `in-progress`.

`Next` resting on a task whose checkbox is already flipped is the ordinary state at a selection boundary: a subagent stops there, and the main agent moves the pointer on before dispatching again. The pointer alone never separates a finished run from an abandoned one. Read `Blockers` for why a run stopped and the `tasks.md` checkboxes for how far it got.

`Findings` is a triage signal, not a historical report. `validate` or `audit` sets its source when that report ends in `FAIL`. `tasks` reads the named reports, creates or adjusts correction tasks, and clears the consumed source. A later failed rerun sets the source again. `BLOCKED` uses `Blockers`, not `Findings`.

`Audit iteration` counts the fix loop, because a bounded loop the agent counts from memory is unbounded across a context boundary. It starts at `0`, rises on each audit FAIL, and the loop escalates to the user when it reaches its limit — the file decides that, never recall.

MUST NOT contain: cross-feature knowledge (decisions, gotchas, conventions — `CONTEXT.md` owns them). `STATE.md` is feature-local progress and routing only; reports own findings and artifact files own their states.

## Conflicts with `CONTEXT.md`

Read `CONTEXT.md` before any design decision. A decision that conflicts with it is either **conformed** to or **explicitly superseded** (documenting why) — never silently ignored.
