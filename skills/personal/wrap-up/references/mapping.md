# Project Resolution via .notes Registry Symlink

Resolve vault root, project config, and base tags from the `wrap-up.yml` registry symlinked into `.notes/`.

## When to Use

- Always loaded first, before any other reference
- All wrap-up steps depend on the output of this resolution

## Vault Root

`.notes/wrap-up.yml` is a local symlink to the shared registry at `{vault_root}/wrap-up.yml` — one registry per vault, shared across every repo. Resolve the symlink target to find the vault root.

When `.notes/wrap-up.yml` is absent, the vault is not linked to this repo yet: see [bootstrap.md](bootstrap.md), then continue here.

## Config Registry

Schema:

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

1. Resolve the repo root: `git rev-parse --show-toplevel` if available, otherwise use the current working directory
2. Read `.notes/wrap-up.yml`
3. Look up the repo root path as a key in `projects`
4. Entry found: use the entry's fields
5. Entry not found: see [bootstrap.md](bootstrap.md), then continue here

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

## Rules

- `obsidian.path` is `--`: skip Obsidian session note
- Daily note always runs, even when `obsidian.path` is `--`
- Base tags apply to every note — downstream refs append context tags
- Vault structure mirrors filesystem conventions (`obsidian.path` Title Case)

## Error Handling

- Malformed YAML: surface the error to the user, do not silently overwrite
