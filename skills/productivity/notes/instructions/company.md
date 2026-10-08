# Create Company Note

Track companies and roles during job application processes — applications, interviews, offers, decisions.

## Load first

Read [mapping.md](../references/mapping.md) for the vault root — this note writes to a fixed top-level folder — and [note-conventions.md](../references/note-conventions.md) for the filename, wikilink, and update rules.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Gather the company info
- [ ] Step 2: Check for an existing note
- [ ] Step 3: Compose the note or the update
- [ ] Step 4: Write and check the note
- [ ] Step 5: Report
```

**Step 1. Gather.** Gather the company name, the role title, the advertised stack, the status (applied, screening, interview, offer, rejected), and how the application started (referral, cold apply, recruiter outreach). Done when each is known.

**Step 2. Check for an existing note.** The note lives at `Companies/<Company Name>/<Role> — <Company Name>.md`, for example `Companies/Stripe/Senior Frontend Engineer — Stripe.md`.

```text
Obsidian:search_notes query="Senior Frontend Engineer Stripe" path="Companies/"
```

When a note for the same role and company exists, ask whether to append a timeline entry or create a separate note, such as for a later re-application. Done when the path is free, or the user chose.

**Step 3. Compose.** For a new note, fill the template below. For an update, compose a Timeline row, the new `status`, and any new observation. Done when a status change carries its Timeline row.

**Step 4. Write and check.** Create a new note with `Obsidian:write_note`. For an update, read the note with `Obsidian:read_note`, append the Timeline row with `Obsidian:patch_note`, and set `status` with `Obsidian:update_frontmatter`; never overwrite the existing timeline. Then run `python3 <this-skill>/scripts/check_note.py company "<note-path>"`, resolving `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose that directory, stop and report an environment problem. Fix each line the script flags with `Obsidian:patch_note` and run it again. Done when the script prints `clean`.

**Step 5. Report.** Report as note-conventions.md "Reporting the Note" states. Done when the report carries the path and what changed.

## Template

ALWAYS use this exact template structure:

````markdown
---
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
status: [applied / screening / interview / offer / rejected]
company: [company-name]
role: [role]
stack:
  - [technology]
tags:
  - company
  - job-search
  - [tags derived from the content]
---
# [Role] — [Company Name]

[What the company does, what the role involves, and why this opportunity is interesting. Capture what attracted attention — the product, team, tech, or scope. Write enough context that revisiting the note months later still surfaces the full picture.]

## Timeline

| Date | Event | Notes |
|------|-------|-------|
| [date applied] | Applied | [how applied, referral?] |
| [date] | [event] | [notes] |

## Decision

[Why accepted, declined, ghosted, or paused. Write the reasoning, not just the outcome.]

## Observations

- #status [current application status]
- #impression [impression of the company or team]
- #lesson [what was learned from the process]

## Relations

- [[Related Note]]
````

## Anti-Pattern: Status-Only Updates

Updating only the frontmatter `status` field strips the narrative — why the status changed, what happened in the conversation, what shifted. Pair every status change with a Timeline row and an observation.
