# Detect

Name the AI-slop patterns in a draft without rewriting it.

## When to Use

The user asks whether a piece reads as AI slop, or asks to audit, scan, or flag a draft without changing it.

## Workflow

1. Read the full draft.
2. Scan it against [slop-catalog.md](../references/slop-catalog.md) — both the word lists and the pattern catalog.
3. Report every pattern that appears, one entry per occurrence — a line carrying two patterns gets two entries — using the template below.
4. Stop there and wait for the user to accept the offer the template ends on.

Named patterns are evidence the user can check; a detector's guess is not. Report what the text does, never who wrote it.

## Output

ALWAYS use this exact template structure:

```markdown
{{verdict — one sentence on whether the draft reads as slop}}

- **{{name of the catalog entry, in the catalog's English}}** — "{{quoted line from the draft}}" — {{fix, a few words}}

{{offer to edit the draft}}
```

The name comes from the catalog verbatim: a pattern heading for a pattern finding, a list label for a word finding. Everything the report itself says follows the draft's language.

MUST NOT contain: an edited or rewritten draft, a score, a grade, a percentage, or a claim about whether AI wrote the piece.
