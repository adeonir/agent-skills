# Debugging Patterns

Pattern comparison against working code, and regression tracing.

## When to Use

When investigation stalls and broken code has to be diffed against a working example, or when the user reports that something used to work.

## Pattern Comparison

Compare the broken code against similar code in the project that works, to spot where it diverges.

### How to Compare

1. **Find working examples** - search the codebase for similar functionality that works correctly (same API calls, same component patterns, same data flow)
2. **Diff structurally** - compare the working and broken code side by side, focusing on structure rather than variable names
3. **Check for divergence** - identify where the broken code deviates from the working pattern

### What to Look For

| Difference | Common Cause |
|------------|-------------|
| Missing step in sequence | Skipped initialization, missing middleware |
| Different argument order | API changed, wrong overload |
| Missing error handling | Catch block absent, no fallback |
| Different import/version | Breaking change in dependency |
| Extra/missing await | Async bug, unhandled promise |
| Different config shape | Schema mismatch, missing field |

## Regression Tracing

When the user reports "this used to work", treat the change history as primary evidence. The bug is somewhere in the diff between the last known good state and now.

### Checklist

1. **Confirm the last working state** -- ask the user when it last worked (commit, release, date)
2. **Inspect git log on the suspect area** -- list commits touching the relevant files since that point
3. **Diff against the last working commit** -- focus on logic changes, not formatting
4. **Check dependency changes** -- review `package.json`, `lockfile`, or equivalents for upgrades in the same window
5. **Bisect when the suspect range is wide** -- `git bisect` narrows it to a single commit when manual diffing is too noisy

### What to Compare

| Source | What to Look For |
|--------|------------------|
| Code diff | Logic changes, removed branches, signature changes |
| Lockfile diff | Major/minor version bumps, transitive shifts |
| Config diff | Env vars, build flags, feature flags toggled |
| Test diff | Tests removed or weakened around the affected area |

The output of regression tracing feeds back into the hypothesis ranking -- a recent commit that touches the failing path is strong evidence and should score above generic theories.
