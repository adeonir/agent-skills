# Save Handoff

Consolidate current conversation state into `.artifacts/HANDOFF.md`.

## Format

ALWAYS use this exact template structure:

````markdown
# Handoff

**Focus:** [what the next session should pick up; 1 line]

**Context:**
- [user's goal, the condition that marks it done, constraints, and why the work is in its current direction]

**Current state:**
- [work completed, remaining work, and relevant workspace state]
- [checks run with their commands and results, when relevant]
````

Append a section below only when its condition holds. Never write "none" — an absent section is the empty answer.

| Section | Add when |
|---------|----------|
| `**Decisions:**` | an active decision, its rationale, or an alternative rejected for it lives in no artifact |
| `**Findings:**` | something was discovered worth carrying |
| `**Open threads:**` | a question is still open |
| `**Blockers:**` | something blocks progress |
| `**References:**` | a path, artifact, or URL orients the next session |

Every section after `Focus` is a list of terse bullets.

The handoff MUST NOT contain:

- Content already carried by artifacts on disk, commits, pull requests, issues, or documentation. Reference that content by path or URL instead.
- Raw conversation history.
- Chat phrasing — "as discussed", "the user confirmed", "we agreed", "you chose". State a rationale, decision, or constraint as a fact about the work, keeping all of its content.
- Secrets of any kind. Replace API keys, tokens, passwords, personally identifiable information, and credentials embedded in URLs with `{redacted}`.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Read and check the existing handoff
- [ ] Step 2: Confirm there is new work to carry
- [ ] Step 3: Compose the handoff
- [ ] Step 4: Capture the workspace state
- [ ] Step 5: Mark unverified claims
- [ ] Step 6: Write the file and check it. If the check fails, return to Step 3
- [ ] Step 7: Report
```

**Step 1. Read the existing handoff.** Read `.artifacts/HANDOFF.md` when present — it is created when absent and consolidated when present. Treat its claims as unverified until checked against the current conversation, workspace, and artifacts. Preserve relevant information, update changed information, and remove superseded or redundant content. Record any unresolved conflict under `Open threads`. Before composing, list in working context one disposition per prior bullet — `kept`, `updated`, `removed`, or `open thread` — and never write the list to the file. Done when the list covers every prior bullet, or the file is confirmed absent.

**Step 2. Confirm new work.** If the conversation holds no work beyond what the existing handoff carries, write nothing, offer to load it instead, and stop. Done when the conversation holds work the handoff does not carry, or the offer is made.

**Step 3. Compose.** Compose the complete handoff from the prior handoff and current working context. When an argument is present, treat it as the next session's focus and tailor `Focus`, `Context`, and `Current state` to it. Done when `Focus`, `Context`, and `Current state` are filled and each optional section is present only when its condition holds.

**Step 4. Capture the workspace state.** For code work, run `git branch --show-current`, `git log -1 --oneline`, and `git status --short`, and take the branch, commit, and changed paths in `Current state` from their output, never from memory. Add the checks run with their commands and results. For a failing check or error, capture the command that reproduces it. Omit workspace details that do not affect resumption. Done when `Current state` carries what the next session needs to reproduce the workspace, or the work involves no code.

**Step 5. Mark unverified claims.** End each load-bearing claim not checked against current evidence with `(unverified: [source])`. A bullet without the mark was verified at save. Keep unresolved beliefs under `Open threads` rather than presenting them as findings or decisions. Done when every load-bearing claim was checked or carries the mark.

**Step 6. Write and check.** Write the handoff to `.artifacts/HANDOFF.md`, then run `python3 <this-skill>/scripts/check_handoff.py .artifacts/HANDOFF.md`, resolving `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose that directory, stop and report an environment problem. The script flags a missing required section, a section that says none, chat phrasing, and secrets; fix each line it flags as its message says and run it again. Done when the script prints `clean` and the file holds no content already carried by an artifact and no raw conversation history; otherwise return to Step 3.

**Step 7. Report.** Report the path, what the handoff holds — its focus and current state — in one to three sentences, and the open threads and blockers it carries. List on one line the prior bullets Step 1 marked `removed`. Never paste the handoff. Done when the report names the path, the focus, every open thread and blocker, and every removed bullet.

## Examples

A consolidated handoff with one optional section and one unverified claim:

```markdown
# Handoff

**Focus:** finish the audit fixes to the `handoff` skill

**Context:**
- Goal: the skill passes the audit checklist with no fail left; done when the decision items are settled and the validator shows no new warning
- Constraint: every edit follows the rules in `.agents/rules/`

**Current state:**
- Branch `main`; changed paths: `skills/productivity/handoff/SKILL.md`, `instructions/save.md`, `instructions/load.md`
- Validator not re-run since the edits

**Open threads:**
- Whether `load.md` keeps its last guideline (unverified: no with/without test run yet)
```
