---
name: git-helpers
description: >-
  Git workflow helper for conventional commits, confidence-scored code review,
  and pull request management. Use when: committing changes, reviewing code,
  creating PRs, generating PR descriptions, analyzing diffs. Triggers on "commit",
  "review", "push", "create PR", "PR description", "summarize changes".
metadata:
  author: github.com/adeonir
  version: "1.0.0"
---

# Git Helpers

Git workflow with conventional commits, confidence-scored code review,
and automated PR management.

## Workflow

```
commit --> review --> summary --> push-pr
```

Each step is independent. Use any workflow in isolation or chain them together.

## Context Loading Strategy

Load only the reference matching the current trigger. Never load multiple references simultaneously unless explicitly noted (code-review.md loads guidelines-audit.md as part of its process).

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Commit changes, create commit | [commit.md](references/commit.md) |
| Review code, check changes | [code-review.md](references/code-review.md) |
| Summarize changes, generate PR description | [summary.md](references/summary.md) |
| Push branch, create PR, open pull request | [push-pr.md](references/push-pr.md) |
| Analyze diff, diff patterns | [workflow-patterns.md](references/workflow-patterns.md) |

Notes:

- `guidelines-audit.md` is not a direct trigger. It is loaded by `code-review.md` as part of the review process.
- `conventional-commits.md` is not a direct trigger. It is loaded by `commit.md` and `push-pr.md` for message format rules.

## Cross-References

```
code-review.md -----> guidelines-audit.md (loaded as part of review)
commit.md ----------> conventional-commits.md (format rules)
push-pr.md ---------> conventional-commits.md (format rules)
```

## Guidelines

- Confidence scoring: only report findings with confidence >= 80
- No attribution lines in commit messages or PRs
- Auto-detect base branch: development > develop > main > master
- Always use imperative mood in commit messages and PR titles
- HEREDOC format for multi-line commit messages
- Analyze actual diff and staged files, never conversation context
- Follow existing project conventions for commit message format

## Error Handling

- No changes to commit: inform user working tree is clean
- gh cli not available: stop and inform user to install it
- No guideline files found: skip guidelines audit, report it
- Merge conflicts: stop and inform user to resolve first
