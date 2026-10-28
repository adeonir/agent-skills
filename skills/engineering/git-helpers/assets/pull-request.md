Here is a sensible default format, but use your best judgment:

```markdown
## Summary

[Short explanation with the smallest visual that makes the key point clear.]

## Changes

- [Meaningful change in imperative mood.]

## Evidence

- `[Reproducible command or step]`
  **Before:** [Observed output or failing test; state if not captured.]
  **After:** [Observed output or passing test; state if not captured.]

## Merge risk

**Door:** [one-way | two-way]

[Optional explanation of reversibility.]

**Blast Radius:** [One-word scope.]

[Optional ramifications of merging.]

Closes #[issue-number]
```

Keep Summary. Omit other sections and the closing reference when they do not apply.

MUST NOT contain: invented execution results, missing-screenshot placeholders, session narrative, rejected alternatives, future tasks, release plans, roadmap references, or attribution lines.
