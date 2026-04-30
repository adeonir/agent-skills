---
name: context-audit
description: >-
  Audit a Claude Code setup for token waste and context bloat across
  MCP servers, CLAUDE.md rules, slash commands, agents, skills, settings,
  and file permissions. Use when troubleshooting slow output, trimming
  a drifted configuration, or running a periodic health check before
  quality degrades.
when_to_use: >-
  Triggers on "audit my context", "check my settings", "why is Claude
  so slow", "token optimization", "context audit", "context bloat",
  "run /context-audit", or after the user pastes /context output and
  asks what to cut. Not for code review (use git-helpers "code review")
  or session wrap-up (use wrap-up).
effort: medium
---

# Context Audit

**Recommended effort:** medium for filter reconciliation and report writing; low for audit script execution.

Bloated context costs twice -- usage limits burn faster and output
quality drops, because models pay less attention to material in the
middle of a long context window. This skill finds the waste and tells
the user what to cut, with the estimated tokens-per-turn each fix saves.

## Workflow

```
context-snapshot --> audit-script --> reconcile-filters --> report --> offer-fixes
```

Each phase feeds the next. The script does the deterministic work
(file scanning, scoring, pre-filtering candidate rules); the model
applies judgment (filter reconciliation, narrative report).

## Context Loading Strategy

Load references on demand at the phase that needs them. Never load all
references upfront. The script output is the factual basis -- references
explain how to interpret and act on it.

| Phase | What to load |
|-------|-------------|
| context-snapshot | Nothing -- ask the user to run `/context` and paste the output before continuing |
| audit-script | Nothing -- run scripts/audit.py and read its JSON |
| reconcile-filters | [filters.md](references/filters.md) |
| report | [templates/report.md](templates/report.md), [scoring.md](references/scoring.md) only if explaining a deduction |
| offer-fixes | Nothing -- ask the user which to apply, show diffs |

In the context-snapshot phase, prompt the user explicitly: "Please run
`/context` in this session and paste the output -- it gives precise
per-category token numbers so MCP cost estimates aren't approximated."
Proceed without it only if the user declines or already pasted it.

[checks.md](references/checks.md) is loaded only if troubleshooting an
unexpected scanner result.

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Audit context, check settings, why is Claude slow | [filters.md](references/filters.md) (loaded in reconcile phase) |
| Explain a deduction or score component | [scoring.md](references/scoring.md) |
| Write the audit report | [report.md](templates/report.md) |
| Troubleshoot a scanner finding | [checks.md](references/checks.md) |

Notes:

- `scoring.md` and `checks.md` are not direct triggers. They are loaded
  on demand within the audit workflow when the model needs to justify a
  number or investigate an unexpected scanner output.

## Cross-References

```
filters.md ---------> scripts/audit.py    (script pre-filters; this file is the judgment layer)
templates/report.md -> scoring.md         (report cites score; scoring rules live here)
checks.md ----------> scripts/audit.py    (checks doc explains what each scanner inspects)
context-audit ------> wrap-up             (suggest periodic re-runs in session notes)
```

## Guidelines

**DO:**
- Lead the report with estimated tokens saved per turn -- that is the user-facing value
- Show a diff for every change, including settings.json -- a bad key breaks the session
- Ask the user to paste `/context` output before scoring; fall back to ~15,000 per server estimate only if they decline
- Treat scripts/audit.py output as the factual basis -- do not re-scan files manually
- Confirm or reclassify the script's pre-filtered rules with judgment from filters.md
- Surface positive findings in a "What's working" section before issues
- Include the cross-file checks the script cannot do: contradictions and redundancies between project and user CLAUDE.md
- Keep CLAUDE.md rules that overlap with a skill trigger -- triggers are heuristic, rules are deterministic

**DON'T:**
- Skip the diff before applying settings.json changes (contrasts: show a diff for every change)
- Estimate MCP token cost when /context output exists (contrasts: ask for /context output before scoring)
- Re-scan files the script already covered (contrasts: treat script output as factual basis)
- Trust pre-filter flags blindly without confirming context (contrasts: confirm or reclassify with judgment)
- Auto-apply fixes without showing diffs first (contrasts: show a diff for every change)
- Lead the report with the score (contrasts: lead with tokens saved)
- Flag a CLAUDE.md rule as redundant because a skill trigger covers the same intent (contrasts: keep deterministic rules alongside heuristic triggers)

## Output

| Default mode | Long audit or repeated review |
|--------------|--------------------------------|
| Inline markdown report in chat | `.artifacts/context-audit/YYYY-MM-DD-report.md` if user asks to save |

The audit JSON from scripts/audit.py is ephemeral; do not save unless
the user asks for it. The baseline file at `.claude/.audit-baseline.json`
is the only persistent artifact, written by scripts/baseline.py for
drift tracking across runs.

## Error Handling

- /context output not provided: proceed with file-only audit, mark estimates with `~` prefix
- No `~/.claude/settings.json`: skip user-scope checks, mention in report
- No project `.claude/`: file-only audit, note that commands, agents, hooks could not be scanned
- No CLAUDE.md anywhere: report "no project rules detected", do not deduct
- audit.py crashes on a malformed file: report which file broke, continue with the rest
- Baseline file missing on `--compare`: instruct the user to run `--save` first
- User declines to run /context after one ask: do not loop, proceed with file-only audit
