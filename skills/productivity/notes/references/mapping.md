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

1. Resolve the repo root: the path on the first line of `git worktree list --porcelain`, after `worktree `. It names the main worktree, so a linked worktree resolves to the same entry. Outside a git repo, use the current working directory.
2. Read `~/.config/wrap-up/projects.yml`. When the file is absent, see [bootstrap.md](bootstrap.md), then continue here.
3. Look up the repo root path as a key in `projects`
4. Hit: use the entry's fields
5. Miss: the repo has no entry yet — see [bootstrap.md](bootstrap.md), then continue here

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

## Error Handling

- Malformed YAML: surface the error to the user, do not silently overwrite
