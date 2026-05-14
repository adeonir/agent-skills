# Load Snapshot

Read `.artifacts/.handoff.md` so the current session resumes
with prior context.

## When to Use

- User invokes a load trigger ("resume session", "load handoff",
  "continue from last") at session start or mid-session
- Wrap-up Load phase consumes the latest snapshot to compose notes
- Silent no-op when the file is absent or empty

## Workflow

1. Check `.artifacts/.handoff.md`:
   - **Absent**: silent no-op, return without output
   - **Empty or has no `## YYYY-MM-DD HH:MM` blocks**: silent no-op
2. Read the file.
3. Locate the topmost `## YYYY-MM-DD HH:MM — {title}` block. This is
   the latest snapshot — saves prepend at the top.
4. Surface the block's contents to working context for the rest of
   the session to consume:
   - `**Focus:**` — always present
   - `**Next step:**` — always present
   - `**Suggested skills:**` — always present
   - `**Decisions:**` — optional, surface when present
   - `**Findings:**` — optional, surface when present
   - `**Open threads:**` — optional, surface when present
   - `**Blockers:**` — optional, surface when present
   - `**References:**` — optional, surface when present
5. Brief output to user: snapshot title + Next step (one line).

## Guidelines

- Read the file once; do not re-read for downstream consumers — share
  via working context
- Do not print the full snapshot to chat unless the user asks; fold
  silently into context
- Do not auto-clear after load — clear is a separate explicit op
- Treat omitted optional sections as empty, not as malformed input

## Error Handling

- File missing: silent no-op
- File empty or no `##` blocks: silent no-op
- Topmost block missing a required section (`Focus`, `Next step`,
  `Suggested skills`): surface what is present and flag the gap to
  the user before continuing
- Optional section absent: skip silently — sections are omitted by
  design when empty
- Read fails: report the error and stop; do not partial-load
