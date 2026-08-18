# Save Handoff

Consolidate current conversation state into `.artifacts/HANDOFF.md`.

## When to Use

- User invokes a save trigger ("save context", "dump conversation", "checkpoint this", "session handoff", "save handoff")
- `.artifacts/HANDOFF.md` is created when absent and consolidated when present

## Format

ALWAYS use this exact template structure:

````markdown
# Handoff

**Focus:** [what the next session should pick up; 1 line]

**Context:**
- [live context the next session needs, including why the work is in its current direction]

**Next step:** [concrete entry point — file, symbol, or command]
````

Append a section below only when its condition holds. Never write "none" — an absent section is the empty answer.

| Section | Add when |
|---------|----------|
| `**Decisions:**` | an active decision and its rationale live in no artifact |
| `**Findings:**` | something was discovered worth carrying |
| `**Open threads:**` | a question is still open |
| `**Blockers:**` | something blocks progress |
| `**References:**` | a path, artifact, or URL orients the next session |

Each is a bullet list.

The handoff MUST NOT contain:

- Content already carried by artifacts on disk, commits, pull requests, issues, or documentation. Reference that content by path or URL instead.
- Claims from the prior handoff that conflict with current evidence.
- Secrets of any kind. Replace API keys, tokens, passwords, personally identifiable information, and credentials embedded in URLs with `{redacted}`.

## Workflow

1. Read `.artifacts/HANDOFF.md` when present. Check its claims against the current conversation and artifacts. Preserve relevant information, update changed information, and remove superseded or redundant content. Record any unresolved conflict under `Open threads`.
2. Compose the complete handoff from the prior handoff and current working context. When an argument is present, treat it as the next session's focus and tailor `Focus`, `Context`, and `Next step` to it.
3. Distinguish verified facts from assumptions. Record an unverified belief as an open thread instead of promoting it to a finding or decision.
4. Compose the complete handoff before writing it to `.artifacts/HANDOFF.md`.
5. Report `Focus` and `Next step`.

## Guidelines

- Keep `Context` and optional sections as terse bullets
- Point `Next step` at a symbol, path, or command rather than a line number; line numbers drift between sessions
