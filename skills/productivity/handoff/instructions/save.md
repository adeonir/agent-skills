# Save Handoff

Consolidate current conversation state into `.artifacts/HANDOFF.md`, one block per topic.

## Format

ALWAYS use this exact template structure:

````markdown
# Handoff

## [topic]

**Context:**
- [user's goal, the condition that marks it done, constraints, and why the work is in its current direction]

**Current state:**
- [work completed and remaining work]
- [checks run with their commands and results, when relevant]
````

A topic is a subject the next session can resume without the others. Each topic has one `##` block; the heading names the subject in a few words, and the first `Context` bullet states its goal. Work on a subject no block covers adds a block, work on a subject a block covers updates that block, and a block with nothing left to carry is removed.

Add a section to a block only when its condition holds. Never write "none" — an absent section is the empty answer.

| Section | Add when |
|---------|----------|
| `**Decisions:**` | an active decision, its rationale, or an alternative rejected for it lives in no artifact |
| `**Findings:**` | something was discovered worth carrying |
| `**Open threads:**` | a question that decides the topic's remaining work is still open |
| `**Blockers:**` | something blocks progress |
| `**References:**` | a path, artifact, or URL orients the next session |

Every section is a list of terse bullets.

The handoff MUST NOT contain:

- Content already carried by artifacts on disk, commits, pull requests, issues, or documentation. Reference that content by path or URL instead.
- Git state: commit hashes, the branch, changed paths, or a commit, push, or merge still to do. The next session reads it from git.
- A matter outside the topic of its block. A side matter the next session can resume on its own gets its own block; any other stays out.
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
- [ ] Step 4: Capture the check results
- [ ] Step 5: Mark unverified claims
- [ ] Step 6: Write the file and check it. If the check fails, return to Step 3
- [ ] Step 7: Report
```

**Step 1. Read the existing handoff.** Read `.artifacts/HANDOFF.md` when present — it is created when absent and consolidated when present. Treat its claims as unverified until checked against the current conversation, workspace, and artifacts. Preserve relevant information, update changed information, and remove superseded or redundant content, topic by topic. Record any unresolved conflict under `Open threads` in its topic. Before composing, list in working context one disposition per prior bullet — `kept`, `updated`, `removed`, or `open thread` — and never write the list to the file. Done when the list covers every prior bullet, or the file is confirmed absent.

**Step 2. Confirm new work.** If the conversation holds no work beyond what the existing handoff carries, write nothing, offer to load it instead, and stop. Done when the conversation holds work the handoff does not carry, or the offer is made.

**Step 3. Compose.** Compose the complete handoff from the prior handoff and current working context, one block per topic. Put the conversation's work under the block of its topic: update that block, or add one when no existing block covers the subject. Leave a block the conversation did not touch as Step 1 dispositioned it. When an argument is present, it names the topic of the conversation's work: use an existing heading when one covers that subject, otherwise use the argument as the new heading, and tailor that block's `Context` and `Current state` to it. Done when every block holds `Context` and `Current state` and each optional section is present only when its condition holds.

**Step 4. Capture the check results.** Add to the `Current state` of the block each check run, with its command and result. For a failing check or error, capture the command that reproduces it. Done when every check run in the conversation is recorded in its block, or none ran.

**Step 5. Mark unverified claims.** End each load-bearing claim not checked against current evidence with `(unverified: [source])`. A bullet without the mark was verified at save. Keep unresolved beliefs under `Open threads` rather than presenting them as findings or decisions. Done when every load-bearing claim was checked or carries the mark.

**Step 6. Write and check.** Write the handoff to `.artifacts/HANDOFF.md`, then run `python3 <this-skill>/scripts/check_handoff.py .artifacts/HANDOFF.md`, resolving `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose that directory, stop and report an environment problem. The script flags a missing topic block, a missing required section, a repeated section or topic, a section that says none, a commit hash, chat phrasing, and secrets; fix each line it flags as its message says and run it again. Done when the script prints `clean` and the file holds no content already carried by an artifact, no git state, no matter outside its block's topic, and no raw conversation history; otherwise return to Step 3.

**Step 7. Report.** Report the path, the topic headings, which block this save updated or added, what the handoff holds in one to three sentences, and the open threads and blockers it carries. List on one line the prior bullets Step 1 marked `removed`. Never paste the handoff. Done when the report names the path, every topic, the block this save touched, every open thread and blocker, and every removed bullet.

## Examples

A consolidated handoff with two topics, one optional section, and one unverified claim:

```markdown
# Handoff

## handoff skill audit

**Context:**
- Goal: the skill passes the audit checklist with no fail left; done when the decision items are settled and the validator shows no new warning
- Constraint: every edit follows the rules in `.agents/rules/`

**Current state:**
- Format and workflow rewritten in `instructions/save.md` and `instructions/load.md`
- Validator not re-run since the edits

**Open threads:**
- Whether `load.md` keeps its last guideline (unverified: no with/without test run yet)

## auth race fix

**Context:**
- Goal: concurrent token refreshes send one request; done when the refresh test passes

**Current state:**
- Race reproduced with the refresh test; fix not started
```
