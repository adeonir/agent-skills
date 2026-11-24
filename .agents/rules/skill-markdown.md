---
paths:
  - "skills/**/SKILL.md"
---

## Router Carries Routing Only

**Impact: HIGH**

A SKILL.md that routes carries the H1, the one-sentence scope, and the index. Every procedure, boundary, tool choice, and term lives in the reference it governs: the agent loads SKILL.md on the first run and re-enters at the reference on later ones.

A one-job skill keeps its procedure in SKILL.md, so its constraints belong there.

**Incorrect:**

```markdown
<!-- SKILL.md -->
## Anti-Pattern: Conversation-Driven Messages

Write the message from the diff, never from chat context.
```

**Correct:**

```markdown
<!-- references/commit.md -->
**Step 3. Write the message.** — from the staged diff, never from chat context. Trace every line back to a hunk before returning it.
```

## Index Every Procedure

**Impact: HIGH**

Give every procedure under `references/` one entry, directly after the opening:

```text
- **<branch>** — <the situation that makes it relevant> → [references/<file>.md](references/<file>.md) · <what loading it buys>
```

The condition lets the agent choose from the entry alone; the payload says what loading the file buys. A single-job skill carries its procedure in `## Workflow`, and the material its steps need is named at the step that needs it.

The index lists procedures only. Material is named by the step that loads it, never listed here.

**Incorrect:**

```markdown
- Commits → [commit.md](references/commit.md)
- [message-sourcing.md](references/message-sourcing.md)
```

**Correct:**

```markdown
- **Commit** — the user asks to commit staged or unstaged changes → [commit.md](references/commit.md) · staging rules and the message bar
- **Create pull request** — a branch is ready for review → [create-pull-request.md](references/create-pull-request.md) · body structure and evidence
```

## Entry Point Format

**Impact: MEDIUM**

Open with the H1, then one sentence stating what the skill covers, then `## Triggers` for a router or `## Quick start` for a single job, then the index. Keep the body at or below 150 lines.

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

- Commit changes ("commit this") → references/commit.md
```

## Frontmatter Carries the Standard Fields

**Impact: MEDIUM**

The frontmatter carries the fields the Agent Skills standard defines: `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. `disable-model-invocation` is the one field outside it, because Claude Code reads it there. Every other host field stays in the host's own configuration, so the skill keeps working where the host ignores it.

**Incorrect:**

```yaml
name: git-helpers
argument-hint: "[focus]"
```

**Correct:**

```yaml
name: git-helpers
description: Conventional commits, pull requests, and branch lifecycle.
```

## Description Names Its Boundary

**Impact: MEDIUM**

Close the `description` with a `Not for <adjacent jobs>` clause naming the neighboring work the skill should not claim. Skills coexist, and without a boundary a description overtriggers onto a neighbor's job. Name only adjacent jobs that exist.

**Incorrect:**

```yaml
description: Git workflow for conventional commits and pull requests. Use when committing staged changes or opening a pull request.
```

**Correct:**

```yaml
description: Git workflow for conventional commits and pull requests. Use when committing staged changes or opening a pull request. Not for code review, acceptance-criteria verification, or session wrap-up.
```
