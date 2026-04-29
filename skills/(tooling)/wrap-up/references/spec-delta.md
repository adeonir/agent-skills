# Spec Delta Check

Detect structural changes from spec-driven work and surface a non-blocking
re-index suggestion. Inform only -- never prompt, never block wrap-up.

## When to Use

- Last step of every wrap-up run, after Obsidian notes complete
- Skipped silently when `.artifacts/.session-dump.md` does not exist

## Workflow

### Step 1: Detect Session Dump

spec-driven writes a single cumulative dump at `.artifacts/.session-dump.md` (root). Each phase across any feature appends a `## YYYY-MM-DD HH:MM -- {phase}` block.

- File does not exist: emit no output, end this step.
- File exists: continue.

### Step 2: Read Latest Phase Entry

Read `.artifacts/.session-dump.md` and locate the last `## YYYY-MM-DD HH:MM -- {phase}` block (the most recent append). Capture:

- The `**Discoveries:**` bullet list within that block
- Optional: `**Decisions:**` bullets, useful when discoveries are sparse

Discovery bullets that mention any of these keywords are structural signals:

- `route`, `endpoint`, `api`
- `module`, `package`, `dependency`, `dep`
- `env var`, `environment variable`, `.env`
- `migration`, `schema`, `table`
- `directory`, `folder`

### Step 3: Run Structural Diff

Run against the feature branch (skip if not in a git repo):

```bash
git diff --name-status $(git merge-base main HEAD)..HEAD
```

Flag a structural delta if any of the following is true:

- Any `A` (added), `D` (deleted), `R` (renamed), or `C` (copied) entry outside `.artifacts/`
- `package.json` `dependencies` or `devDependencies` sections changed
- `.env.example` changed
- New directory under the framework's route root (e.g., `src/app/api/`,
  `pages/api/`, `app/routes/`)

### Step 4: Surface Suggestion

If Step 2 found a structural keyword OR Step 3 flagged a delta, append exactly
one line to wrap-up output:

> Structural changes detected -- consider running `/project-index re-index` to refresh `.agents/codebase/*.md`.

If neither signal fires, emit nothing.

## Guidelines

**DO:**
- Mirror audit's inform-only pattern -- no y/n prompt, no auto-invocation
- Keep output to a single line when the suggestion fires
- Skip silently when `.artifacts/.session-dump.md` does not exist or no signal fires
- Treat the session-dump file existence as the trigger for running this step at all
- Read only the latest `##` block; older blocks are historical, not current state

**DON'T:**
- Prompt the user or block wrap-up completion (contrasts: inform-only)
- Run the structural diff when the session-dump file does not exist (contrasts: file existence is the trigger)
- Re-implement detection logic that audit already owns -- mirror the same flags
- Auto-invoke `/project-index re-index` (contrasts: user decides)
- Walk every block in the file (contrasts: read only the latest phase entry)

## Error Handling

- Not in a git repo: skip Step 3, rely on Step 2 keyword scan only
- `git merge-base` fails (no `main` branch, shallow clone): skip Step 3
- Session-dump file empty or has no `##` blocks: treat as missing, end the step
- Latest phase entry has no Discoveries section or only "none" bullets: rely on Step 3 only
