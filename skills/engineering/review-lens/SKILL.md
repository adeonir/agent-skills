---
name: review-lens
allowed-tools: Bash(git:*) Bash(gh:*) Bash(find:*) Read Write Task
description: >-
  Confidence-scored code review via lens fan-out (security, bugs,
  data-loss, performance, guidelines): each active lens reads the same
  annotated diff in parallel and the main agent consolidates findings.
  Use when reviewing code changes, checking a diff before commit or
  pull request, posting a review as a PR comment, auditing guideline
  compliance, or re-reviewing fixes. Not for acceptance-criteria
  verification, visual design review, or commit/PR/branch mechanics.
---

# Review Lens

Lens-based code review with anti-hallucination diff annotation.
Confidence-scored findings, parallel lens sub-agents, consolidated report.

## Triggers

- **Code review** ("review code", "review my changes", "check my diff",
  "review against main", "review and post as PR comment") →
  [review.md](references/review.md) (loads
  [guidelines-audit.md](references/guidelines-audit.md) as a lens prompt)
- **Re-review** ("re-review", "check fixes", "are the issues resolved")
  → the Re-Review Loop in [review.md](references/review.md)

`guidelines-audit.md` is not a direct trigger — it is the lens prompt
loaded by `review.md` during the guidelines lens fan-out.

## Code Review Fan-Out

`review.md` parallelizes via lens fan-out. After the main agent annotates
the diff and clears the size gate, it selects active lenses based on
changed files (minimum 3, maximum 5), then dispatches them in a **single
turn** — each reads the same annotated diff under a focused scope and
returns markdown findings.

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

## Guidelines

- Annotate the diff with `[L<n>]` markers before fan-out — the line
  allowlist is the anti-hallucination guard
- Use confidence scoring: only report findings with confidence ≥ 80
- Dispatch all active lenses in a single turn so they run in parallel
- Default base branch: `main` (user can override)
- Analyze the actual annotated diff, not conversation context
- Sort the final report by severity, not by lens or discovery order

## Anti-Pattern: Confidence Inflation in Code Review

Reporting findings below 80 confidence buries real issues under noise.
The rubric is calibrated: <80 means speculation or style preference, not
a real bug. When unsure, drop down — gather more context, re-read the
diff — instead of pushing a low-confidence finding through.
