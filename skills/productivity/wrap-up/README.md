# Wrap Up

End-of-session documentation to Obsidian.

## What It Does

```mermaid
flowchart LR
    A[Resolve Project] --> B[Load Handoff]
    B --> C[Obsidian Session Note]
    C --> D[Obsidian Daily Note]
    D --> E[Clear Handoff Automatically]
    E --> F[Offer Archive of Past Months]
```

| Step | Output |
|------|--------|
| Resolve Project | Obsidian path and base tags, used internally |
| Load Handoff | Consolidated handoff context read from the filesystem, used internally |
| Obsidian Session | Session note in Obsidian with the work details |
| Obsidian Daily | Daily note in Obsidian with the day summary |
| Cleanup | Handoff file emptied on the filesystem, automatically |
| Archive offer | Past-month daily notes moved into `Daily/YYYY-MM/` in Obsidian, on yes |

## Usage

```text
/wrap-up
```

The skill runs only from the slash command; the model never starts it on its own.

## Output

- Obsidian session notes under `{obsidian.path}/Sessions/`
- Obsidian daily note at `Daily/YYYY-MM-DD.md`; past months are archived into `Daily/YYYY-MM/` when you accept the offer at the end of a run

## Requirements

| Dependency | Status | Without it |
|------------|--------|------------|
| Obsidian MCP server | required | The workflow cannot write either note |

- An Obsidian vault served by the Obsidian MCP server. On first run in a repo the skill creates the registry at `~/.config/wrap-up/projects.yml` when absent and asks for the project entry.

## FAQ

**Q: What happens if Obsidian MCP is unavailable?** A: The workflow cannot write the session note or the daily note because both use the Obsidian MCP server.

**Q: Does it ask before clearing the session handoff?** A: No. Cleanup writes empty content after every configured note write succeeds. If persistence fails, the handoff remains available for retry.

**Q: Does it move old daily notes on its own?** A: No. When daily notes from an earlier month remain at the root of `Daily/`, the report lists them and asks once whether to move them into `Daily/YYYY-MM/`. Nothing moves without a yes.

**Q: Can I run wrap-up multiple times in a day?** A: Yes. The workflow finds existing notes and appends the new content instead of overwriting them. The daily note merges activities from each invocation.

**Q: What if the project is not in the registry yet?** A: A bootstrap prompt asks for project name, Obsidian path, and base tags. The new entry is appended to `~/.config/wrap-up/projects.yml`.
