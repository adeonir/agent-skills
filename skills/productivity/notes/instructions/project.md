# Create Project Note

Create structured documentation for a project in the Obsidian vault.

## Load first

Read [mapping.md](../references/mapping.md) first — every path below depends on the entry its Project Lookup resolves — and [note-conventions.md](../references/note-conventions.md) for the filename, wikilink, and update rules.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Resolve the project entry
- [ ] Step 2: Gather the project info
- [ ] Step 3: Check for an existing note
- [ ] Step 4: Compose the note
- [ ] Step 5: Write the note
- [ ] Step 6: Report
```

**Step 1. Resolve the project.** Resolve the entry through mapping's Project Lookup. The entry's `name` is the project name, `obsidian.path` the folder, and `tags` the base tags. When `obsidian.path` is `--`, report that the entry skips project-folder writes and stop. Done when `name`, `obsidian.path`, and `tags` are known, or the stop is reported.

**Step 2. Gather.** Gather a brief summary (1-2 sentences) and the tech stack. Done when both are known.

**Step 3. Check for an existing note.** The note lives at `<obsidian.path>/<name>/<name> Overview.md`; the filename stays unique across the vault so wikilinks resolve.

```text
Obsidian:search_notes query="Checkout Refactor Overview" path="<obsidian.path>/"
```

If the note exists, ask whether to append, choose a new name, or cancel. Done when the target path is free, or the user chose.

**Step 4. Compose.** Fill the template below. The context prose and `## Goals` are required; include every other section only when the user mentions relevant content. Done when no slot is left unfilled.

**Step 5. Write.** Create the note with `Obsidian:write_note`. Done when the write returned success.

**Step 6. Report.** Report as note-conventions.md "Reporting the Note" states. Done when the report carries the path and the summary.

## Template

ALWAYS use this exact template structure:

````markdown
---
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
status: active
stack:
  - [technology]
tags:
  - project
  - [base tags from the entry]
  - [tags derived from the content]
---
# [Project Name] Overview

[What this project is, why it exists, what problem it solves. Include the constraints, trade-offs, and context that shaped the approach — enough that someone reading this note later understands the full picture without needing to ask.]

## Goals

- [goal 1]
- [goal 2]

## Learnings

- [what worked well]
- [what didn't work]
- [what to remember next time]

## Observations

- #decision [key technical or product decision]
- #stack [technology choice and rationale]
- #risk [known risk or concern]

## Relations

- [[Related Note]]
````
