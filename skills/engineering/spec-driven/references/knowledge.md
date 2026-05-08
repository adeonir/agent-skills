# Knowledge File Format

Canonical format for `.agents/knowledge.md`, owned by the spec-driven
workflow.

## When to Use

- Loaded by `design.md` Step 8 and `implement.md` Step 10 before appending
- Loaded by `quick-mode.md` Step 8 before appending
- Loaded by the codebase-indexing feedback integration to parse the
  Codebase Feedback queue

## Ownership

- **Sole writer:** the spec-driven workflow (design, implement, quick-mode)
- **Reader only:** the codebase-indexing workflow, and only the
  `## Codebase Feedback` section is mutated (rows cleared after
  integration — never Decisions, never Gotchas)

## File Structure

```markdown
## Decisions

Cross-feature decisions with rationale. One bullet per decision.

- {decision} — {rationale} <!-- feature:{ID} date:YYYY-MM-DD -->

## Gotchas

Traps discovered during design or implementation that would cost time
to rediscover.

- {gotcha} — {context} <!-- feature:{ID} date:YYYY-MM-DD -->

## Codebase Feedback

Queue of discoveries that belong in `.agents/codebase/*.md`. The
codebase-indexing feedback integration consumes and clears this queue.

- {discovery} <!-- target:{conventions|architecture|testing|integrations|workflows|concerns} -->
```

Always keep all three section headers, even when empty. Both readers and
writers rely on the headers existing to locate sections.

## Codebase Feedback Row Format

Every row under `## Codebase Feedback` MUST end with an HTML-comment
metadata trailer:

```
<!-- target:{name} -->
```

**Valid target values:**

| Target | Destination file |
|--------|------------------|
| `conventions` | `.agents/codebase/conventions.md` |
| `architecture` | `.agents/codebase/architecture.md` |
| `testing` | `.agents/codebase/testing.md` |
| `integrations` | `.agents/codebase/integrations.md` |
| `workflows` | `.agents/codebase/workflows.md` |
| `concerns` | `.agents/codebase/concerns.md` |

Rows with unknown targets or malformed metadata are skipped by feedback
integration and reported.

## Section Routing

When appending a discovery during design or implement, route by content:

| Content | Section |
|---------|---------|
| Project-level decision (why we chose X over Y for the project) | `## Decisions` |
| Runtime constraint, API quirk, workaround, non-obvious trap | `## Gotchas` |
| New pattern, convention, architectural insight, testing approach, integration detail, dev/user workflow, tech debt or risk | `## Codebase Feedback` with target tag |
| Inventory/structural fact (installed package, new route, new module, new directory, new env var) | **Not queued** — caught by codebase re-index after audit |
| Forward-looking item (milestone, planned feature, `(TBD)`, feature number) | **Not queued** — `codebase/*.md` is observable current state only |

Feature-specific details (only relevant to the current feature) do NOT
belong here — they live in the feature's own `design.md` or
`implement.md` artifacts.

Inventory and structural facts are not queued because `codebase/*.md`
is re-derived by the codebase-indexing workflow directly from the code.
Queueing them duplicates work and turns the feedback queue into a
changelog. What belongs here is the *interpretive* layer that re-index
cannot infer: the why behind a choice, the trap behind a behavior, the
convention behind a pattern.

## Guidelines

- Queue codebase-level discoveries to `## Codebase Feedback` with the
  correct target tag
- Record cross-feature decisions in `## Decisions` with rationale (the
  *why*, not the *what*)
- Record gotchas in `## Gotchas` with enough context for a future reader
- Use ISO date and feature ID in every row
- Create the file with all three headers if it doesn't exist

## Anti-Pattern: Direct Writes to Codebase Index

Writing directly to `.agents/codebase/*.md` bypasses the integration
flow and risks divergence between the queue and the integrated state.
The codebase-indexing workflow owns those files; spec-driven only
writes to `.agents/knowledge.md`.

## Anti-Pattern: Queueing Inventory Facts

Installed packages, new routes, new modules, new directories, and new
env vars are inventory — they're caught by the codebase re-index after
audit. Queueing them duplicates work and turns the feedback queue into
a changelog. The queue is for interpretive content (why, trap,
convention), not what.

## Error Handling

- File missing: create with the three empty headers before appending
- Section header missing (partial file): add the missing header before
  appending
- Unknown target tag on a row: invalid format, fix before writing
- Conflict between sections (same item appended in Gotchas AND Codebase
  Feedback): keep only the Codebase Feedback entry; Gotchas is for
  behavior, Codebase Feedback is for documentation
