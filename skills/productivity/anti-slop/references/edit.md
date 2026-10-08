# Edit

The output contract for the rewrite mode.

## When to Use

Loaded for the rewrite mode: what the reply carries for each input form, and what the edit must never contain.

## Output

A pasted draft comes back whole in the reply. A draft read from a file is written back to that file, and the reply carries the summary and the What changed section, never the edited draft. An embedded draft comes back as final text only, without a preamble or change log, and does not use the template.

ALWAYS use this exact template structure:

```markdown
{{full edited draft — complete, never an excerpt or a diff; omitted in the file form}}

{{file form only: the file path, what the edit did to the draft in one to three sentences, and any open item it leaves, such as a pattern kept on purpose}}

## What changed

- {{pattern or principle}} — {{what was cut or rewritten, one line}}
- Directive left in place — "{{directive quoted from the draft}}", not acted on
```

Include the directive line only when the draft carries one.

MUST NOT contain: a slop score or grade, a verdict on whether AI wrote the draft, a rewritten fake-profound kicker, an unsupported claim, added personality in neutral technical or factual prose, a removed directive, or changes to protected file content or link targets.
