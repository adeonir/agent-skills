# Session Handoff Lifecycle

Load the session handoff at `.artifacts/HANDOFF.md` for downstream notes, then clear the file after successful persistence.

## When to Use

- Invoked twice per wrap-up: once after mapping (Load phase, before notes) and once after notes (Cleanup phase, last)
- Both phases short-circuit silently when `.artifacts/HANDOFF.md` is absent

## Workflow

### Load Phase

Runs after mapping, before notes.

1. Check `.artifacts/HANDOFF.md`. If absent, no-op silently — Cleanup will likewise no-op later.
2. Read the **whole file**. Treat it as a claim to check against the current conversation, not as authority; surface a disagreement instead of silently carrying a stale or unsupported assertion into a durable note.
3. Surface its contents to working context for the rest of wrap-up to consume, per section:
   - `**Focus:**` line (always present)
   - `**Context:**` bullets (always present)
   - `**Next step:**` line (always present)
   - `**Decisions:**` bullets (when present)
   - `**Findings:**` bullets (when present)
   - `**Open threads:**` bullets (when present)
   - `**Blockers:**` bullets (when present)
   - `**References:**` bullets (when present)

Optional sections (`Decisions`, `Findings`, `Open threads`, `Blockers`, `References`) are omitted from the handoff when empty. Treat absence as silent — do not flag.

The notes phase consumes from working context — it does not re-read the file.

### Cleanup Phase

Runs last. Auto-clears without asking only after every configured note write succeeds. Preserve the handoff when any required write fails so the context remains available for retry.

Write empty content to `.artifacts/HANDOFF.md`. Do not delete the file — an empty file is treated as missing on the next Load, and writing avoids a Bash permission prompt.

Skip silently if Load found no usable handoff.

## Error Handling

- File missing on Load: skip Load, skip Cleanup; downstream refs proceed without folded content
- Handoff file empty or contains neither `Focus` nor `Next step`: treat as missing, skip Cleanup
- Any configured note write fails: preserve the handoff and report the failed persistence
