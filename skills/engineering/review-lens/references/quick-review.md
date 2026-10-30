# Quick Review

The fast, default review. Two cheap agents run in parallel by role — one writes a plain-language walkthrough of the change, the other finds issues across every scope — plus a spec agent when a spec was found, and the main agent assembles a single report. No deep fan-out, no history or PR lookups. Built for everyday changes.

## When to Use

Loaded to run the review in the default mode: two cheap agents in parallel by role, a third for the spec when one exists, no history or PR lookups.

## Fan Out by Role

Dispatch every active agent in a single turn (one Task call each). Each receives `ANNOTATED_DIFF`, `CHANGED_FILES`, and the shared rules from [common.md](common.md).

- **Walkthrough (Haiku):** produce the `## Summary` block — a plain-language description of what the change does, grouped by area or file — plus the `## Highlights` (at least one positive observation). No findings, just orientation.
- **Findings (Sonnet):** a single generalist pass over `ANNOTATED_DIFF` covering every scope. Code findings (security, bugs, data-loss, performance) are returned in the Finding Format ([common.md](common.md)); guideline violations follow [guidelines-audit.md](guidelines-audit.md). Apply the confidence gate here, since quick has no separate judge, and attach a suggested fix where non-obvious. After listing findings, re-read the diff once and name every file left uncommented, stating why it is clean.
- **Spec (Sonnet), only when a spec was found:** also receives the spec content. Compares the diff against it per [spec-review.md](spec-review.md), applies the confidence gate, and returns the `### Spec Compliance` block.

## Assemble

Merge the walkthrough, the findings, and the spec gaps into the [common.md](common.md) output template. The merge script sorts each section by severity.

## Re-Review

Reload the prior findings (from `CODE_REVIEW.md` or chat) and run the fan-out constrained to the previously flagged `file:line` set plus newly changed lines; the spec agent re-checks the requirements behind prior spec gaps, line or not.

## Guidelines

- The findings agent covers every scope in one pass; do not silently drop one because the diff "looks" unrelated.
- The agents are independent — the walkthrough never invents findings, the findings agent never narrates the change, and only the spec agent reads the spec.

## Error Handling

- Binary files in diff: skip and note them in the summary.
- An agent fails: continue with the rest, mark `Partial review` in the totals line.
- Re-review requested with no prior findings: fall back to a standard quick review.
