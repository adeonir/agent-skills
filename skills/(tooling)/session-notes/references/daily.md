# Create Daily Note

Create quick daily logs and journal entries.

## When to Use

- User says "daily note", "today's log", "journal", "what I did today"
- User wants to record daily activities and reflections
- End of day wrap-up

## Language

Default to English. If user writes in Portuguese, use proper accents
throughout (e.g., codigo, informacao, nao, area, sera).

## Workflow

1. **Confirm vault**
   ```bash
   obsidian vaults verbose
   ```

2. **Check if today's note exists**
   Daily notes follow the convention: `Daily/YYYY-MM-DD.md`.
   ```bash
   obsidian daily:path
   obsidian daily:read
   ```
   If the note already exists, follow the **Update Existing Note** flow below.
   If it does not exist, continue with step 3.

3. **Gather project context**
   Use the current working directory to infer the project name (folder name,
   git remote, package.json name). Suggest it to the user and ask what was
   worked on. Activities include meetings, decisions, research, and other work
   that may not produce commits. Use git log only as a supplement if the user
   asks or needs help remembering -- never dump raw commit data into the note.

   If Basic Memory is available (check for `mcp__basic-memory__search` or
   similar tools), search for today's activity to supplement context:
   ```
   basic-memory search "today's date or recent activity"
   basic-memory recent_activity
   ```
   Use findings as suggestions -- let the user confirm what to include.
   If Basic Memory is not available, skip this step entirely.

4. **Compose content**
   Create one `### Project Name` subsection per project under `## Activities`.
   Write bullet points in natural, descriptive language -- not changelog style.

   Good: "Separados conceitos de milestones e releases para evitar confusao"
   Bad: "refactor: separate milestone/release concepts"

5. **Preview and confirm**
   Display the full note content and target file path to the user.
   Ask for confirmation before writing. Accept edits if suggested.

6. **Write note**
   Check if Obsidian CLI is available:
   ```bash
   which obsidian
   ```
   If available, create the daily note:
   ```bash
   obsidian daily
   ```
   Then resolve the absolute path and use the Write tool to set the content:
   ```bash
   obsidian vault info=path
   ```
   The full path is `<vault-path>/Daily/YYYY-MM-DD.md`.

   If CLI is not available, fall back to Write tool to create the file
   directly at the vault path. Ask user for vault path on first use.

## Update Existing Note

When the daily note already exists (user switched projects or is adding to
an earlier entry):

1. **Read current content**
   ```bash
   obsidian daily:read
   ```

2. **Resolve absolute path**
   ```bash
   obsidian vault info=path
   ```
   The file path is `<vault-path>/Daily/YYYY-MM-DD.md`.

3. **Infer project from context**
   Use the current working directory to suggest the project name. Check if a
   subsection for that project already exists in the note.

   If Basic Memory is available, search for activity since the note was last
   updated to suggest new items. Present findings to the user for confirmation.
   If Basic Memory is not available, skip this step.

4. **Gather new content**
   Ask what was worked on. Also ask about learnings, blockers, or tomorrow
   items if relevant.

5. **Edit in place with Edit tool**
   Do NOT use `obsidian daily:append` -- it adds to the end of the file,
   not inside the correct section. Instead, use the Edit tool to:
   - Insert new `### Project Name` subsection at the end of `## Activities`
     (before the next `## ` section or end of file)
   - If the user mentions learnings, blockers, or tomorrow items, insert them
     into the corresponding section (create the section if it does not exist)

6. **Preview and confirm**
   Show only the changes being made, not the full note. Ask for confirmation.

## Content Structure

Only `## Activities` is required. All other sections are optional -- include
them only when the user mentions relevant content.

```markdown
## Activities

### Project Name

- Descriptive bullet point about what was done
- Another activity with enough context to understand later

### Another Project

- What was worked on in this project

## Blockers (optional)

- What got in the way, with context or expected resolution

## Learnings (optional)

- Insights or discoveries worth remembering

## Tomorrow (optional)

- Carry over tasks or upcoming priorities
```

## Quick Capture

For rapid logging throughout the day:

```bash
# Quick append without opening
obsidian daily:append content="- Quick standup note"

# Read current daily note content
obsidian daily:read

# Check tasks in daily note
obsidian tasks daily
obsidian tasks daily todo
```

## Guidelines

**DO:**
- Keep it brief - 5 minutes max
- Link to project notes when mentioning projects `[[Project Name]]`
- Use bullet points for speed
- Ask which projects were worked on and create a subsection for each
- Use the current directory as context to suggest the project name

**DON'T:**
- Write long prose (keep it scannable)
- Duplicate info from project notes (link instead)
- Generate empty sections or placeholder content
- Use changelog/commit-style language in bullet points
- Use `obsidian daily:append` when inserting into the middle of a note

## Next Steps

- Daily notes can be reviewed weekly for patterns
- Insights can feed into brag documents
- Blockers may become project notes
