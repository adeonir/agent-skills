# Project Resolution via .notes Registry Symlink

Resolve vault root, project config, and base tags via a `.notes/` local directory that carries a symlinked `wrap-up.yml` registry file.

## When to Use

- Always loaded first by note-creation refs that need vault paths
- Project, transcription, brag, challenge, and company writes depend on the output of this resolution

## Vault Discovery

Resolution order (stop at the first hit):

1. **Local symlink**: `.notes/wrap-up.yml` exists in the repo. Resolve the symlink target to find the vault root. Continue to project lookup.
2. **Global pointer**: `~/.config/wrap-up/vault` exists and contains a valid absolute path to a directory. Use it as the vault root, then run **auto link** to create the local symlink without prompting. Continue to project lookup.
3. **Bootstrap**: neither exists. Run **vault bootstrap** — the only path that asks the user for the vault path.

### Auto Link

Used when the global pointer resolves but the local symlink is missing (typical second-and-later projects on a machine where the vault is already configured). No prompt.

1. Read `{vault_root}` from `~/.config/wrap-up/vault`.
2. Verify `{vault_root}` exists as a directory and contains `wrap-up.yml`. If either check fails, fall through to vault bootstrap.
3. Create the local symlink: `mkdir -p .notes && ln -s {vault_root}/wrap-up.yml .notes/wrap-up.yml`
4. If in a git repo: add `.notes` to `.git/info/exclude` (create the file if needed).
5. Continue to project lookup.

### Vault Bootstrap

Runs only when both the local symlink and the global pointer are missing — i.e. the first vault use on this machine. Ask the user for the absolute path to the Obsidian vault. After receiving:

1. Verify the path exists as a directory. If invalid, ask again. Do not proceed until valid.
2. If `{vault_path}/wrap-up.yml` does not exist, create it with an empty `projects:` key.
3. Persist the vault path globally so future projects skip the prompt: `mkdir -p ~/.config/wrap-up && printf '%s\n' {vault_path} > ~/.config/wrap-up/vault`
4. Create the local directory and symlink the registry file: `mkdir -p .notes && ln -s {vault_path}/wrap-up.yml .notes/wrap-up.yml`
5. If in a git repo: add `.notes` to `.git/info/exclude` (create the file if needed). Keeps the user-specific path out of the shared `.gitignore`.
6. Continue to project lookup.

## Config Registry

Path: `.notes/wrap-up.yml` — local file symlink to the shared registry at `{vault_root}/wrap-up.yml` (one registry per vault, shared across all repos).

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
- `obsidian.path`: Obsidian folder (Title Case, mirrors filesystem). `--` to skip Obsidian session
- `tags`: base tags applied to every note. Downstream refs append context tags per note.

## Project Lookup

1. Resolve the repo root: `git rev-parse --show-toplevel` if available, otherwise use the current working directory
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

Append the entry under the existing `projects:` key. Do not create a duplicate `projects` key, which would produce invalid YAML. When creating the file for the first time, write the full structure:

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

- **Vault folder for project notes**: `Work/Acme/`
- **Project Overview**: `Work/Acme/Acme Overview.md`
- **Sessions** (when used): `Work/Acme/Sessions/`
- Fixed top-level folders independent of project mapping:
  - **Challenges**: `Challenges/{Company}/`
  - **Brags**: `Brags/`
  - **Meetings / Courses** (transcriptions): `Meetings/` or `Courses/`
  - **Companies**: `Companies/{Company}/`

## Rules

- `obsidian.path` is `--`: skip project-folder writes; fixed-folder writes (Challenges, Brags, Meetings, Companies) still proceed
- Base tags apply to every note — downstream refs append context tags
- Vault structure mirrors filesystem conventions (`obsidian.path` Title Case)
- New project in existing vault: bootstrap appends one entry, no restructuring needed

## Error Handling

- `.notes/wrap-up.yml` missing, global pointer present: run auto link, continue without prompting
- `.notes/wrap-up.yml` missing, global pointer missing or invalid: run vault bootstrap, ask for vault path once
- Global pointer points at a non-existent directory or vault without `wrap-up.yml`: treat as missing, fall through to vault bootstrap
- Invalid vault path during bootstrap: ask again until a valid directory is provided
- `wrap-up.yml` missing at vault root: create it with an empty `projects:` key during vault bootstrap
- Repo root not in registry: run project bootstrap, append entry
- Malformed YAML: surface the error to the user, do not silently overwrite
