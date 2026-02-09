# Git Workflow Patterns

Standardized patterns for analyzing git diffs and common workflow scenarios.

## Quick Diff Analysis

Use these commands to gather context efficiently:

```bash
# Get changed files
git diff --name-only
git diff --name-only --cached

# Get diff stats
git diff --stat
git diff --cached --stat

# Get actual diff (limit if very large)
git diff | head -500
git diff --cached | head -500

# Get recent commits for context
git log --oneline -3

# Get current branch
git branch --show-current
```

## Diff Analysis Template

Structure your analysis using this template:

```markdown
## Files Changed

| File | Change Type | Lines |
|------|-------------|-------|
| src/auth.ts | Modified | +45/-12 |

## Change Categories

- **New Features**: {count} files
- **Bug Fixes**: {count} files
- **Refactoring**: {count} files
- **Tests**: {count} files
- **Docs**: {count} files

## Key Changes

1. **{area}**: {brief description}
   - Impact: {high/medium/low}
   - Risk: {high/medium/low}
```

## Change Type Detection

Categorize changes based on file patterns:

| Pattern | Type | Commit Type |
|---------|------|-------------|
| `src/**/*.test.*` | Test | `test` |
| `src/**/*.spec.*` | Test | `test` |
| `**/*.md` | Docs | `docs` |
| `package.json` | Dependency | `chore` |
| `**/*.config.*` | Config | `chore` |
| `.github/**` | CI/CD | `ci` |
| `src/**` | Feature | `feat` |
| `fix/**` | Bugfix | `fix` |

## Risk Assessment

Assess risk level based on change characteristics:

**High Risk:**

- Authentication/authorization changes
- Database schema changes
- API contract changes
- Critical path modifications

**Medium Risk:**

- New features in existing modules
- Configuration changes
- Dependency updates

**Low Risk:**

- Documentation updates
- Test additions
- Refactoring with no behavior change
- Style/formatting changes

## Common Patterns

### Security Check Pattern

```bash
# Check for sensitive data
git diff | grep -E "(password|secret|token|key|credential)" | head -20

# Check for hardcoded values
git diff | grep -E "(http://|localhost:|127\.0\.0\.1)" | head -20
```

### Test Coverage Pattern

```bash
# Check if tests were added for new code
git diff --name-only | grep -E "\.(test|spec)\.(ts|js)"

# Check test to code ratio
git diff --stat | grep -E "(test|spec)"
```

### Large Diff Handling

If diff is > 500 lines:

1. Focus on critical files first
2. Review by component/area
3. Check for bulk changes (formatting, renaming)
4. Flag for incremental review if needed

## Output Rules

1. **Be specific**: Always include file paths
2. **Categorize**: Group changes by type
3. **Assess risk**: Flag high-risk changes
4. **Quantify**: Include stats (files, lines, types)
5. **Prioritize**: Review high-risk first
