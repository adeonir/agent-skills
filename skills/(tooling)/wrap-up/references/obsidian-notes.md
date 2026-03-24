# Write Obsidian Notes

Create session note in the project folder and update the daily note.

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
- Example: `Ventures/Pensefy/2026-03-22 — BM Reorganization.md`

#### Check for existing note

Search the target folder for a file matching the same date and topic.
If found, append a new section with `patch_note` (horizontal rule
separator and date header).

#### Compose content

```markdown
---
title: 'YYYY-MM-DD — Description'
type: session
tags:
  - session-note
  - {dynamic tags based on content}
---
# YYYY-MM-DD — Description

**Branch:** branch-name
**PR:** pr-url
**Commit:** short-hash commit message

## What Was Done

- 2-5 bullets in past tense, natural language (not changelog)

## Files Modified

- path/to/file -- what changed

## Key Decisions

- Decision + rationale

## Open Items

- [ ] Pending work, blockers, next steps

## Learnings

- Discoveries, surprises, gotchas

## Observations

- #category Observation with context

## Relations

- [[Related Note]]
```

Rules:
- Git metadata only when available, omit entirely if not in a repo
- Omit empty sections
- Past tense, natural language, not changelog
- Observations use `#hashtags` (Obsidian format)
- Use session-notes skill (MCPVault MCP) for write/patch

### 2. Create or update daily note

#### Path

Always `Daily/YYYY-MM-DD.md`.

#### If note does not exist

Create with full template:

```markdown
---
title: 'DayOfWeek, Month DD, YYYY'
type: daily
tags:
  - daily
  - {dynamic tags based on content}
---
# DayOfWeek, Month DD, YYYY

## Activities

### Project Name

- 2-3 bullets per project (past tense, natural language, not changelog)

## Key Decisions

- Decision + rationale

## Learnings

- Discoveries, surprises, gotchas

## Open Items

- [ ] Pending work, blockers, next steps

## Observations

- #category Observation with context

## Relations

- [[Related Note]]
```

#### If note already exists

Use `patch_note` to insert content:
- If the project already has a subsection in Activities, append bullets
- If the project is new, add a `### Project Name` subsection at the end
  of Activities (before the next `##` section)
- Add items to Key Decisions, Learnings, Open Items, Observations, and
  Relations if relevant (create sections if they do not exist)

Rules:
- Activities split by project with H3 headers
- Past tense, natural language, 2-3 bullets per project
- Do not duplicate detail from the session note -- keep it summary-level
- Omit empty sections
- Use session-notes skill (MCPVault MCP) for write/patch

## Guidelines

**DO:**
- Search before creating to avoid duplicates
- Use session-notes skill for all Obsidian writes
- Keep daily note as executive summary, not detailed log
- Link session note from daily note Relations

**DON'T:**
- Use [brackets] in Obsidian observations (Obsidian uses #hashtags)
- Write changelog-style content
- Duplicate full detail from BM notes into Obsidian notes
- Create empty sections or placeholder content
