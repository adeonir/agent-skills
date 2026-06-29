# Create Epic

Plan a thematic container that groups related stories into a cohesive delivery unit.

## When to Use

- User wants to plan a new feature area or initiative
- User says "create epic", "new epic"
- A PRD or brief exists and needs to be broken into deliverable epics

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### 1. Discover

Check for existing context before asking questions:

1. Look for `.artifacts/docs/prd.md` -- extract relevant functional
   requirements and scope
2. Look for `.artifacts/epics/milestones.md` -- find the milestone this
   epic serves, if any
3. Look for `.artifacts/docs/PRODUCT.md` -- extract positioning (value
   proposition, audience posture)
4. If found, summarize what was extracted and confirm with user
5. If not found, ask the user:
   - What problem does this epic solve?
   - Who benefits?
   - What changes for the user when this is done?

**Translate, don't replicate.** Upstream docs (PRD, design doc, PRODUCT.md) stay
read-only and scoped to this epic. Extract only what maps to it, then
**translate into epic language**: strip technical IDs (§3.7, EC-2, ADR-001),
internal reference codes, sibling artifact names, milestone content and
roadmap/sequencing framing, and domain jargon that doesn't stand alone. The
epic carries the facts, not the source document's framing.

Recording *which* milestone the epic serves is the one exception — its direct
parent, captured as the `milestone:` pointer in frontmatter (same as a
story's `epic:`). The pointer names the parent; it never pulls the milestone's
deliverables, scope, or phase ordering into the epic body.

### 2. Draft

Fill the template (below) with discovered context:

- **Name**: kebab-case, descriptive (`user-authentication`,
  `payment-processing`)
- **Title**: short human-readable phrase, slug-safe. No commands,
  flags, file paths, parentheses, brackets, or pipes — becomes branch
  name slug downstream. Declarative — names the capability
  (`User authentication`), never a narrative outcome (`Users can sign
  in securely`). The title maps to the tracker's summary field on
  push; outcome prose lives only in the body's Summary section.
- **Status**: always starts as `planned`
- **Prose context**: what the epic is about, why it exists, what changes
  for the user -- two or three sentences; no scenario narrative, no
  upstream IDs or section references
- **Stories**: checklist of stories with brief descriptions. Each story
  becomes its own artifact later. **Local-only** — when a tracker is
  configured, adapters strip this section from the body on push so the
  tracker's native child panel (Sub-issues, child issues, etc.) stays
  the single source of truth.
- **Scope**: explicit in/out boundaries. Describe capabilities, not
  technologies (e.g., "secure password storage" not "bcrypt hashing")
- **Rabbit Holes**: execution traps specific to this epic — integration
  quirks, ordering constraints, or scope edge cases that will catch
  stories by surprise. Not implementation advice or upstream design notes
- **Open Questions**: strategic unknowns to resolve before or during
  story breakdown; omit the section when nothing is undecided
- **Blocked by**: other epics or stories that must finish before this one
  can start, listed in frontmatter `blocked_by` by path. Lets the tracker
  enforce delivery order; leave empty when nothing blocks it.
- **Milestone**: the milestone this epic serves (from the registry,
  `.artifacts/epics/milestones.md`), as the frontmatter `milestone:` pointer
  (its direct parent). Omit when the epic sits outside any milestone; record
  the parent only, never the milestone's content.
- **References**: durable pointers the next session follows (PRD, design
  doc, UI design). Canonical in the body; frontmatter `sources:` mirrors
  the links for sync

Record every durable reference surfaced during Discover (PRD, brief,
design doc, UI design) in frontmatter `sources:` -- one entry per source.
These are the pointers the resumption gate relies on.

Apply the resumption gate before proceeding:

> **Resumption gate** — Could a fresh session derive this epic's stories
> and scope from it and its references, with no chat history? If no, add
> the missing piece (link, scope boundary, decision) before saving.

Apply the provenance gate as well:

> **Provenance gate** — If the project has a PRD (`.artifacts/docs/prd.md`),
> does this epic record which PRD it derives from? Separately, if the epic
> belongs to a milestone, does it record the `milestone:` pointer? Add
> whichever is missing — or confirm with the user that the epic is
> independent before leaving it blank.

### 3. Save or Push

**If tracker configured** (`git config --get epic-tracker.kind` returns a value and is not `none`):
- Ask the user (per session, cached) whether to push to the tracker
- If yes: load [sync.md](sync.md) and dispatch using the draft content
  directly — no markdown file is created; the tracker is the source of
  truth
- If no: save to `.artifacts/epics/{epic-name}/epic.md`; push later via
  "sync to tracker"

**If no tracker configured** (`epic-tracker.kind` not set or `none`):
- Save to `.artifacts/epics/{epic-name}/epic.md`; create the directory
  if it doesn't exist

If `epic-tracker.kind` is not set, run [sync.md](sync.md) bootstrap first.

## Guidelines

**DO:**
- Extract context from existing docs before asking questions
- Include scope boundaries -- what's explicitly out helps as much as what's in
- List stories in the epic checklist; create them as separate artifacts later
- Run discover first, even when the user provides context directly
- Record PRD provenance when a PRD exists; leave it blank only for epics independent of the PRD
- Hand sizing off to the implementation phase

**DON'T:**
- Include implementation details (criteria stay implementation-agnostic)
- Carry upstream IDs, section numbers, or doc-internal codes (§3.7, EC-2, ADR-001) into the epic — translate to plain language
- Create story artifacts during epic creation (list stories in checklist, create on demand later)
- Skip discover (run discover first regardless of provided context)
- Add size estimates (sizing is an implementation concern)

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{epic-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: planned
sources: []
blocked_by: []  # paths of artifacts that must finish first (epic-name or epic-name/story-name); omit when nothing blocks this
milestone: {{milestone-name or omit when the epic sits outside any milestone}}
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Epic Title}}

## Summary

{{What the epic is about, why it exists, what changes for the user when it ships. Two to three sentences.}}

MUST NOT contain: scenario narratives, upstream IDs (§x.x, EC-N, ADR-NNN), section or document references, sibling epic names, roadmap language, or implementation details.

## Stories

<!-- Local-only: stripped by adapters on push to a tracker. Tracker's
native child panel (GitHub Sub-issues, Linear sub-issues) is the source
of truth for hierarchy once a tracker is wired. -->

- [ ] {{story-name}} — {{brief description of what this story delivers}}
- [ ] {{story-name}} — {{brief description}}

{Stories are linked when created: [001-story-name](001-story-name.md) — description}

## Scope

**In:**

- {{What's included}}

**Out:**

- {{What's explicitly excluded}}

## Rabbit Holes

- {{Execution trap specific to this epic — integration quirk, ordering constraint, or scope edge case}}

MUST NOT contain: implementation advice, upstream design notes, or cross-references to other documents.

## Open Questions

{Remove this section if nothing is undecided. Strategic unknowns to
resolve before or during story breakdown.}

- {{Open question for this epic}}

## References

{Durable pointers the next session follows to recover context. Canonical
home — travels into the tracker description; frontmatter `sources:`
mirrors these links for sync (markdown only, absent in tracker mode).}

- **Milestone:** {{milestone name or "None"}}
- **Brief:** {{link or "None"}}
- **PRD:** {{link — "None" only when the project has no PRD or this epic is independent of it}}
- **Design Doc:** {{link or "None"}}
- **UI Design:** {{link or "None"}}
````

## Error Handling

- The registry has milestones: ask which one this epic serves, or none — the
  `milestone:` pointer is optional and an epic may sit outside any milestone
- User provides vague context: ask clarifying questions, don't assume
- Epic name conflicts with existing: suggest alternative or confirm
  overwrite
