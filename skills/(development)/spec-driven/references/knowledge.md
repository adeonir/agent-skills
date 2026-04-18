# Knowledge File Format

Canonical format for `.agents/knowledge.md`, owned by spec-driven.

## When to Use

- Loaded by design.md Step 7 and implement.md Step 10 before appending
- Loaded by quick-mode.md Step 7 before appending
- Loaded by project-index `integrate-feedback.md` to parse the Codebase Feedback queue

## Ownership

- **Sole writer:** spec-driven (design, implement, quick-mode)
- **Reader only:** project-index, and only the `## Codebase Feedback` section is mutated (rows cleared after integration -- never Decisions, never Gotchas)

## File Structure

```markdown
## Decisions

Cross-feature decisions with rationale. One bullet per decision.

- {decision} -- {rationale} <!-- feature:{ID} date:YYYY-MM-DD -->

## Gotchas

Traps discovered during design or implementation that would cost time to rediscover.

- {gotcha} -- {context} <!-- feature:{ID} date:YYYY-MM-DD -->

## Codebase Feedback

Queue of discoveries that belong in `.agents/codebase/*.md`. project-index consumes and clears via `/project-index integrate feedback`.

- {discovery} <!-- feature:{ID} target:{conventions|architecture|testing|integrations} date:YYYY-MM-DD -->
```

Always keep all three section headers, even when empty. project-index and spec-driven both rely on the headers existing to locate sections.

## Codebase Feedback Row Format

Every row under `## Codebase Feedback` MUST end with an HTML-comment metadata trailer:

```
<!-- feature:{ID} target:{name} date:YYYY-MM-DD -->
```

**Valid target values:**

| Target | Destination file |
|--------|------------------|
| `conventions` | `.agents/codebase/conventions.md` |
| `architecture` | `.agents/codebase/architecture.md` |
| `testing` | `.agents/codebase/testing.md` |
| `integrations` | `.agents/codebase/integrations.md` |

Rows with unknown targets or malformed metadata are skipped by integrate-feedback and reported.

## Section Routing

When appending a discovery during design or implement, route by content:

| Content | Section |
|---------|---------|
| Project-level decision (why we chose X over Y for the project) | `## Decisions` |
| Runtime constraint, API quirk, workaround, non-obvious trap | `## Gotchas` |
| New pattern, convention, architectural insight, testing approach, integration detail | `## Codebase Feedback` with target tag |
| Inventory/structural fact (installed package, new route, new module, new directory, new env var) | **Not queued** -- caught by `/project-index re-index` after audit |
| Forward-looking item (milestone, planned feature, `(TBD)`, feature number) | **Not queued** -- `codebase/*.md` is observable current state only |

Feature-specific details (only relevant to the current feature) do NOT belong here -- they live in the feature's own `design.md` or `implement.md` artifacts.

Inventory and structural facts are not queued because `codebase/*.md` is re-derived by project-index directly from the code. Queueing them duplicates work and turns the feedback queue into a changelog. What belongs here is the *interpretive* layer that re-index cannot infer: the why behind a choice, the trap behind a behavior, the convention behind a pattern.

## Guidelines

**DO:**
- Queue codebase-level discoveries to `## Codebase Feedback` with the correct target tag
- Record cross-feature decisions in `## Decisions` with rationale (the *why*, not the *what*)
- Record gotchas in `## Gotchas` with enough context for a future reader
- Use ISO date and feature ID in every row
- Create the file with all three headers if it doesn't exist

**DON'T:**
- Write `## Architecture` or `## Patterns` headers -- legacy format, removed
- Write directly to `.agents/codebase/*.md` -- project-index territory
- Use target values outside the canonical set
- Re-queue items already integrated (project-index handles dedupe, but redundant work wastes context)
- Let feature-specific details leak into this file
- Queue inventory or structural facts (installed packages, new routes, new modules, new directories, new env vars) -- they belong in `codebase/*.md` via re-index
- Queue forward-looking items (milestones, feature numbers, `(planned)`, `(TBD)`, `(coming soon)`) -- `codebase/*.md` is current state only

## Error Handling

- File missing: create with the three empty headers before appending
- Section header missing (partial file): add the missing header before appending
- Unknown target tag on a row: invalid format, fix before writing
- Conflict between sections (same item appended in Gotchas AND Codebase Feedback): keep only the Codebase Feedback entry; Gotchas is for behavior, Codebase Feedback is for documentation
