# Create

Author a new rule at the level and scope the input calls for.

## Workflow

Run the gates in order. A failed gate stops the run; never write a partial rule file.

1. **Load [classify-and-context.md](../references/classify-and-context.md)** and classify the input. Procedural multi-step → refuse and recommend authoring a skill instead. Lifecycle event → refuse and recommend a hook. One-off task → refuse, suggest doing it directly. Declarative convention → proceed.
2. **Run the context check** from the same reference. Resolve `<this-skill>` to the directory the `SKILL.md` was read from; the duplicate check runs `python3 <this-skill>/scripts/rules_index.py`. Stack mismatch, duplicate topic across all four rules directories, or contradiction with a memory file → flag and ask before writing.
3. **Decide the destination**, same reference. Level from explicit signals; no signal → ask, because writing to a user directory reaches every project on the machine. Home from explicit signals; no signal → `.claude/rules/`. Scope from path signals; a path signal resolves the level to project, and an agents rule stays unconditional.
4. **Load [rule-format.md](../references/rule-format.md)** and render through its flexible template. Keep the explanation paragraph; add principles, an `Incorrect`/`Correct` pair, or a reference only when that section clarifies or verifies the constraint.
5. **Run the verifiability checklist** in the loaded format reference. Fail any check → rewrite before saving.
6. **Write.** New topic → new file under the chosen rules directory, named for the topic: kebab-case descriptive noun, lowercase ASCII, hyphens only (`testing.md`, `api-design.md` — never `rules.md` or `misc.md`). Discovery is recursive, so a subdirectory (`frontend/testing.md`) is available when a level accumulates enough topics to group them. A shared destination writes the file to the named directory and links it into this project only. Existing topic without conflict → append H2. Existing topic with conflict → ask user. Then run `python3 <this-skill>/scripts/rules_index.py`: the written file carries no note about a departure from the template. When a note names it, fix the file and run the script again.
7. **Report.** Report three labelled fields: `Path`; `Holds`, what the rule holds in one to three sentences; `Open items`, the link command for the user to run in other projects, the pointer line an agents rule needs in the memory file, or `none`. Never paste the rule.
