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

MUST NOT contain: content already carried by artifacts on disk, commits, PRs, issues, or documentation — reference those by path or URL instead; claims from the prior handoff that conflict with current evidence; secrets of any kind — replace API keys, tokens, passwords, PII, and credentials embedded in URLs with `{redacted}`.

## Workflow

1. Read `.artifacts/HANDOFF.md` when present. Treat it as a claim to check against the current conversation and artifacts, not as authority: preserve information that remains relevant, update changed state, remove superseded or redundant content, and surface unresolved disagreement as an open thread.
2. Compose the complete handoff from the prior handoff and current working context. When an argument is present, treat it as the next session's focus and tailor `Focus`, `Context`, and `Next step` to it.
3. Distinguish verified facts from assumptions. Record an unverified belief as an open thread instead of promoting it to a finding or decision.
4. Write the consolidated document to `.artifacts/HANDOFF.md`, replacing the prior file only after the complete result is composed.
5. Report `Focus` and `Next step`.

## Guidelines

- Keep `Context` and optional sections as terse bullets
- Point `Next step` at a symbol, path, or command rather than a line number; line numbers drift between sessions
