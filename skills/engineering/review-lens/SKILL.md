---
name: review-lens
allowed-tools: Bash(git:*) Bash(gh:*) Bash(find:*) Read Write Edit Task
description: >-
  Confidence-scored code review in two modes — quick (a fast pass pairing
  a change walkthrough with inline findings, the default) and deep (a
  multi-material fan-out across the diff, guideline files, git history,
  and prior pull requests, with an independent confidence judge). Runs
  locally before a pull request. Use when reviewing code changes,
  checking a diff before commit or PR, running a deep or full review,
  auditing guideline compliance, suggesting or applying fixes, or
  re-reviewing fixes. Not for acceptance-criteria verification, visual
  design review, or commit/PR/branch mechanics.
---

# Review Lens

Code review with anti-hallucination diff annotation and confidence-scored findings, in two modes — a fast walkthrough-plus-findings pass by default, or a multi-material fan-out on demand. Runs before a pull request: the report goes to the chat, with optional fix application and a saved report.

## Triggers

- **Quick review** (default — "review", "review my changes", "check my diff", "review against main") → [quick-review.md](references/quick-review.md)
- **Deep review** ("deep review", "full review", "thorough review") → [deep-review.md](references/deep-review.md)
- **Re-review** ("re-review", "check fixes", "are the issues resolved") → the Re-Review section of the mode that ran (default quick)

Shared rules live in [common.md](references/common.md); guideline discovery lives in [guidelines-audit.md](references/guidelines-audit.md). Neither is a direct trigger.

## Modes

Both modes share the same `[L<n>]` diff annotation, the confidence ≥ 80 bar, the what-not-to-report rules, and the output template (all in `common.md`). They differ in depth and cost:

- **Quick (default)** — two agents run in parallel by role: a Haiku walkthrough describes the change, a Sonnet findings pass catches issues across every scope. Fast, with reasoning where it counts.
- **Deep** — fans out by **material** (diff, guideline files, git history, prior PRs) with an independent confidence judge. Thorough, for risky or wide-reaching changes.

Default to quick. Reach for deep only when the user asks for depth or the change is risky.

## Deep Mode: Material Fan-Out

The fan-out divides by **source of material**, not by concern — each agent reads something the others don't, so each adds new signal. The concerns (security, bugs, data-loss, performance) are a checklist inside one bug-scan, not separate agents. Sonnet is used only for the two reasoning passes; everything else is Haiku.

| Agent | Model | Reads |
|-------|-------|-------|
| setup | inline | annotate `[L<n>]`, size gate, gather guideline paths, walkthrough |
| bug-scan | Sonnet | the diff — security/bugs/data-loss/performance checklist |
| compliance | Haiku | the project's guideline files |
| git-history | Sonnet | `git log` / `blame` of the changed files |
| prior-PRs | Haiku | past PRs + review comments (when `gh` + GitHub remote) |
| judge | Haiku | every finding — scores confidence, drops < 80 |

## Guidelines

- Annotate the diff with `[L<n>]` markers before reviewing — the line allowlist is the anti-hallucination guard in both modes
- Only report findings with confidence ≥ 80
- Default to quick; reserve the deep fan-out for risky or wide diffs
- Guideline discovery reads the project's files — including `.claude/rules/*.md` — never `~/.claude` (personal global settings)
- Suggest fixes freely (they are text); apply to the working tree only with explicit confirmation
- The review runs pre-PR — output goes to the chat (and optional `CODE_REVIEW.md`), never posted to a pull request

## Anti-Pattern: Confidence Inflation

Reporting findings below 80 confidence buries real issues under noise. The rubric is calibrated: <80 means speculation or style preference, not a real bug. When unsure, drop down — gather more context, re-read the diff — instead of pushing a low-confidence finding through.
