# Diverge -- Generate Alternatives

Explore the space broadly. Quantity over quality. Non-obvious options matter
more than safe ones.

## When to Use

After discovery quality gate passes. Loaded automatically as second phase.

## Workflow

Breadth over depth. Generate at least 4 alternatives, aim for 6-8. Include at
least one non-obvious or uncomfortable option. Separate generation from
evaluation -- no judging during diverge.

### Techniques

Select 3-4 techniques relevant to the problem. Not every technique applies to
every brainstorm.

#### Constraint Removal

Remove one constraint at a time and ask: "What would we do if X was not a
limitation?"

Generates options that might be partially achievable even with the constraint
back in place. Reveals where constraints are artificially narrowing the space.

#### Analogy Exploration

Look at how other industries, domains, or products solve similar problems.

Ask: "How does [industry Y] handle [problem X]?" Transfer patterns from one
domain to another. Works best when the user is stuck in familiar territory.

#### Inversion

Ask: "What is the opposite approach? What if we did the exact reverse?"

Often reveals hidden assumptions about the "right" way. Generates alternatives
that challenge the default direction.

#### Decomposition

Break the problem into smaller sub-problems.

Ask: "Can we solve a smaller version first? What is the minimum viable
experiment?" Useful when the scope feels overwhelming or when no single
approach covers everything.

#### Extreme Positions

Push to extremes: "What if we went all-in on X? What if we completely
ignored Y?"

Reveals the spectrum and helps identify where the sweet spot might be.
Works best for trade-off-heavy problems.

#### Status Quo Plus

Ask: "What if we just improved what exists? What is the least disruptive change?"

Important to include as a baseline alternative. Often underrated because it
lacks novelty, but sometimes the right answer is incremental improvement.

### Alternative Capture Format

Capture each alternative as it emerges:

```markdown
**{Name}** -- {one-sentence description}
Technique: {which technique generated it}
Key assumption: {what must hold for this to work}
```

No evaluation yet. That happens in converge.

### Minimum Bar

Before advancing to converge:

| Requirement | Why |
|-------------|-----|
| At least 4 distinct alternatives | Ensures the space is explored, not just the obvious |
| At least 1 non-obvious option | From constraint removal, inversion, or analogy |
| At least 1 uncomfortable option | Challenges assumptions about what is acceptable |
| Status quo or incremental option | Provides a baseline for comparison |

If fewer than 4 alternatives: apply unused techniques before advancing.

## Guidelines

**DO:**
- Separate generation from evaluation completely
- Include the status quo or do-nothing option
- Push past the first 2-3 obvious ideas
- Name each alternative for easy reference in converge
- Select techniques based on problem type, not mechanically

**DON'T:**
- Evaluate or dismiss during diverge
- Settle for only 2-3 alternatives
- Only generate safe or obvious options
- Combine alternatives prematurely (that happens in converge)
- Apply all 6 techniques every time (select the relevant ones)

## Error Handling

- User wants to skip to a specific solution: warn that brainstorming value
  comes from exploring alternatives, suggest docs-writer if they already have
  a direction
- Alternatives feel too similar: apply inversion or constraint removal to
  generate genuinely different options
- Problem is too narrow for 4 alternatives: check if the problem is too
  specific -- consider broadening scope or decomposing differently

## Next Steps

Load [converge.md](converge.md) to evaluate alternatives.

## Task

Generate alternatives using selected techniques. Capture each with a name,
description, technique, and key assumption. Reach the minimum bar before
advancing to converge.
