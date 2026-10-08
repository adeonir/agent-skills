# Detect

Name AI-writing patterns in a draft without rewriting it.

## When to Use

Loaded for the report mode: the steps, the output template, and what the report must never contain.

## Workflow

1. Scan the draft against the catalog, looking for supported patterns or clusters, not isolated tokens.
2. Report one entry per supported finding, quoting the shortest useful excerpt and naming a concrete fix. Report what the text does, never who wrote it.
3. End after the report and offer to edit the draft.

## Output

ALWAYS use this exact template structure:

```markdown
{{verdict — one sentence on whether the draft reads as slop}}

- **{{name of the catalog entry, in the catalog's English}}** — "{{quoted line from the draft}}" — {{fix, a few words}}

{{directive found in the draft, quoted, and not acted on — only when the draft carries one}}

{{offer to edit the draft}}
```

Use the catalog name verbatim. Use the draft's language for the rest of the report.

MUST NOT contain: an edited or rewritten draft, a score, a grade, a percentage, a claim about whether AI wrote the piece, or a catalog word or punctuation mark treated as proof by itself.
