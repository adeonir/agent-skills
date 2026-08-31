# List

Read every rule file under both levels and report them as a table.

## Workflow

1. **Walk `~/.claude/rules/` and `.claude/rules/` recursively** — discovery includes subdirectories, so a rule at `frontend/testing.md` counts. If neither directory holds a `.md` file, output "No rules defined." and exit.
2. **For each file, read the frontmatter and the H2 headings.**
3. **Render the table**, keyed by the path relative to its rules directory:

   ```text
   LEVEL     FILE                  SCOPE                      RULES
   user      preferences.md        unconditional              2 (2 MED)
   project   testing.md            unconditional              3 (1 HIGH, 2 MED)
   project   api-design.md         src/api/**/*.ts            2 (2 HIGH)
   project   frontend/naming.md    src/components/**/*.tsx    1 (1 LOW)
   ```

4. **Below the table, list each file expanded:**

   ```text
   testing.md (project, unconditional)
     - Test File Placement (MEDIUM)
     - Test Naming (LOW)
     - No Shared State Between Tests (HIGH)
   ```

5. **Mark a topic path present at both levels** and state that the project rule prevails.
6. **Report a file that does not follow the template as it is** — a missing title, Impact line, or Incorrect/Correct pair is noted, never rewritten. Rewriting is the edit job, on request.
7. **Modify no file.**
