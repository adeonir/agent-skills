ALWAYS use this exact template structure:

````markdown
---
updated: {{YYYY-MM-DD}}
status: {{draft | stable}}
sources:
  - PRD: {{link to docs/product/PRD.md}}
  - PRODUCT: {{link to PRODUCT.md or "None"}}
---

# Roadmap: {{Project Name}}

{{What this roadmap sequences and the criteria that set its order. State that each title links to its tracker issue and that an entry without a link is not materialized yet.}}

## Phase {{N}} — {{Phase name, or omit the heading for a flat roadmap}}

### {{N}}. {{epic-title-in-kebab-case}} · [{{TRACKER-ID}}]({{tracker URL — omit the separator and the link until the epic exists}})

{{One to three sentences on the outcome the epic delivers and its boundary.}}

- **Driven by:** {{outcome or requirement that motivates this epic}}
- **Requirements:** {{FR/BR/EC/NFR IDs this epic owns — omit the field when the epic owns none}}
- **Blocked by:** {{epic titles in kebab case that this one depends on — omit the field when nothing blocks it}}
- **Tags:** {{foundation | high-risk | external-dependency | validation, comma-separated — omit the field when none applies}}

## Definition of Done

| Criterion | How verified |
| --- | --- |
| {{condition the release must meet}} | {{check that proves it}} |

MUST NOT contain, in any entry: deadlines or dates, per-task detail, section numbers, `ADR-NNN`, or implementation specifics. The frontmatter's `updated` is the only permitted date. Inside an entry, requirement IDs appear only in the `Requirements` field and dependencies only in the `Blocked by` field. The Definition of Done may cite requirement IDs, and carries no dates, section numbers, or `ADR-NNN`. Tags are short signals only; they never replace the outcome description or introduce scheduling.
````

Serialize the settled set: this file owns the roadmap's form, never its content. Never reorder, re-partition, or re-derive an entry here.

- Render the entries in the settled order. Each milestone is a numbered phase heading over its epics, starting at 0. Number the entries continuously across phases. Omit the phase headings when the roadmap has no milestones; a flat roadmap is as valid as one with phase headings.
- Keep the entry's fields in order: `Driven by`, `Requirements`, `Blocked by`, `Tags` — each field omitted when empty.
- Write the prose, headings, and field labels in the PRD's language, and keep the Definition of Done table header as the template states it.
- Write to `docs/product/ROADMAP.md` — committed, alongside `PRD.md`. It is one living doc: update it in place on a re-run and never duplicate the file. Preserve untouched entries as settled.
- Bump the frontmatter `updated` and refresh `status` and `sources` on every write. Set `status` to `stable` when every entry has a tracker link, and to `draft` otherwise.
- The roadmap references its epics; epics never point back at it — they stay self-contained.
