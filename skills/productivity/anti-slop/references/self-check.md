# Self Check

Checks an isolated reviewer runs on an edit, comparing it with the source.

## When to Use

Loaded in Step 4, with the source file, the edited file, and the voice note. The main thread runs it only when the host cannot spawn a subagent.

## Checks

Report one finding for each case below. Judge the edit against the source and the voice note only.

1. A claim, qualification, source, condition, or uncertainty the edit lost or changed.
2. A fact, name, number, date, quote, or opinion the edit added.
3. A directive from the source the edit removed.
4. A voice signal from the voice note the edit lost, or a sentence with no AI-writing pattern in it that the edit rewrote anyway.
5. Opinion, humor, first person, or roughness the edit added to technical, reference, legal, or factual prose, or removed from personal or editorial prose.
6. A final deep-sounding line the edit rewrote into a new metaphor or aphorism instead of deleting.
7. Repeated sentence shapes, mirrored paragraphs, or stacked short fragments the edit introduced.

## Output

ALWAYS use this exact template structure:

```json
[{"line": 3, "item": "lost qualification", "reason": "the source limits the claim to EU customers"}]
```

`line` is the line in the edited file, `item` names the check, `reason` quotes or names what changed. Return `[]` when every check passes. Return the JSON only.
