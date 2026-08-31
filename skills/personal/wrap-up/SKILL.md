---
name: wrap-up
description: "End-of-session context persistence to Obsidian. Use when closing a session, saving work, or documenting what was accomplished. Not for mid-session notes, conversation handoffs, or repository-wide project context."
---

# Wrap Up Session

## Triggers

- **End-of-session command** ("wrap up", "wrap-up", "end session", "finish up", "close session") → run the workflow below

End-of-session documentation to Obsidian. The skill is single-trigger: every invocation runs the full workflow.

## Workflow

```text
mapping → handoff:Load → notes (compose) → handoff:Cleanup
```

1. **Load [mapping.md](references/mapping.md)** and resolve the vault root, the project entry, and the base tags. Every later step depends on this output.
2. **Load [handoff.md](references/handoff.md)** and run its Load phase — the consolidated handoff at `.artifacts/HANDOFF.md`, when present, feeds the note content. It enters as a claim to check against the current conversation, not as authority: report a stale or unsupported claim instead of copying it into a durable note.
3. **Load [notes.md](references/notes.md)** and write the Obsidian session note and the daily note.
4. **Run the Cleanup phase** of the reference loaded in step 2 — clear the handoff once every configured note write succeeded.

Run the four steps in one pass. The initial invocation authorizes all of them: never pause for confirmation between steps, never preview the note content in chat, and report only at the end.
