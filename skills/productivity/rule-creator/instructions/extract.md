# Extract

Move declarative blocks out of an oversized memory file into rule files.

## The source sets the level

Level is a property of where the extraction starts, never a judgment about a section's content:

| Source | Destination |
|--------|-------------|
| `./AGENTS.md`, `./CLAUDE.md`, `./.claude/CLAUDE.md` | `.claude/rules/` |
| `~/.claude/CLAUDE.md` | `~/.claude/rules/` |

One run has one source, so one destination level. Never move a section across levels: when a project section reads like a personal preference that belongs at user level, report it as a finding and stop. The user re-runs extract against the other source if they agree.

## Workflow

Resolve `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose it, stop and report an environment problem.

1. **Load [classify-and-context.md](../references/classify-and-context.md).** The classifier, the context check, and the destination decision this instruction runs per approved section.
2. **Resolve the source.** Run `python3 <this-skill>/scripts/resolve_memory.py <memory-file>`. It follows the `@path` imports, prints the resolved line count, and maps each H2 and H3 to the file and line that hold it. Target the file that holds the sections; when the sections sit in several files, confirm the source with the user. Done when one source file is named.
3. **Measure the resolved content** with the `RESOLVED LINES` count the script printed, not the file on disk. The docs put the target at under 200 lines per memory file, past which context cost rises and adherence drops. Use the number to suggest extract, never as a hard gate.
4. **Walk the headings.** For each H2/H3 section, decide a verdict:
   - **Keep** — short, cross-cutting, no clear topic
   - **Extract as rule** — declarative, self-contained, has a verifiable instruction
   - **Reject** — procedural (belongs in a skill) or lifecycle (belongs in a hook)
5. **Output the verdict list:**

   ```text
   ## Testing conventions          → extract (testing.md, unconditional)
   ## API validation               → extract (api-design.md, src/api/**/*.ts)
   ## Pre-commit checks            → reject (lifecycle, belongs in hook)
   ## General guidance             → keep (cross-cutting)
   ```

6. **Ask the user to confirm or amend the verdicts.** Never extract without explicit approval per item.
7. **Write the rules.** Run `python3 <this-skill>/scripts/rules_index.py` once. For each approved extraction:
   - Skip a section whose heading matches an H2 the index lists at the destination level; an earlier run extracted it. Record it as already extracted.
   - Run the gates from the loaded reference: classify, context, destination. The classifier protects against extracting something that was procedural after all. The destination gate resolves scope only — the level is already fixed by the source.
   - Load [rule-format.md](../references/rule-format.md) and render the rule through its template, then run its verifiability checklist.
   - Scope each rule to its own topic — drop cross-references to other sections of the source or to sibling rule files; carry only the section's own instruction so the rule stands alone.
   - Write the new rule file.

   Done when every approved section has a rule file, written now or found from an earlier run.
8. **Remove the extracted sections from the source.** Only after step 7 is done, remove each section that has a rule file: its heading and its body, up to the next heading of the same or a higher level.
9. **Verify the source.** Run `resolve_memory.py` on the memory file again. Every extracted heading is gone, and every kept or rejected heading is still listed. If a check fails, restore what was lost from the source text read in step 4 and return to step 8.
10. **Output a summary** listing files created, sections already extracted, and sections removed.

## Notes

- Path-scoped rules are the primary win — they remove instructions from every-session context until Claude touches matching files. They are available at project level only.
- Claude Code loads `AGENTS.md` when no `CLAUDE.md` or `CLAUDE.local.md` sits in the working directory or above it, or when a `CLAUDE.md` imports or symlinks to it. Removing a section from an `AGENTS.md` that neither case loads changes nothing for Claude; say so before editing — the file is reaching other agents, not this one.
