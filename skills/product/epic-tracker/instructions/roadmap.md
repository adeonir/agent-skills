# Write the Roadmap

Serialize the settled epic entries `decompose` hands over into `docs/product/ROADMAP.md`. This ref writes the record; it decides nothing.

## When to Use

Composed by [decompose.md](decompose.md) after it has derived, evaluated, ordered, and partitioned the epic set. Not a direct trigger — the user never calls it, and adjusting the roadmap means calling `decompose`, which re-derives the delta and dispatches here again.

The roadmap is `decompose`'s persisted memory of the settled plan: it records every decision so a later run reads them back instead of re-deriving. `decompose` reads it; the create refs read each epic's entry. The roadmap references its epics; the epics never reference the roadmap.

## Workflow

### 1. Receive the entries

`decompose` passes the settled set as structured entries — per epic: title, capability line, `Driven by`, the requirement IDs it owns, its `Blocked by` dependencies, its position in the flow, and its phase (when the flow is phased). This ref does not derive, evaluate, or reorder any of it — it serializes what it is given.

### 2. Serialize via the template

Render the entries into the template below, in the order `decompose` settled. Phase headings are **cosmetic** — a visual grouping for the human reader; they carry no scheduling of their own. (`decompose` derives each epic's milestone from its phase, but that origin lives there, not here.) A flat ordered list is fine when the flow has no phases.

### 3. Write in place

Write to `docs/product/ROADMAP.md` — committed, alongside `PRD.md` and `PRODUCT.md`. Update in place on a re-run; never duplicate the file. Bump the frontmatter `updated` and refresh `sources` on every write. Preserve untouched entries as `decompose` passes them.

## Template

ALWAYS use this exact template structure:

````markdown
---
updated: {{YYYY-MM-DD}}
sources:
  - PRD: {{link to docs/product/PRD.md}}
  - PRODUCT: {{link to docs/product/PRODUCT.md or "None"}}
---

# Roadmap: {{Project Name}}

{{One line on what this roadmap sequences and why.}}

## {{Phase name, or omit the heading for a flat flow}}

1. **{{Epic Title}}** — {{one-line capability the epic delivers}} — _Driven by: {{journey, rule, or goal that motivates this epic}}_ — _Requirements: {{FR/BR/EC/NFR IDs this epic owns — omit the field when the epic owns none}}_ — _Blocked by: {{epic titles this one depends on — omit the field when nothing blocks it}}_ — {{optional tag: foundation | validation | high-risk | external-dependency}}
2. **{{Epic Title}}** — {{one-line capability}} — _Driven by: {{journey, rule, or goal}}_ — _Requirements: {{IDs}}_
````

MUST NOT contain, in any entry: deadlines or dates, per-story detail, section numbers, `DEP-N`, `ADR-NNN`, or implementation specifics. The frontmatter's `updated` is the only permitted date. Requirement IDs (`FR/BR/EC/NFR`) appear only in the `Requirements` field, dependencies only in the `Blocked by` field — never in the capability line or any prose. Tags are short signals only; they never replace the capability description or introduce scheduling.

## Guidelines

- Serialize what `decompose` settled — never reorder, re-partition, or re-derive here; this ref owns the file's form, not its content.
- Keep the entry line's fields in order: capability, `Driven by`, `Requirements`, `Blocked by`, tag — each field omitted when empty.
- Phase headings are cosmetic grouping for the reader; a flat list is equally valid.
- One living doc: update in place, never duplicate.
- The roadmap references its epics; epics never point back at it — they stay self-contained.
- Populate frontmatter `updated` and `sources` on every write.
