---
name: session-notes
description: >
  Create and manage Obsidian notes for projects, companies, technical challenges,
  brag documents, daily logs, AI conversations, and quick captures using the
  Obsidian CLI.
  Use when: documenting projects with PRD/TDD/ADR, tracking job applications
  to companies, recording technical interview challenges, maintaining brag
  documents with achievements, creating daily notes in Obsidian, saving
  conversations from AI tools, or formatting content with Obsidian syntax.
  Triggers on "create project", "new project note", "document company",
  "job application", "technical challenge", "coding interview",
  "brag document", "my achievements", "daily note", "today's log",
  "obsidian note", "note in obsidian", "save conversation", "chat summary", "AI chat", "session summary",
  "save this", "capture this", "quick note",
  "wikilink", "callout", "obsidian markdown".
metadata:
  author: github.com/adeonir
  version: "1.0.0"
---

# Session Notes

Create and manage Obsidian notes using the Obsidian CLI for structured documentation.

## Workflow

```
target-vault --> select-type --> create-note --> populate-content --> preview --> confirm --> write --> link-related
```

Each note type has its own workflow. Use any type independently based on user needs.

## Context Loading Strategy

Load only the reference or guide matching the current trigger. Never load
multiple simultaneously unless explicitly noted.

### Workflows

Note-creation workflows. Each follows the full write cycle (compose,
preview, confirm, write).

| Trigger | Reference |
|---------|-----------|
| project, PRD, TDD, ADR, architecture | [project.md](references/project.md) |
| company, job application, interview | [company.md](references/company.md) |
| challenge, technical challenge, take-home, coding interview | [challenge.md](references/challenge.md) |
| brag, achievement, accomplishment | [brag.md](references/brag.md) |
| daily, today, daily note, journal | [daily.md](references/daily.md) |
| conversation, session, save conversation, AI chat | [conversation.md](references/conversation.md) |
| capture, save this, quick note, paste this | [capture.md](references/capture.md) |

### Guides

Informational references for syntax and vault organization. No vault
write operations are performed.

| Trigger | Guide |
|---------|-------|
| markdown, syntax, wikilink, callout, embed | [markdown.md](guides/markdown.md) |
| vault structure, organize vault | [vault-structure.md](guides/vault-structure.md) |

### Notes

- `templates/*.md` are not loaded into context. The agent uses them as
  reference to compose note content inline via `obsidian create content=<text>`.
- Templates also live in the vault (`Templates/`) for manual use via
  Obsidian's Templates and Daily Notes plugins.

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
- Link related notes using Obsidian wiki-links `[[note-name]]`
- Use kebab-case for filenames (e.g., `my-project.md`)
- Ask user which vault when multiple vaults exist
- Remember vault name after first confirmation to avoid repeated prompts
- Use `obsidian search` to check if a note exists before creating
- Run `obsidian help` or `obsidian help <command>` for up-to-date CLI reference
- Use `silent` flag on `create` to avoid opening the note in Obsidian
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
