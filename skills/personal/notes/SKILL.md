---
name: notes
description: >-
  Creates and manages Obsidian notes for projects, technical challenges, brag
  documents, meeting transcriptions, and company tracking. Use when documenting
  projects, recording technical challenges, maintaining a brag document of
  achievements, preserving meeting, 1:1, standup, or course transcriptions, or
  tracking a company or job application. Not for end-of-session persistence
  across memory systems or for initializing repository-wide project context.
---

# Notes

Creates and manages Obsidian notes using MCPVault MCP for structured documentation.

## Workflow

```
resolve-vault → select-type → compose-note → write → link-related
```

Each note type has its own workflow. Use any type independently.

## Triggers

- **Project note** ("create project", "new project note", "document
  project") → [project.md](references/project.md)
- **Challenge note** ("technical challenge", "take-home", "coding
  interview", "system design") → [challenge.md](references/challenge.md)
- **Brag entry** ("brag document", "achievement", "accomplishment")
  → [brag.md](references/brag.md)
- **Transcription** ("transcription", "meeting notes", "1:1 notes",
  "feedback notes", "standup notes", "lecture notes", "course notes")
  → [transcription.md](references/transcription.md)
- **Company tracking** ("company note", "track interview", "job
  application") → [company.md](references/company.md)
- **Markdown syntax help** ("wikilink", "callout", "embed", "Obsidian
  syntax") → [markdown.md](references/markdown.md)

`mapping.md` is loaded by the note-creation refs to resolve vault paths;
not a direct trigger. `markdown.md` is an informational reference with
no write operations.

## Filename Sanitization

When generating filenames from user input:

- Remove invalid characters: `/ \ : * ? " < > |`
- Replace accented characters with ASCII equivalents (e.g., `é` → `e`,
  `ã` → `a`)
- Use Title Case for all filenames
- Example: `What's Next?` becomes `Whats Next.md`

## Writing Style

- Body: rich prose context after the heading, not just bullet points
- Bullets: describe what happened and why, with enough context to
  understand weeks later
- Observations: `#category content` syntax — Obsidian indexes tags
  natively
- Relations: typed verbs + wikilinks (`- follows [[X]]`,
  `- part_of [[Project]]`, `- contains [[Session]]`); inline
  `[[wikilinks]]` cover ordinary mentions, the Relations section holds
  typed edges that add graph value; omit the section when no typed edges
  apply
- Wikilinks must point to existing files. Verify before linking; orphan
  links create empty files at the vault root

## Guidelines

- Ask one question at a time when gathering context from the user
- Use `write_note` for new notes, `read_note` + `patch_note` for updates
- Use `search_notes` to check if a note exists before creating
- Link related notes using `[[Note Name]]` wikilinks (verify target exists)
- Use Title Case for filenames
- Sanitize filenames from user input

## Anti-Pattern: Orphan Wikilinks

Creating `[[Some Note]]` to a file that does not exist makes Obsidian
generate an empty file at the vault root. Always run `search_notes`
before linking to verify the target exists. If the target is missing,
either create it first or omit the link.

## Anti-Pattern: Template-Driven Updates

Templates apply to new notes only. When updating an existing note, read
it first with `read_note`, then patch with `patch_note`. Re-applying a
template overwrites prior content and loses history.
