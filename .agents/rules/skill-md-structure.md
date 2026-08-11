---
paths:
  - "skills/**/SKILL.md"
---

## Required Top Sections

**Impact: MEDIUM**

SKILL.md opens with the H1 title, then a Triggers or Quick start section — nothing precedes them. The entry point routes the agent, so the trigger surface is the first thing it reads.

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

- Commit changes ("commit this") → commit.md
```

## Forbidden SKILL.md Sections

**Impact: MEDIUM**

SKILL.md never carries `## Cross-References` (skills are isolated), `## Compact Instructions` (skills are stateless), `## Output` (output lives in the reference that produces it), or `## Error Handling` (errors are handled inline in the workflow). Drop these; their content belongs elsewhere or nowhere.

**Incorrect:**

```markdown
## Error Handling

- No changes: inform the user
```

**Correct:**

```markdown
### Step 5: Create Commit

If a hook fails, fix the issue and create a new commit.
```

## Body Under 150 Lines

**Impact: LOW**

Keep SKILL.md at or below 150 lines, preferring 100. Past that, move detail into `references/` so the entry point stays a short router, not the manual.

The cap is a **line count**, not a character budget — the harness enforces no per-line width and no body character limit, so wrapping is purely cosmetic. Do not hard-wrap body prose at ~80 columns; write full-width lines so wrapping never inflates the count. The `description` frontmatter field is the one with a character budget (see `skill-frontmatter`).

**Incorrect:**

```markdown
# Skill

[210 lines of inline tables and step-by-step detail]
```

**Correct:**

```markdown
# Skill

[80 lines routing to references/*.md for the detail]
```
