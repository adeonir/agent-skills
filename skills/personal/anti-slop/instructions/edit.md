# Edit

Rewrite a draft into sharper, more human prose with the minimum effective edit.

## When to Use

The user shares a draft to fix, or asks for writing that is clearer, more direct, more opinionated, or less AI-sounding.

## Workflow

1. Read the full draft before changing anything.
2. Classify the register and output mode. In file mode, mark code, data, frontmatter, links, identifiers, and structural elements as protected.
3. Identify the core point and 3-5 voice signals worth preserving — vocabulary, cadence, bluntness, humor, uncertainty, digressions, level of polish. A supplied writing sample has priority. Keep this note internal; it never reaches the output. If the core point is not identifiable, ask the user.
4. Apply [editing-principles.md](../references/editing-principles.md) and cut what [slop-catalog.md](../references/slop-catalog.md) names. Treat word lists as inspection cues, not bans. Change the least that fixes the draft.
5. Check the edited draft against [self-check.md](../references/self-check.md) directly — one pass, no separate editor and evaluator agents.
6. Any check that fails: fix the draft, then run the checks again.
7. Return the output below.

Reorganize only when the structure hurts meaning or reading. Do not merge or split procedural steps, requirements, headings, or references merely for polish; when structure changes, explain why in What changed when a change log is part of the output.

## Output

A pasted draft comes back whole in the reply. A draft read from a file path is written back to that file, and the reply carries the What changed section alone. Embedded text comes back as final text only, without a preamble or change log.

Use this exact template for pasted and file modes:

```markdown
{{full edited draft — complete, never an excerpt or a diff; omitted when the draft was edited in its own file}}

## What changed

- {{pattern or principle}} — {{what was cut or rewritten, one line}}
```

Embedded mode returns only the final text and does not use this template.

MUST NOT contain: a slop score or grade, a verdict on whether AI wrote the draft, a kicker line rewritten instead of deleted, a claim the draft does not support, added personality in neutral technical or factual prose, or changes to protected file content or link targets.
