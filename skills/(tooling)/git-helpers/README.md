# Git Helpers

Git workflow skill for conventional commits, confidence-scored code review, PR description generation, and pull request creation.

## Installation

```bash
npx skills add adeonir/agent-skills --skill git-helpers
```

## What It Does

Streamlines the git workflow from local changes to merged PR:

```mermaid
flowchart LR
    A[Commit] --> B[Review]
    B --> C[Summary]
    C --> D[Create PR]
```

1. **Commit** - Creates well-formatted conventional commit messages
2. **Review** - Finds bugs, security issues, and guideline violations
3. **Summary** - Generates PR description with impact assessment (saves to `PR_SUMMARY.md`)
4. **Create PR** - Pushes branch and creates pull request via GitHub CLI

## Usage

Use any workflow independently or chain them together:

```
# Commit
commit these changes
commit only staged files

# Review
review my changes
review against main
code review and post as PR comment

# Summary
summarize these changes
generate PR description

# Create PR
push and create PR
create pull request against main

# Chained workflow
commit these changes
review my changes
summarize these changes
push and create PR
```

### Quick Bug Fix

```
# You fixed a bug and want to commit
commit these changes
# Output: "fix: resolve null pointer in user service"

# Create PR directly (skip review for hotfix)
push and create PR
```

### Feature with Full Review

```
# You implemented a new feature
commit these changes
# Output: "feat: add email notifications for orders"

# Review before pushing
review my changes
# Output: CODE_REVIEW.md with findings

# Generate detailed PR description
summarize these changes
# Output: PR_SUMMARY.md created

# Push and create PR
push and create PR
```

## Output

| Workflow | Artifact |
|----------|----------|
| Review | `CODE_REVIEW.md` (findings with confidence scores) |
| Summary | `PR_SUMMARY.md` (PR description with impact assessment) |

## Requirements

- Git
- `gh` CLI (for PR operations)

## Integration

| Skill | How git-helpers connects |
|-------|-------------------------|
| **spec-driven** | Commit and PR workflows after completing implementation tasks |

## FAQ

**Q: Do I need to stage files before committing?**
A: No. By default, the skill stages all modified/new files. Use "commit only staged files" if you prefer to stage manually.

**Q: What base branch is used for comparisons?**
A: Defaults to `main`. You can override by specifying explicitly: "review against develop".

**Q: Why are some issues not reported?**
A: The skill uses conservative confidence scoring (>= 80). Style preferences, hypothetical issues, and "could be simplified" suggestions are intentionally skipped.

**Q: Can I use this without `gh` CLI?**
A: Yes, for commit and review workflows. PR creation requires `gh` CLI.

**Q: How does the guidelines audit work?**
A: It searches for CLAUDE.md and AGENTS.md files in your repository root and checks if your changes comply with documented rules.
