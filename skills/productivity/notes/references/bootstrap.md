# Registry Bootstrap

Create the project entry that [mapping.md](mapping.md) reads, and the registry when it is absent.

## When to Use

- A project write found `~/.config/wrap-up/projects.yml` absent
- A project write found no entry for the repo root under `projects:`

Both are first-run conditions. Once bootstrapped, mapping resolves without loading this file again.

## Add the Project Entry

Ask the user in sequence:

1. Project name (Title Case)
2. Obsidian path (Title Case, e.g. `Work/Acme`, or `--` to skip project-folder writes)
3. Base tags (comma-separated)

Then run `python3 <this-skill>/scripts/registry.py add --name "<name>" --path "<obsidian-path>" --tags "<tags>"`. The script creates the registry when absent, appends the entry for the repo root, and reads it back. Done when the script exits 0; on exit 2, report its message and stop.
