# Note Conventions

The filename, body, wikilink, update, and report rules every note type follows.

## When to Use

Loaded before writing or patching any note, whatever its type.

## Filename Sanitization

When generating filenames from user input:

- Remove characters the OS rejects or Obsidian links break on: `/ \ : * ? " < > | # ^ [ ] %`
- Preserve accented characters — Obsidian imposes no charset limit beyond the filesystem's
- Use Title Case for all filenames
- Example: `What's Next?` becomes `Whats Next.md`

## Writing the Body

State each fact and decision as it stands, in present tense, never the deliberation that produced it; on a patch, write the new state, never the change. A section that records history keeps its history: a timeline, the reasoning behind a company decision, a challenge's approach and trade-offs, learnings, and a brag period.

Leave every trace of the exchange with the agent out of every note, history sections included — "as discussed", "the user confirmed", "we agreed", "you chose". A past event or a rejected option is a fact about the work.

A transcription body passes through verbatim; neither rule applies to it.

## Wikilinks

Creating `[[Some Note]]` to a file that does not exist makes Obsidian generate an empty file at the vault root. Run `Obsidian:search_notes` before linking to verify the target exists. If the target is missing, either create it first or omit the link.

## Updating an Existing Note

Templates apply to new notes only. When updating an existing note, read it first with `Obsidian:read_note`, then patch with `Obsidian:patch_note`. Re-applying a template overwrites prior content and loses history.

Refresh `updated` in the frontmatter whenever an existing note is patched.

## Reporting the Note

After writing or patching a note, report its vault path, what the note holds in one to three sentences — what changed, on an update — and any open item it carries. Never paste the note. For a transcription, describe the note — the kind of session and its topic — and never quote its body.

## Gathering Context

Ask one question at a time when gathering context from the user.
