# Write Obsidian Notes

Create session notes in the project folder and update the daily note using Obsidian MCP tools directly.

## When to Use

- Obsidian session note: when `obsidian.path` is not `--`
- Daily note: always (even when session note is skipped)
- Runs after the handoff Load phase
- Depends on mapping output (Obsidian path, base tags) and on the handoff Load phase (all snapshots folded, grouped by date — Findings → Findings, Decisions → Decisions, Next step + Open threads → Next)

## Obsidian Syntax Rules

Obsidian notes render for humans (Graph view, daily review, Dataview). Keep notes brief and scannable — prose narrative up front, structured sections below, typed relations for graph edges.

- **Frontmatter**: YAML with `title`, `type`, `tags`
- **Observations**: daily notes only. Bullets under `## Observations` formatted as `- #category content`. Category is free-form (examples: `#pattern`, `#method`, `#cadence`, `#blocker`, `#mood` — day-level cross-cutting facts). Use `#hashtags`, not `[brackets]`. Session notes do not have an Observations section.
- **Relations**: typed verb + wikilink under `## Relations`: `- follows [[Target]]`. Common types: `follows`, `part_of`, `expands`, `relates_to`, `implements`, `requires`, `replaces`, `pairs_with`, `extends`, `depends_on`. Inline `[[wikilinks]]` in prose cover ordinary mentions; the Relations section holds typed edges that add graph value.
- **Wikilinks**: only to existing notes or entity files. Orphan links create empty files at the vault root — verify before linking.
- **H1 heading**: all notes omit the body `# H1` — the frontmatter `title` is the canonical heading. Top-level body sections start at `##`.

## Audience and Reference Discipline

Session and daily notes target different audiences. The split is rigid and governs everything that lands in a note, including material folded in from a handoff — the handoff's scope is not the note's scope.

| | Daily | Session |
|---|---|---|
| Reader | stakeholder or future-you scanning what moved | future-you continuing the work |
| Carries | outcomes at product or project level, in prose; never restates the session's technical detail | the technical detail itself |
| Refs allowed | project and feature names only | PR `#N`, Issue `#N`, file paths, commands, `file:line` |
| Refs forbidden | PR/Issue numbers, file paths, shell commands, branch names, commit hashes | branch names, commit hashes |

Both notes carry only references that outlive the work they describe. An identifier scoped to a workspace artifact is forbidden in either note — the artifact can be deleted, leaving the reference pointing at nothing. Name the work in prose instead (`Checkout Refactor`).

## Filename Sanitization

When generating filenames from user input:

- Remove invalid characters: `/ \ : * ? " < > |`
- Preserve accented characters (valid in filenames)
- Use Title Case for all filenames
- Example: `What's Next?` becomes `Whats Next.md`

## Obsidian Tools

Call these directly — do not invoke any skill.

| Tool | Purpose |
|------|---------|
| `Obsidian:write_note` | Create new note with content and frontmatter |
| `Obsidian:read_note` | Read existing note before patching |
| `Obsidian:patch_note` | In-place update (oldString → newString) |
| `Obsidian:search_notes` | Search-before-create, find existing notes |

Always search before creating to avoid duplicates.

## Workflow

### 0. Enrich working context

The claude-mem MCP is an **optional** dependency: notes composed without it are complete, not degraded. When the MCP is present (`mcp__plugin_claude-mem_mcp-search__*`), query it for **current-session** observations relevant to the resolved project before composing notes, recovering mid-session detail that scrolled out of context.

**Scoping rules (mandatory — do not pollute working context):**

- **Time**: current session window only — exclude prior sessions
- **Topic**: filter by project name and the threads already active in the wrap-up; skip parallel unrelated topics from the same session
- **Budget**: top 5-10 most relevant observations, no broad sweeps
- **Fallback**: silent skip when MCP unavailable or returns nothing

The goal is recovering lost session detail before composing executive narrative — not importing history or adjacent threads. Notes stay human-readable: observation IDs do not enter note bodies, consistent with the no-commit-hashes rule.

### Per-date handling

The handoff Load phase groups loaded snapshots by date. When the snapshots span multiple dates, run steps 1-2 once **per date group**: each date gets its own session note(s) and its own daily note, folding only that date's blocks. A single date is the common case — treat multi-date as the exception, not the default.

### 1. Create session note

#### Determine path

- Folder: `{obsidian.path}/Sessions/`
- Filename: `YYYY-MM-DD — Description.md`
- Example: `Work/Acme/Sessions/YYYY-MM-DD — Checkout Refactor.md`

#### Check for existing note

```text
Obsidian:search_notes query="YYYY-MM-DD" path="{obsidian.path}/Sessions/"
```

If a match exists for the same date and topic, read it with `Obsidian:read_note` and append a new section with `Obsidian:patch_note` (horizontal rule `---` plus date header as separator). Otherwise create a new note.

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

When the handoff Load phase surfaced grouped snapshots, fold this date's bullets in before composing the note — the deduplicated union across that day's blocks, not just the latest. Re-apply the Audience and Reference Discipline as you fold.

- `**Findings:**` → brief bullets in `## Findings`
- `**Decisions:**` → `## Decisions` bullets with rationale (name rejected alternatives when applicable)
- `**Next step:**` and `**Open threads:**` → `## Next` bullets, preserving the concrete entry point
- `**Blockers:**` → `## Problems` bullets when applicable, or `## Next` flagged as blocking
- `**Focus:**` and `**References:**` → contribute to the `## Summary` narrative; not a dedicated section
- `**State:**` → nothing; it does not enter either note

#### Write

```text
Obsidian:write_note(
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
- Wikilinks only to existing notes/entities; verify with `Obsidian:search_notes` before linking
- Past tense, natural language
- One project per session note
- Omit empty sections

### 2. Create or update daily note

#### Path

`Daily/YYYY-MM-DD.md`, at the root of `Daily/` — that is where a daily note is created when none exists for the date.

Past months are archived into `Daily/YYYY-MM/` folders. Search for the date before writing: when a note for that date already sits in a monthly folder, patch it there rather than creating a second one at the root. Never create the monthly folder — archiving is not this skill's operation.

#### Daily template

Activities per project (bullet list), Open Items for pending work, Observations for day-level facts that cut across projects, Relations for typed edges to today's session notes.

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
- `## Open Items` only when commitments have an owner, a deadline, or an active blocker — mental follow-ups ("install X locally", "remember to test Y") belong in the handoff or session `## Next`, not here
- `## Observations` for cross-cutting day-level facts — do not restate per-project observations that belong in the session note; common categories: `#pattern`, `#method`, `#cadence`, `#blocker`, `#mood`
- `## Relations` typed edges to today's session notes (`contains`) or other day-level references; omit if no sessions or references

#### If note does not exist

Compose content following the template above. Only `## Activities` is required; omit empty sections.

```text
Obsidian:write_note(
  path="Daily/YYYY-MM-DD.md",
  content="## Activities\n...\n\n## Relations\n- contains [[...]]",
  frontmatter={title: "...", type: "daily", tags: [...]}
)
```

#### If note already exists

Read first with `Obsidian:read_note`, then use `Obsidian:patch_note`:
- If the project already has a subsection in Activities, merge the existing bullets with new bullets — deduplicate, keep distinct items
- If the project is new, add a `### Project Name` subsection at the end of Activities (before the next `##` section)
- Add items to Open Items if relevant (create the section if it does not exist)
- Consolidate `## Observations` and `## Relations` the same way — merge existing with new, deduplicate, keep only distinct items

Rules:
- Activities split by project with `### Project Name` headers
- Observations are day-level and cross-cutting — project-specific facts stay in the session note
- Relations use typed verbs (`contains`, `relates_to`); `contains` points to today's session notes
- Past tense, natural language
- Omit empty sections entirely

## Guidelines

- Write notes immediately — no preview message, no rendered-content dump, no "about to write..." narration. The user invoked wrap-up to persist, not to review drafts in chat.
- Tag every note `[note-type, ...base_tags, ...context_tags]` — `note-type` is `session` or `daily`, `base_tags` come from mapping output, `context_tags` are derived from the session content
- Never write changelog-style content or a list of steps taken

## Error Handling

- Obsidian MCP unavailable: skip the Obsidian step entirely, warn the user
- No meaningful session content: keep the session note brief, still update the daily note
