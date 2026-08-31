# Create

Author a new rule at the level and scope the input calls for.

## Workflow

Run the gates in order. A failed gate stops the run; never write a partial rule file.

1. **Load [classify-and-context.md](../references/classify-and-context.md)** and classify the input. Procedural multi-step → refuse and recommend authoring a skill instead. Lifecycle event → refuse and recommend a hook. One-off task → refuse, suggest doing it directly. Declarative convention → proceed.
2. **Run the context check** from the same reference. Stack mismatch, duplicate topic across both levels, or contradiction with a memory file → flag and ask before writing.
3. **Decide the destination**, same reference. Level from explicit signals; no signal → ask, because writing to `~/.claude/rules/` reaches every project on the machine. Scope from path signals; a path signal resolves the level to project.
4. **Load [rule-format.md](../references/rule-format.md)** and render through its flexible template. Keep the explanation paragraph; add principles, an `Incorrect`/`Correct` pair, or a reference only when that section clarifies or verifies the constraint.
5. **Run the verifiability checklist** in the loaded format reference. Fail any check → rewrite before saving.
6. **Write.** New topic → new file under the chosen level's rules directory, named for the topic: kebab-case descriptive noun, lowercase ASCII, hyphens only (`testing.md`, `api-design.md` — never `rules.md` or `misc.md`). Discovery is recursive, so a subdirectory (`frontend/testing.md`) is available when a level accumulates enough topics to group them. A shared destination writes the file to the named directory and links it into this project only. Existing topic without conflict → append H2. Existing topic with conflict → ask user.
