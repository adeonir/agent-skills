# Note Conventions

The filename, body, wikilink, update, and report rules every note type follows.

## When to Use

Loaded before writing or patching any note, whatever its type.

## Vault Access

Every note operation goes through one channel, tried in this order. Open the Obsidian app only after the user agrees.

1. **CLI (default).** When `command -v obsidian` finds it, run its commands. When a command fails because Obsidian is closed, ask the user whether to open it: on yes, run `open -a Obsidian` and retry; on no, use the MCP tools for the rest of the run.
2. **MCP (fallback).** When the CLI binary is missing, or the user declined to open the app, use the Obsidian MCP tools (`Obsidian:read_note`, `Obsidian:write_note`, `Obsidian:patch_note`, and kin).
3. **Direct vault write (last).** When neither is available, write the note as a plain file into the vault resolved the way the bundled `check_note.py` resolves it: `--vault` when given, the only vault in Obsidian's `obsidian.json`, or the open one.

Every CLI command starts with `vault="<vault>"`, the vault's folder name.

| Operation | Command |
|---|---|
| Search | `obsidian vault="<vault>" search query="<query>" path="<folder>/" format=json` |
| Read | `obsidian vault="<vault>" read path="<path>"` |
| Create | `obsidian vault="<vault>" create path="<path>" content="$(cat "<temp-file>")"`; when the note text holds a literal `\n` or `\t`, write a plain file instead |
| Patch | read the note, edit the text, then run Create with the `overwrite` flag |
| Set property | `obsidian vault="<vault>" property:set name=<name> value=<value> path="<path>"` |
| List a folder | `obsidian vault="<vault>" files folder="<folder>/"` |
| Move | `obsidian vault="<vault>" move path="<path>" to="<dest>"` |

Move or rename a linked note only through the CLI; without it, report the path and skip.

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

Creating `[[Some Note]]` to a file that does not exist makes Obsidian generate an empty file at the vault root. Before linking, verify the target exists with Search in Vault Access, run without `path`. If the target is missing, either create it first or omit the link.

## Updating an Existing Note

Templates apply to new notes only. When updating an existing note, read it first, then patch it — the Read and Patch operations in Vault Access. Re-applying a template overwrites prior content and loses history.

Refresh `updated` in the frontmatter whenever an existing note is patched.

## Reporting the Note

After writing or patching a note, report its vault path, what the note holds in one to three sentences — what changed, on an update — and any open item it carries. Never paste the note. For a transcription, describe the note — the kind of session and its topic — and never quote its body.

## Gathering Context

Ask one question at a time when gathering context from the user.
