# Write Obsidian Notes

Create session and decision notes in the project folder and update
the daily note.

> **LOAD FIRST:** [mapping.md](mapping.md) -- provides Obsidian folder

## When to Use

- Obsidian session note: when Obsidian folder is not `--`
- Daily note: always (even when session note is skipped)
- Runs after BM notes

## Workflow

### 1. Create session note

#### Determine path

- Folder: `{Obsidian folder}/{Project Name}/` (Title Case)
- Filename: `YYYY-MM-DD — Description.md`
- Example: `Ventures/Pensefy/Session/2026-03-22 — BM Reorganization.md`

#### Check for existing note

Search the target folder for a file matching the same date and topic.
If found, append a new section with `patch_note` (horizontal rule
separator and date header).

#### Compose content

Use session-notes skill (MCPVault MCP) to create the note.

Rules:
- Omit empty sections
- Past tense, natural language -- outcomes and decisions, not steps taken
- No git metadata (branches, commits, PRs) or file lists
- Observations use `#hashtags` (Obsidian format)
- Use session-notes skill (MCPVault MCP) for write/patch

### 2. Create decision notes (conditional)

Only when BM decision notes were created in step 5 of bm-notes.md.
One Obsidian decision note per BM decision note created.

#### Determine path

- Folder: `{Obsidian folder}/{Project Name}/Decisions/` (Title Case)
- Filename: `Title — Decision Theme.md`
- Example: `Projects/My Skills/Decisions/Decision Note Format.md`

#### Check for existing note

Search the target folder for a file matching the same theme.
If found, update with `patch_note`.

#### Compose content

Use session-notes skill (MCPVault MCP) to create the note.
Mirror the BM decision note content adapted to Obsidian format.

Rules:
- Observations use `#hashtags` (Obsidian format)
- Omit empty sections
- Use session-notes skill for write/patch

### 3. Create or update daily note

#### Path

Always `Daily/YYYY-MM-DD.md`.

#### If note does not exist

Use session-notes skill (MCPVault MCP) to create the note.

#### If note already exists

Read the existing note first with `read_note`, then use `patch_note`
to update:
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
- Activities split by project with H3 headers
- Past tense, natural language, 3-5 bullets per project after
  consolidation -- capture outcomes and decisions, not steps taken
- Do not duplicate detail from the session note -- keep it summary-level
- Omit empty sections
- Use session-notes skill (MCPVault MCP) for write/patch

## Guidelines

**DO:**
- Search before creating to avoid duplicates
- Use session-notes skill for all Obsidian writes
- Keep daily note as outcomes and decisions, not detailed log
- Read existing daily note before patching to consolidate content
- Link session note from daily note Relations

**DON'T:**
- Use [brackets] in Obsidian observations (Obsidian uses #hashtags)
- Write changelog-style content or list steps taken
- List files modified or git metadata
- Blindly append bullets without reading existing content first
- Let any project subsection exceed 5 bullets -- consolidate
- Duplicate full detail from BM notes into Obsidian notes
- Create empty sections or placeholder content
