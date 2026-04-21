# Write Obsidian Notes

Create session notes in the project folder and update the daily note.
Uses MCPVault MCP tools directly — no dependency on other skills.

> **LOAD FIRST:** [mapping.md](mapping.md) -- provides Obsidian path and base tags

## When to Use

- Obsidian session note: when `obsidian.path` is not `--`
- Daily note: always (even when session note is skipped)
- Runs after BM notes

## Obsidian Syntax Rules

Obsidian notes render for humans (Graph view, daily review, Dataview).
BM notes are agent-consumed. Same substance, different shape: Obsidian
keeps a prose narrative up front, structured sections below, typed
relations for graph edges.

- **Frontmatter**: YAML with `title`, `type`, `tags`
- **Observations**: bullets under `## Observations` formatted as
  `- #category content`. Category is free-form, derived from session
  content (examples: outcome, decision, finding, risk, convention,
  context — not a fixed list). Never use `[brackets]` — that is BM format.
- **Relations**: typed verb + wikilink under `## Relations`:
  `- follows [[Target]]`. Common types: `follows`, `part_of`, `expands`,
  `relates_to`, `implements`, `requires`, `replaces`, `pairs_with`,
  `extends`, `depends_on`. Inline `[[wikilinks]]` in prose cover ordinary
  mentions; the Relations section holds typed edges that add graph value.
- **Wikilinks**: only to existing notes or entity files. Orphan links
  create empty files at the vault root — verify before linking.
- **H1 heading**: all notes omit the body `# H1` — the frontmatter
  `title` is the canonical heading. Top-level body sections start at `##`.

## Filename Sanitization

When generating filenames from user input:

- Remove invalid characters: `/ \ : * ? " < > |`
- Preserve accented characters (valid in filenames)
- Use Title Case for all filenames
- Example: `What's Next?` becomes `Whats Next.md`

## MCPVault Tools

Call these directly — do not invoke any skill.

| Tool | Purpose |
|------|---------|
| `mcp__obsidian__write_note` | Create new note with content and frontmatter |
| `mcp__obsidian__read_note` | Read existing note before patching |
| `mcp__obsidian__patch_note` | In-place update (oldString → newString) |
| `mcp__obsidian__search_notes` | Search-before-create, find existing notes |

Always search before creating to avoid duplicates.

## Workflow

### 1. Create session note

#### Determine path

- Folder: `{obsidian.path}/Sessions/`
- Filename: `YYYY-MM-DD — Description.md`
- Example: `Work/Acme/Sessions/2026-03-22 — BM Reorganization.md`

#### Check for existing note

```
search_notes query="YYYY-MM-DD" path="{obsidian.path}/Sessions/"
```

If a match exists for the same date and topic, read it with `read_note`
and append a new section with `patch_note` (horizontal rule `---` plus
date header as separator). Otherwise create a new note.

#### Session template

Mirrors BM session structure, optimized for human reading. BM sections
`## Findings`, `## Problems`, and `## Next Context` fold into Summary
prose — same substance, different shape.

```markdown
---
title: "YYYY-MM-DD — Description"
type: session
tags:
  - session
  - {base tags from mapping}
  - {context tags from content}
---

## Summary

Prose narrative — context, what happened, decisions with rationale,
findings, problems and root causes, next context for the following
session. Past tense, natural language. [[Wikilinks]] inline only to
notes or entities that already exist.

## Decisions

- Decision + rationale + named alternative rejected (when a real option was considered)

## Open Items

- [ ] Pending work, blockers, next steps

## Observations

- #category content (category free-form, derived from content)

## Relations

- follows [[Previous Session]]
- part_of [[Project]]
```

Section presence:
- `## Summary` and `## Decisions` always present when there is content
- `## Open Items` only when there are pending items
- `## Observations` whenever a fact is worth distilling into a tagged bullet
- `## Relations` as fallback for typed edges that add graph value —
  inline `[[wikilinks]]` in Summary already cover ordinary mentions

#### Write

```
write_note(
  path="{obsidian.path}/Sessions/YYYY-MM-DD — Description.md",
  content="## Summary\n\nProse narrative...\n\n## Decisions\n- ...\n\n## Open Items\n- [ ] ...\n\n## Observations\n- #category ...\n\n## Relations\n- follows [[...]]",
  frontmatter={title: "...", type: "session", tags: ["session", ...base_tags, ...context_tags]}
)
```

Rules:
- Summary prose opens the body; findings, problems, and next-context fold into the narrative
- Decisions bullets distill with rationale — mirror the BM `## Decisions` content
- Name rejected alternatives explicitly in Decisions when a real option was considered
- Observations use `- #category content`; categories come from the content, not a fixed list
- Relations use typed verbs (`- follows [[X]]`) — same verbs as BM, fallback only for graph edges
- Wikilinks only to existing notes/entities; verify with `search_notes` before linking
- Past tense, natural language
- No git metadata (branches, commits, PRs) or file lists
- One project per session note
- Omit empty sections — skip Open Items, Observations, or Relations when empty

### 2. Create or update daily note

#### Path

Always `Daily/YYYY-MM-DD.md`.

#### Daily template

Activities per project (prose paragraph), Open Items for pending work,
Observations for day-level facts that cut across projects, Relations
for typed edges to today's session notes.

```markdown
---
title: "DayOfWeek, Month DD, YYYY"
type: daily
tags:
  - daily
  - {base tags from mapping}
  - {context tags from content}
---

## Activities

### {Project Name}

Prose paragraph (2-4 sentences) — outcomes, decisions, and context from
the day's work on this project. Inline `[[wikilink]]` to the session
note (e.g. [[YYYY-MM-DD — Description]]). Past tense, natural language.

### {Another Project}

...

## Open Items

- [ ] Pending work, blockers, next steps

## Observations

- #category cross-cutting observation (patterns, methods, cadence,
  blockers, mood — day-level facts that are not tied to a single
  project's session)

## Relations

- contains [[YYYY-MM-DD — Session Note]]
```

Section presence:
- `## Activities` always present with at least one project subsection
- `## Open Items` only when there are pending items
- `## Observations` for cross-cutting day-level facts — do not restate
  per-project observations that belong in the session note; common
  categories: `#pattern`, `#method`, `#cadence`, `#blocker`, `#mood`
- `## Relations` typed edges to today's session notes (`contains`) or
  other day-level references; omit if no sessions or references

#### If note does not exist

Compose content following the template above. Only `## Activities` is
required; omit empty sections.

```
write_note(
  path="Daily/YYYY-MM-DD.md",
  content="## Activities\n...\n\n## Relations\n- contains [[...]]",
  frontmatter={title: "...", type: "daily", tags: [...]}
)
```

#### If note already exists

Read first with `read_note`, then use `patch_note`:
- If the project already has a subsection in Activities, rewrite the
  entire subsection: merge the existing paragraph with new activities
  into a single 2-4 sentence paragraph that covers the full day
- If the project is new, add a `### Project Name` subsection at the end
  of Activities (before the next `##` section)
- Add items to Open Items if relevant (create the section if it does
  not exist)
- Consolidate `## Observations` and `## Relations` the same way — merge
  existing with new, deduplicate, keep only distinct items

Rules:
- Activities split by project with `### Project Name` headers
- One prose paragraph per project (2-4 sentences) after consolidation
- Observations are day-level and cross-cutting — project-specific facts
  stay in the session note
- Relations use typed verbs (`contains`, `relates_to`); `contains`
  points to today's session notes
- Past tense, natural language
- Do not duplicate detail from the session note — daily stays
  summary-level
- Omit empty sections entirely

## Guidelines

**DO:**
- Search before creating with `search_notes` to avoid duplicates
- Read existing note before patching (daily, session updates)
- Keep Summary prose substantive — it is the human-readable narrative
  and carries findings, problems, and next-context that BM puts in
  dedicated sections
- Put distilled facts under `## Observations` as `- #category content`
- Use `## Relations` for typed edges (`- follows [[X]]`) that add graph
  value; inline `[[wikilinks]]` in Summary cover ordinary mentions
- Tag every note as `[note-type, ...base_tags, ...context_tags]` —
  `note-type` is one of `session`, `daily`; `base_tags` come from
  mapping output; `context_tags` are derived from the session content
  (work type, topics)
- Use Title Case for folders and filenames
- Omit empty sections — no placeholder headers
- Keep daily note as outcomes and decisions, not detailed log

**DON'T:**
- Call any skill — use MCPVault MCP tools directly
- Use `[brackets]` for observations (that is BM format)
- Add `# H1` to any note — frontmatter `title` is the canonical heading
- Write changelog-style content or list steps taken
- List files modified or git metadata
- Blindly append bullets without reading existing content first
- Let any daily project paragraph exceed 4 sentences — consolidate
- Copy the BM note verbatim — BM `## Findings`, `## Problems`, and
  `## Next Context` fold into Obsidian `## Summary` prose
- Create empty sections or placeholder content
- Create wikilinks to files that don't exist (orphan links)
