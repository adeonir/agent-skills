# Edit

Rewrite a draft into clear, natural prose with the smallest useful edit.

## When to Use

The user shares a draft to fix, or asks for writing that is clearer, more direct, more opinionated, or less AI-sounding.

## Workflow

1. Read the full draft before changing a sentence.
2. Classify the register and output mode. In file mode, mark code, data, frontmatter, links, identifiers, and structural elements as protected.
3. Identify the core point and 3-5 voice signals to preserve: words, rhythm, bluntness, humor, uncertainty, digressions, and level of polish. A supplied writing sample has priority. Keep this note internal. Ask the user if the core point is not clear.
4. Apply [editing-principles.md](../references/editing-principles.md) and the supported patterns in [slop-catalog.md](../references/slop-catalog.md). Treat word lists as cues, not bans. Make the smallest change that fixes the draft.
5. Check the edit against [self-check.md](../references/self-check.md). Run the check directly.
6. Fix each failed check and run the checks again.
7. Return the output below.

Reorganize only when the structure hurts meaning or reading. Do not merge or split procedural steps, requirements, headings, or references just for polish. Explain structural changes in What changed when the output has a change log.

## Output

A pasted draft comes back whole in the reply. A draft read from a file path is written back to that file, and the reply carries the What changed section alone. Embedded text comes back as final text only, without a preamble or change log.

Use this exact template for pasted and file modes:

```markdown
{{full edited draft — complete, never an excerpt or a diff; omitted when the draft was edited in its own file}}

## What changed

- {{pattern or principle}} — {{what was cut or rewritten, one line}}
```

Embedded mode returns only the final text and does not use this template.

MUST NOT contain: a slop score or grade, a verdict on whether AI wrote the draft, a rewritten fake-profound kicker, an unsupported claim, added personality in neutral technical or factual prose, or changes to protected file content or link targets.
