# Save Snapshot

Append a new snapshot block at the top of
`.artifacts/.handoff.md`.

## When to Use

- User invokes a save trigger ("save context", "dump conversation",
  "checkpoint this", "session handoff", "save handoff")
- File is created if absent

## Argument

The skill accepts an optional argument describing what the next
session will focus on:

```
/handoff continue debugging the auth race condition
```

When an argument is present, tailor `Focus`, `Next step`, and
`Suggested skills` to that focus. Without an argument, capture the
current state generically.

## Format

ALWAYS use this exact template structure. Three sections are
required every save; five are optional and must be omitted when
empty (do not write "none").

````markdown
## YYYY-MM-DD HH:MM — {one-line title}

**Focus:** {what the next session should pick up; 1 line}

**Next step:** {concrete entry point — file, function, or command}

**Suggested skills:**
- {skill invocation} — {why the next session should run it}

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
| `Suggested skills` | yes | At least one skill the next session should invoke |
| `Decisions` | no | Omit when no decisions live outside artifacts |
| `Findings` | no | Omit when nothing notable to carry |
| `Open threads` | no | Omit when all threads closed |
| `Blockers` | no | Omit when unblocked |
| `References` | no | Omit when not applicable |

## Anti-Duplication Rule

Do not duplicate content already captured in artifacts on disk,
commits, PRs, issues, or documentation. Reference them by path or URL
instead. The handoff carries only context that lives in the
conversation: unresolved threads, decisions made on the fly, where to
pick up, which skill to invoke next.

## Suggested Skills

List skills the next session should invoke. Be additive to
`Next step` — do not restate the entry point as a skill bullet.
Examples:

- `/spec-driven implement story S-2` — implementation phase pending
  for the auth feature
- `/git-helpers commit` — atomic commits queued before context loss
- `/debug-tools` — race condition root cause still unresolved

When the next step itself is a skill invocation, keep `Suggested
skills` to one bullet that names the same skill plus the rationale,
or expand with adjacent skills the next session may need.

## Workflow

1. Resolve current date and time as `YYYY-MM-DD HH:MM` (local time
   acceptable; pick one convention and keep it).
2. Compose the snapshot from working context. Apply the
   anti-duplication rule — reference artifacts by path, do not
   replay them.
3. If an argument was passed, treat it as the focus of the next
   session and tailor `Focus`, `Next step`, and `Suggested skills`
   accordingly.
4. Decide which optional sections apply. Omit any that would be
   empty — do not include the label.
5. Check `.artifacts/.handoff.md`:
   - **Absent**: create it with `# Handoff` as the H1, then the
     snapshot block immediately after
   - **Present**: prepend the new snapshot block above existing
     content (after the H1, before the previous topmost block)
6. Confirm the file was written and report the snapshot title.

## Guidelines

- Three sections required (`Focus`, `Next step`, `Suggested skills`);
  the rest are optional — omit when empty
- Bullets, not paragraphs — keep each section terse
- Append at the top so load consumers always read the latest first
- Reference artifacts by path or URL; never replay their content
- Tailor to the argument when present; capture generic state when
  absent

## Error Handling

- Bash/Write fails to create file: report the error and stop; do not
  retry silently
- File exists but has no `# Handoff` H1: insert the H1 before
  prepending the new block
- Date/time resolution fails: fall back to `YYYY-MM-DD` only (no time
  component) rather than blocking the save
- Argument is present but unintelligible: treat as no argument and
  fall back to generic capture
