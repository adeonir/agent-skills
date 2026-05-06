# Spec-Driven Session Dump Lifecycle

Load the ephemeral spec-driven dump for downstream notes, run
structural-delta detection, and unlink the file at the end of wrap-up.

## When to Use

- Invoked twice per wrap-up: once after mapping (Load phase, before
  auto-memory) and once after obsidian-notes (Detect + Cleanup phases,
  last)
- All phases short-circuit silently when
  `.artifacts/.session-dump.md` is absent

## Workflow

### Load Phase

Runs after mapping, before auto-memory.

1. Check `.artifacts/.session-dump.md`. If absent, no-op silently —
   Detect and Cleanup will likewise no-op later.
2. Read the file and locate the latest
   `## YYYY-MM-DD HH:MM -- {phase}` block (the most recent append).
   spec-driven appends one block per phase across any feature.
3. Surface the block's contents to working context for the rest of
   wrap-up to consume:
   - `**Discoveries:**` bullets
   - `**Decisions:**` bullets (when present)
   - `**Next Context:**` bullets (when present)

bm-notes and obsidian-notes consume from working context — they do
not re-read the file.

### Detect Phase

Runs after obsidian-notes, before Cleanup. Skipped silently if Load
found no file or no latest block.

#### Step 1: Keyword scan

Scan the in-context `**Discoveries:**` bullets for any of these
structural keywords:

- `route`, `endpoint`, `api`
- `module`, `package`, `dependency`, `dep`
- `env var`, `environment variable`, `.env`
- `migration`, `schema`, `table`
- `directory`, `folder`

#### Step 2: Structural git diff

Skip if not in a git repo. Otherwise run:

```bash
git diff --name-status $(git merge-base main HEAD)..HEAD
```

Flag a structural delta if any of the following is true:

- Any `A` (added), `D` (deleted), `R` (renamed), or `C` (copied)
  entry outside `.artifacts/`
- `package.json` `dependencies` or `devDependencies` sections changed
- `.env.example` changed
- New directory under the framework's route root (e.g.,
  `src/app/api/`, `pages/api/`, `app/routes/`)

#### Step 3: Surface suggestion

If Step 1 found a keyword OR Step 2 flagged a delta, append exactly
one line to wrap-up output:

> Structural changes detected -- consider running `/project-index re-index` to refresh `.agents/codebase/*.md`.

If neither signal fires, emit nothing.

### Cleanup Phase

Runs last, unconditional regardless of Detect output.

Write empty content to `.artifacts/.session-dump.md`. Do not delete the
file — an empty file is treated as missing on the next Load, and writing
avoids a Bash permission prompt.

## Guidelines

**DO:**
- Read the file once in Load and share contents via working context
- Emit at most one suggestion line in Detect
- Run Cleanup unconditionally — the dump is ephemeral by design
- Clear the dump file by writing empty content in Cleanup — avoids
  Bash permission prompts; empty file is treated as missing on next Load
- Treat a missing file as a silent no-op in every phase
- Mirror audit's inform-only pattern — the suggestion is
  informational, never blocking

**DON'T:**
- Prompt the user or block wrap-up exit (contrasts: silent no-op
  + unconditional Cleanup)
- Re-read the dump in bm-notes / obsidian-notes (contrasts: load
  once, share via context)
- Skip Cleanup when Detect emits nothing (contrasts: Cleanup is
  independent of signal)
- Auto-invoke `/project-index re-index` (contrasts: emit one
  suggestion line, user decides)
- Walk every block in the file (contrasts: read only the latest
  phase entry)
- Delete the file — write empty content instead (contrasts: clear
  with empty write, no Bash permission prompt)

## Error Handling

- File missing on Load: skip Load, skip Detect, downstream refs
  proceed without folded content
- Not in a git repo: skip the structural diff in Detect, rely on
  keyword scan only
- `git merge-base` fails (no `main` branch, shallow clone): skip
  the diff, rely on keyword scan only
- Latest phase block has no Discoveries section or only "none"
  bullets: rely on git diff only
- Session-dump file empty or has no `##` blocks: treat as missing,
  skip Detect
- File missing on Cleanup: no-op, skip the empty write
