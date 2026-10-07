# Update Brag Document

Add achievements to a brag document for performance reviews and career growth.

## Load first

Read [mapping.md](../references/mapping.md) for the vault root — this note writes to a fixed top-level folder — and [note-conventions.md](../references/note-conventions.md) for the filename, wikilink, and update rules.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Determine the period file
- [ ] Step 2: Gather the achievement
- [ ] Step 3: Compose the entry
- [ ] Step 4: Write the note
- [ ] Step 5: Report
```

**Step 1. Determine the period.** Search `Brags/` for the current year:

```text
Obsidian:search_notes query="YYYY" path="Brags/"
```

When quarter files (`YYYY Qn.md`) exist, use the current quarter's file; otherwise use the year file (`YYYY.md`). Use a quarter file for a new year only when the user asks for one. Done when the target filename is known and whether it exists.

**Step 2. Gather.** Gather what was accomplished, the context (project, team, situation), the result with a metric, and the category: Impact (business results, user metrics), Technical (architecture, performance, reliability), or Growth (learning, mentoring, new skills, feedback received). Done when each of the four is known.

**Step 3. Compose.** For a new file, fill the template below. For an existing file, compose the entry for its category section. If the entry has neither a metric nor the proxy the anti-pattern below allows, return to Step 2. Done when the entry carries one of them.

**Step 4. Write.** Create a new file with `Obsidian:write_note`. For an existing file, read it with `Obsidian:read_note` and append the entry to its category with `Obsidian:patch_note`. Done when the write returned success.

**Step 5. Report.** Report as note-conventions.md "Reporting the Note" states. Done when the report carries the path and the entry's summary.

## Template

ALWAYS use this exact template structure:

````markdown
---
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
status: active
tags:
  - brag
  - career
  - [tags derived from the content]
---
# [YYYY or YYYY Qn, matching the filename]

[What this period looked like — themes, milestones, shifts in focus. Write enough context that future-you can reconstruct what mattered and why these achievements stand out.]

## Impact

- **[achievement with metrics]**
  - Context: [situation]
  - Result: [quantified outcome]

## Technical

- [technical achievements, architecture decisions]

## Growth

- [new skills, mentoring, feedback received]

## Observations

- #achievement [key accomplishment with metrics]
- #growth [skill or area of development]
- #impact [business or team impact]

## Relations

- [[Related Note]]
````

An entry in its final form:

```markdown
- **Reduced API latency by 40% through query optimization**
  - Context: Checkout refactor project
  - Result: Improved user experience, reduced server costs by $2k/month
```

## Anti-Pattern: Vague Impact Claims

"Improved performance" is invisible at review time. "Reduced p99 latency from 800ms to 220ms" is concrete and defensible. Quantify with a metric, a percentage, or a time saved. When data is unavailable, state the proxy ("estimated 30% fewer support tickets in the affected flow").
