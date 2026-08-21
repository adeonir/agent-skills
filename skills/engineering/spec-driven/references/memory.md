# Memory and Progress

The project's shared memory, the feature state, and the routing signal that sends reports to task triage.

## When to Use

At the load-context step of every phase, and whenever a phase discovers durable project knowledge, reaches an approval gate, finishes a task, or creates or resolves a report signal.

## The three files

| File | Scope | Updated | Read |
|------|-------|---------|------|
| `CONTEXT.md` | project-wide, committed knowledge | when specify records Stakes or a phase records durable Conventions, Decisions, or Gotchas | every phase |
| `.artifacts/specs/<slug>/STATE.md` | feature state and routing | at approval gates, after implement tasks, and when report signals change | every phase for that feature |
| `.artifacts/specs/<slug>/SIGNALS.md` | the feature's verified signal history | when implement or audit records or resolves a signal | audit and the lessons script |

`CONTEXT.md` is shared project memory. `STATE.md` is the operational state of one feature. `SIGNALS.md` is the local history that grounds lessons. None of these files carries the detailed finding text owned by `validate.md` or `audit.md`.

## `CONTEXT.md`

Keep `CONTEXT.md` at the project root, beside `AGENTS.md`, and commit it. It is useful to every developer and agent working in the project.

Write only these sections:

```markdown
## Stakes
- [what the product is]
- [surface] — [what a silent failure here costs]

## Conventions
- [project convention] — [where it applies]

## Decisions
- [decision] — [rationale]; source: [file:line/doc]; scope: [context]

## Gotchas
- [gotcha] — [context]
```

`Conventions` holds durable project rules that implementation must follow. A phase records a convention only when the codebase establishes it and it is useful beyond the current feature. `AGENTS.md` and `CLAUDE.md` belong to the project and no phase writes them. When an entry already exists in either, cite it instead of restating it, so a later edit cannot leave one copy stale.

`Stakes` holds the current product surface and the cost of a silent failure. Specify writes it when absent and rewrites it when a later feature contradicts the current surface. `Decisions` is append-only unless a later decision explicitly supersedes an earlier one. `Gotchas` records durable traps found in the codebase.

Every entry records what is true now. Never record how something worked before, which release changed it, or an API the project no longer calls — a superseded decision is the one exception, and it stays only because a later decision names it. `source:` cites the file that proves the entry; an entry about third-party behaviour with no file to point at carries no `source:` rather than an invented one.

Leave every other section in the file untouched.

MUST NOT contain feature-local state, phase progress, findings, signals, or task notes.

## `STATE.md`

Create it at `.artifacts/specs/<slug>/STATE.md`. Do not create or read a global `.artifacts/STATE.md`.

ALWAYS use this exact structure:

```markdown
## Progress

- **Feature:** <slug>
- **Phase:** specify | design | tasks | implement | validate | audit
- **Next:** [the next task or step, e.g. T-3, run audit, or none]
- **Blockers:** [none | ...]
- **Findings:** [none | validate | audit | validate,audit]

## Notes

- [feature-local observations]
```

`Findings` is a routing field. It names the report files that still carry something for the phase `Phase` points to; it never contains the finding text. The detailed findings remain in `validate.md` or `audit.md`. The phase that consumes a report clears its source after acting on it.

Task completion lives in the `tasks.md` checkboxes and frontmatter. `STATE.md` stores the coarse phase pointer, the next step, blockers, and report routing only. `implement` has no `BLOCKED` artifact state; an open task remains open and `tasks.md` remains `in-progress`.

No audit retry counter belongs in `STATE.md`. The audit report owns the count of consecutive failed audit runs.

## `SIGNALS.md`

Create it at `.artifacts/specs/<slug>/SIGNALS.md`. It is local, machine-owned, and excluded from commits. It records verified signal rows, not detailed findings.

The file uses the contract in [lessons.md](lessons.md). `signals.py` is the only writer.

## Read and write routing

- The feature directory is the `.artifacts/specs/<slug>/` the user names when invoking the phase. With no name, take the only directory there. If more than one directory exists, ask the user which one before reading anything.
- Every phase reads the root `CONTEXT.md` and the feature's `STATE.md` when the feature exists.
- `specify`, `design`, `tasks`, `implement`, `validate`, and `audit` resolve state from that directory.
- `STATE.md` is the only phase router. `Phase` names the phase that owns the next action, and `Next` names the next step inside that phase. Read both before loading downstream artifacts. If `Phase` names an earlier phase, stop and report that phase instead of continuing with stale downstream artifacts.
- `validate` and `audit` write detailed findings to their own reports. `audit` also adds or resolves signal rows through `signals.py`; `validate` writes no signal.
- `implement` records only verified upstream failures; a task failure that is corrected in the same run is not a signal.
- `Findings` names the report that still carries something and `Phase` names the phase that reads it. `Phase` decides: `tasks` reads a report only when `Phase` names `tasks`, and stops and reports the named phase otherwise, whatever `Findings` carries. `tasks` verifies the findings, creates or adjusts correction tasks, and clears the consumed source; `specify` reads the report before rewriting the contract and clears it the same way.
- `audit` reads signal history and runs the lesson promotion flow after writing its report.

- A phase that wrote anything outside the ignored folders names those files at its approval gate and suggests the commit, so the phase leaves no tracked file uncommitted. It never creates the commit: `ready` says the agent finished its part, not that anyone reviewed the artifact, and the review happens at that gate. Nothing is suggested while the artifact is still `draft`.
- Include changes to `CONTEXT.md ## Decisions` in the phase's final summary.

No phase infers a new run from an artifact diff, an isolated `Next` value, or an old status. A phase that cannot proceed writes the routing decision to `STATE.md`; the next invocation follows that decision.

## Deviations during implementation

Record only the four operational differences that may continue in `STATE.md ## Notes`: a different name for the same thing, a file one directory over when placement was open, an unforeseen private helper, or a test name forced by the runner.

For an interface, dependency, design decision, acceptance scenario, or open-question contradiction, leave written changes on disk, name the changed files in `STATE.md ## Blockers`, and route `Phase` and `Next` to `design` for a technical contradiction or `specify` for a contract contradiction. Do not edit upstream artifacts, widen the task, or rewrite history. The user decides whether to keep or discard the changes.

## Conflicts with `CONTEXT.md`

Read `CONTEXT.md` before any design decision. A decision that conflicts with it is either conformed to or explicitly superseded with a reason; never ignore it silently.
