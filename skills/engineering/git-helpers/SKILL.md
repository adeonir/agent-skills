---
name: git-helpers
allowed-tools: Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git add:*) Bash(git commit:*) Bash(git push:*) Bash(git switch:*) Bash(git fetch:*) Bash(git merge:*) Bash(git rebase:*) Bash(git branch:*) Bash(git config:*) Bash(gh pr:*) Read
description: "Git workflow for conventional commits, pull request creation, and pull request merging. Use when committing, opening or pushing a pull request, or merging one. Not for code review, acceptance-criteria checks, general branch management, or session wrap-up."
---

# Git Helpers

Git workflow with conventional commits, pull requests, and pull request merges.

## Triggers

- **Commit changes** ("commit this", "create commit", "ready to commit", "all done") → [commit.md](instructions/commit.md)
- **Push and open PR** ("push this", "create PR", "open pull request", "ready to push") → [create-pull-request.md](instructions/create-pull-request.md)
- **Merge pull request** ("merge PR", "merge pull request", "ready to merge") → [merge-pull-request.md](instructions/merge-pull-request.md)

## References

- [message-sourcing.md](references/message-sourcing.md) — loaded by the commit, create pull request, and merge pull request instructions

## Workflow

```text
commit → create-pull-request → merge-pull-request
```

Each step is independent. Use any workflow in isolation or chain them together.
