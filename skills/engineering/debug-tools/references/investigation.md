# Investigation Workflow

Investigate bugs, find root causes with confidence scoring, and propose minimal fixes.

## When to Use

When debugging unexpected behavior, silent errors, or intermittent failures.

## Understand the Bug

Based on user's description, identify:

- Expected behavior vs actual behavior (the gap to close)
- Symptoms and error messages
- Reproduction steps (exact sequence that triggers the bug)
- Frequency: deterministic, intermittent, or load-dependent
- Recent changes that might have introduced it

If the user did not state expected vs actual or reproduction steps, build them from the code, the tests, or a repro script in the project, and state the assumption. Ask before analyzing only when neither the code nor the tests can give them. Diagnosis built on assumed behavior wastes attempts.

## Analyze Code

Start at the error and trace backwards from the symptom toward its origin.

## Enumerate Hypotheses

Generate 2-3 candidate root causes from the analysis. Multiple hypotheses up front prevent premature commitment to the first plausible explanation.

Score each one 0-100 and carry the number into the report. Give each an evidence type: `stack trace`, `diff`, or `runtime reading` when that source shows the code producing the symptom, and `none` when the mechanism is inferred from reading the code. The `Evidence` line quotes the exact stack frame, diff hunk, or log line that shows the mechanism; output that only repeats the symptom counts as `none`. The score says how far the evidence reaches, so the user can weigh the finding; it decides nothing on its own — the gate in Propose Fix does that, against evidence rather than against a number.

If only one hypothesis is plausible, that is fine -- do not invent weak alternatives to fill the slate. The goal is honest enumeration, not three items.

## Rank Hypotheses

Rank hypotheses by score, highest first — that is reading order. Which one to pursue is the one closest to a mechanism you can show, and the rest stay as fallbacks if the leading theory is disproven.

Here is a sensible default format, but use your best judgment:

**Probable cause — the mechanism is named:**

```markdown
**[85] Login fails silently on expired token**

- File: auth.ts:42
- Evidence type: stack trace
- Evidence: catch block swallows TokenExpiredError without updating UI state
- Fix: Add error state update in catch block to show login form
```

**Needs runtime data — the mechanism is a guess:**

```markdown
**[60] Possible race condition in session refresh**

- File: session.ts:18
- Evidence type: none
- Need: Execution order of refresh vs. redirect calls
- Suggest: Inject logs at session.ts:18, session.ts:25, redirect.ts:10
```

**Multiple hypotheses example:**

```markdown
1. **[75] Stale closure in retry handler** -- file: retry.ts:22, evidence type: diff, evidence: deps array missing `attempt`
2. **[55] Race between cache write and read** -- file: cache.ts:48, evidence type: none, need: ordering of write/read calls
3. **[40] Network flakiness** -- evidence type: none, no mechanism, kept as fallback
```

## Propose Fix

**Gate:** Propose a fix only for a hypothesis whose evidence type is `stack trace`, `diff`, or `runtime reading` — you can point at the code that produces the symptom and say how it produces it. A hypothesis at `none` is a story that fits the symptom: gather runtime evidence first, however high its score. Never propose a fix as exploration.

When root cause is confirmed, present it. Here is a sensible default format, but use your best judgment:

````markdown
## Proposed Fix

**Confidence: {score}**

Root cause: {one sentence explanation}

```diff
// {file}:{line} {diff showing the fix}
```
````

Present the fix; never apply it without the user's approval.

## Verify

Once the fix is applied, run the reproduction and read the result. Hand it to the user only when the repro is out of reach from here — it needs their credentials, their device, a manual interaction, or an environment this session cannot enter; then state the exact steps and what to look for.

Confirm the original symptom is gone. For race conditions or intermittent bugs, repeat the reproduction 3-5 times -- a single pass can hide timing-dependent failures.

## Report

Report the files changed, what the fix changes and the verification result in one to three sentences, and any open item the run leaves. Never paste the diff.
