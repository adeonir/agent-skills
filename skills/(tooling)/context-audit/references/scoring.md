# Scoring and Prioritization

How `scripts/audit.py` computes the score and ranks fixes. Use this
file when the user asks why a deduction happened or how the Top 3 was
selected.

## When to Use

- Loaded only when explaining a deduction or score component
- Not loaded for normal report writing -- the template uses pre-computed
  values from the script output
- Reach for this file when the user pushes back on a number

## Scoring formula

Start at 100. Apply deductions per category, capped per category to
prevent double-counting. Floor at 0.

| Category | Deduction | Cap |
|----------|-----------|-----|
| MCP server with CLI alternative | -3 each | -15 |
| MCP count beyond 5 | -2 per server | -10 |
| CLAUDE.md > 200 lines (resolved) | -10 | -- |
| CLAUDE.md > 500 lines (resolved) | -20 (replaces -10) | -- |
| Each rule auto-flagged by pre-filter | -1 | -20 across all instruction files |
| Skill > 200 lines | -5 each | -15 |
| Skill > 500 lines | -10 each (replaces -5) | -15 |
| Agent > 150 lines | -3 each | -10 |
| Slash command > 100 lines | -2 each | -10 |
| Missing `env.BASH_MAX_OUTPUT_LENGTH` | -5 | -- |
| Missing `permissions.deny` while bloat dirs exist | -10 | -- |

## Why caps matter

Without caps, a project with 20 MCP servers gets crushed (-60) even if
all 20 are used daily. The cap reflects reality: past a threshold, the
pattern is the problem, not the count itself.

The flagged-rules cap of -20 prevents a 1000-line CLAUDE.md from
collapsing the entire score on its own -- the size penalty already
captured most of that signal.

## Score labels

| Range | Label |
|-------|-------|
| 90-100 | CLEAN |
| 70-89 | NEEDS WORK |
| 50-69 | BLOATED |
| 0-49 | CRITICAL |

## Severity for individual issues

| Per-issue deduction | Severity |
|---------------------|----------|
| >= 10 points | CRITICAL |
| 5-9 points | WARNING |
| < 5 points | INFO |

## Top 3 fixes ranking

Rank by **estimated tokens saved per turn divided by effort weight**.
The script pre-computes this; the report just renders the top three.

Effort weights:

| Effort | Weight | Examples |
|--------|--------|----------|
| trivial | 1 | Add settings key, add deny rules |
| small | 2 | Disconnect an unused MCP, delete a redundant rule |
| medium | 4 | Rewrite a vague rule, restructure CLAUDE.md with @imports |
| large | 8 | Compress a long skill, replace MCP with CLI in workflow |

## Token savings heuristics

Built into `scripts/audit.py`:

- **MCP with CLI alternative:** pull from /context if user provided it; otherwise estimate ~15,000 tokens per server
- **Instruction file lines:** ~4 tokens per Markdown line
- **Missing bash output cap:** estimate one truncation event per ~10 turns at ~3,000 tokens per retry
- **Missing deny rules with bloat dirs:** high variance; default 10,000, can be 0 if dirs are small

When an estimate is uncertain, mark with `~` in the report so the user
knows it is approximate.

## Guidelines

**DO:**
- Cite the cap when explaining why a high-count category got a small deduction
- Distinguish quality fixes from token-savings fixes when explaining numbers
- Pull from /context output when the user provided it; estimates only when they did not
- Show the math when justifying a Top 3 ranking decision

**DON'T:**
- Inflate estimates for emphasis (contrasts: show the math)
- Conflate quality fixes (rule rewrites) with token-savings fixes (contrasts: distinguish quality from savings)
- Hide caps behind hand-wavy language (contrasts: cite the cap explicitly)
- Estimate when /context numbers exist (contrasts: pull from /context when provided)

## Error Handling

- /context numbers contradict the heuristic estimate: trust /context, mark heuristic as superseded
- User disputes a deduction: surface the rule that triggered it; let them decide if it should be reclassified
- A category has zero deductions but the user expected one: confirm the scanner picked up the relevant files
