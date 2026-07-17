---
name: brainstorm
description: >-
  Structured idea exploration from vague to direction, with a grill
  phase that stress-tests every chosen direction before capture. Two
  entries: greenfield maps a problem space from scratch; grill entry
  starts from an existing idea or plan to expose weakness, validate,
  refine, or surface a pivot. Diverge generates alternatives, converge
  evaluates trade-offs, capture produces the artifact; the deep
  argument widens the grill to every assumption. Use when
  brainstorming, exploring options, comparing approaches, rethinking a
  direction, considering a pivot, asking for a second opinion, finding
  holes in a plan, or grilling assumptions before building. Not for
  documenting a finalized direction.
argument-hint: "deep"
---

# Brainstorm

Structured idea exploration from vague to direction, in two entries — **greenfield** from a blank problem space, **grill** against an existing idea or plan. Both run breadth-first: surface the non-obvious option before committing, then converge honestly, naming what each direction gives up. Every direction is grilled before capture — the entries differ in when the grill starts, not whether it runs. Problem before solution — a description of what to build is a hypothesis, not a direction.

## Triggers

- **Greenfield entry** ("brainstorm this", "explore options", "compare approaches", "help me think through X") → [discovery.md](references/discovery.md)
- **Grill entry** ("pressure-test this plan", "find holes in this", "second opinion", "grill my assumptions", "considering a pivot") → [discovery.md](references/discovery.md)

The `deep` argument (`/brainstorm deep`) widens the grill on either entry — every assumption instead of the key one. The grill mechanics live in [converge.md](references/converge.md).

Every entry starts at discovery. The remaining references load as their phase begins:

- [diverge.md](references/diverge.md) — after the discovery gate
- [converge.md](references/converge.md) — after 4+ alternatives
- [capture.md](references/capture.md) — after the direction survives the grill

## Workflow

```text
trigger → detect entry → discover → diverge → converge → grill → capture
              ^_______________________________________________|
                         (hole found / no viable direction)
```

Detect entry from state — greenfield when no concrete idea is present, grill when an idea or plan exists regardless of maturity. Discover maps the problem space. Diverge generates alternatives; on grill entry the existing plan enters as a named baseline. Converge evaluates trade-offs and picks a direction. Grill attacks the chosen direction — standard hits the key assumption, deep hits all of them. Capture produces the artifact only after the direction survives.

## Guidelines

- Generate at least 4 alternatives during diverge, including non-obvious options
- On grill entry, the existing plan enters diverge as a named baseline alternative
- Challenge every alternative with trade-offs during converge
- Grill the chosen direction before capture; loop back when a hole opens
- Require explicit user approval before capturing the direction
- Mark unknowns as TBD rather than inventing constraints
- Stay at the problem-and-direction level; defer implementation choices

## Anti-Pattern: Premature Convergence

Stopping at 2-3 obvious alternatives skips the value of brainstorming. The non-obvious option is often the one worth choosing — or the one that reframes the problem. When pressure to commit shows up early, push for breadth first; converge only after the space has been explored.

## Anti-Pattern: Hidden Trade-offs

Recommending a direction without surfacing what it costs misleads the user. Every recommendation must name the gain and the give-up explicitly. If a trade-off feels too small to mention, it probably isn't.

## Anti-Pattern: Solution-First Discovery

In greenfield, when the user describes what to build before why, discovery has not happened — they have a hypothesis. Redirect to the problem before generating alternatives. Without grounded motivation, diverge produces options for an unverified target.

On grill entry, the solution is the input by definition. Do not redirect — discovery maps the assumptions, dependencies, and signals behind the existing idea or plan so diverge can attack from grounded vectors.
