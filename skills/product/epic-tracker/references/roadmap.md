# Build the Roadmap

Organize the project's epics into an ordered flow, derived from the PRD, in `docs/ROADMAP.md`. The roadmap references its epics; the epics never reference the roadmap.

## When to Use

- User says "create roadmap", "plan the roadmap", "organize epics", "roadmap the PRD"
- The delivery needs an ordered plan of epics before or alongside creating them
- Not for creating the epics themselves — that is materialization, see [decompose.md](decompose.md)

## Workflow

### 1. Read the PRD

Look for `docs/product/PRD.md`. If it exists, read its scope, goals, and journeys to decide the epic breakdown and its sequence. If absent, derive the epics from the user directly — the roadmap never depends on the PRD existing.

**Translate, don't replicate.** The PRD stays the source of requirements; its tokens never cross verbatim into the roadmap. Strip PRD IDs (FR-N, BR-N, EC-N) and section numbers — the roadmap names epics and their flow in plain language.

### 2. Organize the epic flow

Lay the epics out in delivery order. Each entry is a capability-level epic — a name plus a one-line intent — sequenced by how the work should flow, not by deadline. Group into phases only when the flow has natural stages; a flat ordered list is fine.

**Capabilities, not specs.** An entry names a capability or objective, never a UI widget, field, endpoint, or technology. Each epic's own scope and stories are decided later when it is materialized, not here.

Present the proposed flow; let the user reorder, add, drop, merge, or split. Settle the flow before writing.

### 3. Write docs/ROADMAP.md

Write the ordered flow to `docs/ROADMAP.md` (committed). Update it in place on re-run — the roadmap is a living plan; never duplicate it. The roadmap lists its epics; it does not create them (that is [decompose.md](decompose.md)).

## Template

Here is a sensible default format, but use your best judgment — phase headings when the flow has stages, a single ordered list when it does not:

````markdown
# Roadmap: {{Project Name}}

{{One line on what this roadmap sequences and why.}}

## {{Phase name, or omit the heading for a flat flow}}

1. **{{epic-name}}** — {{one-line capability the epic delivers}}
2. **{{epic-name}}** — {{one-line capability}}
````

MUST NOT contain: deadlines or dates, per-story detail, PRD IDs (FR-N, BR-N, EC-N), section numbers, or implementation specifics.

## Guidelines

- Read the PRD for context; author the flow in plain language, independent of PRD framing
- Name epics as capabilities, never UI or technology
- Sequence by flow, not deadline — a roadmap orders work, it does not schedule it
- Keep it one living doc; update in place, never duplicate
- The roadmap references its epics; epics never point back at it — they stay self-contained
- Organizing is not creating — materialize epics via [decompose.md](decompose.md)
