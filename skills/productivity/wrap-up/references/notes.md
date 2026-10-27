# Write Obsidian Notes

Create session notes in the project folder and update the daily note in the Obsidian vault.

## When to Use

Loaded to write the notes themselves. The session note is written when `obsidian.path` is not `--`; the daily note is always written, even when the session note is skipped. Both consume the resolved Obsidian path and base tags, plus whatever the handoff Load phase put in working context.

## Contents

- Vault Access
- Obsidian Syntax Rules
- Audience and Reference Discipline
- Subject Matter
- Filename Sanitization
- Workflow: 1. Create session note, 2. Create or update daily note, 3. Offer to archive past months
- Guidelines
- Error Handling

## Vault Access

Every write or read goes through one channel, tried in this order. Never open the Obsidian app or focus its window yourself.

1. **CLI (default).** `obsidian` ships with the desktop app. When `command -v obsidian` finds it, run its commands. The CLI works only while the app runs; with the app closed, a command fails with `The CLI is unable to find Obsidian. Please make sure Obsidian is running and try again.`
2. **MCP (fallback).** When the CLI binary is missing or the app is closed, use the Obsidian MCP tools (`Obsidian:read_note`, `Obsidian:write_note`, `Obsidian:patch_note`, and kin).
3. **Direct vault write (last).** When neither the CLI nor the MCP tools are available, write the notes as plain files into the vault resolved from Obsidian's `obsidian.json`: the only vault, or the open one.

Operations on the CLI. Every command opens with `vault="<vault>"`, the folder name of the vault resolved as in Direct vault write; without it, the CLI fails with `Vault not found.` when no vault is active:

| Operation | Command |
|---|---|
| Search | `obsidian vault="<vault>" search query="<query>" path="<folder>/" format=json` |
| Read | `obsidian vault="<vault>" read path="<path>"` |
| Create | `obsidian vault="<vault>" create path="<path>" content="$(cat "<temp-file>")"` — the value is the whole note, frontmatter included. The CLI turns every `\n` and `\t` in the value into a newline and a tab, with no escape; when the note text holds a literal `\n` or `\t`, write it as a plain file into the vault, as in Direct vault write |
| Patch | read the note, edit the text, then run Create with the `overwrite` flag — a patch is read-modify-rewrite |
| List a folder | `obsidian vault="<vault>" files folder="<folder>/"` |
| Move | `obsidian vault="<vault>" move path="<path>" to="<dest>"` — both endpoints vault-relative; updates links when the vault has Automatically update internal links turned on |

Only the CLI Move updates links. The MCP `Obsidian:move_note` and a plain file write leave every wikilink to the moved note unchanged, so a move of linked notes runs only on the CLI; when the CLI is unavailable, report the path and skip.

## Obsidian Syntax Rules

Obsidian notes render for humans (Graph view, daily review, Dataview). Keep notes brief and scannable — prose narrative up front, structured sections below, typed relations for graph edges.

- **Frontmatter**: YAML with `title`, `type`, `tags`
- **Observations**: daily notes only. Bullets under `## Observations` formatted as `- #category content`. Category is free-form (examples: `#pattern`, `#method`, `#cadence`, `#blocker`, `#mood`). Use `#hashtags`, not `[brackets]`.
- **Relations**: each relation is a verb followed by a wikilink under `## Relations`: `- follows [[Target]]`. Common verbs: `follows`, `part_of`, `contains`, `expands`, `relates_to`, `implements`, `requires`, `replaces`, `pairs_with`, `extends`, `depends_on`. Use inline `[[wikilinks]]` for ordinary mentions. Add a relation only for an explicit connection between notes.
- **Wikilinks**: only to existing notes or entity files. Orphan links create empty files at the vault root — verify each target with Search in Vault Access, run without `path` so it covers the whole vault, before linking.
- **H1 heading**: all notes omit the body `# H1` — the frontmatter `title` is the canonical heading. Top-level body sections start at `##`.
- **Prose**: past tense, natural language. Omit every empty section.

## Audience and Reference Discipline

Session and daily notes target different audiences. The split is rigid and governs everything that lands in a note, including material folded in from a handoff — the handoff's scope is not the note's scope.

| | Daily | Session |
|---|---|---|
| Reader | stakeholder or future-you scanning what moved | future-you continuing the work |
| Carries | outcomes at product or project level, in prose; never restates the session's technical detail | the technical detail of the work itself |
| Refs allowed | project and feature names only | PR `#N`, Issue `#N`, file paths, commands, `file:line` |
| Refs forbidden | PR/Issue numbers, file paths, shell commands, branch names, commit hashes | branch names, commit hashes |

Both notes carry only references that remain valid after the work ends. Do not include an identifier that belongs to a workspace artifact. The artifact can be deleted and leave the reference without a target. Name the work in prose instead (`Checkout Refactor`).

## Subject Matter

Both notes carry the work, never the session that produced it. A note records what the project now is and why, so how the assistant arrived there does not belong in either one.

A fact that changed the project's code, configuration, or content stays, stated as the project fact it became. Three tests decide a borderline line: it holds true for anyone reading the repository months later, it reads the same whether a person or an assistant did the work, and a reader tomorrow, in a week, or in a month would use it to understand or continue the project. A line that fails any test is process or noise — cut it.

Keep out of both notes:

- Mechanics of the session — which steps ran, how work was split, what a subagent did or wrote
- Failures and retries of agents, subagents, or tools, unless the cause is a defect in the project
- State of the working tree — uncommitted or unstaged files, files left to review, leftover artifacts, checkbox progress in spec or task files; a pending item enters `## Next` or `## Open Items` only as project work that remains
- Quirks of the assistant's own tooling, unless the workaround now lives in the project
- Self-correction — a wrong assumption later fixed, a file created by mistake, a value first guessed and then measured
- The exchange behind a decision — "as discussed", "the user confirmed", "we agreed", "the assistant suggested"; a rationale or a rejected alternative is stated as a fact about the project

A recurring practice belongs in the daily note's `## Observations`, at day level and stated as practice. A method tried once in a session is process and stays out of both notes.

## Filename Sanitization

When generating filenames from user input:

- Remove characters the OS rejects or Obsidian links break on: `/ \ : * ? " < > | # ^ [ ] %`
- Preserve accented characters — Obsidian imposes no charset limit beyond the filesystem's
- Use Title Case for all filenames
- Example: `What's Next?` becomes `Whats Next.md`

## Workflow

Compose each note in full before writing it, then check the draft line by line against Audience and Reference Discipline and the three Subject Matter tests. Rewrite or cut every line that fails, and write only a draft with no failing line.

### 1. Create session note

#### Determine path

- Folder: `<obsidian.path>/Sessions/`
- Filename: `YYYY-MM-DD — Description.md`
- Example: `Work/Acme/Sessions/YYYY-MM-DD — Checkout Refactor.md`

#### Check for existing note

```text
obsidian vault="<vault>" search query="YYYY-MM-DD" path="<obsidian.path>/Sessions/" format=json
```

If a match exists for the same date and topic, read it and append a new section with Patch (horizontal rule `---` plus date header as separator). Otherwise create a new note.

#### Session template

ALWAYS use this exact template structure:

```markdown
---
title: "YYYY-MM-DD — [Description]"
type: session
tags:
  - session
  - [base tags from mapping]
  - [context tags from content]
---

## Summary

[2-3 sentence narrative: what happened, key outcome, why it matters. Inline wikilinks only to existing notes.]

## Decisions

- [Decision + rationale + named alternative rejected, when a real option was considered]

## Findings

- [Brief finding worth capturing]

## Problems

- [Problem in the project + root cause + fix]

## Next

- [Entry point for next session: file, function, path, or command]

## Relations

- follows [[Previous Session]]
- part_of [[Project]]
```

MUST NOT contain: branch names, commit hashes, identifiers of workspace artifacts, session mechanics, self-correction, the exchange behind a decision.

Section presence:
- `## Summary` always present
- `## Decisions` when decisions were made
- `## Findings` when there is a notable discovery about this codebase, its stack, or the project's tooling
- `## Problems` when a problem in the project was encountered and resolved or noted
- `## Next` when there is work to continue
- `## Relations` for explicit connections between notes

When the handoff Load phase provides content, include it before composing the note:

- `**Findings:**` → brief bullets in `## Findings`
- `**Decisions:**` → `## Decisions` bullets with rationale (name rejected alternatives when applicable)
- `**Next step:**` and `**Open threads:**` → `## Next` bullets, preserving the concrete entry point
- `**Blockers:**` → `## Problems` bullets when applicable, or `## Next` flagged as blocking
- `**Focus:**`, `**Context:**`, and `**References:**` → contribute to the `## Summary` narrative; not a dedicated section

#### Write

Create the note with Create — the content carries the frontmatter and the body together.

Rules:
- Keep each section brief — this is a human note, not an AI knowledge base
- Findings and Problems: brief bullets only, no detailed narratives
- One project per session note

### 2. Create or update daily note

#### Path

`Daily/YYYY-MM-DD.md`, at the root of `Daily/` — that is where a daily note is created when none exists for the date.

Past months are archived into `Daily/YYYY-MM/` folders. Search for the date before writing: when a note for that date already sits in a monthly folder, patch it there rather than creating a second one at the root. Archiving runs only after the daily note is written; never move a note as part of writing it.

#### Daily template

The title carries the calendar day the note covers, weekend included.

ALWAYS use this exact template structure:

```markdown
---
title: "[Weekday, Month D, YYYY]"
type: daily
tags:
  - daily
  - [base tags from mapping]
  - [context tags from content]
---

## Activities

### [Project Name]

- [Outcome or task, with an inline wikilink to the session note on the first bullet, e.g. [[YYYY-MM-DD — Description]]]
- [Another outcome or task]

### [Another Project]

- ...

## Open Items

- [ ] [Pending work, blockers, next steps]

## Observations

- #category [cross-cutting observation: patterns, methods, cadence, blockers, mood]

## Relations

- contains [[YYYY-MM-DD — Session Note]]
```

MUST NOT contain: PR or Issue numbers, file paths, shell commands, branch names, commit hashes, the session's technical detail.

Section presence:
- `## Activities` always present, split by project with `### Project Name` headers, at least one project subsection
- `## Open Items` only when commitments have an owner, a deadline, or an active blocker — mental follow-ups ("install X locally", "remember to test Y") belong in the handoff or session `## Next`, not here
- `## Observations` for cross-cutting day-level facts — a recurring practice, never a method tried once in a session; project-specific facts stay in the session note
- `## Relations` for `contains` links to today's session notes or other day-level references

#### If note does not exist

Compose content following the template above, then create the note with Create.

#### If note already exists

Read it first, then Patch it:
- If the project already has a subsection in Activities, merge the existing bullets with new bullets — deduplicate, keep distinct items
- If the project is new, add a `### Project Name` subsection at the end of Activities (before the next `##` section)
- Add items to Open Items if relevant (create the section if it does not exist)
- Consolidate `## Observations` and `## Relations` the same way — merge existing with new, deduplicate, keep only distinct items

### 3. Offer to archive past months

After the daily note is written, list `Daily/` with `obsidian vault="<vault>" files folder="Daily/"` and collect the `YYYY-MM-DD.md` files at its root whose month is earlier than the current month. When none exist, skip this step silently.

When some exist, include them in the end-of-run report grouped by target folder, and ask one question: move them into `Daily/YYYY-MM/`? It comes after the report, never before a write. On yes, move each note with Move, which needs the CLI; when the CLI is unavailable, report the paths and leave the notes at the root. Report the count moved per folder. On no, leave them at the root. If a move fails, report the failed path and continue with the rest.

## Guidelines

- Tag every note `[note-type, ...base_tags, ...context_tags]` — `note-type` is `session` or `daily`, `base_tags` come from mapping output, `context_tags` are derived from the session content
- Never write changelog-style content or a list of steps taken

## Error Handling

- Obsidian CLI binary missing or app closed: use the MCP tools; both unavailable: write the notes as plain files into the vault. A move without the CLI: report and leave the notes at the root. Never open the Obsidian app or focus its window.
- No meaningful session content: keep the session note brief, still update the daily note
