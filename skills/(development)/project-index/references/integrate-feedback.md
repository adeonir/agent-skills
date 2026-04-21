# Integrate Codebase Feedback

Consume `.agents/knowledge.md` `## Codebase Feedback` queue, merge items into `.agents/codebase/*.md`, and clear integrated rows.

## When to Use

- spec-driven design or implement prompted the user to integrate
- User explicitly ran `/project-index integrate feedback`
- `.agents/knowledge.md` `## Codebase Feedback` has queued items

## Workflow

### Step 1: Verify Preconditions

- `.agents/knowledge.md` exists and has `## Codebase Feedback` section with rows. If missing or empty, exit with "No feedback to integrate."
- `.agents/codebase/` exists. If missing, exit with "Run `/project-index initialize` first to create `.agents/codebase/`."

### Step 2: Parse Queue

For each row under `## Codebase Feedback`:

- Extract content (text before the HTML comment)
- Extract target from `<!-- target:{name} -->`
- Valid targets: `conventions`, `architecture`, `testing`, `integrations`, `workflows`, `concerns`

Classify each row into one of:

- **Integrate** -- content describes current observable state
- **Skipped (malformed)** -- unknown target or broken metadata
- **Skipped (forward-looking)** -- content describes future plans, milestones, feature numbers, or markers like `(planned)`, `(TBD)`, `(coming soon)`, `(M{N}+)`, "shipped through feature X"

Forward-looking and malformed rows are listed in the final report. They are never merged into `codebase/*.md`, which captures only current state.

Read `.agents/knowledge.md` directly for the queue content.

### Step 3: Group by Target

Group parsed items by target. Each target maps to a file:

| Target | File |
|--------|------|
| `conventions` | `.agents/codebase/conventions.md` |
| `architecture` | `.agents/codebase/architecture.md` |
| `testing` | `.agents/codebase/testing.md` |
| `integrations` | `.agents/codebase/integrations.md` |
| `workflows` | `.agents/codebase/workflows.md` |
| `concerns` | `.agents/codebase/concerns.md` |

### Step 4: Merge

For each target file:

1. If file doesn't exist, create it using the project-index template (`templates/{name}.md`).
2. Read the file's existing structure (table format, section headers).
3. For each item in the group:
   - Check if content already exists (substring match or `file:line` anchor match). If yes, mark as duplicate.
   - Otherwise, append using the file's existing format.
4. Preserve the `feature:{ID}` and `date:` metadata by adding an inline note when the target format doesn't have a column for it.

### Step 5: Clear Integrated Rows

Rewrite `.agents/knowledge.md`:

- Remove integrated rows from `## Codebase Feedback`
- Keep the section header even if now empty
- Never modify `## Decisions` or `## Gotchas`
- Remove duplicate rows too (they're already in the target file) with a note in the report

### Step 6: Report

Show:

- Integrated: N items (X conventions, Y architecture, Z testing, W integrations)
- Skipped duplicates: M items
- Skipped malformed: P items (if any)
- Skipped forward-looking: K items (if any, with the offending content for user review)
- Target files touched: {list}

## Guidelines

**DO:**
- Preserve each target file's existing format (table columns, section headers)
- Merge idempotently -- rerunning must be a no-op
- Clear only `## Codebase Feedback`, never other sections of knowledge.md
- Use project-index templates when creating a missing target file

**DON'T:**
- Overwrite existing content in any target file
- Invent target names outside the canonical set (`conventions`, `architecture`, `testing`, `integrations`)
- Modify `## Decisions` or `## Gotchas` sections
- Auto-run without a user trigger (spec-driven prompts, user decides)
- Merge rows describing future plans, milestones, feature numbers, or `(planned)`/`(TBD)` markers -- skip and list them in the report under "forward-looking" for the user to reconcile at the source

## Error Handling

- `.agents/knowledge.md` missing: "No feedback to integrate."
- `## Codebase Feedback` missing or empty: "No queued items."
- `.agents/codebase/` missing: "Run `/project-index initialize` first."
- Unknown target tag on a row: skip, include in malformed report
- Target file create fails (filesystem error): abort, report state so user can recover
