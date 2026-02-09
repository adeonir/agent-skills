---
name: debug-tools
description: >-
  Iterative debugging workflow with confidence scoring and strategic log injection.
  Five phases: investigate, inject logs, propose fix, verify, cleanup.
  Use when: debugging unexpected behavior, silent errors, intermittent failures,
  or issues requiring runtime data. Triggers on "debug", "fix bug", "investigate",
  "trace issue", "add debug logs", "cleanup debug logs".
metadata:
  author: github.com/adeonir
  version: "1.0.0"
---

# Debug Tools

Iterative debugging workflow with targeted log injection and cleanup.

## Workflow

```
investigate --> inject logs --> propose fix --> verify --> cleanup
     ^_________________________________________|
```

The workflow loops back to investigation if the fix doesn't work.

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
log-injection.md ----> log-cleanup.md (cleanup removes injected logs)
```

## Guidelines

- Confidence scoring: >= 70 report as probable cause, 50-69 suggest logs, < 50 don't report
- Always use `[DEBUG]` prefix for injected logs (enables cleanup)
- Never log sensitive data (passwords, tokens, PII)
- Minimal fix: smallest change that resolves the issue
- Cleanup is automatic after fix is verified
- Uses whatever debugging tools are available in the environment

## Error Handling

- No bug description provided: ask user to describe the issue
- Cannot reproduce: suggest adding debug logs
- Fix doesn't work: return to investigation phase
- Logs left behind: user can request cleanup anytime
