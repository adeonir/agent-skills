# Deep Review (Multi-Material Fan-Out)

The thorough review. Several agents run in parallel, each reading a **different source of material** — the diff, the project's guideline files, the spec, the git history, and (when available) prior pull requests — so each surfaces signal a single pass over the diff could not reach. A separate agent then judges every finding's confidence. Reserved for risky or wide-reaching changes.

## When to Use

Loaded to run the review in deep mode: a fan-out by material with an independent confidence judge, at higher cost than quick mode.

## Why fan out by material, not by concern

A capable model already looks for security, bugs, data-loss, and performance in one reading of a diff — splitting those into separate agents re-reads the same material at multiplied cost for little new signal. The leverage is in giving each agent **different material**: the history and prior reviews carry information the diff alone does not. So the concerns become a checklist inside one bug-scan; the fan-out divides by source.

## Prepare

- Gather the project's guideline file paths once (Find Guideline Files in [guidelines-audit.md](guidelines-audit.md)) and pass them to the compliance agent so it does not rediscover them.
- Write the `## Summary` walkthrough — a plain-language description of the change, grouped by area — and the `## Highlights` (at least one positive observation drawn from the change).

## Select Active Agents

Two agents always run; three are conditional:

- **bug-scan** and **compliance** — always.
- **spec** — when a spec was found. If not, skip it.
- **git-history** — when the changed files have meaningful history (skip on brand-new files with no prior commits).
- **prior-PRs** — when `gh` is available **and** the repo has a GitHub remote. If not, skip it and note the skip in the totals line.

## Fan Out by Material

Dispatch the active agents in a single turn. Each returns findings in the Finding Format ([common.md](common.md)) and attaches a suggested fix where non-obvious. Finders **surface candidates** with their reasoning — they do not drop on confidence; the judge is the single gate.

| Agent | Model | Reads | Looks for |
|-------|-------|-------|-----------|
| bug-scan | Sonnet | `ANNOTATED_DIFF` | the full concern checklist in one pass: security, bugs, data-loss, performance |
| compliance | Haiku | the gathered guideline files | diff vs explicit documented rules — follow [guidelines-audit.md](guidelines-audit.md) |
| spec | Sonnet | the spec content | missing/partial, incorrect, and out-of-scope behavior — follow [spec-review.md](spec-review.md) |
| git-history | Sonnet | `git log` / `git blame` of `CHANGED_FILES` | regressions, reverted fixes, and changes that contradict why the code was last touched |
| prior-PRs | Haiku | past PRs touching these files + their review comments (`gh`) | recurring concerns reviewers raised before that apply again |

The bug-scan concern checklist:

- **security** — injection, XSS, auth bypass, credential/secret exposure, PII in logs, missing signature/CORS checks, sensitive fields in response DTOs
- **bugs** — logic errors, runtime failures, swallowed errors, weakened error handling or test assertions, dead code, type assertions hiding real errors
- **data-loss** — destructive migrations, wrong update/delete predicates, missing transactions on multi-write paths, irreversible ops behind weak guards
- **performance** — N+1 queries, unbounded `find()` without pagination, sequential `await` for independent operations

## Judge (batched, Opus)

Collect every finding from every agent and pass them to **one** Opus judge in a single call. For each finding it returns a confidence score 0-100 (rubric in [common.md](common.md)); for guideline findings it confirms the cited rule actually says what the finding claims, and for spec findings that the quoted requirement says what the gap claims. The judge is independent of the finders — a finder never scores its own work.

## Assemble

1. Attach each judge score to its finding as a `- confidence: N` line. The merge script dedups across agents by `file:line` + similar title, keeps the highest severity, and sorts each section by severity.
2. Merge into the [common.md](common.md) output template.
3. For `## Files With No Findings`: from `CHANGED_FILES`, list files that received zero findings; exclude `*.json`, `*.yaml`, `*.lock`, `*.d.ts`, and pure type-declaration files.

## Re-Review

Reload the prior findings (from `CODE_REVIEW.md` or chat) and run the fan-out and judge constrained to the previously flagged `file:line` set plus newly changed lines; the spec agent re-checks the requirements behind prior spec gaps, line or not.

## Guidelines

- Each agent reads **different** material — never send the same source to two agents.
- Skip a conditional agent cleanly and note it, rather than running it on empty material.

## Error Handling

- `gh` unavailable or no GitHub remote: skip prior-PRs, note it, continue.
- An agent fails: continue with the rest, mark `Partial review` in the totals line.
- Re-review requested with no prior findings: fall back to a standard deep review.
