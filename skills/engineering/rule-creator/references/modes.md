# Modes

Detailed workflow for each mode dispatched by SKILL.md. Create lives
across the SKILL.md gates and the rule-format reference; the other
modes live here.

## When to Use

Loaded when dispatch resolves to list, edit, extract, or delete. The
create mode reads SKILL.md and rule-format directly and does not need
this file.

## List

Read every `.md` file under `.claude/rules/` and produce a table.

### Steps

1. Check `.claude/rules/` exists. If not, output "No rules defined in
   this project." and exit.
2. For each file, read the frontmatter and the H2 headings.
3. Render the table:

   ```
   FILE                  SCOPE                      RULES
   testing.md            global                     3 (1 HIGH, 2 MED)
   api-design.md         src/api/**/*.ts            2 (2 HIGH)
   typescript.md         src/**/*.{ts,tsx}          4 (3 MED, 1 LOW)
   ```

4. Below the table, list each file expanded:

   ```
   testing.md (global)
     - Test File Placement (MEDIUM)
     - Test Naming (LOW)
     - No Shared State Between Tests (HIGH)
   ```

5. Do not modify any file.

## Edit

Update an existing rule by name.

### Steps

1. Resolve target. The user said "edit rule X". X may be a filename
   (`testing.md`), a topic (`testing`), or a rule title (`Test File
   Placement`).
   - Filename match → use directly.
   - Topic match → use `<topic>.md`.
   - Rule title match → grep H2 headings across `.claude/rules/`,
     pick the file that contains it.
   - Ambiguous → list candidates and ask.
2. Read the file. Output the current rule (or the full file when
   there is only one rule).
3. Apply the requested change. Common changes:
   - Update Impact level
   - Refine the explanation paragraph
   - Replace Incorrect or Correct example
   - Add or update Reference link
   - Tighten `paths:` glob
4. Re-run the verifiability checklist from rule-format.md.
5. Re-run the context check from classify-and-context.md when the
   scope or stack reference changes.
6. Write back. Preserve order of unrelated rules in the file.

### When the rule does not exist

Tell the user the rule is missing and offer to create it. Do not
silently fall through to create mode; ask explicitly.

## Extract

Move declarative blocks out of an oversized `CLAUDE.md` into rule
files. Triggered when the user says CLAUDE.md is too big or asks to
split it.

### Steps

1. Read the target CLAUDE.md (project root, `.claude/CLAUDE.md`, or
   nested — confirm which with the user when multiple exist).
2. Walk the headings. For each H2/H3 section, decide a verdict:
   - **Keep in CLAUDE.md** — short, cross-cutting, no clear topic
   - **Extract as rule** — declarative, self-contained, has a
     verifiable instruction
   - **Reject** — procedural (belongs in a skill) or lifecycle
     (belongs in a hook)
3. Output the verdict list:

   ```
   ## Testing conventions          → extract (testing.md, global)
   ## API validation               → extract (api-design.md, src/api/**/*.ts)
   ## Pre-commit checks            → reject (lifecycle, belongs in hook)
   ## General guidance             → keep (cross-cutting)
   ```

4. Ask the user to confirm or amend the verdicts. Never extract
   without explicit approval per item.
5. For each approved extraction:
   - Run the same gates as create: classify, context, scope, render,
     verifiability. The classifier protects against extracting
     something that was procedural after all.
   - Scope each rule to its own topic — drop cross-references to other
     CLAUDE.md sections or sibling rule files; carry only the section's
     own instruction so the rule stands alone.
   - Write the new rule file.
   - Remove the corresponding section from CLAUDE.md.
6. After all extractions, output a summary listing files created and
   sections removed.

### Notes

- The Claude Code docs treat 200 lines as the size at which CLAUDE.md
  starts losing adherence. Use that as the trigger to suggest
  extract, not as a hard rule.
- Path-scoped rules are the primary win — they remove instructions
  from every-session context until Claude touches matching files.

## Delete

Remove a rule file.

### Steps

1. Resolve target the same way as edit.
2. Read the file and show the user what is about to be deleted —
   the full content, not just the filename.
3. Ask for explicit confirmation: "Delete this rule?". Default no.
4. On confirmation, `rm` the file.
5. Output a summary: filename deleted, scope, rule titles removed.

### When a rule contains multiple H2 sections

If the user wants to delete only one rule from a multi-rule file,
route to edit mode instead. Delete operates at file granularity.

## Refuse

Triggered by the classifier in SKILL.md, not by user input directly.

### Steps

1. Output the verdict from the classifier (procedural / lifecycle /
   one-off).
2. Recommend the correct destination:
   - Procedural → author a skill instead
   - Lifecycle → configure a Claude Code hook
   - One-off → do the work directly in the current session
3. Do not write any rule file.
4. Do not invoke another skill automatically. The user confirms and
   re-invokes if needed.
