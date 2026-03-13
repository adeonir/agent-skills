---
name: session-notes
description: >-
  Create and manage Obsidian notes for projects, companies, technical
  challenges, brag documents, daily logs, AI conversations, and quick captures
  using the Obsidian CLI. Use when documenting projects, tracking job
  applications, recording interview challenges, maintaining brag documents,
  creating daily notes, or saving AI conversations. Triggers on "create
  project", "new project note", "document company", "job application",
  "technical challenge", "brag document", "daily note", "today's log",
  "obsidian note", "save conversation", "chat summary", "session summary",
  "save this", "capture this", "quick note".
license: MIT
metadata:
  author: Adeonir Kohl
---

# Session Notes

Create and manage Obsidian notes using the Obsidian CLI for structured documentation.

## Workflow

```
target-vault --> select-type --> create-note --> populate
  --> preview --> confirm --> write --> link-related
```

Each note type has its own workflow. Use any type independently based on user needs.

## Context Loading Strategy

Load only the reference or guide matching the current trigger. Never load
multiple simultaneously unless explicitly noted.

- `templates/*.md` are not loaded into context. The agent uses them as
  reference to compose note content.
- Templates also live in the vault (`Templates/`) for manual use via
  Obsidian's Templates and Daily Notes plugins.

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Project, PRD, Design Doc, ADR, architecture | [project.md](references/project.md) |
| Company, job application, interview | [company.md](references/company.md) |
| Challenge, technical challenge, take-home, coding interview | [challenge.md](references/challenge.md) |
| Brag, achievement, accomplishment | [brag.md](references/brag.md) |
| Daily, today, daily note, journal | [daily.md](references/daily.md) |
| Conversation, session, save conversation, AI chat | [conversation.md](references/conversation.md) |
| Capture, save this, quick note, paste this | [capture.md](references/capture.md) |
| Markdown, syntax, wikilink, callout, embed | [markdown.md](guides/markdown.md) |
| Vault structure, organize vault | [vault-structure.md](guides/vault-structure.md) |

Notes:

- `markdown.md` and `vault-structure.md` are informational guides (no write operations).
- All other references are note-creation workflows (compose, preview, confirm, write).

## Cross-References

```
company --> challenge     (interview triggers challenge)
company --> brag          (interview learnings become achievements)
challenge --> brag        (completed challenge becomes achievement)
daily --> brag            (daily insights feed brag document)
project --> daily         (project work logged in daily notes)
conversation --> daily    (conversation insights logged in daily)
conversation --> brag     (conversation outcomes become achievements)
```

## Guidelines

**DO:**

- Always verify vault with user before creating notes (`obsidian vaults verbose`)
- Compose note content inline following `templates/*.md` structure
- Preview the full note content and target path before writing, ask for confirmation
- Check CLI availability with `which obsidian`; if unavailable, fall back to Write tool at vault path
- Link related notes using Obsidian wiki-links `[[Note Name]]`
- Use Title Case for filenames (e.g., `My Project.md`)
- Ask user which vault when multiple vaults exist
- Remember vault name after first confirmation to avoid repeated prompts
- Use `obsidian search` to check if a note exists before creating
- Run `obsidian help` or `obsidian help <command>` for up-to-date CLI reference
- Use `silent` flag on `create` to avoid opening the note in Obsidian
- For mid-file edits, resolve the absolute path with `obsidian vault info=path`
  combined with the note's relative path, then use the Edit tool directly
- When templates in the skill are updated, remind user to sync vault copies (`Templates/`)

**DON'T:**

- Overwrite or delete existing vault files -- always append, rename, or cancel
- Assume vault location without confirmation
- Create notes without user confirmation of content
- Use templates for updates (templates are for new notes only)
- Create duplicate notes - search first with `obsidian search query=<name>`
- Use absolute paths in wiki-links (always relative)

## Output

Notes are created in the user's Obsidian vault:

```
Vault/
├── Projects/
├── Companies/
├── Challenges/
├── Brags/
├── Conversations/
├── Daily/
└── Templates/
```

## Error Handling

- Vault not found: ask user for correct vault name (`obsidian vaults verbose`)
- Note already exists: ask to append, choose new name, or cancel
- CLI not available for content: fall back to Write tool with content composed from templates
- Obsidian CLI not available: fall back to Write tool to create the file directly at the vault path; ask user for vault path on first use
- Empty required fields: prompt user for missing information
