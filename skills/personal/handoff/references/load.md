# Load Snapshot

Read `.artifacts/HANDOFF.md` so the current session resumes with prior context.

## When to Use

- User invokes a load trigger ("resume session", "load handoff", "continue from last") at session start or mid-session
- Another workflow needs the latest snapshot as input

## Workflow

1. Read `.artifacts/HANDOFF.md`. Silent no-op — no output at all — when the file is absent, empty, or carries no dated `## YYYY-MM-DD` block.
2. Take the topmost dated block: `## YYYY-MM-DD HH:MM — {title}`, or `## YYYY-MM-DD — {title}` when the save had no clock. Saves prepend, so the topmost is the latest.
3. Report the block's title and `Next step`, then a one-line index of the remaining block headers as `MM-DD — {title}` joined by ` | `. Omit the index line when the file holds a single block.
4. Read an older block only when the user names one from the index.

## Guidelines

- Do not print the topmost block in full unless asked — reading it already puts it in context
- Do not clear after load; clear is a separate explicit op
- Flag the gap when the topmost block lacks `Focus` or `Next step`, then continue with what is present
- Treat the index as an inventory, not a queue — older blocks stay unread until named
