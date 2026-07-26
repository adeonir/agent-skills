# Modes

Workflow for the list, edit, extract, and delete modes.

## When to Use

Loaded when dispatch resolves to list, edit, extract, or delete. Create lives across the SKILL.md gates and [rule-format.md](rule-format.md) and does not read this file.

## List

Read every `.md` file under both rules directories and produce a table.

### Steps

1. Walk `~/.claude/rules/` and `.claude/rules/` recursively — discovery includes subdirectories, so a rule at `frontend/testing.md` counts. If neither directory holds a `.md` file, output "No rules defined." and exit.
2. For each file, read the frontmatter and the H2 headings.
3. Render the table, keyed by the path relative to its rules directory:

   ```text
   LEVEL     FILE                  SCOPE                      RULES
   user      preferences.md        unconditional              2 (2 MED)
   project   testing.md            unconditional              3 (1 HIGH, 2 MED)
   project   api-design.md         src/api/**/*.ts            2 (2 HIGH)
   project   frontend/naming.md    src/components/**/*.tsx    1 (1 LOW)
   ```

4. Below the table, list each file expanded:

   ```text
   testing.md (project, unconditional)
     - Test File Placement (MEDIUM)
     - Test Naming (LOW)
     - No Shared State Between Tests (HIGH)
   ```

5. When the same topic path exists at both levels, mark it and state that the project rule prevails.
6. Report a file that does not follow the template as it is — a missing title, Impact line, or Incorrect/Correct pair is noted, never rewritten. Rewriting is the edit mode's job, on request.
7. Do not modify any file.

## Edit

Update an existing rule by name.

### Steps

1. Resolve target across both levels. The user said "edit rule X". X may be a filename (`testing.md`), a topic (`testing`), or a rule title (`Test File Placement`).
   - Filename match → use directly.
   - Topic match → use `<topic>.md`.
   - Rule title match → grep H2 headings across both rules directories, pick the file that contains it.
   - Ambiguous, including the same topic present at both levels → list candidates with their level and ask.
2. Read the file. Output the current rule (or the full file when there is only one rule). When the resolved path is a symlink, name its target and state that the edit writes through to every project linked to it, then confirm before applying.
3. Apply the requested change. Common changes:
   - Update Impact level
   - Refine the explanation paragraph
   - Replace Incorrect or Correct example
   - Add or update Reference link
   - Tighten `paths:` glob
4. Re-run the verifiability checklist from rule-format.md.
5. Re-run the context check from classify-and-context.md when the scope or stack reference changes.
6. Write back. Preserve order of unrelated rules in the file.

### When the rule does not exist

Tell the user the rule is missing and offer to create it. Do not silently fall through to create mode; ask explicitly.

## Extract

Move declarative blocks out of an oversized memory file into rule files.

### The source sets the level

Level is a property of where the extraction starts, never a judgment about a section's content:

| Source | Destination |
|--------|-------------|
| `./AGENTS.md`, `./CLAUDE.md`, `./.claude/CLAUDE.md` | `.claude/rules/` |
| `~/.claude/CLAUDE.md` | `~/.claude/rules/` |

One run has one source, so one destination level. Never move a section across levels: when a project section reads like a personal preference that belongs at user level, report it as a finding and stop. The user re-runs extract against the other source if they agree.

### Steps

1. Resolve the source. A `CLAUDE.md` may be a pointer rather than the content — a one-line `@AGENTS.md` import carries the whole imported file. Follow imports as described in [classify-and-context.md](classify-and-context.md), then target the file that actually holds the content. Confirm with the user when several independent sources exist.
2. Measure the resolved content, not the file on disk. The docs put the target at under 200 lines per memory file, past which context cost rises and adherence drops; a one-line `CLAUDE.md` importing four hundred lines is over it. Use the number to suggest extract, never as a hard gate.
3. Walk the headings. For each H2/H3 section, decide a verdict:
   - **Keep** — short, cross-cutting, no clear topic
   - **Extract as rule** — declarative, self-contained, has a verifiable instruction
   - **Reject** — procedural (belongs in a skill) or lifecycle (belongs in a hook)
4. Output the verdict list:

   ```text
   ## Testing conventions          → extract (testing.md, unconditional)
   ## API validation               → extract (api-design.md, src/api/**/*.ts)
   ## Pre-commit checks            → reject (lifecycle, belongs in hook)
   ## General guidance             → keep (cross-cutting)
   ```

5. Ask the user to confirm or amend the verdicts. Never extract without explicit approval per item.
6. For each approved extraction:
   - Run the same gates as create: classify, context, destination, render, verifiability. The classifier protects against extracting something that was procedural after all. The destination gate resolves scope only — the level is already fixed by the source.
   - Scope each rule to its own topic — drop cross-references to other sections of the source or to sibling rule files; carry only the section's own instruction so the rule stands alone.
   - Write the new rule file.
   - Remove the corresponding section from the source file.
7. After all extractions, output a summary listing files created and sections removed.

### Notes

- Path-scoped rules are the primary win — they remove instructions from every-session context until Claude touches matching files. They are available at project level only.
- Claude Code reads `CLAUDE.md`, not `AGENTS.md`. Removing a section from an `AGENTS.md` changes what Claude loads only when a `CLAUDE.md` imports it or symlinks to it; when nothing does, say so before editing — the file is reaching other agents, not this one.

## Delete

Remove a rule file.

### Steps

1. Resolve target the same way as edit.
2. Read the file and show the user what is about to be deleted — the full content, not just the filename.
3. Ask for explicit confirmation, naming the level: "Delete this rule?". At user level, state that it stops applying to every project on the machine. Default no.
4. On confirmation, `rm` the file.
5. Output a summary: filename deleted, level, scope, rule titles removed.

### When the target is a symlink

Two different acts share one filename, so ask which before removing anything:

- **Unlink here** — remove the link, leaving the shared target intact. The rule stops applying to this project only.
- **Delete the target** — remove the shared file. The rule dies everywhere, and every other project keeps a dangling link the skill cannot reach to clean up.

Default to unlinking; it is the narrower act, and the wider one is not reversible from here.

### When a rule contains multiple H2 sections

If the user wants to delete only one rule from a multi-rule file, route to edit mode instead. Delete operates at file granularity.
