---
name: debug-tools
description: "Evidence-led debugging for unexpected, silent, or intermittent failures. Use when tracing bugs, adding targeted logs, or verifying fixes. Not for known one-line fixes, runtime review of deployed services, or PM bug triage."
---

# Debug Tools

Iterative debugging workflow with flexible technique selection and escalation.

## Triggers

- **Debug a bug** ("debug this", "investigate", "trace issue", "fix bug", "why is X broken") → run the workflow below
- **Add debug logs** ("add debug logs", "inject logs", "trace with logs") → enter at step 3
- **Cleanup logs** ("remove debug logs", "cleanup logs") → enter at step 5
- **Pattern lookup** ("debug patterns", "common bugs", "used to work") → enter at step 2

## Workflow

```text
investigate → fix → verify → done
  ^_______________________|  (max 3 attempts, then escalate)
```

1. **Load [investigation.md](references/investigation.md)** and work its steps: understand the bug, analyze the code, enumerate hypotheses with confidence scores, report, propose a fix, verify. Enter at the step the current state calls for — a session already carrying evidence does not restart at Step 1.
2. **Load [debugging-patterns.md](references/debugging-patterns.md)** when a symptom needs matching against a known bug shape, when analysis stalls and the broken code has to be diffed against a working example, or when the user reports that something used to work.
3. **Load [log-injection.md](references/log-injection.md)** when reading the code cannot show the mechanism and only observing the running system can. Not every session needs it.
4. **Fix and verify.** Propose a fix only when the evidence names the mechanism; never as exploration. Run the reproduction after the fix is applied, and repeat it 3-5 times for a race condition or an intermittent bug.
5. **Load [log-cleanup.md](references/log-cleanup.md)** once the fix is verified, or on explicit request. Run it before changes go to version control.

A sensitive value never reaches an injected log — passwords, tokens, API keys, PII, session identifiers. This binds anywhere a log is added, including mid-investigation without step 3 loaded.

## Anti-Pattern: Symptom Whack-a-Mole

Fixing the same symptom in multiple places signals an architectural issue, not a localized bug. When fix N introduces bug N+1, stop. The 4th attempt must escalate to architectural review: re-examine the abstraction, the missing layer, or the flawed assumption — not retry a deeper version of the same approach.
