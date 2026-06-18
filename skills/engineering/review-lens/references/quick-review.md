# Quick Review

The fast, default review. Two cheap agents run in parallel by role — one writes a plain-language walkthrough of the change, the other finds issues across every scope — and the main agent assembles a single report. No deep fan-out, no history or PR lookups. Built for everyday changes.

## When to Use

Default when the user asks to "review" changes, "check my diff", or review against a base branch without asking for depth. Reach for [deep-review.md](deep-review.md) only on risky or wide-reaching changes, or when the user asks for a "deep", "full", or "thorough" review.

Shared rules — diff annotation, size gate, confidence rubric, what-not-to-report, output template, fix suggestions, data trust boundary — live in [common.md](common.md) and apply here in full.

## Workflow

Start immediately when triggered. No confirmation needed to begin.

### Step 1: Setup (inline, main agent)

- **Target:** run `git status --porcelain`. If there are uncommitted changes, review the working directory; otherwise compare the current branch against the base.
- **Base:** the branch the user names, else `main`.
- Capture `DIFF` and `CHANGED_FILES`, then produce `ANNOTATED_DIFF` with the annotation algorithm in [common.md](common.md). Apply the size gate.

### Step 2: Fan Out — Two Agents in Parallel by Role

Dispatch both in a single turn (two Task calls). Each receives `ANNOTATED_DIFF`, `CHANGED_FILES`, and the shared rules from [common.md](common.md).

- **Walkthrough (Haiku):** produce the `## Summary` block — a plain-language description of what the change does, grouped by area or file — plus the `## Highlights` (at least one positive observation). No findings, just orientation.
- **Findings (Sonnet):** a single generalist pass over `ANNOTATED_DIFF` covering every scope. Code issues (security, bugs, data-loss, performance) are returned in the Finding Format ([common.md](common.md)); guideline violations use the violation shape and discovery in [guidelines-audit.md](guidelines-audit.md) (includes `.claude/rules/*.md`). Cite only `[L<n>]` lines, apply the confidence rubric (report `>= 80`), and attach a suggested fix where non-obvious. After listing findings, re-read the diff once and name every file left uncommented, stating why it is clean (second-pass coverage).

### Step 3: Assemble and Output

The main agent merges the walkthrough and the findings into the [common.md](common.md) output template, sorts findings by severity (order in `common.md`), and renders the report. Then it follows the output-channel and fix-suggestion rules in [common.md](common.md): print to the terminal, offer to save `CODE_REVIEW.md`, and offer to apply the suggested fixes (opt-in, with confirmation).

## Re-Review

On "re-review" / "check fixes": reload the prior findings (from `CODE_REVIEW.md` or chat), re-run the setup and fan-out steps constrained to the previously flagged `file:line` set plus newly changed lines, and mark each prior finding `fixed`, `persisting`, or `regressed`. Output the status table ([common.md](common.md)) before the standard report.

## Guidelines

- Keep the `[L<n>]` annotation and the `>= 80` confidence bar — quick changes the depth, not the rigor.
- The findings agent covers every scope in one pass; do not silently drop one because the diff "looks" unrelated.
- The two agents are independent — the walkthrough never invents findings, the findings agent never narrates the change.
- Sort the final report by severity, not by discovery order.

## Error Handling

- No changes to review: tell the user there is nothing to review.
- No base branch found: ask which branch to compare against.
- Binary files in diff: skip and note them in the summary.
- Diff exceeds the size gate: stop, cite the limits, suggest splitting the branch.
- Re-review requested with no prior findings: fall back to a standard quick review.
