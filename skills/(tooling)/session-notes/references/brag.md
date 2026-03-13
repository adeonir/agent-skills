# Update Brag Document

Add achievements to brag document for performance reviews and career growth.

## When to Use

- User says "brag document", "my achievements", "add accomplishment"
- User mentions something they're proud of at work
- User wants to track wins for performance review

## Workflow

1. **Confirm vault**
   ```bash
   obsidian vaults verbose
   ```

2. **Determine time period**
   - Current year: `Brags 2025.md`
   - Or by quarter: `Brags 2025 Q1.md`
   - Ask user preference on first use

3. **Check if brag doc exists**
   ```bash
   obsidian search query="Brags 2025" path=Brags
   ```

4. **Create or append**
   - If doesn't exist: create with template
   - If exists: append new achievement to the appropriate category

5. **Gather achievement details**
   - What was accomplished
   - Context (project, team, situation)
   - Result with metrics (quantify when possible)
   - Category (impact, technical, growth)

6. **Preview and confirm**
   Display the full note content (or the new entry to append) and target
   file path to the user. Ask for confirmation before writing.
   Accept edits if suggested.

7. **Write note**
   Check if Obsidian CLI is available:
   ```bash
   which obsidian
   ```
   If available, compose content following `templates/brag.md` structure.
   For new document:
   ```bash
   obsidian create path="Brags/Brags 2025.md" content="# March 2025" silent
   ```
   For existing document - append achievement to the appropriate category:
   ```bash
   obsidian append path="Brags/Brags 2025.md" content="- **Reduced API latency by 40%**\n  - Context: Checkout refactor\n  - Result: Improved response time"
   ```
   If CLI is not available, fall back to Write tool (new) or Edit tool (append)
   to modify the file directly at the vault path (ask user for vault path on first use).

## Achievement Format

```markdown
- **Reduced API latency by 40% through query optimization**
  - Context: Checkout refactor project
  - Result: Improved user experience, reduced server costs by $2k/month
```

## Guidelines

**DO:**
- Quantify impact when possible (%, $, time saved)
- Include both technical and soft skill achievements
- Record achievements as they happen (don't wait for review)
- Categorize by type (impact, technical, growth)
- Include context for future reference

**DON'T:**
- Be vague about impact ("improved performance" -> "reduced load time by 2s")
- Only record big wins - small consistent improvements matter
- Wait until review season to document
- Use passive voice ("was responsible for" -> "led", "built", "shipped")

## Categorization

Common categories for organizing brags:
- **Impact** - Business results, user metrics
- **Technical** - Architecture, performance, reliability
- **Growth** - Learning, mentoring, new skills, feedback received

## Next Steps

- User may want to review full document periodically
- User may extract achievements for resume or performance review
