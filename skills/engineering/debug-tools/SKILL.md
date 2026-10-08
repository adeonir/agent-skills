---
name: debug-tools
description: "Evidence-led debugging for unexpected, silent, intermittent, or regressed behavior, including slowdowns and leaks. Use when tracing a bug to its root cause, finding what broke something that used to work, adding or removing targeted debug logs, or verifying a fix. Not for known one-line fixes, code review of a diff, runtime review of deployed services, or PM bug triage."
---

# Debug Tools

Iterative debugging workflow that gates a fix on evidence and escalates after repeated failures.

## Triggers

- **Debug a bug** ("debug this", "investigate", "trace issue", "fix bug", "why is X broken") → Step 1
- **Regression or comparison** ("used to work", "broke after the update", "works there but not here") → Step 2
- **Add debug logs** ("add debug logs", "inject logs", "trace with logs") → Step 3
- **Cleanup logs** ("remove debug logs", "cleanup logs") → Step 5

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Investigate
- [ ] Step 2: Compare against working code (when needed)
- [ ] Step 3: Gather runtime evidence (when needed)
- [ ] Step 4: Fix and verify
- [ ] Step 5: Clean up logs
```

Start at the step the session's state calls for; a session already carrying evidence does not restart at Step 1.

**Step 1. Investigate.** Load [investigation.md](references/investigation.md) and work its sections from Understand the Bug through Rank Hypotheses. Done when every hypothesis carries a score and an evidence type, and the leading one either has evidence or names the runtime data it needs.

**Step 2. Compare against working code.** When analysis stalls and the broken code has to be diffed against a working example, or when the user reports that something used to work, load [debugging-patterns.md](references/debugging-patterns.md). Done when the comparison or the regression trace is in hand; then return to Step 1 to re-rank.

**Step 3. Gather runtime evidence.** When reading the code cannot show the mechanism and only observing the running system can, load [log-injection.md](references/log-injection.md). Done when the reproduction's output is read; then return to Step 1 to re-rank.

**Step 4. Fix and verify.** Work the Propose Fix, Verify, and Report sections of investigation.md. Done when the reproduction no longer shows the symptom and the report is written. If the symptom remains, return to Step 1 with what the run showed.

**Step 5. Clean up logs.** Once the fix is verified, or on explicit request, load [log-cleanup.md](references/log-cleanup.md). Run it before changes go to version control. Done when the script's `find` reports no `[DEBUG]` statement and the project's syntax check passes.

A sensitive value never reaches an injected log — passwords, tokens, API keys, PII, session identifiers. This binds anywhere a log is added, including mid-investigation without Step 3 loaded.

## Anti-Pattern: Symptom Whack-a-Mole

Fixing the same symptom in multiple places signals an architectural issue, not a localized bug. End each Step 4 report whose symptom remains with `Attempt N of 3`, and read that number back before proposing another fix. After three, stop fixing: the fourth move is an architectural assessment for the user — what was tried and why it failed, whether the issue is systemic (wrong abstraction, missing layer, flawed assumption), and the architectural change that would resolve it. Stop and reassess earlier when the root cause keeps changing, the changes grow with each attempt, or the confidence score drops between attempts.
