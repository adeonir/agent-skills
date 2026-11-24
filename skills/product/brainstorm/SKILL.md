---
name: brainstorm
description: "Idea exploration from a blank problem space or from an existing plan, before building. Use when comparing approaches, reconsidering a direction, or weighing a pivot. Not for documenting a finalized direction, stress-testing a plan, or settling open decisions one question at a time."
---

# Brainstorm

Explore an idea from vague to a direction, in two entries — **greenfield** from a blank problem space, **plan** from an existing idea or plan.

## Workflow

```text
trigger → detect entry → discover → diverge → converge → challenge → capture
              ^_________________________________________________|
                         (hole found / no viable direction)
```

The `deep` argument widens the challenge on either entry: every assumption instead of the key one.

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Detect the entry from state
- [ ] Step 2: Map the problem space
- [ ] Step 3: Diverge into at least 4 alternatives
- [ ] Step 4: Converge, then challenge the direction
- [ ] Step 5: Capture the direction
```

**Step 1. Detect the entry from state.** Greenfield when no concrete idea is present; plan when an idea or plan exists, regardless of its maturity. Both run the same chain — they differ in when the challenge starts, not whether it runs. Done when the entry is named.

**Step 2. Map the problem space.** Load [discovery.md](references/discovery.md) · the discovery gate that opens diverge. On greenfield, a description of what to build is a hypothesis, not a direction: redirect to the problem before generating alternatives, because without grounded motivation diverge produces options for an unverified target. On plan entry the solution is the input by definition — do not redirect; map the assumptions, dependencies, and signals behind the existing plan so diverge can attack from grounded vectors. Done when the problem space is mapped and the gate passes.

**Step 3. Diverge.** Load [diverge.md](references/diverge.md) · the generation method and its quality bar. Generate at least 4 alternatives, including non-obvious ones. When pressure to commit shows up early, push for breadth first. On plan entry, the existing plan enters here as a named baseline alternative. Done when 4 or more alternatives exist.

**Step 4. Converge and challenge.** Load [converge.md](references/converge.md) · the trade-off method and the challenge. Evaluate trade-offs, pick a direction, and name the gain and the give-up of every recommendation — a direction recommended without its cost misleads the user, and a trade-off that feels too small to mention usually is not. Then challenge the chosen direction: standard hits the key assumption, `deep` hits every one. Done when the direction survives the challenge; when the challenge opens a hole or leaves no viable direction, return to Step 3.

**Step 5. Capture.** Load [capture.md](references/capture.md) · the artifact shape and where it lives. Done when the direction is written and the entry it pivots or validates carries the result.

## Guidelines

- Mark unknowns as TBD rather than inventing constraints
- Stay at the problem-and-direction level; defer implementation choices
