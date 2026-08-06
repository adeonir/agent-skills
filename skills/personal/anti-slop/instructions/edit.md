# Edit

Rewrite a draft into sharper, more human prose with the minimum effective edit.

## When to Use

The user shares a draft to fix, or asks for writing that is clearer, more direct, more opinionated, or less AI-sounding.

## Workflow

1. Read the full draft before changing anything.
2. Identify the core point and 3-5 voice signals worth preserving — vocabulary, cadence, bluntness, humor, uncertainty, digressions, level of polish. Keep this note internal; it never reaches the output. If the core point is not identifiable, ask the user.
3. Apply [editing-principles.md](../references/editing-principles.md) and cut what [slop-catalog.md](../references/slop-catalog.md) names. Change the least that fixes the draft.
4. Check the edited draft against [self-check.md](../references/self-check.md) directly — one pass, no separate editor and evaluator agents.
5. Any check that fails: fix the draft, then run the checks again.
6. Return the output below.

Reorganizing the draft is allowed when the structure hurts the piece; when it happens, the reason goes in What changed.

## Output

A pasted draft comes back whole in the reply. A draft read from a file path is written back to that file, and the reply carries the What changed section alone.

ALWAYS use this exact template structure:

```markdown
{{full edited draft — complete, never an excerpt or a diff; omitted when the draft was edited in its own file}}

## What changed

- {{pattern or principle}} — {{what was cut or rewritten, one line}}
```

MUST NOT contain: a slop score or grade, a verdict on whether AI wrote the draft, a kicker line rewritten instead of deleted, or a claim the draft does not support.
