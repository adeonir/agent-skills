# Write the Roadmap

Serialize the settled epic entries `decompose` hands over into `docs/product/ROADMAP.md`. This ref writes the record; it decides nothing.

## When to Use

Composed by `decompose` after it has derived, evaluated, ordered, and partitioned the epic set. Not a direct trigger — the user never calls it, and adjusting the roadmap means calling `decompose`, which re-derives the delta and dispatches here again.

The roadmap is `decompose`'s persisted memory of the settled plan: it records every decision so a later run reads them back instead of re-deriving. `decompose` reads it, and `epic.md` reads the entry for the epic it is drafting — no other create ref touches the roadmap. The roadmap references its epics; the epics never reference the roadmap.

## Workflow

### 1. Receive the entries

`decompose` passes the settled set as structured entries — per epic: title, outcome description, `Driven by`, the requirement IDs it owns, its `Blocked by` dependencies, its tags, its tracker link when the epic exists, its position in the flow, and its milestone (when the roadmap has milestones) — plus the ordering criteria and the Definition of Done for the whole roadmap. After materializing, it passes the tracker links of the epics it created. This ref does not derive, evaluate, or reorder any of it — it serializes what it is given.

### 2. Serialize via the template

Render the entries into the template below, in the order `decompose` settled. Each milestone is a numbered phase heading over its epics, starting at 0; `decompose` settles the grouping. Number the entries continuously across phases. Omit the phase headings when the roadmap has no milestones. Write the prose, headings, and field labels in the PRD's language, and keep the Definition of Done table header as the template states it.

### 3. Write in place

Write to `docs/product/ROADMAP.md` — committed, alongside `PRD.md`. Update in place on a re-run; never duplicate the file. Bump the frontmatter `updated` and refresh `status` and `sources` on every write. Set `status` to `stable` when every entry has a tracker link, and to `draft` otherwise. Preserve untouched entries as `decompose` passes them.

## Template

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

## Guidelines

- Serialize what `decompose` settled — never reorder, re-partition, or re-derive here; this ref owns the file's form, not its content.
- Keep the entry's fields in order: `Driven by`, `Requirements`, `Blocked by`, `Tags` — each field omitted when empty.
- A flat roadmap is as valid as one with phase headings.
- One living doc: update in place, never duplicate.
- The roadmap references its epics; epics never point back at it — they stay self-contained.
- Populate frontmatter `updated`, `status`, and `sources` on every write.
