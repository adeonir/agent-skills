# Session Handoff Lifecycle

Load the session handoff at `.artifacts/HANDOFF.md` for notes written later, then clear the file after successful persistence.

## When to Use

Loaded for the two phases that bracket note writing: the Load phase makes the handoff fields available, and the Cleanup phase empties the file afterwards. Both phases skip silently when `.artifacts/HANDOFF.md` is absent.

## Workflow

### Load Phase

Runs after mapping, before notes.

1. Check `.artifacts/HANDOFF.md`. If absent, no-op silently — Cleanup will likewise no-op later.
2. Read the **whole file**. Report a claim the current conversation or the repository contradicts — a file that no longer exists, a next step already done, a decision since reversed — instead of copying it into a durable note. A claim neither confirmed nor contradicted carries over.
3. Make these fields available to the rest of the workflow:
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

Run this phase once the note writes finish. If every configured note write succeeds, clear the handoff without asking. If any configured note write fails, preserve the handoff so the user can retry.

Write empty content to `.artifacts/HANDOFF.md`. Do not delete the file. An empty file is treated as missing on the next Load, and writing avoids a Bash permission prompt.

Skip silently if Load found no usable handoff.

## Error Handling

- Handoff file empty or contains neither `Focus` nor `Next step`: treat as missing, skip Cleanup
