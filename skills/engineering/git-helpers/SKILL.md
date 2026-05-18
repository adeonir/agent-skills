---
name: git-helpers
description: >-
  Git workflow helper for conventional commits, confidence-scored code
  review (lens fan-out: security, bugs, data-loss, performance,
  guidelines), PR description generation, pull request creation, and
  branch lifecycle. Use when committing changes, reviewing code,
  creating PRs, merging branches, or when ready to commit / push / open
  a PR / finish a branch. Triggers: "commit this", "create a commit",
  "code review", "review this PR", "review this diff", "push this",
  "ready to push", "create PR", "open a pull request", "summarize
  changes", "finish branch", "merge branch", "merge PR", "cleanup
  branch". Not for acceptance-criteria verification, visual design
  review, or session wrap-up.
---

# Git Helpers

Git workflow with conventional commits, confidence-scored code review,
and automated PR management.

## Triggers

- **Commit changes** ("commit this", "create commit", "ready to commit",
  "all done") → [commit.md](references/commit.md)
- **Code review** ("review code", "check changes", "review my diff")
  → [code-review.md](references/code-review.md) (loads
  [guidelines-audit.md](references/guidelines-audit.md) as a lens prompt)
- **PR description** ("summarize changes", "generate PR description")
  → [summary.md](references/summary.md)
- **Push and open PR** ("push this", "create PR", "open pull request",
  "ready to push") →
  [create-pull-request.md](references/create-pull-request.md)
- **Merge and clean up** ("finish branch", "merge branch", "merge PR",
  "cleanup branch") → [finish-branch.md](references/finish-branch.md)

`guidelines-audit.md` is not a direct trigger — it is the lens prompt
loaded by `code-review.md` during the guidelines lens fan-out.

## Workflow

```
commit --> review --> summary --> create-pull-request --> finish-branch
```

Each step is independent. Use any workflow in isolation or chain them
together.

## Code Review Fan-Out

`code-review.md` parallelizes via lens fan-out. After the main agent
annotates the diff and clears the size gate, it selects active lenses
based on changed files (minimum 3, maximum 5), then dispatches them in a
**single turn** — each reads the same annotated diff under a focused
scope and returns markdown findings.

| Lens | Scope | When active |
|------|-------|-------------|
| `security` | SQL injection, XSS, auth bypass, secrets, PII | always |
| `bugs` | Logic errors, runtime failures, swallowed errors | always |
| `guidelines` | Violations of project guideline files | always |
| `data-loss` | Destructive migrations, wrong delete predicates | when diff matches data patterns |
| `performance` | N+1 queries, sequential awaits, unbounded find | when diff matches perf patterns |

After the fan-out, the main agent consolidates: dedup on `file:line`,
severity sort, gap detection, partial-run handling. Cross-lens
visibility cannot be split across sub-agents.

Commit, summary, create-pull-request, and finish-branch run inline on
the main agent (single-output workflows, no fan-out value).

## Guidelines

- Preview commit messages before committing — always show and ask for
  confirmation
- Use confidence scoring: only report findings with confidence ≥ 80
- Default base branch: `main` (user can override)
- Use HEREDOC format for multi-line commit messages
- Analyze the actual diff and staged files, not conversation context
- Prefer single-line commit messages — only add a body for complex or
  breaking changes

## Anti-Pattern: Conversation-Driven Commits

Writing the commit message from chat context produces fabricated quotes,
restated diff content, and missing rationale. The staged diff is the
single source of truth. Discard prior context, run `git diff --cached`,
and write the message from what the diff shows.

## Anti-Pattern: Confidence Inflation in Code Review

Reporting findings below 80 confidence buries real issues under noise.
The rubric is calibrated: <80 means speculation or style preference, not
a real bug. When unsure, drop down — gather more context, re-read the
diff — instead of pushing a low-confidence finding through.

## Anti-Pattern: Default GitHub Merge Subject

The default `Merge pull request #N from {branch}` message strips
intent and conventional commit type. Always pass a custom subject:
`{type}: {description} (#{pr-number})`.
