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
   Each item in What Was Done is a single line: bold project/topic name
   followed by a one-sentence summary. Not a changelog.

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
   Use the current working directory to suggest the project name. Check if
   that project already appears in What Was Done.

   If Basic Memory is available, search for activity since the note was last
   updated to suggest new items. Present findings to the user for confirmation.
   If Basic Memory is not available, skip this step.

3. **Gather new content**
   Ask what was worked on. Also ask about decisions, learnings, or open items
   if relevant.

4. **Edit in place**
   Use `patch_note` to insert content at the right location:
   - Add new bullet to `## What Was Done` (before the next `## ` section)
   - If the user mentions decisions, learnings, or open items, insert them
     into the corresponding section (create the section if it does not exist)
   ```
   patch_note path="Daily/YYYY-MM-DD.md" oldString="..." newString="..."
   ```

## Content Structure

Only `## What Was Done` is required. All other sections are optional -- include
them only when the user mentions relevant content. Omit empty sections.

```markdown
## What Was Done

- **Project/Topic** -- 1 sentence summary (not a changelog)
- **Another Project** -- What was accomplished, at a high level

## Key Decisions (optional)

- Decision + rationale (why, not just what)

## Learnings (optional)

- Discoveries, surprises, gotchas

## Open Items (optional)

- [ ] Pending work, blockers, next steps

## Observations

- #progress Key progress on a project
- #decision Decision made during the day
- #learning Something discovered worth remembering

## Relations

- [[Project Name]]
```

## Guidelines

**DO:**
- Keep it brief -- 5 minutes max
- Ask one question at a time -- never batch multiple questions
- Link to project notes when mentioning projects `[[Project Name]]`
- Use bullet points for speed
- Use the current directory as context to suggest the project name
- Write What Was Done as executive summary, not step-by-step

**DON'T:**
- Duplicate info from project notes (link instead)
- Generate empty sections or placeholder content
- Use changelog/commit-style language in bullet points
- Split What Was Done into subsections per project (use bold prefix instead)

## Next Steps

- Daily notes can be reviewed weekly for patterns
- Insights can feed into brag documents
- Open items may become project notes
