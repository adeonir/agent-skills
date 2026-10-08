# Project Resolution via the Registry

Resolve the vault paths, and for project notes the project folder, from the registry at `~/.config/wrap-up/projects.yml`.

## When to Use

- Loaded first by every note-creation instruction
- Challenge, brag, transcription, and company writes need the **Vault Root** section only — they write to fixed top-level folders
- Project writes continue through **Project Lookup**

## Vault Root

Every note path is relative to the vault the Obsidian MCP server serves. The vault root needs no registry and no bootstrap.

## Fixed Folders

Independent of any project entry, at the vault root:

- **Challenges**: `Challenges/<Company>/`
- **Brags**: `Brags/`
- **Meetings / Courses**: `Meetings/` or `Courses/`
- **Companies**: `Companies/<Company>/`

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
- `obsidian.path`: Obsidian folder (Title Case, mirrors filesystem). `--` to skip project-folder writes
- `tags`: base tags applied to project notes, alongside tags derived from the content. Fixed-folder notes take tags from their content only.

## Project Lookup

Run `python3 <this-skill>/scripts/registry.py lookup`, resolving `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose that directory, stop and report an environment problem. The script resolves the repo root to the main worktree, so a linked worktree finds the same entry.

- Exit 0: use the entry it prints as JSON (`root`, `name`, `obsidian_path`, `tags`)
- Exit 1: the registry or the entry is missing — load [bootstrap.md](bootstrap.md), then continue here
- Exit 2: the registry cannot be parsed — report the script's message and stop; never edit the registry by hand

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

- **Vault folder for project notes**: `Work/Acme/`
- **Project Overview**: `Work/Acme/Acme Overview.md`

## Rules

- `obsidian.path` is `--`: skip project-folder writes; fixed-folder writes still proceed
- Vault structure mirrors filesystem conventions (`obsidian.path` Title Case)

