# Session Handoff Lifecycle

Load the blocks of `.artifacts/HANDOFF.md` that this session worked on for notes written later, then remove those blocks after successful persistence.

## When to Use

Loaded for the two phases that bracket note writing: the Load phase makes the fields of this session's blocks available, and the Cleanup phase removes those blocks afterwards. Both phases skip silently when `.artifacts/HANDOFF.md` is absent.

## Workflow

### Load Phase

Runs after mapping, before notes.

1. Check `.artifacts/HANDOFF.md`. If absent, no-op silently — Cleanup will likewise no-op later.
2. Read the **whole file**. It holds one `## <topic>` block per subject, saved by this session and by others. Pick this session's blocks: a block belongs when its `**Context:**` goal and its `**Current state:**` describe work this conversation did or continued. Leave every other block untouched and report its heading once as belonging to another session. When no block belongs, treat the handoff as unrelated: skip Cleanup and report it once. Read on only for this session's blocks.
3. The blocks predate the work done after their last save, so the current conversation and the repository take precedence on current state. Where the session's work superseded a claim in one of this session's blocks — a step since done, a branch since merged — record the current state and drop the claim without reporting it. Report a claim only when the session's work does not explain the contradiction — a file that no longer exists, a decision reversed outside this session — and never copy it into a durable note. A claim neither confirmed nor contradicted carries over.
4. Make these fields of this session's blocks available to the rest of the workflow, and keep the exact heading of each block for Cleanup:
   - `**Context:**` bullets (always present)
   - `**Current state:**` bullets (always present)
   - `**Decisions:**` bullets (when present)
   - `**Findings:**` bullets (when present)
   - `**Open threads:**` bullets (when present)
   - `**Blockers:**` bullets (when present)
   - `**References:**` bullets (when present)

Optional sections (`Decisions`, `Findings`, `Open threads`, `Blockers`, `References`) are omitted from a block when empty. Treat absence as silent — do not flag.

The notes phase consumes from working context — it does not re-read the file.

### Cleanup Phase

Run this phase once the note writes finish. If every configured note write succeeds, remove this session's blocks without asking: run `python3 <this-skill>/scripts/drop_blocks.py .artifacts/HANDOFF.md "<heading>" ...` with the exact heading of each block Load kept, resolving `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose that directory, stop and report an environment problem. The script leaves every other block unchanged and empties the file when no block remains. When it exits 1 or 2, report its message and leave the file as it is. If any configured note write fails, preserve the whole handoff so the user can retry.

Skip silently if Load found no block that belongs to this session.

## Error Handling

- Handoff file empty or holding no `##` topic block: treat as missing, skip Cleanup
- No block describes work this session did: treat as missing, preserve the file, skip Cleanup
