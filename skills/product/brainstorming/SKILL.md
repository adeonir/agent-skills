---
name: brainstorming
description: >-
  Structured idea exploration from vague to direction, or pressure-test
  of an existing idea or plan. Two paths: greenfield maps a problem
  space from scratch; relentless stress-tests existing thinking to
  expose weakness, validate, refine, or surface a pivot. Diverge
  generates alternatives, converge evaluates trade-offs, capture
  produces the artifact. Use when brainstorming, exploring options,
  comparing approaches, rethinking a direction, considering a pivot,
  asking for a second opinion, finding holes in a plan, or grilling
  assumptions before building. Not for documenting a finalized
  direction.
argument-hint: "[deep]"
---

# Brainstorming

Structured idea exploration from vague to direction.

## Workflow

```
trigger → detect path → discover → diverge → converge → capture
              ^________________________________|  (if no viable direction)
```

Detect path from entry state — greenfield when no concrete idea is
present, relentless when an idea or plan exists regardless of
maturity. Discover maps the problem space. Diverge generates
alternatives. Converge evaluates trade-offs and picks a direction.
Capture produces the artifact.

## References

- Discovery (any entry) → [discovery.md](references/discovery.md)
- Diverge (after discovery gate) → [diverge.md](references/diverge.md)
- Converge (after 4+ alternatives) → [converge.md](references/converge.md)
- Capture (after user approves direction) → [capture.md](references/capture.md)

Workflow always starts with discovery. Load each reference when its
phase begins.

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

In greenfield, when the user describes what to build before why,
discovery has not happened — they have a hypothesis. Redirect to the
problem before generating alternatives. Without grounded motivation,
diverge produces options for an unverified target.

In relentless, the solution is the input by definition. Do not
redirect — discovery maps the assumptions, dependencies, and signals
behind the existing idea or plan so diverge can attack from grounded
vectors.
