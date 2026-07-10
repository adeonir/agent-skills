# Save Snapshot

Append a new snapshot block at the top of `.artifacts/HANDOFF.md`.

## When to Use

- User invokes a save trigger ("save context", "dump conversation", "checkpoint this", "session handoff", "save handoff")
- File is created if absent

## Argument

The skill accepts an optional argument describing what the next session will focus on:

```
/handoff continue debugging the auth race condition
```

When an argument is present, tailor `Focus` and `Next step` to that focus. Without an argument, capture the current state generically.

## Format

ALWAYS use this exact template structure. Two sections are required every save; five are optional and must be omitted when empty (do not write "none").

````markdown
## YYYY-MM-DD HH:MM — {one-line title}

**Focus:** {what the next session should pick up; 1 line}

**Next step:** {concrete entry point — file, function, or command}

**Decisions:**
- {decision + rationale}

**Findings:**
- {discovery worth carrying}

**Open threads:**
- {unresolved question or branch}

**Blockers:**
- {what blocks progress + what would unblock}

**References:**
- {paths, artifact links, URLs}
````

| Section | Required | Notes |
|---------|----------|-------|
| `Focus` | yes | One-line orientation for the next session |
| `Next step` | yes | Concrete entry point — file, function, command |
| `Decisions` | no | Omit when no decisions live outside artifacts |
| `Findings` | no | Omit when nothing notable to carry |
| `Open threads` | no | Omit when all threads closed |
| `Blockers` | no | Omit when unblocked |
| `References` | no | Omit when not applicable |

## Anti-Duplication Rule

Do not duplicate content already captured in artifacts on disk, commits, PRs, issues, documentation, or claude-mem observations. Reference them by path or URL instead. The handoff carries only context that lives in the conversation: unresolved threads, decisions made on the fly, where to pick up, which skill to invoke next.

## Enrich Phase

Run before composing the snapshot. When the claude-mem MCP is available (`mcp__plugin_claude-mem_mcp-search__*`), query for **current-session** observations relevant to `Focus`. Fold matches into working context so mid-session detail that scrolled out is recovered before the snapshot is written.

**Scoping rules (mandatory — do not pollute working context):**

- **Time**: current session window only — exclude prior sessions
- **Topic**: filter by `Focus` keywords; skip parallel unrelated threads even when they belong to the same session
- **Budget**: top 5-10 most relevant observations, no broad sweeps
- **Fallback**: silent skip when MCP is unavailable, returns nothing, or the conversation has no clear Focus yet

The goal is recovering lost session detail, not importing history or adjacent threads. Snapshot Findings/Decisions stay terse human prose — observation IDs do not enter the snapshot body.

## Workflow

1. Resolve current date and time as `YYYY-MM-DD HH:MM` (local time acceptable; pick one convention and keep it).
2. Run the Enrich Phase to fold relevant current-session observations into working context. Skip silently when claude-mem MCP is absent.
3. Compose the snapshot from working context. Apply the anti-duplication rule — reference artifacts by path, do not replay them. Redact secrets: replace API keys, tokens, passwords, PII, and credentials embedded in URLs with `{redacted}` before writing.
4. If an argument was passed, treat it as the focus of the next session and tailor `Focus` and `Next step` accordingly.
5. Decide which optional sections apply. Omit any that would be empty — do not include the label.
6. Check `.artifacts/HANDOFF.md`:
   - **Absent**: create it with `# Handoff` as the H1, then the snapshot block immediately after
   - **Present**: prepend the new snapshot block above existing content (after the H1, before the previous topmost block)
7. Confirm the file was written and report the snapshot title.

## Guidelines

- Two sections required (`Focus`, `Next step`); the rest are optional — omit when empty
- Bullets, not paragraphs — keep each section terse
- Append at the top so load consumers always read the latest first
- Reference artifacts by path or URL; never replay their content
- Redact secrets before writing — API keys, tokens, passwords, PII, and credentials in URLs become `{redacted}`; conversation context is not a safe place for secrets
- Tailor to the argument when present; capture generic state when absent
- Run Enrich Phase when claude-mem MCP is available; scope strictly to current session + Focus topic; skip silently otherwise

## Error Handling

- Bash/Write fails to create file: report the error and stop; do not retry silently
- File exists but has no `# Handoff` H1: insert the H1 before prepending the new block
- Date/time resolution fails: fall back to `YYYY-MM-DD` only (no time component) rather than blocking the save
- Argument is present but unintelligible: treat as no argument and fall back to generic capture
- claude-mem MCP unavailable, returns nothing, or query times out: skip Enrich Phase silently and compose from working context only
