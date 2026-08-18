# Registry Bootstrap

Create the vault link and the project entry that [mapping.md](mapping.md) reads.

## When to Use

- `.notes/wrap-up.yml` is absent — the vault is not linked to this repo
- The repo root has no entry under `projects:` in the registry

Both are first-run conditions. Once bootstrapped, mapping resolves without loading this file again.

## Link the Vault

Runs when `.notes/wrap-up.yml` is absent.

### Configured vault path present

`~/.config/wrap-up/vault` holds a valid absolute path to a directory. The vault is already configured on this machine, which is typical for a second or later repo. Do not prompt the user.

1. Read `{vault_root}` from `~/.config/wrap-up/vault`.
2. Verify `{vault_root}` exists as a directory and contains `wrap-up.yml`. If either check fails, continue to the next section.
3. Create the local symlink: `mkdir -p .notes && ln -s {vault_root}/wrap-up.yml .notes/wrap-up.yml`
4. If in a git repo: add `.notes` to `.git/info/exclude` (create the file if needed).

### Configured vault path missing or invalid

The first wrap-up on this machine, and the only path that asks the user for the vault. Ask for the absolute path to the Obsidian vault. After receiving:

1. Verify the path exists as a directory. If invalid, ask again. Do not proceed until valid.
2. If `{vault_path}/wrap-up.yml` does not exist, create it with an empty `projects:` key.
3. Persist the vault path globally so future projects skip the prompt: `mkdir -p ~/.config/wrap-up && printf '%s\n' {vault_path} > ~/.config/wrap-up/vault`
4. Create the local directory and symlink the registry file: `mkdir -p .notes && ln -s {vault_path}/wrap-up.yml .notes/wrap-up.yml`
5. If in a git repo: add `.notes` to `.git/info/exclude` (create the file if needed). Keeps the user-specific path out of the shared `.gitignore`.

## Add the Project Entry

Runs when the repo root is not a key under `projects:`. Ask the user in sequence:

1. Project name (Title Case)
2. Obsidian path (Title Case, e.g. `Work/Acme`, or `--` to skip session)
3. Base tags (comma-separated)

Append the entry under the existing `projects:` key. Do not create a duplicate `projects` key, which would produce invalid YAML. When creating the file for the first time, write the full structure:

```yaml
projects:
  /absolute/path/to/repo:
    name: Project Name
    obsidian:
      path: Prefix/Project
    tags:
      - tag1
```

A new project in an existing vault appends one entry — no restructuring.

## Error Handling

- Configured vault path points at a non-existent directory or a vault without `wrap-up.yml`: treat it as missing and ask for the vault path
- Invalid vault path: ask again until a valid directory is provided
