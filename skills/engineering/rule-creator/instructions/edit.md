# Edit

Update an existing rule by name.

## Workflow

1. **Resolve the target across both levels.** The user said "edit rule X". X may be a filename (`testing.md`), a topic (`testing`), or a rule title (`Test File Placement`).
   - Filename match → use directly.
   - Topic match → use `<topic>.md`.
   - Rule title match → grep H2 headings across both rules directories, pick the file that contains it.
   - Ambiguous, including the same topic present at both levels → list candidates with their level and ask.
2. **Read the file.** Output the current rule, or the full file when there is only one rule. When the resolved path is a symlink, name its target and state that the edit writes through to every project linked to it, then confirm before applying.
3. **Apply the requested change.** Common changes: update the Impact level, refine the explanation paragraph, replace an Incorrect or Correct example, add or update a Reference link, tighten the `paths:` glob.
4. **Load [rule-format.md](../references/rule-format.md)** and re-run its verifiability checklist against the edited rule.
5. **Load [classify-and-context.md](../references/classify-and-context.md)** and re-run its context check when the scope or the stack reference changed.
6. **Write back.** Preserve the order of unrelated rules in the file.

## When the rule does not exist

Tell the user the rule is missing and offer to create it. Do not silently fall through to create; ask explicitly.
