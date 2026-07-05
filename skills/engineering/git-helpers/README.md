# Git Helpers

Git workflow skill for conventional commits, pull request creation, and branch lifecycle.

## What It Does

Runs the git workflow from local changes to merged PR:

```mermaid
flowchart LR
    A[Commit] --> B[Create PR]
    B --> C[Finish]
```

| Phase | Output |
|-------|--------|
| Commit | Conventional commit message based on staged diff |
| Create PR | Pushed branch + opened pull request via `gh` CLI |
| Finish Branch | Branch updated, merged, deleted local + remote |

## Usage

Use any workflow independently or chain them:

```text
commit these changes
commit only staged files

push and create PR
create pull request against main

finish branch
merge branch
merge PR
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
finish branch
```

## Requirements

- Git
- `gh` CLI (for PR operations)

## FAQ

**Q: Do I need to stage files before committing?**
A: No. By default, the skill stages modified and untracked files by name. If you already staged something before asking, the skill gives a heads-up so nothing lands silently. Use "commit only staged files" if you prefer to stage manually and skip the auto-stage step.

**Q: What base branch is used for pull requests?**
A: The repo's default branch, detected via `gh` (with `main` as fallback). Override by specifying explicitly: "create PR against develop".

**Q: Can I use this without `gh` CLI?**
A: Yes, for the commit workflow. PR creation and merge operations require `gh` CLI.
