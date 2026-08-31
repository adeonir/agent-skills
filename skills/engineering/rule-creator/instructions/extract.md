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

1. **Load [classify-and-context.md](../references/classify-and-context.md)** — the classifier, the context check, and the destination decision this instruction runs per approved section.
2. **Resolve the source.** A `CLAUDE.md` may be a pointer rather than the content — a one-line `@AGENTS.md` import carries the whole imported file. Follow imports as the loaded reference describes, then target the file that actually holds the content. Confirm with the user when several independent sources exist.
3. **Measure the resolved content**, not the file on disk. The docs put the target at under 200 lines per memory file, past which context cost rises and adherence drops; a one-line `CLAUDE.md` importing four hundred lines is over it. Use the number to suggest extract, never as a hard gate.
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
7. **For each approved extraction:**
   - Run the gates from the loaded reference: classify, context, destination. The classifier protects against extracting something that was procedural after all. The destination gate resolves scope only — the level is already fixed by the source.
   - Load [rule-format.md](../references/rule-format.md) and render the rule through its template, then run its verifiability checklist.
   - Scope each rule to its own topic — drop cross-references to other sections of the source or to sibling rule files; carry only the section's own instruction so the rule stands alone.
   - Write the new rule file.
   - Remove the corresponding section from the source file.
8. **Output a summary** listing files created and sections removed.

## Notes

- Path-scoped rules are the primary win — they remove instructions from every-session context until Claude touches matching files. They are available at project level only.
- Claude Code reads `CLAUDE.md`, not `AGENTS.md`. Removing a section from an `AGENTS.md` changes what Claude loads only when a `CLAUDE.md` imports it or symlinks to it; when nothing does, say so before editing — the file is reaching other agents, not this one.
