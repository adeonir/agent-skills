# Project Resolution via .notes Registry Symlink

Resolve the vault root, and for project notes the project folder and base tags, from the `wrap-up.yml` registry symlinked into `.notes/`.

## When to Use

- Loaded first by any note-creation reference
- Challenge, brag, transcription, and company writes need the **Vault Root** section only — they write to fixed top-level folders
- Project writes continue through **Project Lookup**

## Vault Root

`.notes/wrap-up.yml` is a local symlink to the shared registry at `{vault_root}/wrap-up.yml` — one registry per vault, shared across every repo. Resolve the symlink target to find the vault root.

When `.notes/wrap-up.yml` is absent, the vault is not linked to this repo yet: see [bootstrap.md](bootstrap.md), then continue here.

## Fixed Folders

Independent of any project entry, at the vault root:

- **Challenges**: `Challenges/{Company}/`
- **Brags**: `Brags/`
- **Meetings / Courses**: `Meetings/` or `Courses/`
- **Companies**: `Companies/{Company}/`

## Config Registry

Schema:

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
- `tags`: base tags applied to every note. Downstream refs append context tags per note.

## Project Lookup

1. Resolve the repo root: `git rev-parse --show-toplevel` if available, otherwise use the current working directory
2. Read `.notes/wrap-up.yml`
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
- **Sessions** (when used): `Work/Acme/Sessions/`

## Rules

- `obsidian.path` is `--`: skip project-folder writes; fixed-folder writes still proceed
- Base tags apply to every note — downstream refs append context tags
- Vault structure mirrors filesystem conventions (`obsidian.path` Title Case)

## Error Handling

- Malformed YAML: surface the error to the user, do not silently overwrite
