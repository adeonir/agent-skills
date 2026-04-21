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

- **Observations**: `- #category content` (hashtags, not `[brackets]`)
- **Relations**: `- [[Note Title]]` (wikilinks only, not `- relation_type [[...]]`)
- **Frontmatter**: YAML with `title`, `type`, `tags`
- The `title` in frontmatter must match the `# Heading` in the body
- Wikilinks must point to existing files — orphan links create empty
  files at the vault root. Verify before linking.

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

Compose the body following this template exactly. Omit empty sections.

```markdown
---
title: "YYYY-MM-DD — Description"
type: session
tags:
  - session
  - {base tags from mapping}
  - {context tags from content}
---

# YYYY-MM-DD — Description

## Summary

- {2-5 bullets describing context, outcomes, and decisions.
  Past tense, natural language. Focus on what was achieved
  and why, not steps taken.}

## Key Decisions

- {Decision + rationale (why, not just what)}

## Open Items

- [ ] {Pending work, blockers, next steps}

## Learnings

- {Discoveries, surprises, gotchas}

## Observations

- #category {Observation with context}

## Relations

- [[Related Note]]
```

#### Write

```
write_note(
  path="{obsidian.path}/Sessions/YYYY-MM-DD — Description.md",
  content="# YYYY-MM-DD — Description\n\n## Summary\n...",
  frontmatter={title: "...", type: "session", tags: ["session", ...base_tags, ...context_tags]}
)
```

Rules:
- Only `## Summary` is required. All other sections are optional.
- Omit empty sections entirely — do not leave headers with no content.
- Past tense, natural language — outcomes and decisions, not steps taken.
- No git metadata (branches, commits, PRs) or file lists.
- One project per session note.

### 2. Create decision notes (conditional)

Only when BM decision notes were created in step 5 of bm-notes.md.
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

# Decision Title

## Context

{Context — what prompted the decision, background, constraints.
Rich prose, not just bullets. Enough for someone to understand
weeks later without asking.}

## Decisions

### 1. Short title

{Rationale, alternatives considered, why this was chosen.
One subsection per distinct decision.}

## Observations

- #decision {Key decision condensed}
- #rationale {Why this choice over alternatives}
- #constraint {Limitation that shaped the decision}

## Relations

- [[Related Note]]
```

Rules:
- `## Context` prose and `## Decisions` section are required.
- One decision note per theme — group related decisions, not per session.
- Mirror the BM decision note content adapted to Obsidian format.
- Omit empty sections.

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

# DayOfWeek, Month DD, YYYY

## Activities

### {Project Name}

- {3-5 bullets per project. Past tense, natural language.
  Capture outcomes and decisions, not steps taken.
  Each bullet must make sense weeks later without extra context.}

## Key Decisions

- {Decision + rationale (why, not just what)}

## Learnings

- {Discoveries, surprises, gotchas}

## Open Items

- [ ] {Pending work, blockers, next steps}

## Observations

- #category {Observation with context}

## Relations

- [[Related Note]]
```

#### If note does not exist

Compose content following the template above. Only `## Activities`
is required; omit other sections if empty.

```
write_note(
  path="Daily/YYYY-MM-DD.md",
  content="...",
  frontmatter={title: "...", type: "daily", tags: [...]}
)
```

#### If note already exists

Read first with `read_note`, then use `patch_note`:
- If the project already has a subsection in Activities, rewrite the
  entire subsection: merge existing bullets with new activities and
  consolidate into 3-5 summary bullets that cover the full day
- If the project is new, add a `### Project Name` subsection at the end
  of Activities (before the next `##` section)
- Add items to Key Decisions, Learnings, Open Items, Observations, and
  Relations if relevant (create sections if they do not exist)
- Consolidate Observations and Relations the same way: merge existing
  with new, deduplicate, keep only distinct items

Rules:
- Activities split by project with `### Project Name` headers
- Past tense, natural language
- 3-5 bullets per project after consolidation — capture outcomes and
  decisions, not steps taken
- Do not duplicate detail from the session note — keep summary-level
- Omit empty sections entirely

## Guidelines

**DO:**
- Search before creating with `search_notes` to avoid duplicates
- Read existing note before patching (daily, session updates)
- Follow the full template — frontmatter + all relevant sections
- Tag every note as `[note-type, ...base_tags, ...context_tags]` —
  `note-type` is one of `session`, `decision`, `daily`; `base_tags`
  come from mapping output; `context_tags` are derived from the session
  content (work type, topics)
- Use `#hashtags` for observations (Obsidian format)
- Use `[[wikilinks]]` for relations (verify target exists)
- Keep daily note as outcomes and decisions, not detailed log
- Link session note from daily note Relations
- Use Title Case for folders and filenames
- Omit empty sections — no placeholder headers

**DON'T:**
- Call any skill — use MCPVault MCP tools directly
- Use `[brackets]` for observations (that is BM format)
- Use `- relation_type [[...]]` for relations (that is BM format)
- Write changelog-style content or list steps taken
- List files modified or git metadata
- Blindly append bullets without reading existing content first
- Let any project subsection exceed 5 bullets — consolidate
- Duplicate full detail from BM notes into Obsidian notes
- Create empty sections or placeholder content
- Create wikilinks to files that don't exist (orphan links)
