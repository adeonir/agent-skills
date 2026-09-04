---
name: review-lens
allowed-tools: Bash(git:*) Bash(gh:*) Bash(find:*) Read Write Edit Task
description: "Code review in quick and deep modes, with confidence-scored findings. Use for diff review, guideline audits, re-reviewing fixes, or applying findings before a pull request. Not for markdown or prose review, acceptance-criteria verification, visual design review, or commit and branch mechanics."
---

# Review Lens

Code review with anti-hallucination diff annotation and confidence-scored findings, in two modes — a fast walkthrough-plus-findings pass by default, or a multi-material fan-out on demand. Runs before a pull request: the report goes to the chat, with optional fix application and a saved report.

## Triggers

- **Quick review** (default — "review", "review my changes", "check my diff", "review against main") → run the workflow below
- **Deep review** ("deep review", "full review", "thorough review") → run it in deep mode
- **Re-review** ("re-review", "check fixes", "are the issues resolved") → run it against the prior findings

## Workflow

Start immediately when triggered. No confirmation needed to begin.

1. **Load [common.md](references/common.md)** — the diff annotation algorithm, the size gate, the confidence rubric, what not to report, the output template, the fix-suggestion rules, and the data trust boundary. Both modes apply it in full.
2. **Set up.** Run `git status --porcelain`: review the working directory when it has uncommitted changes, otherwise compare the current branch against the base the user names, else `main`. Capture the diff and changed files, annotate every added line with its `[L<n>]` marker, and apply the size gate before going further.
3. **Pick the mode.** Default to quick and load [quick-review.md](references/quick-review.md). Load [deep-review.md](references/deep-review.md) only when the user asks for depth or the change is risky or wide-reaching — it fans out by material, at higher cost.
4. **Load [guidelines-audit.md](references/guidelines-audit.md)** for the guideline-compliance portion, whichever mode ran.
5. **Assemble and output.** Render the loaded template, sorted by severity. On a re-review, mark each prior finding `fixed`, `persisting`, or `regressed` and output the status table first. Print to the terminal, offer to save `CODE_REVIEW.md`, then offer to apply the suggested fixes.

## Guidelines

- Annotate the diff with `[L<n>]` markers before reviewing — the line allowlist is the anti-hallucination guard in both modes
- Only report findings with confidence >= 80
- Default to quick; reserve the deep fan-out for risky or wide diffs
- Guideline discovery reads the project's files — including `.claude/rules/*.md` — never `~/.claude` (personal global settings)
- Suggest fixes freely (they are text); apply to the working tree only with explicit confirmation
- The review runs pre-PR — output goes to the chat (and optional `CODE_REVIEW.md`), never posted to a pull request

## Anti-Pattern: Confidence Inflation

Reporting findings below 80 confidence buries real issues under noise. The rubric is calibrated: <80 means speculation or style preference, not a real bug. When unsure, drop down — gather more context, re-read the diff — instead of pushing a low-confidence finding through.
