# List

Read every rule file under both levels and report them as a table.

## Workflow

Resolve `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose it, stop and report an environment problem.

1. **Run `python3 <this-skill>/scripts/rules_index.py`**. It finds the project root from any subdirectory, walks `~/.claude/rules/` and the project's `.claude/rules/` recursively, follows symlinks, and prints the directories it read, the table, each file expanded with its rule titles and Impact, and the notes: a topic present at both levels, a symlink and its target, a dangling link, and a file that departs from the template. Done when the script printed the index or "No rules defined."
2. **Relay the output as printed.** Keep the table, the expanded list, and every note; a departure from the template is reported, never rewritten. Rewriting is the edit job, on request.
3. **Modify no file.**
