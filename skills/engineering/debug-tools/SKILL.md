---
name: debug-tools
description: "Evidence-led debugging for unexpected, silent, or intermittent failures. Use when tracing bugs, adding targeted logs, or verifying fixes. Not for known one-line fixes, runtime review of deployed services, or PM bug triage."
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
