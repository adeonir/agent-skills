# Registry Bootstrap

Create the registry and the project entry that the project lookup reads.

## When to Use

- `~/.config/wrap-up/projects.yml` is absent
- The repo root has no entry under `projects:` in the registry

Both are first-run conditions. Once bootstrapped, the project lookup resolves without loading this file again.

## Create the Registry

Runs when `~/.config/wrap-up/projects.yml` is absent. Create the directory with `mkdir -p ~/.config/wrap-up`, then write the file with an empty `projects:` key.

## Add the Project Entry

Runs when the repo root is not a key under `projects:`. The key is the repo root the project lookup resolved. Ask the user in sequence:

1. Project name (Title Case)
2. Obsidian path (Title Case, e.g. `Work/Acme`, or `--` to skip session)
3. Base tags (comma-separated)

Append the entry under the existing `projects:` key. Do not create a duplicate `projects` key, which would produce invalid YAML:

```yaml
projects:
  /absolute/path/to/repo:
    name: Project Name
    obsidian:
      path: Prefix/Project
    tags:
      - tag1
```

A new project appends one entry — no restructuring.
