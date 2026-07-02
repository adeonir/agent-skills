---
paths:
  - "skills/**/SKILL.md"
---

## Reserved Name Tokens

**Impact: MEDIUM**

A skill `name` is kebab-case (lowercase letters, digits, hyphens) and never contains `anthropic` or `claude`. Because the name becomes the slash command, it must not collide with a Claude Code built-in (`code-review`, `review`, `simplify`, `security-review`); pick a distinct name when the job overlaps one.

**Incorrect:**

```yaml
name: claude_code-review
```

**Correct:**

```yaml
name: review-lens
```

## Third-Person Description

**Impact: MEDIUM**

Write `description` in the third person or as a noun phrase, never first or second person. A first-person ("I help...") or second-person ("You can use...") description reads as marketing and weakens trigger matching.

**Incorrect:**

```yaml
description: I help you write conventional commits and open pull requests.
```

**Correct:**

```yaml
description: Git workflow for conventional commits and pull request creation.
```

## Inline Triggers

**Impact: MEDIUM**

Weave trigger keywords into the description prose — action verbs and topical nouns inside sentences. Do not add a separate "Triggers:" list of quoted phrases, and never rely on a bare single word, which collides between skills; every literal phrase is two words or more.

**Incorrect:**

```yaml
description: >-
  Commit helper.
  Triggers: commit, push, pr
```

**Correct:**

```yaml
description: >-
  Git workflow for conventional commits and pull requests. Use when committing
  staged changes, opening a pull request, or merging a branch.
```

## No when_to_use Field

**Impact: MEDIUM**

Keep triggers and capability inside `description`; do not add a `when_to_use` field. The open Agent Skills standard caps `description` at 1,024 chars and defines no `when_to_use`, so a split has nowhere to go and fragments the single source — tighten the prose instead of spilling into a second field.

**Incorrect:**

```yaml
description: Git workflow for commits.
when_to_use: when committing or opening a PR
```

**Correct:**

```yaml
description: >-
  Git workflow for commits. Use when committing staged changes or opening
  a pull request.
```
