---
name: git-helpers
description: "Git workflow for conventional commits, pull request creation, and pull request merging. Use when committing, opening or pushing a pull request, or merging one. Not for code review, acceptance-criteria checks, general branch management, or session wrap-up."
compatibility: Requires git, gh, and python3.
allowed-tools: Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git add:*) Bash(git commit:*) Bash(git push:*) Bash(git switch:*) Bash(git fetch:*) Bash(git merge:*) Bash(git rebase:*) Bash(git branch:*) Bash(git config:*) Bash(gh pr:*) Bash(python3:*) Read
---

# Git Helpers

Git workflow with conventional commits, pull requests, and pull request merges.

## Triggers

- **Commit** — the user asks to commit staged or unstaged changes ("commit this") → [commit.md](references/commit.md) · staging rules, the message bar, and the body tests
- **Create pull request** — a branch is ready for review ("push this", "create PR") → [create-pull-request.md](references/create-pull-request.md) · guards, branch reading, and body sections
- **Merge pull request** — a pull request is ready to land ("merge PR") → [merge-pull-request.md](references/merge-pull-request.md) · merge method, state checks, and cleanup

```mermaid
flowchart LR
    commit --> create-pull-request --> merge-pull-request
```

Each job is independent. Use any one in isolation or chain them.
