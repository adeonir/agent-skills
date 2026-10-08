---
paths:
  - "skills/**/README.md"
---

## Fixed README Sections

**Impact: MEDIUM**

A skill README carries only these parts, in this order: the H1, a one-line tagline, `## What It Does`, `## Usage`, then the optional `## Output`, `## Requirements`, and `## FAQ`. Move any other section out: what a user of the skill needs becomes a FAQ entry, what describes the skill's internals stays in its instructions and references, and an attribution goes to a `CREDITS.md` in the skill folder.

**Incorrect:**

```markdown
## Usage
...
## References

`references/discovery.md` is loaded first by every operation...

## Credits

Inspired by ...
```

**Correct:**

```markdown
## Usage
...
## Requirements
...
## FAQ
...
```

## What It Does Shape

**Impact: MEDIUM**

`## What It Does` opens with the mermaid diagram, with no prose or list before it, and follows it with one table of two columns: the skill's own unit (`Phase`, `Mode`, `Operation`, `Note Type`) and `Output`. Fold a description or a third column into the `Output` cell instead of adding text around the table.

**Incorrect:**

```markdown
## What It Does

Creates notes across five note types:

| Phase | What Happens | Output |
```

**Correct:**

````markdown
## What It Does

```mermaid
...
```

| Note Type | Output |
````

## Self-Explanatory Usage Requests

**Impact: MEDIUM**

`## Usage` holds one `text` block of requests a user would type, one per line, with at least one request for each file in `instructions/`. Write each request so it explains itself, never with a comment after it; a request that needs a comment is rewritten. One sentence after the block is allowed only to state a condition of use.

**Incorrect:**

```text
map the screen flow      # wireframes — stops at the plan
decompose                -- run the ceremony
```

**Correct:**

```text
map the screen flow and stop at the plan
break this epic into stories and tasks
```

## README Title

**Impact: LOW**

The H1 is the `interface.display_name` from the skill's `agents/openai.yaml`, or the folder name in Title Case when that file is absent. The tagline under it states what the skill does without repeating the name.

**Incorrect:**

```markdown
# Wrap Up Session

wrap-up — end-of-session documentation to Obsidian.
```

**Correct:**

```markdown
# Wrap Up

End-of-session documentation to Obsidian.
```

## One-Line FAQ Entries

**Impact: LOW**

Write each FAQ entry as one paragraph, `**Q: <question>?** A: <answer>`, with the answer on the same line as the question.

**Incorrect:**

```markdown
**Q: Does load auto-clear the handoff?**

A: No. Load reads the handoff; clear is a separate explicit operation.
```

**Correct:**

```markdown
**Q: Does load auto-clear the handoff?** A: No. Load reads the handoff; clear is a separate explicit operation.
```
