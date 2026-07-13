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

1. Look for `docs/product/PRD.md` -- extract relevant functional requirements and scope, and note the requirement IDs (`FR/BR/EC/NFR`) this epic owns for `## Requirements` (Draft, below). Also note the PRD's **Definition of Done** and **External Dependencies** when they shape this epic's scope or risks.
2. Look for `docs/product/PRODUCT.md` -- extract positioning (value proposition, audience posture).
3. Look for `docs/ROADMAP.md` -- read for sequencing context that may inform `blocked_by` suggestions, and for this epic's entry. When the entry carries a `Requirements` field, that set is the epic's `## Requirements` — the partition was settled across the whole PRD, so inherit it rather than re-deriving the IDs from the PRD alone. It enters as a claim, not authority: when the set contradicts the epic's scope — an ID the scope cannot cover, or one that plainly belongs to a neighbor — surface the mismatch and settle it against the roadmap before drafting, rather than silently adding or dropping IDs here. Do not record the roadmap as a source; epics never reference the roadmap.
4. Look for `docs/tech/design-doc.md` if it exists -- read only for constraints that may affect scope or rabbit holes. Record it in `## References` if relevant.
5. If found, summarize what was extracted and confirm with user
6. If not found, ask the user:
   - What problem does this epic solve?
   - Who benefits?
   - What changes for the user when this is done?

**Translate, don't replicate.** Upstream docs (PRD, design doc, PRODUCT) stay read-only and scoped to this epic. Extract only what maps to it, then **translate into epic language**: strip `§3.7` section numbers, internal reference codes, sibling artifact names, roadmap/sequencing framing, and domain jargon that doesn't stand alone. The epic carries the facts, not the source document's framing. The one exception is backward provenance: the PRD requirement IDs this epic owns (`FR/BR/EC/NFR`) are recorded in `## Requirements`, never in prose. `ADR-NNN` is a decision dependency, not an owned requirement — it stays out of `## Requirements` and travels with the Design Doc in References when the epic depends on one.

### 2. Draft

Fill the template (below) with discovered context:

- **Name**: kebab-case, descriptive (`user-authentication`, `payment-processing`)
- **Title**: short human-readable phrase, slug-safe. No commands, flags, file paths, parentheses, brackets, or pipes — becomes branch name slug downstream. Declarative — names the capability (`User authentication`), never a narrative outcome (`Users can sign in securely`). The name is translated from its source, not copied: strip any borrowed token — reference or ticket codes, section numbers, code identifiers, document or sibling-artifact names — which travel in References or the body, never the title. The title maps to the tracker's summary field on push; outcome prose lives only in the body's Summary section.
- **Status**: always starts as `planned`
- **Prose context**: what the epic is about, why it exists, what changes for the user -- two or three sentences; no scenario narrative, no upstream IDs or section references
- **Stories**: checklist of stories with brief descriptions. Each story becomes its own artifact later. **Local-only** — when a tracker is configured, adapters strip this section from the body on push so the tracker's native child panel (Sub-issues, child issues, etc.) stays the single source of truth.
- **Scope**: explicit in/out boundaries. Describe capabilities, not technologies (e.g., "secure password storage" not "bcrypt hashing")
- **Requirements**: the PRD requirement IDs this epic owns (`FR/BR/EC/NFR`), as a flat list — a contract the child stories operationalize, each AC linking back via `Satisfies`. Inherited from the roadmap entry's `Requirements` field when one exists; derived from the PRD only when the epic is created without a roadmap. Omit the section when the epic derives from no PRD. `ADR-NNN` is excluded — a decision dependency, not an owned requirement. Every ID here must be satisfiable by stories within this epic's scope.
- **Rabbit Holes**: execution traps specific to this epic — integration quirks, ordering constraints, or scope edge cases that will catch stories by surprise. Not implementation advice or upstream design notes
- **Open Questions**: strategic unknowns to resolve before or during story breakdown; omit the section when nothing is undecided
- **Blocked by**: other epics or stories that must finish before this one can start, listed in `blocked_by` — tracker ids/URLs when a tracker is configured, local paths otherwise. Lets the tracker enforce delivery order; leave empty when nothing blocks it.
- **References**: durable pointers the next session follows (PRD, design doc, UI design). Canonical in the body; frontmatter `sources:` mirrors the links for sync

**Declare, don't narrate.** The discovery conversation is input, never content. The body states standing facts in present tense: a resolved decision enters as fact (`Auth uses magic links`), never as its history (`we discussed OAuth but the user preferred magic links`). Strip conversation narrative — "as discussed", "the user confirmed", "we agreed" — and decision history; an unresolved decision goes to Open Questions, not the prose.

Record every durable reference surfaced during Discover (PRD, PRODUCT, brief, design doc, UI design) in frontmatter `sources:` — one entry per source, using typed labels. These are the pointers the resumption gate relies on.

Apply the resumption gate before proceeding:

> **Resumption gate** — Could a fresh session derive this epic's stories
> and scope from it and its references, with no chat history? If no, add
> the missing piece (link, scope boundary, decision) before saving.

Apply the provenance gate as well:

> **Provenance gate** — If the project has a PRD (`docs/product/PRD.md`),
> does this epic record which PRD it derives from? Add it if missing — or
> confirm with the user that the epic is independent before leaving it
> blank.

### 3. Save or Push

**If tracker configured** (`git config --get epic-tracker.kind` returns a value and is not `none`):
- Load [sync.md](sync.md) and dispatch using the draft content directly — no markdown file is created; the tracker is the source of truth
- User asked to keep it local: save to `.artifacts/epics/{epic-name}/epic.md`; push later via "sync to tracker"

**If no tracker configured** (`epic-tracker.kind` not set or `none`):
- Save to `.artifacts/epics/{epic-name}/epic.md`; create the directory if it doesn't exist
- User named a tracker: load [sync.md](sync.md) and dispatch to that tracker's adapter

An explicit destination in the user's request overrides the configured `kind` for this artifact only; it never rewrites the config. See [sync.md](sync.md) "Explicit Override".

If `epic-tracker.kind` is not set, run [sync.md](sync.md) bootstrap first.

## Guidelines

**DO:**
- Extract context from existing docs before asking questions
- Consider the PRD's Definition of Done and External Dependencies when shaping scope, rabbit holes, and open questions
- Use the roadmap for `blocked_by` suggestions and for the requirement set assigned to this epic; never record it as a source or name it in the body
- Include scope boundaries -- what's explicitly out helps as much as what's in
- List stories in the epic checklist as placeholders; create them as separate artifacts later
- Run discover first, even when the user provides context directly
- Record PRD provenance when a PRD exists; leave it blank only for epics independent of the PRD
- Record the PRD requirement IDs the epic owns (`FR/BR/EC/NFR`) in `## Requirements` as a contract for child stories; inherit them from the roadmap entry when one exists; omit when the epic derives from no PRD
- Hand sizing off to the implementation phase
- Use typed labels in frontmatter `sources:` (PRD, PRODUCT, Design Doc, UI Design)

**DON'T:**
- Include implementation details (criteria stay implementation-agnostic)
- Carry `§3.7` section numbers, sibling names, or doc-internal codes into the epic prose — translate to plain language (requirement IDs are the exception: they go in `## Requirements`)
- Create story artifacts during epic creation (list stories in checklist, create on demand later)
- Skip discover (run discover first regardless of provided context)
- Add size estimates (sizing is an implementation concern)
- Reference the roadmap in the epic body or sources

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{epic-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: planned
sources:
  - PRD: {{link to docs/product/PRD.md or "None"}}
  - PRODUCT: {{link to docs/product/PRODUCT.md or "None"}}
  - Design Doc: {{link to docs/tech/design-doc.md or "None"}}
  - UI Design: {{link to UI design or "None"}}
blocked_by: []  # artifacts that must finish first — tracker ids/URLs when a tracker is configured, local paths (epic-name or epic-name/story-name) otherwise; omit when nothing blocks this
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

MUST NOT contain: conversation narrative ("as discussed", "we agreed", "the user confirmed"), decision history, scenario narratives, `§x.x` section numbers, document references, sibling epic names, roadmap language, or implementation details. Requirement IDs (`FR/BR/EC/NFR`) belong in `## Requirements`, never the Summary; `ADR-NNN` belongs in References.

## Stories

<!-- Local-only: stripped by adapters on push to a tracker. Tracker's
native child panel (GitHub Sub-issues, Linear sub-issues) is the source
of truth for hierarchy once a tracker is wired. Names here are
placeholders; they are refined when each story is materialized via
story.md. -->

- [ ] {{story-name}} — {{brief description of what this story delivers}}
- [ ] {{story-name}} — {{brief description}}

{Stories are linked when created: [001-story-name](001-story-name.md) — description}

## Scope

**In:**

- {{What's included}}

**Out:**

- {{What's explicitly excluded — stated in this epic's own terms, never naming the sibling that owns it. Example: "Multi-factor authentication" not "MFA epic"}}

## Requirements

{Remove this section when the epic derives from no PRD.}

- {{PRD requirement IDs this epic owns — e.g. FR-3, FR-4, BR-2. Flat list; the child stories operationalize these, each AC linking back via `Satisfies`. Every ID here must be coverable by stories inside this epic.}}

MUST NOT contain: `§x.x` section numbers, sibling names, roadmap refs, or `ADR-NNN` (a decision dependency → References).

## Rabbit Holes

- {{Execution trap specific to this epic — integration quirk, ordering constraint, or scope edge case. Example: "Third-party identity provider rate limits may block bulk imports" not "use a queue"}}

MUST NOT contain: implementation advice, upstream design notes, or cross-references to other documents.

## Open Questions

{Remove this section if nothing is undecided. Strategic unknowns to
resolve before or during story breakdown.}

- {{Open question for this epic}}

## References

{Durable pointers the next session follows to recover context. Canonical
home — travels into the tracker description; frontmatter `sources:`
mirrors these links for sync (markdown only, absent in tracker mode).}

- **PRODUCT:** {{link or "None"}}
- **PRD:** {{link — "None" only when the project has no PRD or this epic is independent of it}}
- **Design Doc:** {{link or "None"}}
- **UI Design:** {{link or "None"}}
````

## Error Handling

- User provides vague context: ask clarifying questions, don't assume
- Epic name conflicts with existing: suggest alternative or confirm overwrite
