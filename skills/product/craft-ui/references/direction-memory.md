# Direction Memory

The append-only log of the directions each surface already spent, and the line that records a chosen one.

## When to Use

Loaded before setting the directions for a round and before marking one chosen: it settles which directions are spent and how the choice is written down.

## The log

The directions this project already spent live in `.artifacts/design/VARIANTS.md` — append-only, one line per direction generated, grouped by surface.

ALWAYS use this exact template structure:

```markdown
## {{surface}} · {{brand | product}}

- {{direction}} — **chosen**: {{what the choice turned on}}
- {{direction}}
```

A direction already listed under a surface does not come back. One marked **chosen** may return when the surface is being extended rather than re-explored. A surface with no section yet has no history.

The reason on the chosen line is what a later round cannot reconstruct from the direction name alone. Write the property that won, in one clause — "the only one where the pricing table stayed readable at three tiers". A round that reopens a settled look reads this line first.

When the directions were compared inside the running application, the chosen line also names the branch that holds the experiment, after the reason:

```markdown
- {{direction}} — **chosen**: {{what the choice turned on}} (branch experiment/{{surface}})
```

MUST NOT contain: an arrangement, a block name, token values, copy strings, a review of any direction, or the exchange behind a pick ("the user preferred", "we went with", "as discussed"). The reason names what the choice turned on as a property of the direction, never how well a direction was executed and never why the others lost.
