# Create Session Note

Create a session note documenting work done on a specific project.

## When to Use

- User says "session note", "document this session", "save session"
- End of a focused work session on a project
- After completing a task, ticket, refactor, or investigation

## Workflow

1. **Determine project and folder**
   Load [mapping.md](mapping.md) to resolve the vault folder from the current
   working directory. Session notes go in the `Sessions/` subfolder:
   `{Folder}/{Project}/Sessions/`.

2. **Check for existing note**
   Session notes use the convention: `{Folder}/{Project}/Sessions/YYYY-MM-DD — Description.md`.
   Search for a note matching the same date and topic in the target folder.
   ```
   search_notes query="YYYY-MM-DD" path="{Folder}/{Project}/Sessions/"
   ```
   If a match exists, follow the **Update Existing Note** flow below.

3. **Gather context**
   Ask the user what was worked on. Supplement with:
   - Git log and diff stat (if in a repo)
   - Basic Memory session notes from today (if available)
   Use findings as suggestions -- let the user confirm what to include.

4. **Choose filename**

   | Session type | Pattern | Example |
   |---|---|---|
   | Ticket work | `YYYY-MM-DD — {TICKET-ID} Description.md` | `2026-03-22 — P40-54955 Fix Auth Redirect.md` |
   | Refactor/feature | `YYYY-MM-DD — Description.md` | `2026-03-22 — BM Reorganization.md` |
   | Investigation | `YYYY-MM-DD — Investigation Description.md` | `2026-03-22 — Investigation Auth Timeout.md` |

5. **Compose and write**
   ```
   write_note path="{Folder}/{Project}/Sessions/YYYY-MM-DD — Description.md" content="..." frontmatter={...}
   ```

## Update Existing Note

When a session note for the same project and topic already exists today:

1. **Read current content**
   ```
   read_note path="{Folder}/{Project}/Sessions/YYYY-MM-DD — Description.md"
   ```

2. **Append new content**
   Add new bullets to existing sections or create new sections as needed.
   Use a horizontal rule `---` and date header if appending a separate session
   to the same note.
   ```
   patch_note path="..." oldString="..." newString="..."
   ```

## Content Structure

Only `## Summary` is required. All other sections are optional -- include
them only when the user mentions relevant content. Omit empty sections.

Summary uses 2-5 bullets describing facts, outcomes, and decisions.
Focus on what was done, written, shipped, or decided — not steps taken,
not reasoning, not file paths.

## Guidelines

**DO:**
- Keep one project per note; use daily note for cross-project context
- Use past tense and natural language
- Write Summary as bullet points with facts, outcomes, and decisions (not tasks, git metadata, or reasoning)
- Include only sections with content; omit empty sections
- Link to related daily notes and project notes

**DON'T:**
- Mix multiple projects in one session note (contrasts: one project per note)
- List tasks, steps executed, files modified, or git metadata (contrasts: facts, outcomes, decisions)
- Include reasoning, motivations, file paths, or technical specifics (contrasts: outcomes over process)
- Generate empty sections or placeholder content (contrasts: include only sections with content)

## Next Steps

- Session notes feed into daily notes (summary of the day)
- Key decisions may become project-level documentation
- Open items carry over to next session or daily note
