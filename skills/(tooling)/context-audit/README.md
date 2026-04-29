# Context Audit

Audit a Claude Code setup for token waste and context bloat across MCP servers, CLAUDE.md, slash commands, agents, skills, settings, and file permissions.

## Installation

```bash
npx skills add adeonir/agent-skills --skill context-audit
```

## What It Does

Combines deterministic file scanning with qualitative judgment to find context waste, score the setup, and prioritize fixes by estimated tokens saved per turn.

```mermaid
flowchart LR
    A[/context snapshot] --> B[audit.py scan]
    B --> C[reconcile filters]
    C --> D[score and report]
    D --> E[offer fixes diff-first]
```

| Phase | Output |
|-------|--------|
| /context snapshot | Real token overhead numbers (or file-only fallback) |
| audit.py scan | JSON with MCP, CLAUDE.md, skills, settings, deny-rule findings + pre-filtered rule candidates |
| reconcile filters | Confirmed flagged rules with file/line/filter/reason |
| score and report | Markdown report with "What's working", issues, Top 3 ranked by savings/effort |
| offer fixes | Diffs for settings.json, deny rules, CLAUDE.md edits |

## Usage

```
audit my context
check my settings
why is Claude so slow
token optimization
context audit
context bloat
run /context-audit
```

After pasting `/context` output:

```
here's my /context — what should I cut?
```

For drift tracking across sessions, save a baseline once, then compare on later runs:

```bash
# After running audit.py:
python scripts/baseline.py --save /tmp/audit.json

# Weeks later, fresh audit:
python scripts/audit.py --out /tmp/audit.json
python scripts/baseline.py --compare /tmp/audit.json
```

## Output

Default mode: inline markdown report in chat.

If the user asks to save: `.artifacts/context-audit/YYYY-MM-DD-report.md`.

The drift baseline file persists at `.claude/.audit-baseline.json` -- written by `scripts/baseline.py --save`, read by `scripts/baseline.py --compare`.

## Requirements

- Python 3 (stdlib only -- no external packages)
- A Claude Code project to audit (works on minimal setups too)

## Integration

| With | Connection |
|------|-----------|
| wrap-up | Recommend periodic audits in session notes; note score changes over time |
| project-index | Different domain: project-index documents the codebase, context-audit documents the agent setup |
