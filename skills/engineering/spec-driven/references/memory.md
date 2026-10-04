# Memory and Progress

The project's shared memory and the feature state.

## When to Use

At the load-context step of every phase, and whenever a phase discovers durable project knowledge, reaches an approval gate, or finishes a task.

## The two files

| File | Scope | Updated | Read |
|------|-------|---------|------|
| `PROJECT.md` | project-wide, committed knowledge | when a phase records durable Conventions, Decisions, or Gotchas | every phase |
| `.artifacts/specs/<slug>/STATE.md` | feature state and routing | at approval gates and after implement tasks | every phase for that feature |

`PROJECT.md` is shared project memory. `STATE.md` is the operational state of one feature. Neither file carries the detailed finding text owned by `validate.md`.

## `PROJECT.md`

Keep `PROJECT.md` at the project root, beside `AGENTS.md`, and commit it. It is useful to every developer and agent working in the project.

Write only these sections:

```markdown
## Conventions
- [project convention] — [where it applies]

## Decisions
- [decision] — [rationale]; source: [file:line/doc]; scope: [context]

## Gotchas
- [gotcha] — [context]
```

`Conventions` holds durable project rules that implementation must follow. A phase records a convention only when the codebase establishes it and it is useful beyond the current feature. `AGENTS.md` and `CLAUDE.md` belong to the project and no phase writes them. When an entry already exists in either, cite it instead of restating it, so a later edit cannot leave one copy stale.

`Decisions` is append-only unless a later decision explicitly supersedes an earlier one. `Gotchas` records durable traps found in the codebase.

Every entry records what is true now. Never record how something worked before, which release changed it, or an API the project no longer calls — a superseded decision is the one exception, and it stays only because a later decision names it. `source:` cites the file that proves the entry; an entry about third-party behaviour with no file to point at carries no `source:` rather than an invented one.

Leave every other section in the file untouched.

MUST NOT contain feature-local state, phase progress, findings, task notes, or conversation narrative ("as discussed", "we agreed", "the user confirmed").

## `STATE.md`

Create it at `.artifacts/specs/<slug>/STATE.md`. Do not create or read a global `.artifacts/STATE.md`.

ALWAYS use this exact structure:

```markdown
## Progress

- **Feature:** <slug>
- **Phase:** specify | design | tasks | implement | validate
- **Next:** [the next task or step, e.g. T-3, run validate, or none]
- **Blockers:** [none | ...]

## Notes

- [feature-local observations]
```

Task completion lives in the `tasks.md` checkboxes and frontmatter. `STATE.md` stores the coarse phase pointer, the next step, and blockers only. `implement` has no `BLOCKED` artifact state; an open task remains open and `tasks.md` remains `in-progress`.

Write `Blockers` and `Notes` as what holds now, in present tense: an edit writes the new state, never the change, and no entry carries its history or the conversation that produced it ("as discussed", "the user confirmed", "we agreed").

## Read and write routing

- The feature directory is the `.artifacts/specs/<slug>/` the user names when invoking the phase. With no name, take the only directory there. If more than one directory exists, ask the user which one before reading anything.
- Every phase reads the root `PROJECT.md` and the feature's `STATE.md` when the feature exists.
- `specify`, `design`, `tasks`, `implement`, and `validate` resolve state from that directory.
- `STATE.md` is the only phase router. `Phase` names the phase that owns the next action, and `Next` names the next step inside that phase. Read both before loading downstream artifacts. If `Phase` names an earlier phase, stop and report that phase instead of continuing with stale downstream artifacts.
- `validate` writes detailed findings to its own report.
- A `validate` FAIL sets `Phase: tasks` and `Next: validate findings`; `tasks` verifies the findings in `validate.md` and creates or adjusts correction tasks.
- Every artifact's structure is canonical in the instruction or reference that owns it. Load the owning file before reading an existing file in `.artifacts/`: an existing file is context, and the template wins on divergence.
- The only cross-feature input a new feature reads is the root `PROJECT.md`; never forage sibling features or `archive/` for shape or decisions.
- A phase that wrote anything names only non-ignored files at its approval gate and suggests the commit, so the phase leaves no tracked file uncommitted. Run `git check-ignore -v .artifacts/` once before naming artifact files; when it reports a match, treat new artifacts below that directory as local state and never stage them implicitly. A previously tracked artifact remains tracked. The phase never creates the commit: `ready` says the agent finished its part, not that anyone reviewed the artifact, and the review happens at that gate. Nothing is suggested while the artifact is still `draft`.
- Include changes to `PROJECT.md ## Decisions` in the phase's final summary.

No phase infers a new run from an artifact diff, an isolated `Next` value, or an old status. A phase that cannot proceed writes the routing decision to `STATE.md`; the next invocation follows that decision.
