# Create Daily Note

Create quick daily logs and journal entries.

## When to Use

- User says "daily note", "today's log", "journal", "what I did today"
- User wants to record daily activities and reflections
- End of day wrap-up

## Workflow

1. **Confirm vault**
   ```bash
   obsidian vaults verbose
   ```

2. **Determine filename and path**
   Daily notes follow the convention: `Daily/YYYY-MM-DD.md`
   (e.g., `Daily/2025-03-04.md`). Check if today's note already exists:
   ```bash
   obsidian daily:path
   obsidian daily:read
   ```

3. **Compose content**
   Ask the user what they worked on. Activities include meetings, decisions,
   research, and other work that may not produce commits. Use git log only
   as a supplement if the user asks or needs help remembering -- never dump
   raw commit data into the note.

4. **Preview and confirm**
   Display the full note content and target file path to the user.
   Ask for confirmation before writing. Accept edits if suggested.

5. **Write note**
   Check if Obsidian CLI is available:
   ```bash
   which obsidian
   ```
   If available, create or open daily note:
   ```bash
   obsidian daily
   ```
   Append quick entry without opening:
   ```bash
   obsidian daily:append content="- {{content}}"
   ```
    If CLI is not available, fall back to Write tool to create the file
    directly at the vault path using the daily note path convention
    (`Daily/YYYY-MM-DD.md`). Ask user for vault path on first use.

## Quick Capture

For rapid logging throughout the day:

```bash
# Quick append without opening
obsidian daily:append content="- {{quick note}}"

# Read current daily note content
obsidian daily:read

# Check tasks in daily note
obsidian tasks daily
obsidian tasks daily todo
```

## Content Structure

Typical daily note sections:

```markdown
## Activities

### {{Project Name}} (optional subtopics)

- What was worked on
- Meetings attended
- Decisions made

## Blockers

- What got in the way
- Help needed

## Learnings

- New things discovered
- Insights

## Tomorrow

- Carry over tasks
- Upcoming priorities
```

## Guidelines

**DO:**
- Keep it brief - 5 minutes max
- Link to project notes when mentioning projects `[[Project Name]]`
- Use bullet points for speed
- Include emotional state/morale if relevant
- Tag with #daily or #journal for searchability

**DON'T:**
- Write long prose (keep it scannable)
- Skip days (even "nothing special" is data)
- Duplicate info from project notes (link instead)
- Worry about perfect formatting

## Next Steps

- Daily notes can be reviewed weekly for patterns
- Insights can feed into brag documents
- Blockers may become project notes
