# Git Helpers

Git workflow skill for conventional commits, confidence-scored code review, PR description generation, and pull request creation.

## What It Does

This skill streamlines the git workflow from local changes to merged PR:

```
commit --> review --> summary --> push PR
```

1. **Commit** - Creates well-formatted conventional commit messages
2. **Review** - Finds bugs, security issues, and guideline violations
3. **Summary** - Generates PR description with impact assessment (saves to `PR_DETAILS.md`)
4. **Push PR** - Pushes branch and creates PR via GitHub CLI

## Usage

Use any workflow independently or chain them together:

### Individual Workflows

```
commit these changes
commit only staged files

review my changes
review against main
code review and post as PR comment

summarize these changes
generate PR description

push and create PR
create pull request against main
```

### Chained Workflow Example

```
# Complete workflow from commit to PR
commit these changes
review my changes
summarize these changes
push and create PR
```

## Examples

### Example 1: Quick Bug Fix

```
# You fixed a bug and want to commit
commit these changes

# Output: "fix: resolve null pointer in user service"

# Create PR directly (skip review for hotfix)
push and create PR
```

### Example 2: Feature with Full Review

```
# You implemented a new feature
commit these changes

# Output: "feat: add email notifications for orders"

# Review before pushing
review my changes

# Output: CODE_REVIEW.md with findings
# "[85] [orders.ts:42] Potential race condition in email queue"

# Generate detailed PR description
summarize these changes

# Output: PR_DETAILS.md created

# Push and create PR
push and create PR
```

### Example 3: Review Against Specific Branch

```
# You're on a feature branch, want to review against develop
review against develop

# Or post review as PR comment
review my changes and post as PR comment
```

### Example 4: Commit Only Staged Files

```
# You staged specific files manually
commit only staged files

# Only commits what you staged, doesn't run git add .
```

### Example 5: Partial Workflow

```
# Just need a commit message
commit these changes

# Just need PR description without pushing
summarize these changes

# Just review uncommitted changes
review my changes
```

## Details

### Commit

Analyzes your diff and creates a conventional commit message (`feat:`, `fix:`, `refactor:`, etc). Stages all files by default, or use "commit only staged files" to commit only what's already staged.

### Review

Analyzes changes for security issues, bugs, data loss risks, and performance problems. Only reports issues with >= 80 confidence. Also checks compliance with project guideline files (CLAUDE.md, AGENTS.md).

### Describe (Summary)

Creates `PR_DETAILS.md` with categorized file changes, technical flow, impact assessment (Risk/Performance/Compatibility), testing instructions, and priority review areas.

### Push PR

Requires `gh` CLI. Pushes branch and creates PR with formatted title and concise body.

## Requirements

- Git
- `gh` CLI (for PR operations)

Works with any agent that supports the standard skill format (SKILL.md + references).

---

## FAQ

**Q: Do I need to stage files before committing?**
A: No. By default, the skill stages all modified/new files. Use "commit only staged files" if you prefer to stage manually.

**Q: What base branch is used for comparisons?**
A: Auto-detection order: `development` → `main` → `master`. You can also specify explicitly: "review against main".

**Q: Why are some issues not reported?**
A: The skill uses conservative confidence scoring (>= 80). Style preferences, hypothetical issues, and "could be simplified" suggestions are intentionally skipped.

**Q: Can I use this without `gh` CLI?**
A: Yes, for commit and review workflows. PR creation requires `gh` CLI.

**Q: How does the guidelines audit work?**
A: It searches for CLAUDE.md and AGENTS.md files in your repository root and checks if your changes comply with documented rules.
