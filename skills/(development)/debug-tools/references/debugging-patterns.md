# Debugging Patterns

Quick-reference for common bug patterns, pattern comparison, and debugging decision-making.

For framework-specific log examples, see [log-injection.md](log-injection.md).

## When to Use

When looking up common bug patterns, pattern comparison techniques, or confidence
scoring guidelines. Also loaded during investigation when pattern comparison is needed.

## Common Bug Patterns

| Pattern | Symptom | Check |
|---------|---------|-------|
| Null access | "Cannot read property X of undefined" | Optional chaining, defaults |
| Race condition | Works sometimes, fails randomly | Async ordering, state timing |
| Stale closure | Using old values in callbacks | useCallback deps, event bindings |
| API mismatch | Data not displaying | Response shape, null handling |
| Silent error | Nothing happens | Empty catch blocks, missing error state |
| Infinite loop | App freezes | Dependency arrays, state updates |
| Memory leak | Performance degrades over time | Event listeners, subscriptions |
| Timing issue | Works in dev, fails in prod | Timing assumptions, async/await |

## Pattern Comparison

When investigation stalls, compare broken code against working examples to spot
the difference. This technique is effective for bugs introduced by recent changes
or when similar code elsewhere works correctly.

### How to Compare

1. **Find working examples** - search the codebase for similar functionality that
   works correctly (same API calls, same component patterns, same data flow)
2. **Diff structurally** - compare the working and broken code side by side,
   focusing on structure rather than variable names
3. **Check for divergence** - identify where the broken code deviates from the
   working pattern

### What to Look For

| Difference | Common Cause |
|------------|-------------|
| Missing step in sequence | Skipped initialization, missing middleware |
| Different argument order | API changed, wrong overload |
| Missing error handling | Catch block absent, no fallback |
| Different import/version | Breaking change in dependency |
| Extra/missing await | Async bug, unhandled promise |
| Different config shape | Schema mismatch, missing field |

### When to Use Pattern Comparison

- Root cause confidence is below 70 after initial analysis
- The bug appeared after a change to working code
- Similar code in the project works correctly
- The error suggests a contract or interface mismatch

## Confidence Scoring Reference

See [investigation.md](investigation.md) for the full confidence scoring table.

## Tool Integration

Use available debugging tools (runtime inspection, browser devtools, semantic analysis,
documentation lookup) to enhance the debugging process. The agent discovers and adapts
to whatever tools are available in the environment.

## When to Debug vs When NOT to

**Use debug-tools:**

- Unexpected behavior
- Silent errors
- Intermittent failures
- Issues requiring runtime data

**Don't use debug-tools:**

- Syntax errors (linter resolves)
- Type errors (TypeScript resolves)
- Obvious bugs in diff (use code review)

## Error Handling

- Pattern doesn't match framework: adapt the pattern to the specific framework conventions
- No matching pattern found for the symptom: fall back to general investigation with debug logs
- Multiple patterns match the same symptom: use confidence scoring to prioritize the most likely cause
