# Output Template

The strict report format for a reliability analysis.

## When to Use

Step 7 of the analysis, to format the final report. Loaded alongside SKILL.md.

## Template

ALWAYS use this exact template structure:

```text
## <Skill Name>: Reliability Analysis

### Trigger reliability: <Clean | Leaky | Narrow>
<does it fire on the right requests; note any description rewrite and its held-out re-test result>

### Workflow: <filename> — N steps

| Step | Nature | Baseline | Risk |
|------|--------|----------|------|
| 1. <name> | deterministic | ~99% | low |
| 2. <name> | generation (free-form) | ~82% | high |

End-to-end: ~99% × … × ~82% ≈ X% (<tier>)

### Full chain (if chained): M total steps

End-to-end: <Wa> × <Wb> × … ≈ Y% (<tier>)

### Top Variance Points

**1. <workflow> Step N — <name>** · Risk: <low|medium|high> · ~<current> → ~<target>
- Failure mode: <concrete bad output, not "it varies">
- Why it varies: <nature + internal complexity>
- Lever: <scripts / idempotence / explicit I/O>
- Suggestion: <concrete fix, or a ready-to-paste description rewrite>
- Expected gain: <baseline shift and its effect on the workflow product>

**2. ...**

**3. ...**

### Verification plan
For each change above, how to confirm it worked:
- <change> → <re-run / check> → <success looks like> → <next if it fails>

### Summary
<2–3 sentences on where to focus for the highest reliability gain>
```

Exclude the apply step (Step 8) from this printed template.
