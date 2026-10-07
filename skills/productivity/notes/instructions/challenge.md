# Create Challenge Note

Document technical challenges from interview processes.

## Load first

Read [mapping.md](../references/mapping.md) for the vault root — this note writes to a fixed top-level folder — and [note-conventions.md](../references/note-conventions.md) for the filename, wikilink, and update rules.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Gather the challenge info
- [ ] Step 2: Generate the path
- [ ] Step 3: Check for an existing note
- [ ] Step 4: Compose the note
- [ ] Step 5: Write the note
- [ ] Step 6: Report
```

**Step 1. Gather.** Gather the company (when part of an interview process), a brief description, the tech stack, the time constraints, and the status (pending, completed, submitted, feedback received). Done when each is known or stated as absent.

**Step 2. Generate the path.** `Challenges/<Company>/<Type Topic>.md`, Title Case; use a context name such as `Algo` when no company applies. Examples: `Challenges/Stripe/System Design URL Shortener.md`, `Challenges/Algo/Binary Tree Traversal.md`. Done when the path is set.

**Step 3. Check for an existing note.**

```text
Obsidian:search_notes query="System Design URL Shortener" path="Challenges/"
```

When a note exists, update it as note-conventions.md "Updating an Existing Note" states. Done when the path is free, or the update path is chosen.

**Step 4. Compose.** Fill the template below. Paraphrase the challenge text, never copy it verbatim. Record a failed attempt as fully as a success. Done when no slot is left unfilled.

**Step 5. Write.** Create the note with `Obsidian:write_note`. Done when the write returned success.

**Step 6. Report.** Report as note-conventions.md "Reporting the Note" states. Done when the report carries the path and the summary.

## Template

ALWAYS use this exact template structure:

````markdown
---
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
status: [pending / completed / submitted / feedback-received]
company: [company]
stack:
  - [technology]
tags:
  - challenge
  - interview
  - [tags derived from the content]
---
# [Challenge Description]

[What the challenge was about, the constraints (time, tools, scope), and the environment. Include the initial reaction and how the problem was framed before diving in.]

## Approach

[How the problem was approached — thought process, trade-offs considered]

## Solution

[The solution — code, architecture, a mermaid diagram for system design, and time and space complexity for an algorithm]

## Learnings

- [what was learned]
- [what could be done differently]
- [feedback received, when any]

## Observations

- #technique [approach or pattern used]
- #lesson [key takeaway]

## Relations

- [[Related Note]]
````

## Anti-Pattern: Skipping Failed Attempts

Failed challenges contain the most useful learnings — they reveal which assumptions broke and what would be tried differently. Documenting only successes turns the challenge log into a vanity record. Capture both.
