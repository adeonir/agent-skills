---
name: session-notes
description: >-
  Create and manage Obsidian notes for projects, technical challenges,
  brag documents, and meeting transcriptions using MCPVault MCP. Use when
  documenting projects, recording technical challenges, maintaining brag
  documents, or preserving meeting and course transcriptions in Obsidian.
when_to_use: >-
  Triggers on "create project note", "new project note",
  "technical challenge", "brag document", "achievement", "accomplishment",
  "transcription", "meeting notes", "standup notes", "lecture notes",
  "course notes". Not for initializing .agents/ project context
  (use project-index), or end-of-session wrap-up (use wrap-up).
---

# Session Notes

Create and manage Obsidian notes using MCPVault MCP for structured documentation.

## Workflow

```
resolve-vault --> select-type --> compose-note --> write --> link-related
```

Each note type has its own workflow. Use any type independently based on user needs.

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Project, new project note, document project | [project.md](references/project.md) |
| Challenge, technical challenge, take-home, coding interview | [challenge.md](references/challenge.md) |
| Brag, achievement, accomplishment | [brag.md](references/brag.md) |
| Transcription, meeting notes, standup, lecture, course notes | [transcription.md](references/transcription.md) |
| Markdown, syntax, wikilink, callout, embed | [markdown.md](guides/markdown.md) |
| Vault structure, organize vault | [vault-structure.md](guides/vault-structure.md) |

Notes:

- `markdown.md` and `vault-structure.md` are informational guides (no write operations).
- `mapping.md` is not a direct trigger. It is loaded by `project.md` to resolve vault paths.
- All other references are note-creation workflows (compose, write, link).
- Templates under `templates/` are reference structure only; do not load them into context.

## Cross-References

```
mapping.md <-- project.md   (project loads mapping to resolve vault path)
challenge --> brag           (completed challenge becomes achievement)
```

## Filename Sanitization

When generating filenames from user input:

- Remove invalid characters: `/ \ : * ? " < > |`
- Replace accented characters with ASCII equivalents (e.g., `é` → `e`, `ã` → `a`)
- Use Title Case for all filenames
- Example: `What's Next?` becomes `Whats Next.md`

## Writing Style

- Language: English for all notes
- Body: rich prose context after the heading, not just bullet points
- Bullet points: describe what happened and why, with natural language, and with enough context to understand weeks later
- Observations: `#category content` syntax -- tags are indexed by Obsidian natively
- Relations: typed verbs + wikilinks (`- follows [[X]]`, `- part_of [[Project]]`, `- contains [[Session]]`) -- common types include `follows`, `part_of`, `expands`, `relates_to`, `implements`, `requires`, `replaces`, `pairs_with`, `extends`, `depends_on`, `contains`; inline `[[wikilinks]]` in prose cover ordinary mentions, the Relations section holds typed edges that add graph value; omit the section if no typed edges apply
- Wikilinks must point to existing files. Before adding a project link, verify the `{Name} Overview.md` file exists in the vault. Never create orphan wikilinks -- clicking them creates empty files at the vault root

## Guidelines

**DO:**

- Ask one question at a time when gathering context from the user
- Compose note content following `templates/*.md` structure
- Use `write_note` for new notes, `read_note` + `patch_note` for updates
- Use `search_notes` to check if a note exists before creating
- Link related notes using Obsidian wiki-links `[[Note Name]]`
- Use Title Case for filenames (e.g., `My Project.md`)
- Sanitize filenames from user input (see Filename Sanitization above)

**DON'T:**

- Batch multiple questions to the user (contrasts: one question at a time)
- Overwrite or delete existing vault files (contrasts: append, rename, or cancel)
- Use templates for updates (contrasts: templates are for new notes only)
- Create duplicate notes (contrasts: search first with `search_notes`)
- Use absolute paths in wiki-links (contrasts: always relative)
- Create wikilinks to files that don't exist in the vault (contrasts: verify target exists before linking)

## Output

Notes are created in the user's Obsidian vault:

```
Vault/
├── {VaultFolder}/
│   └── {Project}/
│       └── {Project Name} Overview.md
├── Challenges/
├── Brags/
└── Meetings/
```

The `{VaultFolder}` depends on the project category (e.g., `Work/`, `Ventures/`,
`Projects/`). See [mapping.md](references/mapping.md) for resolution.

## Error Handling

- MCPVault unavailable: inform user the skill requires MCPVault MCP server
- Vault not found: ask user for correct vault name
- Note already exists: ask to append, choose new name, or cancel
- Empty required fields: prompt user for missing information
