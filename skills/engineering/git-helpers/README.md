# Git Helpers

Git workflow skill for conventional commits, confidence-scored code review, and pull request creation.

## What It Does

Streamlines the git workflow from local changes to merged PR:

```mermaid
flowchart LR
    A[Commit] --> B[Review]
    B --> C[Create PR]
    C --> D[Finish]
```

| Phase | Output |
|-------|--------|
| Commit | Conventional commit message based on staged diff |
| Review | Lens-based findings (security, bugs, data-loss, performance, guidelines) with confidence ≥ 80 |
| Create PR | Pushed branch + opened pull request via `gh` CLI |
| Finish Branch | Branch updated, merged, deleted local + remote |

## Usage

Use any workflow independently or chain them:

```text
commit these changes
commit only staged files

review my changes
review against main
code review and post as PR comment

push and create PR
create pull request against main

finish branch
merge branch
merge PR
```

### Quick bug fix

```text
# commit and ship without full review
commit these changes
push and create PR
```

### Feature with full review

```text
commit these changes
review my changes
push and create PR
finish branch
```

## Output

| Workflow | Artifact |
|----------|----------|
| Review | `CODE_REVIEW.md` (findings with confidence scores) — optional, only when user asks to save |

## Requirements

- Git
- `gh` CLI (for PR operations)

## FAQ

**Q: Do I need to stage files before committing?**
A: No. By default, the skill stages modified and untracked files by
name. If you already staged something before asking, the skill gives
a heads-up so nothing lands silently. Use "commit only staged files"
if you prefer to stage manually and skip the auto-stage step.

**Q: What base branch is used for comparisons?**
A: Defaults to `main`. Override by specifying explicitly: "review
against develop".

**Q: Why are some issues not reported?**
A: The skill uses conservative confidence scoring (≥ 80). Style
preferences, hypothetical issues, and "could be simplified" suggestions
are intentionally skipped.

**Q: Can I use this without `gh` CLI?**
A: Yes, for commit and review workflows. PR creation and merge
operations require `gh` CLI.

**Q: How does the guidelines audit work?**
A: It searches for `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, and
`.editorconfig` files inside the repository root and checks if changes
comply with documented rules. Personal global settings (e.g.,
`~/.claude/CLAUDE.md`) are excluded.

**Q: What's the size limit for code review?**
A: 3000 lines or 40 files. Above that, the review stops and suggests
splitting the branch — beyond those limits, fan-out lenses can no
longer reliably hold the full diff in context.
