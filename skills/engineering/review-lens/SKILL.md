---
name: review-lens
allowed-tools: Bash(git:*) Bash(gh:*) Bash(find:*) Read Write Task
description: >-
  Confidence-scored code review in two modes: quick (single-pass,
  default) and deep (lens fan-out across security, bugs, data-loss,
  performance, guidelines). Use when reviewing code changes, checking a
  diff before commit or pull request, running a deep or full review,
  posting a review as a PR comment, auditing guideline compliance, or
  re-reviewing fixes. Not for acceptance-criteria verification, visual
  design review, or commit/PR/branch mechanics.
---

# Review Lens

Code review with anti-hallucination diff annotation and confidence-scored
findings, in two modes — a fast single pass by default, or a parallel lens
fan-out on demand.

## Triggers

- **Quick review** (default — "review", "review my changes", "check my
  diff", "review against main") →
  [quick-review.md](references/quick-review.md)
- **Deep review** ("deep review", "full review", "thorough review",
  "review every lens") → [deep-review.md](references/deep-review.md)
  (loads [guidelines-audit.md](references/guidelines-audit.md) as a lens
  prompt)
- **Re-review** ("re-review", "check fixes", "are the issues resolved")
  → the Re-Review section of the mode that originally ran (default quick)

`guidelines-audit.md` is not a direct trigger — it is the lens prompt
loaded by deep review during the guidelines lens fan-out.

## Modes

Both modes share the same `[L<n>]` diff annotation, the confidence ≥ 80
bar, the what-not-to-report rules, and the output format. They differ only
in how the diff is read:

- **Quick (default)** — one agent reads the whole annotated diff in a
  single pass and reports across every scope. Fast, inline, no sub-agents.
- **Deep** — the diff fans out to 3–5 lens sub-agents in parallel; the
  main agent consolidates. Thorough, for risky or wide-reaching changes.

Default to quick. Reach for deep only when the user asks for depth or the
change is risky.

## Deep Mode: Lens Fan-Out

`deep-review.md` parallelizes via lens fan-out. After the main agent
annotates the diff and clears the size gate, it selects active lenses based
on changed files (minimum 3, maximum 5), then dispatches them in a **single
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
severity sort, gap detection, partial-run handling. Cross-lens visibility
cannot be split across sub-agents.

## Guidelines

- Annotate the diff with `[L<n>]` markers before reviewing — the line
  allowlist is the anti-hallucination guard in both modes
- Use confidence scoring: only report findings with confidence ≥ 80
- Default to quick; reserve the deep fan-out for risky or wide diffs
- In deep mode, dispatch all active lenses in a single turn so they run in
  parallel
- Default base branch: `main` (user can override)
- Analyze the actual annotated diff, not conversation context
- Sort the final report by severity, not by lens or discovery order

## Anti-Pattern: Confidence Inflation in Code Review

Reporting findings below 80 confidence buries real issues under noise.
The rubric is calibrated: <80 means speculation or style preference, not
a real bug. When unsure, drop down — gather more context, re-read the
diff — instead of pushing a low-confidence finding through.
