# Note Conventions

The filename, wikilink, and update rules every note type follows.

## When to Use

Loaded before writing or patching any note, whatever its type.

## Filename Sanitization

When generating filenames from user input:

- Remove characters the OS rejects or Obsidian links break on: `/ \ : * ? " < > | # ^ [ ] %`
- Preserve accented characters — Obsidian imposes no charset limit beyond the filesystem's
- Use Title Case for all filenames
- Example: `What's Next?` becomes `Whats Next.md`

## Wikilinks

Creating `[[Some Note]]` to a file that does not exist makes Obsidian generate an empty file at the vault root. Run `Obsidian:search_notes` before linking to verify the target exists. If the target is missing, either create it first or omit the link.

## Updating an Existing Note

Templates apply to new notes only. When updating an existing note, read it first with `Obsidian:read_note`, then patch with `Obsidian:patch_note`. Re-applying a template overwrites prior content and loses history.

Refresh `updated` in the frontmatter whenever an existing note is patched.

## Gathering Context

Ask one question at a time when gathering context from the user.
