# Create Decision Note

Create a decision note documenting significant choices made during a project.

## When to Use

- User says "decision note", "document decision", "record decision"
- After making architectural, stack, scope, or convention decisions
- When a decision needs its own note rather than living inside a session note

## Workflow

1. **Determine project and folder**
   Use the current working directory to infer the project name. Map it to the
   corresponding vault folder (e.g., `Work/Jaya/`, `Ventures/Pensefy/`).
   Decision notes go in the `Decisions/` subfolder:
   `{Folder}/{Project}/Decisions/`.
   If the project cannot be determined, ask the user.

2. **Check for existing note**
   Decision notes are thematic -- one per subject, not per session.
   Search for an existing decision note on the same topic:
   ```
   search_notes query="Decision Title" path="{Folder}/{Project}/Decisions/"
   ```
   If a match exists, update it instead of creating a new one.

3. **Gather context**
   Ask the user what was decided. Supplement with:
   - Basic Memory decision notes from the same project (if available)
   - Session context from today
   Use findings as suggestions -- let the user confirm what to include.

4. **Choose filename**
   Use a descriptive title that captures the decision theme:

   | Decision type | Pattern | Example |
   |---|---|---|
   | Architecture | `Architecture Description.md` | `Architecture Feature Folders.md` |
   | Stack | `Stack Description.md` | `Stack Payment Gateway.md` |
   | Scope | `Scope Description.md` | `Scope MVP Definition.md` |
   | Convention | `Convention Description.md` | `Convention Commit Format.md` |

5. **Compose and write**
   ```
   write_note path="{Folder}/{Project}/Decisions/Decision Title.md" content="..." frontmatter={...}
   ```

## Update Existing Note

When a decision note for the same theme already exists:

1. **Read current content**
   ```
   read_note path="{Folder}/{Project}/Decisions/Decision Title.md"
   ```

2. **Append or update content**
   Add new decisions as numbered subsections under `## Decisions`.
   Update context prose if the background has changed.
   ```
   patch_note path="..." oldString="..." newString="..."
   ```

## Content Structure

Context prose between H1 and Decisions is required. The `## Decisions` section
is required with at least one numbered subsection. All other sections are
optional -- include only when relevant. Omit empty sections.

Additional sections (comparative tables, tier breakdowns, impact analysis)
appear as complexity demands. No fixed list -- use whatever the decision needs.

## Guidelines

**DO:**
- Group by theme, not by session -- one decision note per subject
- Include rationale and alternatives rejected
- Update existing decision notes instead of creating duplicates
- Link to the session where the decision was made
- Use prose context to explain background and constraints

**DON'T:**
- Create one decision note per session (use session notes for that)
- List decisions without rationale
- Generate empty sections or placeholder content
- Duplicate content already in session or debrief notes

## Next Steps

- Decision notes link to project overview and session notes
- Major decisions may feed into project-level documentation (ADR, Design Doc)
- Related decisions across projects can be linked via wiki-links
