---
name: wrap-up
description: "End-of-session persistence of the session's work to Obsidian as a session note per project and the daily note. Use when closing a work session and recording what it changed. Not for mid-session checkpoints, conversation handoffs, standalone project or meeting notes, or repository-wide project context."
disable-model-invocation: true
---

# Wrap Up Session

## Triggers

- **End-of-session command** (`/wrap-up`) → run the workflow below

End-of-session documentation to Obsidian. The skill is single-trigger: every invocation runs the full workflow.

## Workflow

```text
mapping → handoff:Load → notes (compose) → handoff:Cleanup → archive offer
```

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Resolve the project entry
- [ ] Step 2: Load the handoff
- [ ] Step 3: Write the session note and the daily note
- [ ] Step 4: Clear the handoff
- [ ] Step 5: Collect past-month daily notes
- [ ] Step 6: Report
```

**Step 1. Resolve the project.** Load [mapping.md](references/mapping.md) and resolve the project entry and the base tags. When the registry or the entry is missing, load [bootstrap.md](references/bootstrap.md) as mapping directs. Every later step depends on this output. Done when the entry's `name`, `obsidian.path`, and `tags` are known.

**Step 2. Load the handoff.** Load [handoff.md](references/handoff.md) and run its Load phase — the consolidated handoff at `.artifacts/HANDOFF.md`, when present, feeds the note content. It enters as a claim to check, not as authority: report a claim the current conversation or the repository contradicts instead of copying it into a durable note. Done when the handoff fields are in working context, or the handoff is known to be absent.

**Step 3. Write the notes.** Load [notes.md](references/notes.md) and write the Obsidian session note and the daily note. If a draft fails the check in notes.md, rewrite it and check again before writing. Done when each configured write returned success or a failure to report.

**Step 4. Clear the handoff.** Run the Cleanup phase of handoff.md — clear the handoff once every configured note write succeeded. Done when the handoff is empty, or preserved because a write failed.

**Step 5. Collect past months.** Offer to archive past months as notes.md sets out — daily notes from earlier months still at the root of `Daily/` are listed in the report, and moved into their monthly folder only on the user's yes. Done when the list is collected, or none exist.

**Step 6. Report.** End with one report: the session note path when one was written and the daily note path, what the notes record in one to three sentences — what changed, on an update — and the open items: a contradicted handoff claim, a failed write, and the past-month daily notes awaiting the archive answer, grouped by target folder. Never paste either note. Done when the report carries the note paths, the summary, and every open item, or states that none exist.

Run the six steps in one pass. The initial invocation authorizes the first four: never pause for confirmation between them, never preview the note content in chat, and report only at the end. Two exceptions: the bootstrap questions on a first run in Step 1, and the archive question in Step 5, asked once alongside the report.
