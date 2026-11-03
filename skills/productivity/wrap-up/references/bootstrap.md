# Registry Bootstrap

Create or update the project entry that the project lookup reads, and create the registry when it is absent.

## When to Use

- `~/.config/wrap-up/projects.yml` is absent
- The repo root has no entry under `projects:` in the registry

Once bootstrapped, the project lookup resolves without loading this file again.

## Check for a Moved Project

When the lookup listed entries whose root no longer exists, ask the user whether this repo is one of them. On yes, follow Update the Project Entry; on no, follow Add the Project Entry. When the lookup listed none, follow Add the Project Entry.

## Update the Project Entry

Ask the user for the new project name, Obsidian path, and base tags, showing the current values to keep.

Run `python3 <this-skill>/scripts/registry.py update --from "<old-root>" --name "<name>" --path "<obsidian-path>" --tags "<tags>"`. The script moves the entry to the repo root and reads it back. On exit 2 because the repo root already has an entry, show that entry and ask whether to overwrite it; on yes, run the command again with `--replace`. On any other exit 2, report the script's message and stop.

Keep the `previous_name`, `previous_obsidian_path`, and `previous_tags` the script prints for the note workflow. Done when the script exits 0.

## Add the Project Entry

Ask the user in sequence:

1. Project name (Title Case)
2. Obsidian path (Title Case, e.g. `Work/Acme`, or `--` to skip session)
3. Base tags (comma-separated)

Then run `python3 <this-skill>/scripts/registry.py add --name "<name>" --path "<obsidian-path>" --tags "<tags>"`. The script creates the registry when absent, appends the entry for the repo root, and reads it back. Done when the script exits 0; on exit 2, report its message and stop.
