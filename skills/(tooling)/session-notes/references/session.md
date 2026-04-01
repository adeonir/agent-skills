# Create Session Note

Create a session note documenting work done on a specific project.

## When to Use

- User says "session note", "document this session", "save session"
- End of a focused work session on a project
- After completing a task, ticket, refactor, or investigation

## Workflow

1. **Determine project and folder**
   Use the current working directory to infer the project name. Map it to the
   corresponding vault folder (e.g., `Work/Jaya/`, `Ventures/Pensefy/`).
   Session notes go in the `Sessions/` subfolder:
   `{Folder}/{Project}/Sessions/`.
   If the project cannot be determined, ask the user.

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

Summary uses 2-5 bullets describing context, outcomes, and decisions.
Focus on what was done, written, shipped, or decided — not steps taken,
not reasoning, not file paths.

## Guidelines

**DO:**
- Keep it focused on one project per note
- Use past tense and natural language
- Write Summary as bullet points with outcomes and context, not a task list
- Link to related daily notes and project notes

**DON'T:**
- Mix multiple projects in one session note (use daily note for that)
- List tasks or steps executed (that is a changelog)
- List files modified (that is git log)
- Include git metadata (branches, commits, PRs)
- Include file paths or directory names (those belong in debrief)
- Explain reasoning or motivations (those belong in debrief)
- Generate empty sections or placeholder content

## Next Steps

- Session notes feed into daily notes (summary of the day)
- Key decisions may become project-level documentation
- Open items carry over to next session or daily note
