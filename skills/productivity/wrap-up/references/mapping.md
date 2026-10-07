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

1. Resolve the repo root: the path on the first line of `git worktree list --porcelain`, after `worktree `. It names the main worktree, so a linked worktree resolves to the same entry. Outside a git repo, use the current working directory.
2. Read `~/.config/wrap-up/projects.yml`. When the file is absent, load [bootstrap.md](bootstrap.md), then continue here.
3. Look up the repo root path as a key in `projects`
4. Entry found: use the entry's fields
5. Entry not found: load [bootstrap.md](bootstrap.md), then continue here

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

## Error Handling

- Malformed YAML: surface the error to the user, do not silently overwrite
