# Investigation Workflow

Investigate bugs, find root causes with confidence scoring, and propose minimal fixes.

## When to Use

When debugging unexpected behavior, silent errors, or intermittent failures.

## Phases Overview

You operate in phases 1, 3, and 4 of the debugging workflow:

| Phase | Purpose |
|-------|---------|
| 1. Investigate | Analyze code, find root cause |
| 3. Propose Fix | Suggest minimal correction |
| 4. Verify | Confirm fix worked |

## Phase 1: Investigate

### Step 1: Understand the Bug

Based on user's description, identify:

- Symptoms and error messages
- When/how the bug occurs
- Recent changes that might have introduced it

### Step 2: Analyze Code

Use available runtime inspection, browser debugging, semantic analysis, and documentation tools
to investigate the issue. The agent discovers and uses whatever tools are available in the environment.

#### Focus Areas

| Area | What to Look For |
|------|------------------|
| Error source | Stack traces, error messages, throw statements |
| Data flow | Where data originates, transforms, breaks |
| State | Mutations, race conditions, stale closures |
| Boundaries | API contracts, type mismatches, null checks |
| Timing | Async operations, event order, lifecycle |

### Step 3: Apply Confidence Scoring

Rate each finding 0-100:

| Score | Meaning | Action |
|-------|---------|--------|
| >= 70 | High (>= 70) | Report as probable cause |
| 50-69 | Medium (50-69) | Suggest logs to confirm |
| < 50 | Low (< 50) | Do not report |

### Step 4: Report Findings

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

If no root cause found with >= 70 confidence, load [log-injection.md](log-injection.md).

## Phase 3: Propose Fix

When root cause is confirmed, present:

````markdown
## Proposed Fix

**Confidence: {score}**

Root cause: {one sentence explanation}

```diff
// {file}:{line}
{diff showing the fix}
```
````

### Guidelines for Fixes

- Minimal change that resolves the issue
- No speculative fixes
- Include confidence score
- Ask user to approve before applying

## Phase 4: Verify

After user applies fix:

1. Ask user to reproduce the original bug
2. Confirm the fix worked
3. If not fixed, return to Phase 1 (investigate again)
4. If fixed, proceed to cleanup phase

## Guidelines

1. **Start from error** - trace backwards from symptoms
2. **One root cause** - focus on the most probable, not a list
3. **Score honestly** - don't inflate confidence
4. **Ask if stuck** - request logs or clarification
5. **Minimal fix** - smallest change that works
6. **No speculation** - only report findings >= 50

## Error Handling

- No stacktrace or error message: ask user for more details
- Cannot access source code: inform user and suggest alternatives
- Investigation inconclusive after analysis: suggest adding debug logs

## Task

Execute the appropriate phase based on current state:

- **Phase 1**: Investigate the bug described by the user
- **Phase 3**: Propose a fix for the confirmed root cause
- **Phase 4**: Verify the fix resolved the issue
