---
name: brainstorming
description: >-
  Structured idea exploration from vague to direction, or stress-test of
  an existing plan. Two paths: standard (vague idea, adaptive deepening)
  and relentless (existing plan, pressure-test before building). Diverge
  generates alternatives, converge evaluates trade-offs, capture produces
  the artifact. Use when ideas are vague, multiple directions exist, or
  the user wants to pressure-test a plan. Triggers: "brainstorm",
  "explore ideas", "what should we build", "explore options", "think
  through this", "compare approaches", "stress-test this", "grill me on
  this plan". Not for formalizing an already-chosen direction.
argument-hint: "[deep]"
---

# Brainstorming

Structured idea exploration from vague to direction.

## Workflow

```
trigger --> detect path --> discover --> diverge --> converge --> capture
              ^________________________________|  (if no viable direction)
```

Detect path from entry state (standard for vague ideas, relentless for
existing plans). Discover maps the problem space. Diverge generates
alternatives. Converge evaluates trade-offs and picks a direction. Capture
produces the artifact.

## Triggers

- **Vague idea / open exploration** ("brainstorm", "explore ideas",
  "what should we build", "think through this") →
  [discovery.md](references/discovery.md) (standard path)
- **Existing plan / pressure-test** ("stress-test this", "grill me on
  this plan", `/brainstorming deep`) →
  [discovery.md](references/discovery.md) (relentless path)
- **Generate alternatives** (loaded after discovery completes) →
  [diverge.md](references/diverge.md)
- **Evaluate and decide** (loaded after diverge produces ≥4 options) →
  [converge.md](references/converge.md)

The full workflow always starts with discovery regardless of trigger.
Load each subsequent reference only when its phase begins.

## Guidelines

- Generate at least 4 alternatives during diverge, including non-obvious
  options
- Challenge every alternative with trade-offs during converge
- Require explicit user approval before capturing the direction
- Mark unknowns as TBD rather than inventing constraints
- Stay at the problem-and-direction level; defer implementation choices

## Anti-Pattern: Premature Convergence

Stopping at 2-3 obvious alternatives skips the value of brainstorming.
The non-obvious option is often the one worth choosing — or the one that
reframes the problem. When pressure to commit shows up early, push for
breadth first; converge only after the space has been explored.

## Anti-Pattern: Hidden Trade-offs

Recommending a direction without surfacing what it costs misleads the
user. Every recommendation must name the gain and the give-up explicitly.
If a trade-off feels too small to mention, it probably isn't.

## Anti-Pattern: Solution-First Discovery

When the user describes what to build before why, discovery has not
happened — they have a hypothesis. Redirect to the problem before
generating alternatives. Without grounded motivation, diverge produces
options for an unverified target.
