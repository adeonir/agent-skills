---
name: session-notes
description: >-
  Create and manage Obsidian notes for projects, companies, technical
  challenges, brag documents, daily logs, and AI conversations using
  MCPVault MCP. Use when documenting projects, tracking job applications,
  recording interview challenges, maintaining brag documents, creating
  daily notes, or saving AI conversations. Triggers on "create project",
  "new project note", "document company", "job application", "technical
  challenge", "brag document", "daily note", "today's log", "obsidian
  note", "save conversation", "chat summary", "session summary".
---

# Session Notes

Create and manage Obsidian notes using MCPVault MCP for structured documentation.

## Workflow

```
resolve-vault --> select-type --> compose-note --> write --> link-related
```

Each note type has its own workflow. Use any type independently based on user needs.

## Vault Resolution

Run once per session before any write operation. All references assume the vault
is already resolved.

1. Check if MCPVault MCP is available (look for `write_note`, `read_note` tools)
2. Use `list_directory` to verify the vault root is accessible
3. If Obsidian CLI is available (`which obsidian`), use `obsidian vaults verbose`
   to list vaults and confirm with user
4. If multiple vaults exist, ask user which one to use
5. Remember the vault name for the rest of the session

Once resolved, all references use relative paths from the vault root
(e.g., `Daily/2026-03-20.md`, `Projects/My Project/Overview.md`).

## Filename Sanitization

When generating filenames from user input:

- Remove invalid characters: `/ \ : * ? " < > |`
- Preserve accented characters (valid in filenames)
- Use Title Case for all filenames
- Example: `What's Next?` becomes `Whats Next.md`

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
| Markdown, syntax, wikilink, callout, embed | [markdown.md](guides/markdown.md) |
| Vault structure, organize vault | [vault-structure.md](guides/vault-structure.md) |

Notes:

- `markdown.md` and `vault-structure.md` are informational guides (no write operations).
- All other references are note-creation workflows (compose, write, link).

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

## Writing Style

- Language: English for all notes
- Body: rich prose context after the heading, not just bullet points
- Bullet points: describe what happened and why, with natural language, and with enough context to understand weeks later
- Observations: `#category content` syntax -- tags are indexed by Obsidian natively
- Relations: `[[Note Title]]` wikilinks only -- omit the section if no related notes exist in the vault

## Guidelines

**DO:**

- Resolve vault once per session (see Vault Resolution above)
- Compose note content following `templates/*.md` structure
- Use `write_note` for new notes, `read_note` + `patch_note` for updates
- Use `search_notes` to check if a note exists before creating
- Link related notes using Obsidian wiki-links `[[Note Name]]`
- Use Title Case for filenames (e.g., `My Project.md`)
- Sanitize filenames from user input (see Filename Sanitization above)
- When templates in the skill are updated, remind user to sync vault copies (`Templates/`)

**DON'T:**

- Overwrite or delete existing vault files -- always append, rename, or cancel
- Assume vault location without confirmation
- Use templates for updates (templates are for new notes only)
- Create duplicate notes -- search first with `search_notes`
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
└── Daily/
```

## Error Handling

- MCPVault unavailable: inform user the skill requires MCPVault MCP server
- Vault not found: ask user for correct vault name
- Note already exists: ask to append, choose new name, or cancel
- Empty required fields: prompt user for missing information
