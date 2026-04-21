# Create Daily Note

Create quick daily logs and journal entries.

## When to Use

- User says "daily note", "today's log", "journal", "what I did today"
- User wants to record daily activities and reflections
- End of day wrap-up

## Workflow

1. **Check if today's note exists**
   Daily notes follow the convention: `Daily/YYYY-MM-DD.md`.
   ```
   search_notes query="YYYY-MM-DD" path="Daily/"
   ```
   If the note already exists, follow the **Update Existing Note** flow below.
   If it does not exist, continue with step 2.

2. **Gather project context**
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

3. **Compose content**
   Create one `### Project Name` subsection per project under `## Activities`.
   One prose paragraph (2-4 sentences) per project covering outcomes,
   decisions, and context. Inline `[[wikilink]]` to today's session note.
   Past tense, natural language. Not a changelog -- focus on outcomes and
   context.

4. **Write note**
   ```
   write_note path="Daily/YYYY-MM-DD.md" content="..." frontmatter={...}
   ```

## Update Existing Note

When the daily note already exists (user switched projects or is adding to
an earlier entry):

1. **Read current content**
   ```
   read_note path="Daily/YYYY-MM-DD.md"
   ```

2. **Infer project from context**
   Use the current working directory to suggest the project name. Check if a
   subsection for that project already exists in Activities.

   If Basic Memory is available, search for activity since the note was last
   updated to suggest new items. Present findings to the user for confirmation.
   If Basic Memory is not available, skip this step.

3. **Gather new content**
   Ask what was worked on. Also ask about open items or cross-cutting
   observations if relevant.

4. **Edit in place**
   Use `patch_note` to insert content at the right location:
   - Add new `### Project Name` subsection at the end of `## Activities`
     (before the next `## ` section)
   - If the project subsection already exists, rewrite the entire
     subsection: merge the existing paragraph with new activities into a
     single 2-4 sentence paragraph that covers the full day
   - If the user mentions open items or observations, insert them into
     the corresponding section (create the section if it does not exist)
   - Consolidate `## Observations` and `## Relations` the same way --
     merge existing with new, deduplicate, keep only distinct items
   ```
   patch_note path="Daily/YYYY-MM-DD.md" oldString="..." newString="..."
   ```

## Content Structure

Only `## Activities` is required. All other sections are optional -- include
them only when the user mentions relevant content. Omit empty sections.

Activities use one `### Project Name` subsection per project with one prose
paragraph (2-4 sentences) each. Past tense, natural language. Capture
outcomes, decisions, and context from the day's work on the project. Inline
`[[wikilink]]` to today's session note.

Observations are day-level and cross-cutting -- project-specific facts
stay in the session note. Common categories: `#pattern`, `#method`,
`#cadence`, `#blocker`, `#mood`.

Relations use typed verbs (`contains`, `relates_to`); `contains` points
to today's session notes.

## Guidelines

**DO:**
- Keep it brief -- 5 minutes max
- Link to project notes when mentioning projects `[[Project Name]]`
- Write one prose paragraph (2-4 sentences) per project subsection
- Use past tense and natural language
- Use the current directory as context to suggest the project name
- Write Activities as outcomes and decisions, not steps taken
- Use Observations only for cross-cutting day-level facts

**DON'T:**
- Duplicate info from project notes or session notes (contrasts: link instead)
- Generate empty sections or placeholder content (contrasts: omit empty sections)
- Use bullet lists for Activities (contrasts: prose paragraph per project)
- Exceed 4 sentences in a project paragraph (contrasts: consolidate to 2-4)
- Restate project-specific observations in the daily (contrasts: cross-cutting only)

## Next Steps

- Daily notes can be reviewed weekly for patterns
- Insights can feed into brag documents
- Open items may become project notes
