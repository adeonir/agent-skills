# Session Handoff Lifecycle

Load any session handoff at `.artifacts/.handoff.md` for
downstream notes, run structural-delta detection, and clear the file
at the end so it does not leak into the next session.

## When to Use

- Invoked twice per wrap-up: once after mapping (Load phase, before
  obsidian-notes) and once after obsidian-notes (Detect + Cleanup
  phases, last)
- All phases short-circuit silently when
  `.artifacts/.handoff.md` is absent

## Workflow

### Load Phase

Runs after mapping, before obsidian-notes.

1. Check `.artifacts/.handoff.md`. If absent, no-op silently —
   Detect and Cleanup will likewise no-op later.
2. Read the file and locate the topmost
   `## YYYY-MM-DD HH:MM — {title}` block (the latest snapshot).
   Snapshots are appended newest-at-top by the producer.
3. Surface the block's contents to working context for the rest of
   wrap-up to consume:
   - `**Focus:**` line (always present)
   - `**Next step:**` line (always present)
   - `**Suggested skills:**` bullets (always present)
   - `**Decisions:**` bullets (when present)
   - `**Findings:**` bullets (when present)
   - `**Open threads:**` bullets (when present)
   - `**Blockers:**` bullets (when present)
   - `**References:**` bullets (when present)

Optional sections (`Decisions`, `Findings`, `Open threads`,
`Blockers`, `References`) are omitted from snapshots when empty.
Treat absence as silent — do not flag.

obsidian-notes consumes from working context — it does not re-read
the file.

### Detect Phase

Runs after obsidian-notes, before Cleanup. Skipped silently if Load
found no file or no latest snapshot.

#### Step 1: Keyword scan

Scan the in-context `**Findings:**`, `**References:**`, and
`**Suggested skills:**` bullets for any of these structural keywords
(skip sections that were omitted from the snapshot):

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

> Structural changes detected — consider re-indexing the codebase to refresh `.agents/codebase/*.md`.

If neither signal fires, emit nothing.

### Cleanup Phase

Runs last. Auto-clears without asking — wrap-up has already persisted
the snapshot to Obsidian, so the on-disk handoff is redundant by the
end of the workflow.

Write empty content to `.artifacts/.handoff.md`. Do not delete
the file — an empty file is treated as missing on the next Load, and
writing avoids a Bash permission prompt.

Skip silently if Load found no file or no latest snapshot.

## Guidelines

**DO:**
- Read the file once in Load and share contents via working context
- Emit at most one suggestion line in Detect
- Clear the handoff by writing empty content at the end — the
  snapshot is already in Obsidian; empty file is treated as missing
  on the next Load and avoids a Bash permission prompt
- Treat a missing file as a silent no-op in every phase
- Mirror audit's inform-only pattern — the suggestion is
  informational, never blocking

**DON'T:**
- Re-read the handoff in obsidian-notes (contrasts: load once, share
  via context)
- Walk every snapshot in the file (contrasts: read only the topmost
  snapshot — latest first)
- Delete the file — write empty content instead (contrasts: clear
  with empty write, no Bash permission prompt)
- Prompt y/n before clearing (contrasts: wrap-up has already saved
  the snapshot to Obsidian, so the on-disk copy is redundant)

## Error Handling

- File missing on Load: skip Load, skip Detect, skip Cleanup;
  downstream refs proceed without folded content
- Not in a git repo: skip the structural diff in Detect, rely on
  keyword scan only
- `git merge-base` fails (no `main` branch, shallow clone): skip
  the diff, rely on keyword scan only
- Latest snapshot has no Findings section or only "none" bullets:
  rely on git diff only
- Handoff file empty or has no `##` blocks: treat as missing,
  skip Detect and Cleanup
