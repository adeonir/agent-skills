# Create Company Note

Track companies and roles during job application processes — applications,
interviews, offers, decisions.

## When to Use

- User says "company note", "track interview", "job application",
  "track this role"
- User mentions an interview process or offer to remember

## Vault Resolution

Load [mapping.md](mapping.md) first to resolve vault root via the 3-tier
fallback (local symlink → global pointer → bootstrap).

## Workflow

1. **Gather company info**
   - Company name
   - Role title
   - Stack (technologies advertised)
   - Application status (applied, screening, interview, offer, rejected)
   - How the application started (referral, cold apply, recruiter outreach)

2. **Generate folder and filename**
   - Folder: `Companies/{{Company Name}}/`
   - Filename: `{{Role}} — {{Company Name}}.md`
   - Example: `Companies/Stripe/Senior Frontend Engineer — Stripe.md`

3. **Check if exists**

   ```
   search_notes query="{{Role}} {{Company Name}}" path="Companies/"
   ```

   If a note for the same role+company exists, ask whether to append a
   new timeline entry or create a separate note (e.g., re-application
   later).

4. **Compose content** using the template below.

5. **Write note**

   ```
   write_note path="Companies/{{Company Name}}/{{Role}} — {{Company Name}}.md" content="..."
   ```

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{company-slug}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: {{applied / screening / interview / offer / rejected}}
sources: []
company: {{company-name}}
role: {{role}}
stack:
  - {{technology}}
tags:
  - company
  - job-search
  - {{dynamic tags based on content}}
---
# {{Role}} — {{Company Name}}

{{What the company does, what the role involves, and why this opportunity
is interesting. Capture what attracted attention — the product, team,
tech, or scope. Write enough context that revisiting the note months
later still surfaces the full picture.}}

## Timeline

| Date | Event | Notes |
|------|-------|-------|
| {{date-applied}} | Applied | {{how applied, referral?}} |
| {{date}} | {{event}} | {{notes}} |

## Decision

{{Why accepted, declined, ghosted, or paused. Write the reasoning, not
just the outcome.}}

## Observations

- #status {{current application status}}
- #impression {{impression of the company or team}}
- #lesson {{what was learned from the process}}

## Relations

- [[{{Related Note}}]]
````

## Updating Existing Company Notes

When the application progresses (interview scheduled, offer received,
decision made):

1. Read the note with `read_note`
2. Use `patch_note` to append a row to the Timeline table
3. Update the frontmatter `status` field via `find_replace`
4. Add new observations as the process unfolds

Do not overwrite — keep the historical timeline intact.

## Guidelines

- Update the Timeline table as events happen (interviews, offers,
  feedback) rather than reconstructing from memory later
- Capture impressions of the team and process — useful for future
  application decisions and referrals
- Link related notes (challenge notes for technical interviews, brag
  notes when applying impacted achievements)

## Anti-Pattern: Status-Only Updates

Updating only the frontmatter `status` field strips the narrative — why
the status changed, what happened in the conversation, what shifted.
Always pair a status change with a Timeline row and an observation.
