# Integrate Codebase Feedback

Consume `.agents/knowledge.md ## Codebase Feedback` queue, merge items into `.agents/codebase/*.md`, and clear integrated rows.

## When to Use

- An implementation skill prompted the user to integrate
- User explicitly says "integrate feedback", "integrate discoveries", "sync knowledge"
- `.agents/knowledge.md ## Codebase Feedback` has queued items

## Workflow

### Step 1: Verify Preconditions

- `.agents/knowledge.md` exists and has `## Codebase Feedback` section with rows. If missing or empty, exit with "No feedback to integrate."
- `.agents/codebase/` exists. If missing, exit with "Run initialize first to create `.agents/codebase/`."

### Step 2: Sync Decisions

Read `## Decisions` rows from `.agents/knowledge.md` (if the section exists and has rows).

For each decision row:

1. Check if a matching row already exists in `.agents/codebase/architecture.md ## Key Decisions` table (substring match on decision text).
2. If not found, append the row to `## Key Decisions`.
3. Do NOT remove rows from `## Decisions` in `knowledge.md` — decisions are a permanent record.

If `architecture.md` does not exist yet, skip this step silently.

### Step 3: Parse Queue

For each row under `## Codebase Feedback`:

- Extract content (text before the HTML comment)
- Extract target from `<!-- target:{name} -->`
- Valid targets: `conventions`, `architecture`, `testing`, `integrations`, `workflows`, `features`, `review`

Classify each row into one of:

- **Integrate** — content describes current observable state
- **Skipped (malformed)** — unknown target or broken metadata
- **Skipped (forward-looking)** — content describes future plans, milestones, feature numbers, or markers like `(planned)`, `(TBD)`, `(coming soon)`, `(M{N}+)`, "shipped through feature X"

Forward-looking and malformed rows are listed in the final report. They are never merged into `codebase/*.md`, which captures only current state.

Read `.agents/knowledge.md` directly for the queue content.

### Step 4: Group by Target

Group parsed items by target. Each target maps to a file:

| Target | File |
|--------|------|
| `conventions` | `.agents/codebase/conventions.md` |
| `architecture` | `.agents/codebase/architecture.md` |
| `testing` | `.agents/codebase/testing.md` |
| `integrations` | `.agents/codebase/integrations.md` |
| `workflows` | `.agents/codebase/workflows.md` |
| `features` | `.agents/codebase/features.md` (only when the file exists; skip otherwise) |
| `review` | `.agents/codebase/review.md` |

### Step 5: Merge

For each target file:

1. If file does not exist, create it using the template inlined in the matching reference (`architecture.md`, `conventions.md`, etc.).
2. Read the file's existing structure (table format, section headers).
3. For each item in the group:
   - Check if content already exists (substring match or `file:line` anchor match). If yes, mark as duplicate.
   - Otherwise, append using the file's existing format.
4. Preserve `feature:{ID}` and `date:` metadata by adding an inline note when the target format does not have a column for it.

### Step 6: Clear Integrated Rows

Rewrite `.agents/knowledge.md`:

- Remove integrated rows from `## Codebase Feedback`
- Keep the section header even if now empty
- Never modify `## Decisions` or `## Gotchas`
- Remove duplicate rows too (they're already in the target file) with a note in the report

### Step 7: Report

Show:

- Integrated: N items (by target: conventions, architecture, testing, integrations, workflows, review)
- Decisions synced: N items (if any were synced)
- Skipped duplicates: M items
- Skipped malformed: P items (if any)
- Skipped forward-looking: K items (if any, with the offending content for user review)
- Target files touched: {list}

## Guidelines

- Preserve each target file's existing format (table columns, section headers)
- Merge idempotently — rerunning must be a no-op
- Clear only `## Codebase Feedback`, never other sections of `knowledge.md`
- Use the matching ref template when creating a missing target file

## Anti-Pattern: Forward-Looking Merge

Rows describing future plans, milestones, feature numbers, or `(planned)` / `(TBD)` markers must be skipped and listed under "forward-looking" in the report. The codebase docs capture only what exists today; the user reconciles forward-looking items at the source.

## Error Handling

- `.agents/knowledge.md` missing: "No feedback to integrate."
- `## Codebase Feedback` missing or empty: "No queued items."
- `.agents/codebase/` missing: "Run initialize first."
- Unknown target tag on a row: skip, include in malformed report
- Target file create fails (filesystem error): abort, report state so user can recover
