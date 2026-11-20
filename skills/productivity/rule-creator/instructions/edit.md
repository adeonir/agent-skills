# Edit

Update an existing rule by name.

## Workflow

1. **Resolve the target across every rules directory.** Resolve `<this-skill>` to the directory the `SKILL.md` was read from, then run `python3 <this-skill>/scripts/rules_index.py`. Match X against its output: a filename (`testing.md`), a topic (`testing`), or a rule title (`Test File Placement`). Ambiguous, including the same topic present in more than one directory → list the candidates with their level and ask.
2. **Read the file.** Output the current rule, or the full file when there is only one rule. When the index marks the file as a symlink, name its target and state that the edit writes through to every project linked to it.
3. **Apply the requested change.**
4. **Load [rule-format.md](../references/rule-format.md)** and re-run its verifiability checklist against the edited rule.
5. **Load [classify-and-context.md](../references/classify-and-context.md)** and re-run its context check when the scope or the stack reference changed.
6. **Write back.** Preserve the order of unrelated rules in the file. Then run `python3 <this-skill>/scripts/rules_index.py`: the file carries no note about a departure from the template. When a note names it, fix the file and run the script again.
7. **Report.** Report three labelled fields: `Path`; `Changed`, what changed in one to three sentences; `Open items`, the link command for the user to run in other projects, the pointer line an agents rule needs in the memory file, or `none`. Never paste the rule.

## When the rule does not exist

Tell the user the rule is missing and offer to create it. Do not silently fall through to create; ask explicitly.
