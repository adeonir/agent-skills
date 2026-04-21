# Write Obsidian Notes

Create session and decision notes in the project folder and update
the daily note. Uses MCPVault MCP tools directly — no dependency on
other skills.

> **LOAD FIRST:** [mapping.md](mapping.md) -- provides Obsidian path and base tags

## When to Use

- Obsidian session note: when `obsidian.path` is not `--`
- Daily note: always (even when session note is skipped)
- Runs after BM notes

## Obsidian Syntax Rules

Obsidian uses a distinct format from Basic Memory. Do not mix them.

- **Frontmatter**: YAML with `title`, `type`, `tags`
- **Observations**: prefer inline `#hashtags` woven into prose. Use a
  `## Observations` section only as fallback when no natural inline spot
  exists. Never use `[brackets]` — that is BM format.
- **Relations**: prefer inline `[[wikilinks]]` woven into prose. Use a
  `## Relations` section only as fallback when no natural inline spot
  exists. Never use `- relation_type [[...]]` — that is BM format.
- **Wikilinks** must point to existing files — orphan links create empty
  files at the vault root. Verify before linking.
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

Prose body — context, what happened this session, decisions made with
rationale, learnings and surprises woven in. Past tense, natural language.
Wikilinks inline to related notes (e.g. [[YYYY-MM-DD — Previous Session]],
[[Decision Theme]]). Hashtags inline where a fact warrants tagging.

## Open Items

- [ ] Pending work, blockers, next steps
```

Fallback sections (only when no inline opportunity exists):

```markdown
## Observations

- #category content

## Relations

- [[Related Note]]
```

#### Write

```
write_note(
  path="{obsidian.path}/Sessions/YYYY-MM-DD — Description.md",
  content="Prose body...\n\n## Open Items\n- [ ] ...",
  frontmatter={title: "...", type: "session", tags: ["session", ...base_tags, ...context_tags]}
)
```

Rules:
- Prose body is the core — weave decisions, learnings, and wikilinks in
- `## Open Items` is the only standard section; add only if there are items
- Fallback sections only when inline is not natural
- Past tense, natural language
- No git metadata (branches, commits, PRs) or file lists
- One project per session note

### 2. Create decision notes (conditional)

Only when BM decision notes were created in step 4 of bm-notes.md.
One Obsidian decision note per BM decision note created.

#### Determine path

- Folder: `{obsidian.path}/Decisions/`
- Filename: `Title — Decision Theme.md`
- Example: `Work/Acme/Decisions/Decision Note Format.md`

#### Check for existing note

```
search_notes query="Decision Theme" path="{obsidian.path}/Decisions/"
```

If a match exists for the same theme, read it with `read_note` and
update with `patch_note`.

#### Decision template

```markdown
---
title: "Decision Title"
type: decision
tags:
  - decision
  - {base tags from mapping}
  - {context tags from content}
---

## Context

Prose — what prompted the decision, background, constraints, rationale,
alternatives considered. Rich enough for a reader weeks later to follow
without asking. Wikilinks inline to related decisions or sessions
(e.g. [[Adjacent Theme]], [[YYYY-MM-DD — Session]]). Hashtags inline where
a fact warrants tagging.

## Decisions

### 1. Short title

Rationale, alternatives considered, why this was chosen. One subsection
per distinct decision.
```

Fallback sections (only when no inline opportunity exists):

```markdown
## Observations

- #category content

## Relations

- [[Related Note]]
```

Rules:
- `## Context` prose and `## Decisions` section are required
- One decision note per theme — group related decisions, not per session
- Mirror the BM decision note content adapted to Obsidian format
- Fallback sections only when inline is not natural

### 3. Create or update daily note

#### Path

Always `Daily/YYYY-MM-DD.md`.

#### Daily template

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
the day's work on this project. Wikilinks inline to the session note
(e.g. [[YYYY-MM-DD — Description]]). Past tense, natural language.

### {Another Project}

...

## Open Items

- [ ] Pending work, blockers, next steps
```

Fallback sections (only when no inline opportunity exists):

```markdown
## Observations

- #category content

## Relations

- [[Related Note]]
```

#### If note does not exist

Compose content following the template above. Only `## Activities` is
required; omit `## Open Items` and fallback sections if empty.

```
write_note(
  path="Daily/YYYY-MM-DD.md",
  content="## Activities\n...",
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
- Consolidate fallback `## Observations` and `## Relations` the same way
  — merge existing with new, deduplicate, keep only distinct items

Rules:
- Activities split by project with `### Project Name` headers
- One prose paragraph per project (2-4 sentences) after consolidation
- Past tense, natural language
- Do not duplicate detail from the session note — daily stays
  summary-level
- Omit empty sections entirely

## Guidelines

**DO:**
- Search before creating with `search_notes` to avoid duplicates
- Read existing note before patching (daily, session updates)
- Prefer prose body + inline wikilinks/hashtags over standalone sections
- Use `## Observations` / `## Relations` only as fallback
- Tag every note as `[note-type, ...base_tags, ...context_tags]` —
  `note-type` is one of `session`, `decision`, `daily`; `base_tags`
  come from mapping output; `context_tags` are derived from the session
  content (work type, topics)
- Use Title Case for folders and filenames
- Omit empty sections — no placeholder headers
- Keep daily note as outcomes and decisions, not detailed log

**DON'T:**
- Call any skill — use MCPVault MCP tools directly
- Use `[brackets]` for observations (that is BM format)
- Use `- relation_type [[...]]` for relations (that is BM format)
- Add `# H1` to any note — frontmatter `title` is the canonical heading
- Write changelog-style content or list steps taken
- List files modified or git metadata
- Blindly append bullets without reading existing content first
- Let any daily project paragraph exceed 4 sentences — consolidate
- Duplicate full detail from BM notes into Obsidian notes
- Create empty sections or placeholder content
- Create wikilinks to files that don't exist (orphan links)
