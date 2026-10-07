# Registry Bootstrap

Create the registry and the project entry that [mapping.md](mapping.md) reads.

## When to Use

- A project write found `~/.config/wrap-up/projects.yml` absent
- A project write found no entry for the repo root under `projects:`

Both are first-run conditions. Once bootstrapped, mapping resolves without loading this file again.

## Create the Registry

Runs when `~/.config/wrap-up/projects.yml` is absent. Create the directory with `mkdir -p ~/.config/wrap-up`, then write the file with an empty `projects:` key.

## Add the Project Entry

Runs when a project write finds no key for the repo root under `projects:`. The key is the repo root mapping resolved. Ask the user in sequence:

1. Project name (Title Case)
2. Obsidian path (Title Case, e.g. `Work/Acme`, or `--` to skip project-folder writes)
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
