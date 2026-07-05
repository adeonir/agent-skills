---
name: git-helpers
allowed-tools: Bash(git:*) Bash(gh:*) Read
description: >-
  Git workflow helper for conventional commits, pull request creation,
  and branch lifecycle. Use when committing staged or unstaged changes,
  opening or pushing pull requests, merging branches, or cleaning up
  after a merge. Not for code review, acceptance-criteria verification,
  visual design review, or session wrap-up.
---

# Git Helpers

Git workflow with conventional commits and automated PR management.

## Triggers

- **Commit changes** ("commit this", "create commit", "ready to commit", "all done") → [commit.md](references/commit.md)
- **Push and open PR** ("push this", "create PR", "open pull request", "ready to push") → [create-pull-request.md](references/create-pull-request.md)
- **Merge and clean up** ("finish branch", "merge branch", "merge PR", "cleanup branch") → [finish-branch.md](references/finish-branch.md)

## Workflow

```text
commit → create-pull-request → finish-branch
```

Each step is independent. Use any workflow in isolation or chain them together.

## Guidelines

- Base branch: the repo's default (user can override)
- Prefer single-line commit messages — add a body only when the change has several meaningful parts or a *why* the diff doesn't show

## Anti-Pattern: Conversation-Driven Messages

Writing a commit, PR, or merge message from chat context produces fabricated quotes, rejected approaches presented as fact, and restated diff content. The diff is the single source of *what* changed; the conversation supplies at most an explicit *why* the user stated. Before writing, trace every line back to a hunk in the diff — a line that names a change the diff does not show came from the conversation, so drop it.

## Anti-Pattern: Default GitHub Merge Subject

The default `Merge pull request #N from {branch}` message strips intent and conventional commit type. Always pass a custom subject: `{type}: {description} (#{pr-number})`.
