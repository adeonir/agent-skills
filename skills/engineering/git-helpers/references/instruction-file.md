# Resolving the Project Instruction File

Which file carries the project's agent instructions, resolved the same way by every skill.

## When to Use

Loaded by a step that reads or maintains the repository's instruction file — the `CLAUDE.md` / `AGENTS.md` file the harness reads. Resolves one file per repository. A job that reads every `AGENTS.md`, splits memory content, or places facts across folders follows its own skill contract instead.

## Resolution

Run from inside the repository:

1. Resolve the repository root: `git rev-parse --show-toplevel`.
2. Pick the target:
   - `CLAUDE.md` at the root, when it exists.
   - Else `.claude/CLAUDE.md`, when it exists.
   - When the picked `CLAUDE.md` imports `AGENTS.md` — a line containing only `@AGENTS.md`, `./AGENTS.md`, or `../AGENTS.md` — resolve the import relative to the importing file and use that path.
   - Else `AGENTS.md` at the root.
3. A target that resolves outside the repository is an error.

Reading needs only the target.

## Maintaining an Owned Block

- The block is one level-two section, titled by the contract that owns it, ending at the next heading of depth two or shallower.
- A fenced example is never a heading: track CommonMark fences — up to three leading spaces, at least three markers, a closing fence matching the opening marker type and at least its length — and scan nothing inside one. An unclosed fence is an error.
- Replace the section body in place and preserve the file's CRLF/LF endings; append the section at the end with a blank-line separation when it is absent.
- Duplicate owned sections, more than one nonblank line of unrelated body content, or an unresolved target are errors reported for manual resolution; on any failure the file stays untouched.
