---
name: debug-tools
description: >-
  Iterative debugging workflow with confidence scoring, pattern comparison, and
  strategic log injection. Investigate, fix, verify loop with auto-cleanup of
  debug logs and escalation to architectural review after 3 failed attempts. Use
  when diagnosing unexpected behavior, silent errors, or intermittent failures,
  when tests pass but the app fails or it works in dev but not in prod, when
  tracing an issue, or when adding or cleaning up debug logs. Not for known
  one-line fixes where the user names file and line, runtime error review on
  deployed services, or PM bug-report triage.
---

# Debug Tools

Iterative debugging workflow with flexible technique selection and escalation.

## Triggers

- **Debug a bug** ("debug this", "investigate", "trace issue", "fix bug", "why is X broken") → [investigation.md](references/investigation.md)
- **Add debug logs** ("add debug logs", "inject logs", "trace with logs") → [log-injection.md](references/log-injection.md)
- **Cleanup logs** ("remove debug logs", "cleanup logs") → [log-cleanup.md](references/log-cleanup.md)
- **Pattern lookup** ("debug patterns", "common bugs", "used to work") → [debugging-patterns.md](references/debugging-patterns.md)

Multiple references may load during one debugging session — investigation often leads to log injection, then back to investigation.

## Workflow

```text
investigate → fix → verify → done
  ^_______________________|  (max 3 attempts, then escalate)
```

Core loop: investigate, fix, verify. Techniques (log injection, pattern comparison, focus area analysis) are tools within investigation, not mandatory phases. Log cleanup happens automatically after verification succeeds.

A sensitive value never reaches an injected log — passwords, tokens, API keys, PII, session identifiers. This binds anywhere a log is added, including mid-investigation without the injection workflow loaded.

## Anti-Pattern: Symptom Whack-a-Mole

Fixing the same symptom in multiple places signals an architectural issue, not a localized bug. When fix N introduces bug N+1, stop. The 4th attempt must escalate to architectural review: re-examine the abstraction, the missing layer, or the flawed assumption — not retry a deeper version of the same approach.
