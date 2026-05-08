# Write Obsidian Notes

Create session notes in the project folder and update the daily note
using MCPVault MCP tools directly.

## When to Use

- Obsidian session note: when `obsidian.path` is not `--`
- Daily note: always (even when session note is skipped)
- Runs after BM notes
- Depends on mapping output (Obsidian path, base tags) and on the
  session-dump Load phase (latest block folded — Discoveries → Findings,
  Decisions → Decisions, Next Context → Next)

## Obsidian Syntax Rules

Obsidian notes render for humans (Graph view, daily review, Dataview).
Keep notes brief and scannable — prose narrative up front, structured
sections below, typed relations for graph edges.

- **Frontmatter**: YAML with `title`, `type`, `tags`
- **Observations**: daily notes only. Bullets under `## Observations`
  formatted as `- #category content`. Category is free-form (examples:
  `#pattern`, `#method`, `#cadence`, `#blocker`, `#mood` — day-level
  cross-cutting facts). Use `#hashtags`, not `[brackets]`.
  Session notes do not have an Observations section.
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

2-3 sentence narrative. What happened, key outcome, why it matters.
Past tense, natural language. [[Wikilinks]] inline only to existing notes.

## Decisions

- Decision + rationale + named alternative rejected (when a real option was considered)

## Findings

- Brief finding worth capturing (omit section when nothing notable)

## Problems

- Problem + root cause + fix (omit section when nothing notable)

## Next

- Entry point for next session (file, function, path, or command)

## Relations

- follows [[Previous Session]]
- part_of [[Project]]
```

Section presence:
- `## Summary` always present
- `## Decisions` when decisions were made
- `## Findings` when there is a notable technical discovery
- `## Problems` when a problem was encountered and resolved or noted
- `## Next` when there is work to continue
- `## Relations` for typed edges that add graph value

When `session-dump.md` Load surfaced a latest phase block, fold its
bullets in before composing the note:

- `**Discoveries:**` → brief bullets in `## Findings`
- `**Decisions:**` → `## Decisions` bullets with rationale (name
  rejected alternatives when applicable)
- `**Next Context:**` → `## Next` bullets, preserving the concrete
  entry point

#### Write

```
write_note(
  path="{obsidian.path}/Sessions/YYYY-MM-DD — Description.md",
  content="## Summary\n\n2-3 sentence narrative...\n\n## Decisions\n- ...\n\n## Findings\n- ...\n\n## Problems\n- ...\n\n## Next\n- ...\n\n## Relations\n- follows [[...]]",
  frontmatter={title: "...", type: "session", tags: ["session", ...base_tags, ...context_tags]}
)
```

Rules:
- Keep each section brief — this is a human note, not an AI knowledge base
- Decisions bullets distill with rationale — name rejected alternatives when a real option was considered
- Findings and Problems: brief bullets only, no detailed narratives
- Relations use typed verbs (`- follows [[X]]`) — fallback for graph edges only
- Wikilinks only to existing notes/entities; verify with `search_notes` before linking
- Past tense, natural language
- No git metadata (branches, commits, PRs) or file lists
- One project per session note
- Omit empty sections

### 2. Create or update daily note

#### Path

Always `Daily/YYYY-MM-DD.md`.

#### Daily template

Activities per project (bullet list), Open Items for pending work,
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

- Outcome or task, with inline `[[wikilink]]` to the session note
  on the first bullet (e.g. [[YYYY-MM-DD — Description]])
- Another outcome or task

### {Another Project}

- ...

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
- If the project already has a subsection in Activities, merge the
  existing bullets with new bullets — deduplicate, keep distinct items
- If the project is new, add a `### Project Name` subsection at the end
  of Activities (before the next `##` section)
- Add items to Open Items if relevant (create the section if it does
  not exist)
- Consolidate `## Observations` and `## Relations` the same way — merge
  existing with new, deduplicate, keep only distinct items

Rules:
- Activities split by project with `### Project Name` headers
- Bullets per project, mix of outcomes and tasks — count scales with
  session depth
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
- Keep session Summary brief — 2-3 sentences, human narrative, not an AI knowledge base
- Use `## Relations` for typed edges (`- follows [[X]]`) that add graph
  value; inline `[[wikilinks]]` in Summary cover ordinary mentions
- Tag every note as `[note-type, ...base_tags, ...context_tags]` —
  `note-type` is one of `session`, `daily`; `base_tags` come from
  mapping output; `context_tags` are derived from the session content
  (work type, topics)
- Use Title Case for folders and filenames
- Omit empty sections — no placeholder headers
- Keep daily note as outcomes and tasks in bullets, not a detailed log
- Map session-dump Discoveries → Findings bullets, Decisions → Decisions, Next Context → Next

**DON'T:**
- Call any skill — use MCPVault MCP tools directly
- Use `[brackets]` for observations — use `#hashtags` instead (contrasts: Obsidian Syntax Rules)
- Add `# H1` to any note — frontmatter `title` is the canonical heading
- Write changelog-style content or list steps taken
- List files modified or git metadata
- Blindly append bullets without reading existing content first
- Write prose paragraphs in Activities — use bullets (contrasts: bullets per project)
- Turn session notes into detailed logs — keep them brief and human-scannable (contrasts: keep session Summary brief)
- Create empty sections or placeholder content
- Create wikilinks to files that don't exist (orphan links)
- Expand Findings or Problems into detailed narratives (contrasts: brief bullets only)

## Error Handling

- Obsidian/MCPVault unavailable: skip Obsidian step entirely, warn user
- Daily note already exists: read with `read_note`, update with `patch_note`
- No meaningful session content: keep session brief, still update daily note
