# Detect

Name AI-writing patterns in a draft without rewriting it.

## When to Use

Loaded for the report mode: the steps, the output template, and what the report must never contain.

## Workflow

1. Read the full draft.
2. Scan it against [slop-catalog.md](slop-catalog.md). Treat word lists as inspection cues and look for supported patterns or clusters, not isolated tokens.
3. Report one entry per supported finding, quoting the shortest useful excerpt and naming a concrete fix. Preserve deliberate wording that the surrounding context supports.
4. End after the report and offer to edit the draft.

Report evidence the user can check, not a detector's guess. Do not report an isolated formal word, dash, curly quote, repeated opening, disclaimer, limitation, real alternative, quotation, example, or structured heading as slop by itself. Report what the text does, never who wrote it.

## Output

Use this exact template:

```markdown
{{verdict — one sentence on whether the draft reads as slop}}

- **{{name of the catalog entry, in the catalog's English}}** — "{{quoted line from the draft}}" — {{fix, a few words}}

{{offer to edit the draft}}
```

Use the catalog name verbatim. Use the draft's language for the rest of the report.

MUST NOT contain: an edited or rewritten draft, a score, a grade, a percentage, a claim about whether AI wrote the piece, or a catalog word or punctuation mark treated as proof by itself.
