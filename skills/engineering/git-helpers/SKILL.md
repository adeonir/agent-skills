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

- **Commit changes** ("commit this", "create commit", "ready to commit",
  "all done") → [commit.md](references/commit.md)
- **Push and open PR** ("push this", "create PR", "open pull request",
  "ready to push") →
  [create-pull-request.md](references/create-pull-request.md)
- **Merge and clean up** ("finish branch", "merge branch", "merge PR",
  "cleanup branch") → [finish-branch.md](references/finish-branch.md)

## Workflow

```text
commit → create-pull-request → finish-branch
```

Each step is independent. Use any workflow in isolation or chain them
together.

## Guidelines

- Always preview and confirm the commit message before committing — a
  deliberate guard against weak drafts; skipped only in autonomous/headless
  runs where no human is present
- Base branch: the repo's default (user can override)
- Use HEREDOC format for multi-line commit messages
- Analyze the actual diff and staged files, not conversation context
- Prefer single-line commit messages — add a body only when the change
  has several meaningful parts or a *why* the diff doesn't show

## Anti-Pattern: Conversation-Driven Commits

Writing the commit message from chat context produces fabricated quotes,
restated diff content, and missing rationale. The staged diff is the
single source of truth. Discard prior context, run `git diff --cached`,
and write the message from what the diff shows.

## Anti-Pattern: Default GitHub Merge Subject

The default `Merge pull request #N from {branch}` message strips
intent and conventional commit type. Always pass a custom subject:
`{type}: {description} (#{pr-number})`.
