# Project Resolution via the Registry

Resolve the project entry and the base tags from the registry at `~/.config/wrap-up/projects.yml`.

## When to Use

Loaded to resolve the project entry for this repo and the base tags applied to every note.

## Vault

Every note path is relative to the vault the Obsidian MCP server serves. The registry lives outside the vault and holds no vault path.

## Config Registry

`~/.config/wrap-up/projects.yml`, one registry per machine, shared across every repo. Schema:

```yaml
projects:
  /absolute/path/to/repo:
    name: Project Name
    obsidian:
      path: Prefix/Project
    tags:
      - base-tag-1
      - base-tag-2
```

Fields:

- `name`: Title Case project name, used in headers and wikilinks
- `obsidian.path`: Obsidian folder (Title Case, mirrors filesystem). `--` to skip Obsidian session
- `tags`: base tags applied to every note — session and daily. Downstream refs append context tags per note.

## Project Lookup

Run `python3 <this-skill>/scripts/registry.py lookup`, resolving `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose that directory, stop and report an environment problem. The script resolves the repo root to the main worktree, so a linked worktree finds the same entry.

- Exit 0: use the entry it prints as JSON (`root`, `name`, `obsidian_path`, `tags`)
- Exit 1: the registry or the entry is missing — load [bootstrap.md](bootstrap.md), then continue here
- Exit 2: the registry cannot be parsed — report the script's message and stop; never edit the registry by hand

## Resolved Paths

Given this entry:

```yaml
/Users/alice/code/acme:
  name: Acme
  obsidian:
    path: Work/Acme
  tags:
    - acme
```

- **Obsidian session**: `Work/Acme/Sessions/YYYY-MM-DD — Description.md`
- **Obsidian daily**: `Daily/YYYY-MM-DD.md` (always the same)
