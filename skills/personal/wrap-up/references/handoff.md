# Session Handoff Lifecycle

Load any session handoff at `.artifacts/.session-handoff.md` for
downstream notes, run structural-delta detection, and ask before
clearing.

## When to Use

- Invoked twice per wrap-up: once after mapping (Load phase, before
  auto-memory) and once after obsidian-notes (Detect + Cleanup phases,
  last)
- All phases short-circuit silently when
  `.artifacts/.session-handoff.md` is absent

## Workflow

### Load Phase

Runs after mapping, before auto-memory.

1. Check `.artifacts/.session-handoff.md`. If absent, no-op silently —
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

bm-notes and obsidian-notes consume from working context — they do
not re-read the file.

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

Runs last. Cleanup is opt-in: ask before clearing.

> Clear `.artifacts/.session-handoff.md`? (y/n)

If accepted: write empty content to `.artifacts/.session-handoff.md`.
Do not delete the file — an empty file is treated as missing on the
next Load, and writing avoids a Bash permission prompt.

If declined or skipped: leave the file intact. Future saves continue
to prepend at the top, preserving the snapshot history.

## Guidelines

**DO:**
- Read the file once in Load and share contents via working context
- Emit at most one suggestion line in Detect
- Ask before Cleanup — the handoff persists across sessions by design
- Clear the handoff by writing empty content when accepted — avoids
  Bash permission prompts; empty file is treated as missing on next
  Load
- Treat a missing file as a silent no-op in every phase
- Mirror audit's inform-only pattern — the suggestion is
  informational, never blocking

**DON'T:**
- Auto-clear without asking (contrasts: Cleanup is opt-in; the
  handoff is persistent across sessions by design)
- Re-read the handoff in bm-notes or obsidian-notes (contrasts: load
  once, share via context)
- Walk every snapshot in the file (contrasts: read only the topmost
  snapshot — latest first)
- Delete the file — write empty content instead (contrasts: clear
  with empty write, no Bash permission prompt)

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
- User declines Cleanup: leave file intact, no-op
