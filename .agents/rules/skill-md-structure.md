---
paths:
  - "skills/**/SKILL.md"
---

## No Constraint in a Routing SKILL.md

**Impact: HIGH**

A SKILL.md that routes to `instructions/` carries routing only. Never place in it a constraint that changes what an instruction produces — an anti-pattern, a guideline, a tool choice, a boundary, a term an instruction cites. The agent loads SKILL.md on the first invocation and re-enters at the instruction on every later one, so a constraint left at the top reaches the first run and no other. Move it into the instruction it governs, or into a `references/` file that instruction loads as a step.

A one-job skill has no `instructions/` and its SKILL.md is the procedure, so its constraints belong there; nothing re-enters below it.

**Incorrect:**

```markdown
<!-- SKILL.md -->
## Anti-Pattern: Conversation-Driven Messages

Write the message from the diff, never from chat context.
```

**Correct:**

```markdown
<!-- instructions/commit.md -->
3. **Write the message** — from the staged diff, never from chat context. Trace every line back to a hunk before returning it.
```

## Instructions as the Only Routing Target

**Impact: HIGH**

In a skill that has `instructions/`, every link in SKILL.md points at one. A link to `references/` makes the same file reachable two ways — routed from the top and loaded by a procedure — and the routed copy arrives without the procedure that knows what to do with it. A reference enters context because a step asked for it, never because SKILL.md announced it; a one-job SKILL.md is itself that step, and links its references directly.

**Incorrect:**

```markdown
## Triggers

- Commit changes ("commit this") → [commit.md](references/commit.md)

## References

- [untrusted-content.md](references/untrusted-content.md) — the trust boundary
```

**Correct:**

```markdown
## Triggers

- Commit changes ("commit this") → [commit.md](instructions/commit.md)
```

## Required Top Sections

**Impact: MEDIUM**

SKILL.md opens with the H1 title, then a Triggers or Quick start section — nothing precedes them. It is the first thing the agent reads, so it states what the skill answers to before anything else, whether it routes from there or runs the procedure itself.

**Incorrect:**

```markdown
# Git Helpers

## Philosophy

Commits should tell a story...
```

**Correct:**

```markdown
# Git Helpers

## Triggers

- Commit changes ("commit this") → instructions/commit.md
```

## Forbidden SKILL.md Sections

**Impact: MEDIUM**

A routing SKILL.md never carries `## Anti-Pattern` or `## Guidelines` — both are constraints, and each belongs to the instruction it governs. No SKILL.md, routing or one-job, carries `## Cross-References` (skills are isolated), `## Compact Instructions` (skills are stateless), `## Output` (output lives where it is produced), or `## Error Handling` (errors are handled inline in the workflow). Drop these; their content belongs elsewhere or nowhere.

**Incorrect:**

```markdown
## Error Handling

- No changes: inform the user
```

**Correct:**

```markdown
5. **Create the commit** — when a hook fails, fix the issue and create a new commit.
```

## Routing Over Bulk Reads

**Impact: MEDIUM**

SKILL.md names the condition that selects each instruction, and each step names the reference it needs; neither instructs the agent to read the whole bundle. A blanket read puts every file in context for a request that needed one, and turns each file's own entry condition into dead text.

**Incorrect:**

```markdown
## Triggers

Read every file in `instructions/` before starting.
```

**Correct:**

```markdown
## Triggers

- Commit changes ("commit this") → instructions/commit.md
- Open a pull request ("open PR") → instructions/create-pull-request.md
- Merge a pull request ("merge PR") → instructions/finish-branch.md
```

## Body Under 150 Lines

**Impact: LOW**

Keep SKILL.md at or below 150 lines, preferring 100. Past that, move detail into the instruction that uses it, or into a reference the procedure loads, so the entry point stays short rather than becoming the manual.

The cap is a **line count**, not a character budget — the harness enforces no per-line width and no body character limit, so wrapping is purely cosmetic. Do not hard-wrap body prose at ~80 columns; write full-width lines so wrapping never inflates the count. The `description` frontmatter field is the one with a character budget (see `skill-frontmatter`).

**Incorrect:**

```markdown
# Skill

[210 lines of inline tables and step-by-step detail]
```

**Correct:**

```markdown
# Skill

[40 lines routing to instructions/*.md]
```
