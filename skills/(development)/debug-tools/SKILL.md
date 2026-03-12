---
name: debug-tools
description: >-
  Iterative debugging workflow with confidence scoring, pattern
  comparison, and strategic log injection. Use when debugging unexpected
  behavior, silent errors, intermittent failures, or when something isn't
  working, tests pass but app fails, or works in dev but not in prod. Triggers
  on "debug", "fix bug", "investigate", "trace issue", "add debug logs",
  "cleanup debug logs", "why is this broken", "not working".
license: MIT
allowed-tools: Read, Grep, Bash
metadata:
  author: Adeonir Kohl
---

# Debug Tools

Iterative debugging workflow with flexible technique selection and escalation.

## Workflow

```
investigate --> fix --> verify --> done
  ^_______________________|  (max 3 attempts, then escalate)
```

Core loop: investigate, fix, verify. Techniques (log injection, pattern
comparison, focus area analysis) are tools within investigation, not mandatory
phases. Log cleanup happens automatically after verification succeeds.

## Context Loading Strategy

Load only the reference matching the current trigger. Multiple references may be
loaded during a full debugging session (investigation often leads to log injection).

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Debug issue, investigate bug, fix bug | [investigation.md](references/investigation.md) |
| Add debug logs, inject logs, trace with logs | [log-injection.md](references/log-injection.md) |
| Remove debug logs, cleanup logs | [log-cleanup.md](references/log-cleanup.md) |
| Debug patterns, log format, common bugs | [debugging-patterns.md](references/debugging-patterns.md) |

## Cross-References

```
investigation.md <---> log-injection.md (investigation may request logs)
investigation.md <---> log-cleanup.md (after fix verified)
investigation.md <---> debugging-patterns.md (pattern comparison)
log-injection.md ----> log-cleanup.md (cleanup removes injected logs)
```

## Guidelines

**DO:**
- Use confidence scoring: >= 70 report as probable cause, 50-69 suggest logs
- Compare broken code against working examples when root cause is unclear
- Always use `[DEBUG]` prefix for injected logs (enables cleanup)
- Apply minimal fix: smallest change that resolves the issue
- Clean up debug logs automatically after fix is verified
- Track fix attempts: after 3 failed fixes, escalate on the 4th to architectural review
- Use whatever debugging tools are available in the environment

**DON'T:**
- Report findings with confidence < 50
- Log sensitive data (passwords, tokens, PII)
- Apply large refactors as part of a bug fix
- Leave debug logs in production code
- Keep retrying the same approach when fixes fail repeatedly

## Error Handling

- No bug description provided: ask user to describe the issue
- Cannot reproduce: suggest adding debug logs
- Fix doesn't work: return to investigation with new evidence
- Three failed fix attempts: escalate to architectural review on the next attempt
- Logs left behind: user can request cleanup anytime
