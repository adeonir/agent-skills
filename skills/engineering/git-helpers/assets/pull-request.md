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

<!-- Before screenshot: [screen or state] -->
<!-- After screenshot: [screen or state] -->

## Merge risk

**Door:** [one-way | two-way]

[Optional explanation of reversibility.]

**Blast Radius:** [One-word scope.]

[Optional ramifications of merging.]

Closes #N
```

Keep Summary. Omit other sections and the closing reference when they do not apply. Keep a screenshot comment only for a missing screenshot of a UI change.

The `Closes #N` line is for a GitHub tracker only — it closes the issue on merge. On a Linear tracker the issue completes through the id in the branch name, so end the Summary instead with `Spec: [issue-id]` (URL when known) linking the issue whose acceptance criteria the reviewer verifies.

MUST NOT contain: invented execution results, visible missing-screenshot placeholders, session narrative, rejected alternatives, future tasks, release plans, roadmap references, or attribution lines.
