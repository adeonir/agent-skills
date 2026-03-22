---
name: git-helpers
description: >-
  Git workflow helper for conventional commits, confidence-scored
  code review, pull request management, and branch lifecycle. Use when
  committing changes, reviewing code, creating PRs, merging branches, or
  when the user is done coding and ready to commit, wants feedback on
  changes, needs to push and open a PR, or wants to finish and merge a
  branch. Triggers on "commit", "review", "push", "create PR",
  "summarize changes", "done", "ready to push", "check my code",
  "finish branch", "merge branch", "merge PR", "cleanup branch".
---

# Git Helpers

Git workflow with conventional commits, confidence-scored code review,
and automated PR management.

## Workflow

```
commit --> review --> summary --> create-pull-request --> finish-branch
```

Each step is independent. Use any workflow in isolation or chain them together.

## Context Loading Strategy

Load only the reference matching the current trigger. Never load multiple references simultaneously unless explicitly noted (code-review.md loads guidelines-audit.md as part of its process).

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Commit changes, create commit, done, ready to commit | [commit.md](references/commit.md) |
| Review code, check changes, check my code | [code-review.md](references/code-review.md) |
| Summarize changes, generate PR description | [summary.md](references/summary.md) |
| Push branch, create PR, open pull request, ready to push | [create-pull-request.md](references/create-pull-request.md) |
| Finish branch, merge branch, merge PR, cleanup branch | [finish-branch.md](references/finish-branch.md) |

Notes:

- `guidelines-audit.md` is not a direct trigger. It is loaded by `code-review.md` as part of the review process.

## Cross-References

```
code-review.md -------------> guidelines-audit.md (loaded as part of review)
create-pull-request.md -----> templates/pull-request.md (PR body template)
finish-branch.md -----------> commit.md (squash commit message conventions)
```

## Guidelines

**DO:**
- Preview commit messages before committing -- always show and ask for confirmation
- Use confidence scoring: only report findings with confidence >= 80
- Default base branch: main (user can override)
- Use imperative mood in commit messages and PR titles
- Use HEREDOC format for multi-line commit messages
- Analyze actual diff and staged files
- Follow existing project conventions for commit message format
- Prefer single-line commit messages -- only add body for complex or breaking changes

**DON'T:**
- Add attribution lines in commit messages or PRs
- Base analysis on conversation context instead of actual diff
- Report findings with confidence < 80
- Override project conventions with generic rules

## Output

| Reference | Output |
|-----------|--------|
| summary.md | `PR_SUMMARY.md` (PR description with impact assessment) |
| code-review.md | Terminal output or PR comment (optionally saved to `CODE_REVIEW.md`) |

## Error Handling

- No changes to commit: inform user working tree is clean
- gh cli not available: stop and inform user to install it
- No guideline files found: skip guidelines audit, report it
- Merge conflicts: stop and inform user to resolve first
