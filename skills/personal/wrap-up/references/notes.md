# Write Obsidian Notes

Create session notes in the project folder and update the daily note using Obsidian MCP tools directly.

## When to Use

- Obsidian session note: when `obsidian.path` is not `--`
- Daily note: always (even when session note is skipped)
- Runs after the handoff Load phase
- Depends on mapping output (Obsidian path, base tags) and on the handoff Load phase (Findings → Findings, Decisions → Decisions, Next step + Open threads → Next)

## Obsidian Syntax Rules

Obsidian notes render for humans (Graph view, daily review, Dataview). Keep notes brief and scannable — prose narrative up front, structured sections below, typed relations for graph edges.

- **Frontmatter**: YAML with `title`, `type`, `tags`
- **Observations**: daily notes only. Bullets under `## Observations` formatted as `- #category content`. Category is free-form (examples: `#pattern`, `#method`, `#cadence`, `#blocker`, `#mood` — day-level cross-cutting facts). Use `#hashtags`, not `[brackets]`. Session notes do not have an Observations section.
- **Relations**: each relation is a verb followed by a wikilink under `## Relations`: `- follows [[Target]]`. Common verbs: `follows`, `part_of`, `expands`, `relates_to`, `implements`, `requires`, `replaces`, `pairs_with`, `extends`, `depends_on`. Use inline `[[wikilinks]]` for ordinary mentions. Use the Relations section for explicit connections between notes.
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

Both notes carry only references that remain valid after the work ends. Do not include an identifier that belongs to a workspace artifact. The artifact can be deleted and leave the reference without a target. Name the work in prose instead (`Checkout Refactor`).

## Filename Sanitization

When generating filenames from user input:

- Remove characters the OS rejects or Obsidian links break on: `/ \ : * ? " < > | # ^ [ ] %`
- Preserve accented characters — Obsidian imposes no charset limit beyond the filesystem's
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
- `## Relations` for explicit connections between notes

When the handoff Load phase provides content, include it before composing the note. Apply the Audience and Reference Discipline to that content.

- `**Findings:**` → brief bullets in `## Findings`
- `**Decisions:**` → `## Decisions` bullets with rationale (name rejected alternatives when applicable)
- `**Next step:**` and `**Open threads:**` → `## Next` bullets, preserving the concrete entry point
- `**Blockers:**` → `## Problems` bullets when applicable, or `## Next` flagged as blocking
- `**Focus:**`, `**Context:**`, and `**References:**` → contribute to the `## Summary` narrative; not a dedicated section

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
- Write a relation as a verb followed by a wikilink (`- follows [[X]]`). Add a relation only when it records an explicit connection between notes.
- Wikilinks only to existing notes/entities; verify with `Obsidian:search_notes` before linking
- Past tense, natural language
- One project per session note
- Omit empty sections

### 2. Create or update daily note

#### Path

`Daily/YYYY-MM-DD.md`, at the root of `Daily/` — that is where a daily note is created when none exists for the date.

Past months are archived into `Daily/YYYY-MM/` folders. Search for the date before writing: when a note for that date already sits in a monthly folder, patch it there rather than creating a second one at the root. Never create the monthly folder — archiving is not this skill's operation.

#### Daily template

Use Activities for project work, Open Items for pending work, Observations for day-level facts that apply across projects, and Relations for explicit connections to today's session notes.

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
- `## Relations` for explicit connections to today's session notes (`contains`) or other day-level references; omit if no sessions or references

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
