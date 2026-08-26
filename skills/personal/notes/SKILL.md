---
name: notes
description: "Obsidian note creation and updates for projects, challenges, achievements, transcriptions, companies, and job applications. Use when documenting work or preserving meeting and lecture notes. Not for session handoffs or repository-wide project context."
---

# Notes

Creates and manages Obsidian notes using the Obsidian MCP for structured documentation.

## Triggers

- **Project note** ("create project", "new project note", "document project") → [project.md](references/project.md)
- **Challenge note** ("technical challenge", "take-home", "coding interview", "system design") → [challenge.md](references/challenge.md)
- **Brag entry** ("brag document", "achievement", "accomplishment") → [brag.md](references/brag.md)
- **Transcription** ("transcription", "meeting notes", "1:1 notes", "feedback notes", "standup notes", "lecture notes", "course notes") → [transcription.md](references/transcription.md)
- **Company tracking** ("company note", "track interview", "job application") → [company.md](references/company.md)

`mapping.md` is loaded by the note-creation refs to resolve vault paths; not a direct trigger.

## Workflow

```text
resolve-vault → select-type → compose-note → write → link-related
```

Each note type has its own workflow. Use any type independently.

## Filename Sanitization

When generating filenames from user input:

- Remove characters the OS rejects or Obsidian links break on: `/ \ : * ? " < > | # ^ [ ] %`
- Preserve accented characters — Obsidian imposes no charset limit beyond the filesystem's
- Use Title Case for all filenames
- Example: `What's Next?` becomes `Whats Next.md`

## Guidelines

- Ask one question at a time when gathering context from the user
- Refresh `updated` in the frontmatter whenever an existing note is patched

## Anti-Pattern: Orphan Wikilinks

Creating `[[Some Note]]` to a file that does not exist makes Obsidian generate an empty file at the vault root. Always run `Obsidian:search_notes` before linking to verify the target exists. If the target is missing, either create it first or omit the link.

## Anti-Pattern: Template-Driven Updates

Templates apply to new notes only. When updating an existing note, read it first with `Obsidian:read_note`, then patch with `Obsidian:patch_note`. Re-applying a template overwrites prior content and loses history.
