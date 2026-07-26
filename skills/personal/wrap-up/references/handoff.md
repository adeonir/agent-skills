# Session Handoff Lifecycle

Load any session handoff at `.artifacts/HANDOFF.md` for downstream notes, then clear the file at the end so it does not leak into the next session.

## When to Use

- Invoked twice per wrap-up: once after mapping (Load phase, before obsidian-notes) and once after obsidian-notes (Cleanup phase, last)
- Both phases short-circuit silently when `.artifacts/HANDOFF.md` is absent

## Workflow

### Load Phase

Runs after mapping, before obsidian-notes.

1. Check `.artifacts/HANDOFF.md`. If absent, no-op silently — Cleanup will likewise no-op later.
2. Read the **whole file**. Collect **every** dated block — `## YYYY-MM-DD HH:MM — {title}`, or `## YYYY-MM-DD — {title}` when the save had no clock — not just the topmost. A long session may append many snapshots across distinct threads and dates; each carries context worth persisting. A newer snapshot does not supersede an older one. Walking every block is specific to wrap-up, which persists the full session — a mid-session resume only needs the latest.
3. Group the collected blocks by date (the `YYYY-MM-DD` in each header). Deduplicate within and across blocks: a finding or decision repeated across checkpoints collapses to one item; genuinely distinct items are all kept. Read every block before deciding duplicates — never drop an older item just because a newer block exists.
4. Surface the grouped, deduplicated contents to working context for the rest of wrap-up to consume, per section:
   - `**Focus:**` line (always present)
   - `**Next step:**` line (always present)
   - `**State:**` line (always present; loaded for context, never carried into a note — branch names and commit hashes are forbidden in both notes)
   - `**Decisions:**` bullets (when present)
   - `**Findings:**` bullets (when present)
   - `**Open threads:**` bullets (when present)
   - `**Blockers:**` bullets (when present)
   - `**References:**` bullets (when present)

Optional sections (`Decisions`, `Findings`, `Open threads`, `Blockers`, `References`) are omitted from snapshots when empty. Treat absence as silent — do not flag.

obsidian-notes consumes from working context — it does not re-read the file.

### Cleanup Phase

Runs last. Auto-clears without asking — wrap-up has already persisted the snapshot to Obsidian, so the on-disk handoff is redundant by the end of the workflow.

Write empty content to `.artifacts/HANDOFF.md`. Do not delete the file — an empty file is treated as missing on the next Load, and writing avoids a Bash permission prompt.

Skip silently if Load found no file or no snapshot.

## Guidelines

**DO:**
- Read the whole file once in Load — every snapshot block — and share contents via working context
- Group loaded snapshots by date and deduplicate before surfacing — collapse repeats, keep distinct items from every block
- Clear the handoff by writing empty content at the end — the snapshot is already in Obsidian; empty file is treated as missing on the next Load and avoids a Bash permission prompt
- Treat a missing file as a silent no-op in every phase

**DON'T:**
- Re-read the handoff in obsidian-notes (contrasts: load once, share via context)
- Read only the topmost block (contrasts: walk every snapshot — a resume needs only the latest, but wrap-up persists the whole session)
- Drop older snapshots as superseded (contrasts: newest does not replace older — merge distinct items, collapse only true repeats)
- Delete the file — write empty content instead (contrasts: clear with empty write, no Bash permission prompt)
- Prompt y/n before clearing (contrasts: wrap-up has already saved the snapshot to Obsidian, so the on-disk copy is redundant)

## Error Handling

- File missing on Load: skip Load, skip Cleanup; downstream refs proceed without folded content
- Handoff file empty or has no `##` blocks: treat as missing, skip Cleanup
