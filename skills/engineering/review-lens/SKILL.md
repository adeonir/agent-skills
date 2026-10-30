---
name: review-lens
allowed-tools: Bash(git:*) Bash(gh:*) Bash(find:*) Bash(python3:*) Read Write Edit Task
description: "Code review in quick and deep modes, with confidence-scored findings and a check of the change against its spec or issue. Use for diff review, guideline audits, spec compliance review, re-reviewing fixes, or applying findings before a pull request. Not for markdown or prose review, manual acceptance testing, visual design review, or commit and branch mechanics."
---

# Review Lens

Code review with anti-hallucination diff annotation and confidence-scored findings, in two modes — a fast walkthrough-plus-findings pass by default, or a multi-material fan-out on demand. Runs before a pull request: the report goes to the chat, with optional fix application and a saved report.

## Triggers

- **Quick review** (default — "review", "review my changes", "check my diff", "review against main") → run the workflow below
- **Deep review** ("deep review", "full review", "thorough review") → run it in deep mode
- **Re-review** ("re-review", "check fixes", "are the issues resolved") → run it against the prior findings

## Workflow

Start immediately when triggered. No confirmation needed to begin.

```text
Progress:
- [ ] Step 1: Load the shared rules
- [ ] Step 2: Set up
- [ ] Step 3: Locate the spec
- [ ] Step 4: Run the mode
- [ ] Step 5: Report
```

**Step 1. Load the shared rules.** Load [common.md](references/common.md), [guidelines-audit.md](references/guidelines-audit.md), and [spec-review.md](references/spec-review.md). The modes hand these rules to their agents. Done when all three are loaded.

**Step 2. Set up.** Run `git status --porcelain`. With uncommitted changes, the range is the working tree (`git diff HEAD`); otherwise it is the current branch against the base the user names, else `main` (`git diff <base>...HEAD`). Run `git diff <range> | python3 <this-skill>/scripts/annotate_diff.py | tee ${TMPDIR:-/tmp}/review-lens-annotated.diff`: its output above `CHANGED_FILES:` is `ANNOTATED_DIFF`, and the paths below it are `CHANGED_FILES`. With no changes, tell the user there is nothing to review and stop. With no base branch found, ask which branch to compare against. If the script exits 1, check the range and run it again. Done when `ANNOTATED_DIFF` and `CHANGED_FILES` are in hand.

**Step 3. Locate the spec.** Follow the Locate the Spec section of spec-review.md. Done when the spec content is in hand or the totals line will show `Spec: none`.

**Step 4. Run the mode.** Default to quick and load [quick-review.md](references/quick-review.md). Load [deep-review.md](references/deep-review.md) only when the user asks for depth or the change is risky or wide-reaching — it fans out by material, at higher cost. Run the mode through its Assemble section; on a re-review, constrain it with the mode's Re-Review section. Write every returned item under its `## Findings`, `## Guidelines Compliance`, or `## Spec Compliance` heading, each with its `- confidence: N` line, and pipe that text into `python3 <this-skill>/scripts/merge_findings.py ${TMPDIR:-/tmp}/review-lens-annotated.diff`. The script drops an item with an unknown severity, a missing or sub-80 confidence, or a line with no `[L<n>]` marker (a `missing/partial` spec gap has no line), dedups, and sorts each section by severity. If it exits 1, fix the input it names and run it again. Done when the script's sections and `COUNTS:` line are in hand.

**Step 5. Report.** Render the common.md output template from the script's sections, taking the totals from its `COUNTS:` line. On a re-review, mark each prior finding `fixed`, `persisting`, or `regressed` and output the status table first. Print to the terminal, then offer to apply the suggested fixes under the Fix Suggestions rules. Done when the report is printed and the offer is made.

## Anti-Pattern: Confidence Inflation

Reporting findings below 80 confidence buries real issues under noise. The rubric is calibrated: <80 means speculation or style preference, not a real bug. When unsure, drop down — gather more context, re-read the diff — instead of pushing a low-confidence finding through.
