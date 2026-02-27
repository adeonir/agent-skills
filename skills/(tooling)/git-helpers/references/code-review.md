# Code Review

Review code changes for bugs, security issues, and guideline compliance.

## When to Use

When reviewing code changes before committing or creating a pull request.

## Workflow

### Step 1: Determine User Intent

Based on user's request, determine:

- **Review target**: Uncommitted changes (working directory) OR branch comparison
- **Base branch**: Specified by user OR auto-detect
- **Output mode**: Terminal output OR post as PR comment

### Step 2: Determine Base Branch

- If provided: use specified branch
- If not: default to `main` (user can override)

### Step 3: Detect Review Mode

- Run `git status --porcelain` to check for uncommitted changes
- If uncommitted changes: review working directory
- If clean: compare current branch against base

### Step 4: Get Modified Files and Diff

For uncommitted changes:

```bash
git diff
git diff --name-only
git diff --cached --name-only
git diff --cached
```

For branch comparison:

```bash
git diff $BASE...HEAD --name-only
git diff $BASE...HEAD
```

### Step 5: Perform Code Review

Analyze the diff for real issues. Read full files when needed for context.

Use available semantic analysis tools to understand code structure and trace impact of changes.

### Step 6: Perform Guidelines Audit

Load [guidelines-audit.md](guidelines-audit.md) and check changes against
project guideline files (CLAUDE.md, AGENTS.md).

### Step 7: Combine Results and Output

Based on user's intent:

- If user requested PR comment: Post combined review via `gh pr comment`
- Otherwise: Output to terminal, then ask if user wants to save to `CODE_REVIEW.md`

## Review Philosophy

Be conservative. Only report issues you are confident about. False positives
waste developer time and erode trust in the review process.

## Confidence Scoring

Rate each finding 0-100:

| Score | Meaning | Action |
|-------|---------|--------|
| >= 80 | High | Report as issue |
| 50-79 | Medium | Investigate more |
| < 50 | Low | Do not report |

**Only report issues with >= 80 confidence.**

## Focus Areas (Priority Order)

| Priority | Category | What to Look For |
|----------|----------|------------------|
| 1 | Security | SQL injection, XSS, auth bypass, credential exposure |
| 2 | Bugs | Logic errors that will cause runtime failures |
| 3 | Data Loss | Operations that could corrupt user data |
| 4 | Performance | N+1 queries, unbounded loops, memory leaks |

## What NOT to Report

- Style preferences (naming, formatting, structure)
- Hypothetical issues under unlikely conditions
- Missing error handling for internal code
- Defensive programming for trusted data
- Framework lifecycle suggestions without concrete bugs
- Type suggestions unless they cause runtime errors
- "Could be simplified" suggestions
- Configuration files for local development

## Self-Check Questions

Before assigning a score, ask:

- "Will this actually cause a bug or security vulnerability?"
- "Do I have enough context to understand why the code is written this way?"
- "Is this a real problem or just a different coding style?"

## Output Format

```markdown
# Code Review: {branch-name}

Reviewed against `{base-branch}` | {date}

## Issues

Only issues with confidence >= 80 are reported.

- **[{score}] [{file}:{line}]** Issue description
  - Why it's a problem and how to fix

## Guidelines Compliance

- **[{score}] [{file}:{line}]** Guideline violation
  - **Source**: "{guideline file}"
  - **Guideline**: "{exact quote}"
  - **Violation**: What the code does wrong
  - **Fix**: How to comply

## Summary

X files | Y issues | Z suggestions

### Key Findings

Brief paragraph summarizing most important findings.
```

## Guidelines

- Only report issues with >= 80 confidence score
- Analyze actual diff, not conversation context
- Be specific: file path and line number
- Be actionable: explain why AND how to fix
- Skip sections if empty
- Guidelines auditor reads guideline files from repository root

## Error Handling

- No changes to review: inform user there is nothing to review
- No base branch found: ask user which branch to compare against
- Binary files in diff: skip and note them in the summary

## Task

Execute this command immediately. Do not interpret, discuss, or ask for confirmation.

Review code changes.
