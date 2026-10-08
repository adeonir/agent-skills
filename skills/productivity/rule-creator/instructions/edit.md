# Edit

Update an existing rule by name.

## Workflow

1. **Resolve the target across both levels.** Resolve `<this-skill>` to the directory the `SKILL.md` was read from, then run `python3 <this-skill>/scripts/rules_index.py`. Match X against its output: a filename (`testing.md`), a topic (`testing`), or a rule title (`Test File Placement`). Ambiguous, including the same topic present at both levels → list the candidates with their level and ask.
2. **Read the file.** Output the current rule, or the full file when there is only one rule. When the index marks the file as a symlink, name its target and state that the edit writes through to every project linked to it.
3. **Apply the requested change.**
4. **Load [rule-format.md](../references/rule-format.md)** and re-run its verifiability checklist against the edited rule.
5. **Load [classify-and-context.md](../references/classify-and-context.md)** and re-run its context check when the scope or the stack reference changed.
6. **Write back.** Preserve the order of unrelated rules in the file.
7. **Report.** Report the path, what changed in one to three sentences, and any open item the rule carries. Never paste the rule.

## When the rule does not exist

Tell the user the rule is missing and offer to create it. Do not silently fall through to create; ask explicitly.
