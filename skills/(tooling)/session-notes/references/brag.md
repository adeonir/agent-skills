# Update Brag Document

Add achievements to brag document for performance reviews and career growth.

## When to Use

- User says "brag document", "my achievements", "add accomplishment"
- User mentions something they're proud of at work
- User wants to track wins for performance review

## Workflow

1. **Determine time period**
   - Current year: `{{YYYY}}.md`
   - Or by quarter: `{{YYYY}} Q1.md`
   - Ask user preference on first use

2. **Check if brag doc exists**
   ```
   search_notes query="{{YYYY}}" path="Brags/"
   ```

3. **Create or append**
   - If doesn't exist: create with template
   - If exists: append new achievement to the appropriate category

4. **Gather achievement details**
   - What was accomplished
   - Context (project, team, situation)
   - Result with metrics (quantify when possible)
   - Category (impact, technical, growth)

5. **Write note**
   New document:
   ```
   write_note path="Brags/{{YYYY}}.md" content="..."
   ```
   Append to existing:
   ```
   read_note path="Brags/{{YYYY}}.md"
   patch_note path="Brags/{{YYYY}}.md" oldString="..." newString="..."
   ```

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
