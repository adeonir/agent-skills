# Update Auto-Memory

Review the session and update Claude Code auto-memory files.

## When to Use

- Always runs first in the wrap-up sequence
- Runs even for trivial sessions (report "nothing to update")

## Workflow

1. **Read current memory index**
   Read `MEMORY.md` at the auto-memory path for the current project.
   If it does not exist, create it.

2. **Review session content**
   Scan the conversation for:
   - Decisions made and their rationale
   - User corrections or preferences (feedback)
   - New information about the user's role or workflow (user)
   - Project phase changes, milestones, or status updates (project)
   - External references discovered (reference)

3. **Compare with existing memories**
   Read relevant memory files. Check if:
   - An existing memory needs updating (status changed, new info)
   - A new memory should be created (something not yet captured)
   - Nothing changed (report "nothing to update" and move on)

4. **Update or create memory files**
   Follow the auto-memory format:
   ```markdown
   ---
   name: memory-name
   description: one-line description
   type: user | feedback | project | reference
   ---

   Content with **Why:** and **How to apply:** lines.
   ```

5. **Update MEMORY.md index**
   Add pointers to new files. Keep the index under 200 lines.

## Guidelines

**DO:**
- Only save what is useful for future sessions
- Update existing memories instead of creating duplicates
- Include "Why" and "How to apply" for feedback and project memories
- Convert relative dates to absolute dates

**DON'T:**
- Save ephemeral task details or current conversation context
- Duplicate information from CLAUDE.md files
- Save code patterns or architecture derivable from reading the code
- Create memories for trivial or obvious information
