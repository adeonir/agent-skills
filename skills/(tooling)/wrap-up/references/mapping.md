# Project Resolution via .notes Symlink

Resolve vault root, project config, and base tags via a `.notes/`
symlink and a shared `wrap-up.yml` registry.

## When to Use

- Always loaded first, before any other reference
- All wrap-up steps depend on the output of this resolution

## Vault Discovery

Check `.notes/` in the current working directory (symlink or real directory).

- Exists: resolve its target as the vault root. Continue to project lookup.
- Missing: run vault bootstrap.

### Vault Bootstrap

Ask the user for the absolute path to the Obsidian vault. After receiving:

1. Verify the path exists as a directory. If invalid, ask again. Do not
   proceed until valid.
2. Create the symlink: `ln -s {vault_path} .notes`
3. If in a git repo: add `.notes` (no trailing slash) to
   `.git/info/exclude` (create the file if needed). Git treats symlinks
   as files, so `.notes/` would fail to match. This avoids polluting the
   shared `.gitignore` with a user-specific entry.
4. Continue to project lookup.

## Config Registry

Path: `.notes/wrap-up.yml` (at vault root, shared across all repos).

Schema:

```yaml
projects:
  /absolute/path/to/repo:
    name: Project Name
    bm:
      project: main
      path: prefix/project
    obsidian:
      path: Prefix/Project
    tags:
      - base-tag-1
      - base-tag-2
```

Fields:

- `name`: Title Case project name, used in headers and wikilinks
- `bm.project`: BM project identifier (default `main`). `--` to skip BM
- `bm.path`: BM directory (lowercase, mirrors filesystem). `--` to skip BM
- `obsidian.path`: Obsidian folder (Title Case, mirrors filesystem).
  `--` to skip Obsidian session
- `tags`: base tags applied to every note — session, decision, daily.
  Downstream refs append context tags per note.

## Project Lookup

1. Resolve the repo root: `git rev-parse --show-toplevel` if available,
   otherwise use the current working directory
2. Read `.notes/wrap-up.yml`
3. Look up the repo root path as a key in `projects`
4. Hit: use the entry's fields
5. Miss: run project bootstrap

### Project Bootstrap

Ask the user in sequence:

1. Project name (Title Case)
2. BM project (default `main`, or `--` to skip BM)
3. BM path (lowercase, e.g. `work/acme`, or `--` to skip BM)
4. Obsidian path (Title Case, e.g. `Work/Acme`, or `--` to skip session)
5. Base tags (comma-separated)

Append the entry under the existing `projects:` key. Do not create a
duplicate `projects` key, which would produce invalid YAML. When creating
the file for the first time, write the full structure:

```yaml
projects:
  /absolute/path/to/repo:
    name: Project Name
    bm:
      project: main
      path: prefix/project
    obsidian:
      path: Prefix/Project
    tags:
      - tag1
```

## Resolved Paths

Given this entry:

```yaml
/Users/alice/code/acme:
  name: Acme
  bm:
    project: main
    path: work/acme
  obsidian:
    path: Work/Acme
  tags:
    - acme
```

- **BM session**: `work/acme/sessions/YYYY-MM-DD — Description.md`
- **BM decision**: `work/acme/decisions/Title — Theme.md`
- **Obsidian session**: `Work/Acme/Sessions/YYYY-MM-DD — Description.md`
- **Obsidian decision**: `Work/Acme/Decisions/Title — Theme.md`
- **Obsidian daily**: `Daily/YYYY-MM-DD.md` (always the same)

## Rules

- `bm.project` or `bm.path` is `--`: skip auto-memory and BM notes entirely
- `obsidian.path` is `--`: skip Obsidian session and decision notes
- Daily note always runs, even when all other paths are `--`
- Base tags apply to every note — downstream refs append context tags
- Vault structure mirrors filesystem conventions (`bm.path` lowercase,
  `obsidian.path` Title Case)
- New project in existing vault: bootstrap appends one entry, no
  restructuring needed

## Error Handling

- `.notes/` missing: ask for vault path, create symlink, continue
- Invalid vault path: ask again until a valid directory is provided
- `wrap-up.yml` missing at vault root: create on first project bootstrap
- Repo root not in registry: run project bootstrap, append entry
- Malformed YAML: surface the error to the user, do not silently overwrite
