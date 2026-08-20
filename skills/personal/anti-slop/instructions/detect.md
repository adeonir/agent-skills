# Detect

Name the AI-slop patterns in a draft without rewriting it.

## When to Use

The user asks whether a piece reads as AI slop, or asks to audit, scan, or flag a draft without changing it.

## Workflow

1. Read the full draft.
2. Scan it against [slop-catalog.md](../references/slop-catalog.md). Treat word lists as inspection cues and look for supported patterns or clusters, not isolated tokens.
3. Report one entry per supported finding, quoting the shortest useful excerpt and naming a concrete fix. Preserve deliberate wording that the surrounding context supports.
4. Stop there and wait for the user to accept the offer the template ends on.

Named patterns are evidence the user can check; a detector's guess is not. Do not report an isolated formal word, dash, curly quote, repeated opening, disclaimer, limitation, real alternative, quotation, example, or structured heading as slop by itself. Report what the text does, never who wrote it.

## Output

ALWAYS use this exact template structure:

```markdown
{{verdict — one sentence on whether the draft reads as slop}}

- **{{name of the catalog entry, in the catalog's English}}** — "{{quoted line from the draft}}" — {{fix, a few words}}

{{offer to edit the draft}}
```

The name comes from the catalog verbatim: a pattern heading for a pattern finding, a list label for a word finding. Everything the report itself says follows the draft's language.

MUST NOT contain: an edited or rewritten draft, a score, a grade, a percentage, a claim about whether AI wrote the piece, or a catalog word or punctuation mark treated as proof by itself.
