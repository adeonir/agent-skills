# Wrap Up Session

End-of-session documentation to Obsidian.

## What It Does

```mermaid
flowchart TD
    A[Resolve Project] --> B[Load Handoff]
    B --> C[Obsidian Session Note]
    C --> D[Obsidian Daily Note]
    D --> E[Detect Structural Delta]
    E --> F[Clear Handoff opt-in]
```

| Step | System | Output | Audience |
|------|--------|--------|----------|
| Resolve Project | -- | Obsidian path, base tags | Internal |
| Load Handoff | filesystem | Latest snapshot folded into context | Internal |
| Obsidian Session | Obsidian | Session note (work details) | Humans |
| Obsidian Daily | Obsidian | Daily note (day summary) | Humans |
| Cleanup | filesystem | Empty handoff file (opt-in) | Internal |

## Usage

```
wrap up
end session
finish up
close session
```

## Output

- Obsidian session notes under `{obsidian.path}/Sessions/`
- Obsidian daily note in `Daily/YYYY-MM-DD.md`

## Requirements

- MCPVault MCP server (for Obsidian notes)
- `.notes/` symlink in the repo root pointing to the Obsidian vault
- `wrap-up.yml` at the vault root with a `projects` registry

## FAQ

**Q: What happens if Obsidian MCP is unavailable?**
A: The session step is skipped with a warning. The daily note still
attempts to write. The skill is best-effort.

**Q: Does it ask before clearing the session handoff?**
A: Yes. The handoff persists across sessions by design, so wrap-up
asks before clearing it. Decline to keep snapshot history; accept to
reset.

**Q: Can I run wrap-up multiple times in a day?**
A: Yes. Existing notes are detected and appended to rather than
overwritten. The daily note merges activities from each invocation.

**Q: What if the project is not in the registry yet?**
A: A bootstrap prompt asks for project name, Obsidian path, and base
tags. The new entry is appended to `wrap-up.yml`.
