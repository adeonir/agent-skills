---
name: brainstorm
description: "Idea exploration from a blank problem space or stress-testing an existing plan before building. Use when comparing approaches, finding gaps, reconsidering a direction, or weighing a pivot. Not for documenting a finalized direction."
---

# Brainstorm

Structured idea exploration from vague to direction, in two entries — **greenfield** from a blank problem space, **grill** against an existing idea or plan.

## Triggers

- **Greenfield entry** ("brainstorm this", "explore options", "compare approaches", "help me think through X") → run the workflow below
- **Grill entry** ("pressure-test this plan", "find holes in this", "second opinion", "grill my assumptions", "considering a pivot") → run the workflow below

The `deep` argument (`/brainstorm deep`) widens the grill on either entry — every assumption instead of the key one.

## Workflow

```text
trigger → detect entry → discover → diverge → converge → grill → capture
              ^_______________________________________________|
                         (hole found / no viable direction)
```

1. **Detect the entry from state.** Greenfield when no concrete idea is present; grill when an idea or plan exists, regardless of its maturity. Both run the same chain — they differ in when the grill starts, not whether it runs.
2. **Load [discovery.md](references/discovery.md)** and map the problem space. On greenfield, a description of what to build is a hypothesis, not a direction: redirect to the problem before generating alternatives, because without grounded motivation diverge produces options for an unverified target. On grill entry the solution is the input by definition — do not redirect; map the assumptions, dependencies, and signals behind the existing plan so diverge can attack from grounded vectors.
3. **Load [diverge.md](references/diverge.md)** after the discovery gate and generate at least 4 alternatives, including non-obvious ones. Stopping at 2-3 obvious options skips the value of the exercise: the non-obvious option is often the one worth choosing, or the one that reframes the problem. When pressure to commit shows up early, push for breadth first. On grill entry, the existing plan enters here as a named baseline alternative.
4. **Load [converge.md](references/converge.md)** once 4+ alternatives exist. Evaluate trade-offs, pick a direction, and name the gain and the give-up of every recommendation — a direction recommended without its cost misleads the user, and a trade-off that feels too small to mention usually is not. Then grill the chosen direction: standard hits the key assumption, `deep` hits every one.
5. **Return to step 3** when the grill opens a hole or leaves no viable direction.
6. **Load [capture.md](references/capture.md)** only after the direction survives the grill, and only with explicit user approval to capture it.

## Guidelines

- Mark unknowns as TBD rather than inventing constraints
- Stay at the problem-and-direction level; defer implementation choices
