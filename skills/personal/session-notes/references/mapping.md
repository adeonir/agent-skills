# Project Resolution via .notes Registry Symlink

Resolve vault root, project config, and base tags via a `.notes/` local
directory that carries a symlinked `wrap-up.yml` registry file.

## When to Use

- Always loaded first, before any other reference
- All wrap-up steps depend on the output of this resolution

## Vault Discovery

Check `.notes/wrap-up.yml` in the current working directory. The file is
a symlink into the shared registry at the vault root.

- Exists: resolve the symlink target to find the vault root. Continue to
  project lookup.
- Missing: run vault bootstrap.

### Vault Bootstrap

Ask the user for the absolute path to the Obsidian vault. After receiving:

1. Verify the path exists as a directory. If invalid, ask again. Do not
   proceed until valid.
2. If `{vault_path}/wrap-up.yml` does not exist, create it with an empty
   `projects:` key.
3. Create the local directory and symlink the registry file:
   `mkdir -p .notes && ln -s {vault_path}/wrap-up.yml .notes/wrap-up.yml`
4. If in a git repo: add `.notes` to `.git/info/exclude` (create the file
   if needed). Keeps the user-specific path out of the shared `.gitignore`.
5. Continue to project lookup.

## Config Registry

Path: `.notes/wrap-up.yml` — local file symlink to the shared registry at
`{vault_root}/wrap-up.yml` (one registry per vault, shared across all repos).

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
- `tags`: base tags applied to every note — session and daily.
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
- **Obsidian session**: `Work/Acme/Sessions/YYYY-MM-DD — Description.md`
- **Obsidian daily**: `Daily/YYYY-MM-DD.md` (always the same)

## Rules

- `bm.project` or `bm.path` is `--`: skip auto-memory and BM notes entirely
- `obsidian.path` is `--`: skip Obsidian session note
- Daily note always runs, even when all other paths are `--`
- Base tags apply to every note — downstream refs append context tags
- Vault structure mirrors filesystem conventions (`bm.path` lowercase,
  `obsidian.path` Title Case)
- New project in existing vault: bootstrap appends one entry, no
  restructuring needed

## Error Handling

- `.notes/wrap-up.yml` missing: ask for vault path, create the local `.notes/`
  dir and symlink the registry file, continue
- Invalid vault path: ask again until a valid directory is provided
- `wrap-up.yml` missing at vault root: create it with an empty `projects:`
  key during vault bootstrap
- Repo root not in registry: run project bootstrap, append entry
- Malformed YAML: surface the error to the user, do not silently overwrite
