# Investigation Workflow

Investigate bugs, find root causes with confidence scoring, and propose minimal fixes.

## When to Use

When debugging unexpected behavior, silent errors, or intermittent failures.

## Workflow

Execute the appropriate step based on current state: Understand + Analyze, Propose Fix, or Verify.

### Step 1: Understand the Bug

Based on user's description, identify:

- Expected behavior vs actual behavior (the gap to close)
- Symptoms and error messages
- Reproduction steps (exact sequence that triggers the bug)
- Frequency: deterministic, intermittent, or load-dependent
- Recent changes that might have introduced it

If the user did not state expected vs actual or reproduction steps, ask before analyzing. Diagnosis built on assumed behavior wastes attempts.

### Step 2: Analyze Code

Use available runtime inspection, browser debugging, semantic analysis, and documentation tools to investigate the issue. The agent discovers and uses whatever tools are available in the environment.

#### Focus Areas

| Area | What to Look For |
|------|------------------|
| Error source | Stack traces, error messages, throw statements |
| Data flow | Where data originates, transforms, breaks |
| State | Mutations, race conditions, stale closures |
| Boundaries | API contracts, type mismatches, null checks |
| Timing | Async operations, event order, lifecycle |
| Regression | Diff against last working commit, git log/blame on suspect lines, recent dependency upgrades |

#### Pattern Comparison

When the root cause is unclear, compare broken code against working examples:

1. Find similar code in the project that works correctly
2. Diff the working version against the broken one
3. Focus on structural differences (argument order, missing steps, different patterns)
4. Check if a recent change broke a previously working pattern

See [debugging-patterns.md](debugging-patterns.md) for common patterns and comparison guidance.

### Step 3: Enumerate Hypotheses

Generate 2-3 candidate root causes from the analysis. Multiple hypotheses up front prevent premature commitment to the first plausible explanation. Score each one 0-100:

| Score | Meaning | Action |
|-------|---------|--------|
| >= 70 | High (>= 70) | Report as probable cause |
| 50-69 | Medium (50-69) | Suggest logs to confirm |
| < 50 | Low (< 50) | Keep as alternative, do not report |

If only one hypothesis is plausible, that is fine -- do not invent weak alternatives to fill the slate. The goal is honest enumeration, not three items.

### Step 4: Report Findings

Rank hypotheses by score, highest first. The top candidate drives the next action; lower-scored ones stay as fallbacks if the leading theory is disproven.

**Probable cause (>= 70):**

```markdown
**[85] Login fails silently on expired token**

- File: auth.ts:42
- Evidence: catch block swallows TokenExpiredError without updating UI state
- Fix: Add error state update in catch block to show login form
```

**Need runtime data (50-69):**

```markdown
**[60] Possible race condition in session refresh**

- File: session.ts:18
- Need: Execution order of refresh vs. redirect calls
- Suggest: Inject logs at session.ts:18, session.ts:25, redirect.ts:10
```

**Multiple hypotheses example:**

```markdown
1. **[75] Stale closure in retry handler** -- file: retry.ts:22, evidence: deps array missing `attempt`
2. **[55] Race between cache write and read** -- file: cache.ts:48, need: ordering of write/read calls
3. **[40] Network flakiness** -- low, kept as fallback
```

If no hypothesis reaches >= 70 confidence, load [log-injection.md](log-injection.md) to gather runtime evidence and re-rank.

### Step 5: Propose Fix

**Gate:** Root cause must be confirmed at ≥70 confidence before any fix is proposed. Below that threshold, gather more evidence first — load [log-injection.md](log-injection.md). Never propose a fix as exploration.

When root cause is confirmed, present:

````markdown
## Proposed Fix

**Confidence: {score}**

Root cause: {one sentence explanation}

```diff
// {file}:{line} {diff showing the fix}
```
````

Fix guidelines:

- Minimal change that resolves the issue
- No speculative fixes
- Include confidence score
- Ask user to approve before applying

### Step 6: Verify

After user applies fix:

1. Provide explicit reproduction steps for the user to run
2. Ask user to reproduce the original bug
3. For race conditions or intermittent bugs, ask user to reproduce 3-5 times -- a single pass can hide timing-dependent failures
4. Confirm the fix worked
5. If not fixed, return to Step 1 (investigate again with new evidence)
6. If fixed, clean up debug logs (load [log-cleanup.md](log-cleanup.md))

## Fix Attempt Tracking

Track each fix attempt. After 3 failed fixes, escalate:

| Attempt | Action |
|---------|--------|
| 1 | Apply fix based on investigation |
| 2 | Reassess with new evidence, try different approach |
| 3 | Last attempt with deeper analysis |
| 4+ | Escalate to architectural review |

Escalation means: stop fixing symptoms and re-examine the broader design. Present the user with an architectural assessment:

- What was tried and why it failed
- Whether the issue is systemic (wrong abstraction, missing layer, flawed assumption)
- Suggested architectural changes to resolve the root cause

## Red Flags

Signals that the debugging process has gone off-track:

- Fixing the same symptom in multiple places
- Each fix introduces a new bug
- The "root cause" keeps changing
- Changes grow larger with each attempt
- Confidence score drops between attempts

When red flags appear, stop and reassess. The issue may be architectural, not a localized bug.

## Guidelines

**DO:**
- Start from the error and trace backwards from symptoms
- Enumerate 2-3 ranked hypotheses, then converge on the highest-scored one
- Score honestly -- don't inflate confidence
- Compare broken code against working examples when root cause is unclear
- Request logs or clarification when stuck
- Apply the smallest fix that resolves the issue
- Track fix attempts and escalate after 3 failures

**DON'T:**
- Report findings with confidence below 50 (contrasts: honest scoring)
- Commit to the first plausible cause without alternatives (contrasts: enumerate 2-3 ranked hypotheses)
- Propose speculative fixes without evidence (contrasts: smallest fix once root cause confirmed)
- Inflate confidence to skip log injection (contrasts: request logs when stuck)
- Retry the same approach after it fails (contrasts: track attempts and escalate)

## Error Handling

- No stacktrace or error message: ask user for more details
- Cannot access source code: inform user and suggest alternatives
- Investigation inconclusive after analysis: suggest adding debug logs
- Three failed fixes: escalate to architectural review
