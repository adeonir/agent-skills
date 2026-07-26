# Save Snapshot

Append a new snapshot block at the top of `.artifacts/HANDOFF.md`.

## When to Use

- User invokes a save trigger ("save context", "dump conversation", "checkpoint this", "session handoff", "save handoff")
- File is created if absent

## Current state

Run these before composing; they answer the snapshot header and the `State` field:

```bash
date '+%Y-%m-%d %H:%M'
git branch --show-current 2>/dev/null
git log -1 --oneline 2>/dev/null
git status --short 2>/dev/null
```

## Format

ALWAYS use this exact template structure:

````markdown
## YYYY-MM-DD HH:MM — {one-line title}

**Focus:** {what the next session should pick up; 1 line}

**Next step:** {concrete entry point — file, symbol, or command}

**State:** {branch, uncommitted files, last commit; plus what this session applied but did not commit}
````

Append a section below only when its condition holds. Never write "none" — an absent section is the empty answer.

| Section | Add when |
|---------|----------|
| `**Decisions:**` | a decision was made that lives in no artifact |
| `**Findings:**` | something was discovered worth carrying |
| `**Open threads:**` | a question is still open |
| `**Blockers:**` | something blocks progress |
| `**References:**` | a path, artifact, or URL orients the next session |

Each is a bullet list.

MUST NOT contain: content already carried by artifacts on disk, commits, PRs, issues, or documentation — reference those by path or URL instead; secrets of any kind — replace API keys, tokens, passwords, PII, and credentials embedded in URLs with `{redacted}`.

## Enrich Phase

The claude-mem MCP is an **optional** dependency: a snapshot composed without it is complete, not degraded. When the MCP is present (`mcp__plugin_claude-mem_mcp-search__*`), query it for observations relevant to `Focus` before composing the snapshot, recovering mid-session detail that scrolled out of context. Scope strictly:

- **Time**: current session window only
- **Topic**: `Focus` keywords only; skip parallel threads even when they belong to the same session
- **Budget**: top 5-10 observations, no broad sweeps
- **Fallback**: silent skip when the MCP is absent, returns nothing, or `Focus` is not yet clear

Observation IDs do not enter the snapshot body.

## Workflow

1. Run the **Current state** commands. Use the timestamp as the snapshot header.
2. Run the Enrich Phase.
3. Compose `State` from the branch, uncommitted files, and last commit they returned, plus anything this session applied that is not yet committed. Omit the field outside a git repo, where the three git commands return nothing.
4. Compose the remaining sections from working context. When an argument is present, treat it as the next session's focus and tailor `Focus` and `Next step` to it.
5. Write `.artifacts/HANDOFF.md`:
   - **Absent**: create it with `# Handoff` as the H1, then the snapshot block
   - **Present**: prepend the snapshot block after the H1, above the previous topmost block; insert the H1 first when the file lacks one
6. Report the snapshot title.

## Guidelines

- Bullets, not paragraphs — keep each section terse
- Point `Next step` at a symbol, path, or command rather than a line number; line numbers drift between sessions
