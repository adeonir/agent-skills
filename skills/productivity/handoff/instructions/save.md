# Save Handoff

Consolidate current conversation state into `.artifacts/HANDOFF.md`.

## Format

ALWAYS use this exact template structure:

````markdown
# Handoff

**Focus:** [what the next session should pick up; 1 line]

**Context:**
- [user's goal, constraints, and why the work is in its current direction]

**Current state:**
- [work completed, remaining work, and relevant workspace state]
- [checks run and results, when relevant]
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
- Chat phrasing — "as discussed", "the user confirmed", "we agreed", "you chose". State a rationale, decision, or constraint as a fact about the work, keeping all of its content.
- Secrets of any kind. Replace API keys, tokens, passwords, personally identifiable information, and credentials embedded in URLs with `{redacted}`.

## Workflow

1. Read `.artifacts/HANDOFF.md` when present — it is created when absent and consolidated when present. Treat its claims as unverified until checked against the current conversation, workspace, and artifacts. Preserve relevant information, update changed information, and remove superseded or redundant content. Record any unresolved conflict under `Open threads`.
2. Compose the complete handoff from the prior handoff and current working context. When an argument is present, treat it as the next session's focus and tailor `Focus`, `Context`, and `Current state` to it.
3. Carry the user's goal and constraints, the rationale for the current direction, work completed, and remaining work. Let the next session infer its next action from this context.
4. For code work, capture the relevant branch, commit, changed paths, and checks with their results. Omit workspace details that do not affect resumption.
5. Mark each load-bearing claim `verified` with its evidence or `unverified` with its source. Keep unresolved beliefs under `Open threads` rather than presenting them as findings or decisions.
6. Compose the complete handoff before writing it to `.artifacts/HANDOFF.md`.
7. Report `Focus` and `Current state`.

## Guidelines

- Keep `Context` and optional sections as terse bullets
- Include enough rationale to explain the current direction; omit raw conversation history
- Reference existing artifacts instead of copying their contents
