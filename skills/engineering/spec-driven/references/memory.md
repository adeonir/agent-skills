# Memory and Progress

The project's shared memory, the active feature state, and the routing signal that sends reports to task triage.

## When to Use

At the load-context step of every phase, and whenever a phase discovers durable project knowledge, reaches an approval gate, finishes a task, or creates or resolves a report signal.

## The three files

| File | Scope | Updated | Read |
|------|-------|---------|------|
| `CONTEXT.md` | project-wide, committed memory | when specify records Stakes or a phase records durable Decisions or Gotchas | every phase |
| `.artifacts/specs/{slug}/STATE.md` | active feature state and routing | at approval gates, after implement tasks, and when report signals change | every phase for the active feature |
| `.artifacts/specs/{slug}/SIGNALS.md` | active feature's verified signal history | when implement, validate, or audit records or resolves a signal | audit and the lessons script |

`CONTEXT.md` is shared project knowledge. `STATE.md` is the operational state of one feature. `SIGNALS.md` is the local history that grounds lessons. None of these files carries the detailed finding text owned by `validate.md` or `audit.md`.

## `CONTEXT.md`

Keep `CONTEXT.md` at the project root, beside `AGENTS.md`, and commit it. It is useful to every developer and agent working in the project.

Use only these sections:

```markdown
## Stakes
- {what the product is}
- {surface} — {what a silent failure here costs}

## Decisions
- {decision} — {rationale}; source: {file:line/doc}; scope: {context}

## Gotchas
- {gotcha} — {context}
```

Do not add `## Conventions`. Normative repository rules belong in `AGENTS.md` or `CLAUDE.md`. A project pattern discovered in code belongs in `Decisions` or `Gotchas` only when it is durable and useful beyond the active feature.

`Stakes` holds the current product surface and the cost of a silent failure. Specify writes it when absent and rewrites it when a later feature contradicts the current surface. `Decisions` is append-only unless a later decision explicitly supersedes an earlier one. `Gotchas` records durable traps found in the codebase.

MUST NOT contain feature-local state, phase progress, findings, signals, or task notes.

## `STATE.md`

Create it at `.artifacts/specs/{slug}/STATE.md` for the active feature. Do not create or read a global `.artifacts/STATE.md`.

ALWAYS use this exact structure:

```markdown
## Progress

- **Feature:** {slug}
- **Phase:** specify | design | tasks | implement | validate | audit
- **Next:** {the next task or step, e.g. T-3, run audit, or none}
- **Blockers:** {none | ...}
- **Findings:** {none | validate | audit | validate,audit}

## Notes

- {feature-local observations}
```

`Findings` is a routing field. It names the report files that still need task triage; it never contains the finding text. The detailed findings remain in `validate.md` or `audit.md`. `tasks` clears each source after verifying the report and creating or adjusting correction tasks.

Task completion lives in the `tasks.md` checkboxes and frontmatter. `STATE.md` stores the coarse phase pointer, the next step, blockers, and report routing only. `implement` has no `BLOCKED` artifact state; an open task remains open and `tasks.md` remains `in-progress`.

No audit retry counter belongs in `STATE.md`. The audit report owns the count of consecutive failed audit runs.

## `SIGNALS.md`

Create it at `.artifacts/specs/{slug}/SIGNALS.md`. It is local, machine-owned, and excluded from commits. It records verified signal rows, not detailed findings.

The file uses the contract in [lessons.md](lessons.md). `signals.py` is the only writer.

## Read and write routing

- Every phase reads the root `CONTEXT.md` and the active feature's `STATE.md` when the feature exists.
- `specify`, `design`, `tasks`, `implement`, `validate`, and `audit` resolve state from the active feature directory.
- `STATE.md` is the only phase router. `Phase` names the phase that owns the next action, and `Next` names the next step inside that phase. Read both before loading downstream artifacts. If `Phase` names an earlier phase, stop and report that phase instead of continuing with stale downstream artifacts.
- `validate` and `audit` write detailed findings to their own reports and add or resolve signal rows through `signals.py`.
- `implement` records only verified upstream failures; a task failure that is corrected in the same run is not a signal.
- `tasks` reads `STATE.md` first. When `Findings` names a report, it reads that report, verifies the findings, creates or adjusts correction tasks, and clears the consumed routing value. This report triage takes precedence over `Phase`.
- `audit` reads signal history and runs the lesson promotion flow after writing its report.

No phase infers a new run from an artifact diff, an isolated `Next` value, or an old status. A phase that cannot proceed writes the routing decision to `STATE.md`; the next invocation follows that decision.

## Deviations during implementation

Record only the four operational differences that may continue in `STATE.md ## Notes`: a different name for the same thing, a file one directory over when placement was open, an unforeseen private helper, or a test name forced by the runner.

For an interface, dependency, design decision, acceptance scenario, or open-question contradiction, leave written changes on disk, name the changed files in `STATE.md ## Blockers`, and route `Phase` and `Next` to `design` for a technical contradiction or `specify` for a contract contradiction. Do not edit upstream artifacts, widen the task, or rewrite history. The user decides whether to keep or discard the changes.

## Conflicts with `CONTEXT.md`

Read `CONTEXT.md` before any design decision. A decision that conflicts with it is either conformed to or explicitly superseded with a reason; never ignore it silently.
