# Git Helpers

Git workflow skill for conventional commits, pull request creation, and pull request merging.

## What It Does

Runs the git workflow from local changes to merged PR:

```mermaid
flowchart LR
    A[Commit] --> B[Create PR]
    B --> C[Merge PR]
```

| Phase | Output |
|-------|--------|
| Commit | Conventional commit message based on staged diff |
| Create PR | Opened pull request via `gh` CLI |
| Merge PR | Merged pull request via `gh` CLI; optional cleanup commands shown |

## Usage

Use any workflow independently or chain them:

```text
commit these changes
commit only staged files

push and create PR
create pull request against main

merge PR
merge pull request
```

### Quick bug fix

```text
commit these changes
push and create PR
```

### Feature flow

```text
commit these changes
push and create PR
merge pull request
```

## Requirements

- Git
- `gh` CLI (for PR operations)

## FAQ

**Q: Do I need to stage files before committing?** A: No. By default, the skill stages modified and untracked files by name. If you already staged something before asking, the skill flags it so nothing lands silently. Use "commit only staged files" if you prefer to stage manually and skip the auto-stage step.

**Q: What base branch is used for pull requests?** A: The repo's default branch, with `main` as fallback. The base is shown for confirmation before the PR opens, so you can point the PR at another branch then — or name it upfront: "create PR against develop".

**Q: Can I use this without `gh` CLI?** A: Yes, for the commit workflow. PR creation and merge operations require `gh` CLI.

**Q: Does "merge pull request" run start to finish on its own?** A: No. It asks for confirmation before merging the pull request.

**Q: Does the skill delete branches?** A: No. After a successful merge, it can display local and remote deletion commands for the user to run manually.
