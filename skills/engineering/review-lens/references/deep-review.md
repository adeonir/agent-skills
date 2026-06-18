# Deep Review (Multi-Material Fan-Out)

The thorough review. Several agents run in parallel, each reading a **different source of material** — the diff, the project's guideline files, the git history, and (when available) prior pull requests — so each surfaces signal a single pass over the diff could not reach. A separate agent then judges every finding's confidence. Reserved for risky or wide-reaching changes.

## When to Use

When the user asks for a "deep", "full", or "thorough" review, or the change is risky or wide-reaching. The default [quick-review.md](quick-review.md) covers the everyday case more cheaply.

Shared rules — annotation, size gate, confidence rubric, what-not-to-report, output template, fix suggestions, data trust boundary — live in [common.md](common.md) and apply throughout.

## Why fan out by material, not by concern

A capable model already looks for security, bugs, data-loss, and performance in one reading of a diff — splitting those into separate agents re-reads the same material at multiplied cost for little new signal. The leverage is in giving each agent **different material**: the history and prior reviews carry information the diff alone does not. So the concerns become a checklist inside one bug-scan; the fan-out divides by source.

## Workflow

### Step 1: Setup (inline, main agent)

- Determine target and base as in [quick-review.md](quick-review.md) Step 1; capture `DIFF` and `CHANGED_FILES`; produce `ANNOTATED_DIFF` (annotation algorithm in [common.md](common.md)); apply the size gate.
- Gather the project's guideline file paths once (per [guidelines-audit.md](guidelines-audit.md), including `.claude/rules/*.md`) and pass them to the compliance agent so it does not rediscover them.
- Write the `## Summary` walkthrough — a plain-language description of the change, grouped by area — and the `## Highlights` (at least one positive observation drawn from the change).

### Step 2: Select Active Agents

Two agents always run; two are conditional:

- **bug-scan** and **compliance** — always.
- **git-history** — when the changed files have meaningful history (skip on brand-new files with no prior commits).
- **prior-PRs** — when `gh` is available **and** the repo has a GitHub remote. If not, skip it and note the skip in the totals line.

### Step 3: Fan Out by Material

Dispatch the active agents in a single turn. Each returns findings in the Finding Format ([common.md](common.md)), citing only `[L<n>]` lines and attaching a suggested fix where non-obvious. Finders **surface candidates** with their reasoning — they do not drop on confidence; the judge (Step 4) is the single `>= 80` gate.

| Agent | Model | Reads | Looks for |
|-------|-------|-------|-----------|
| bug-scan | Sonnet | `ANNOTATED_DIFF` | the full concern checklist in one pass: security, bugs, data-loss, performance |
| compliance | Haiku | the gathered guideline files | diff vs explicit documented rules — follow [guidelines-audit.md](guidelines-audit.md) |
| git-history | Sonnet | `git log` / `git blame` of `CHANGED_FILES` | regressions, reverted fixes, and changes that contradict why the code was last touched |
| prior-PRs | Haiku | past PRs touching these files + their review comments (`gh`) | recurring concerns reviewers raised before that apply again |

The bug-scan concern checklist:

- **security** — injection, XSS, auth bypass, credential/secret exposure, PII in logs, missing signature/CORS checks, sensitive fields in response DTOs
- **bugs** — logic errors, runtime failures, swallowed errors, weakened error handling or test assertions, dead code, type assertions hiding real errors
- **data-loss** — destructive migrations, wrong update/delete predicates, missing transactions on multi-write paths, irreversible ops behind weak guards
- **performance** — N+1 queries, unbounded `find()` without pagination, sequential `await` for independent operations

### Step 4: Judge (batched, Haiku)

Collect every finding from every agent and pass them to **one** Haiku judge in a single call. For each finding it returns a confidence score 0-100 (rubric in [common.md](common.md)); for guideline findings it confirms the cited rule actually says what the finding claims. Drop everything below 80. The judge is independent of the finders — a finder never scores its own work.

### Step 5: Consolidate

1. Dedup by `file:line` + similar title across agents; keep the highest severity and merge sources.
2. Sort by severity (order in [common.md](common.md)).
3. Coverage: from `CHANGED_FILES`, list files that received zero findings; exclude `*.json`, `*.yaml`, `*.lock`, `*.d.ts`, and pure type-declaration files.
4. If an agent errored, continue with the rest and note `Partial review (<N> of <M> agents)` in the totals line.

### Step 6: Output

Render with the [common.md](common.md) output template (summary on top, issues, guideline compliance, highlights, coverage). Then follow the output-channel and fix rules in [common.md](common.md): print to the terminal, offer to save `CODE_REVIEW.md`, and offer to apply the suggested fixes (opt-in, with confirmation).

## Re-Review

On "re-review" / "check fixes": reload prior findings, re-run the fan-out and judge steps constrained to the previously flagged `file:line` set plus newly changed lines, and mark each prior finding `fixed`, `persisting`, or `regressed`. Output the status table ([common.md](common.md)) before the standard report.

## Guidelines

- Each agent reads **different** material — never send the same source to two agents.
- Keep find and judge separate; the judge is the only gate to the report.
- Skip a conditional agent cleanly and note it, rather than running it on empty material.
- Sort the final report by severity, not by agent or discovery order.

## Error Handling

- No changes to review: tell the user there is nothing to review.
- No base branch found: ask which branch to compare against.
- `gh` unavailable or no GitHub remote: skip prior-PRs, note it, continue.
- Diff exceeds the size gate: stop, cite the limits, suggest splitting the branch.
- An agent fails: continue with the rest, mark `Partial review` in the totals line.
- Re-review requested with no prior findings: fall back to a standard deep review.
