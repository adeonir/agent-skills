# Branch Summary

Generate a comprehensive PR description comparing current branch with base branch,
save to `PR_DETAILS.md`.

## Pre-execution Validation

Always validate before running analysis:

```bash
# Verify base branch exists (priority: development > develop > main > master)
for branch in development develop main master; do
  git show-ref --verify --quiet refs/heads/$branch && echo $branch && break
done

# Confirm current branch is NOT the base branch
git branch --show-current
```

**Requirements:**

- Base branch must exist in repository
- Current branch must NOT be the base branch (avoid empty diffs)

## Process

### Step 1: Detect Base Branch

If not specified:

```bash
for branch in development develop main master; do
  git show-ref --verify --quiet refs/heads/$branch && echo $branch && break
done
```

### Step 2: Gather Context

Run in parallel:

```bash
# Extract tickets from branch name
git branch --show-current

# Get diff statistics
git diff {base}...HEAD --stat

# Get file change status
git diff {base}...HEAD --name-status

# Get commit history
git log {base}..HEAD --oneline

# Get detailed diff for content analysis
git diff {base}...HEAD
```

### Step 3: Analyze and Categorize Files

- **Core Changes**: Main application source files
- **API Changes**: Endpoint modifications, services
- **State Management**: Store/state files
- **UI Components**: Component files
- **Configuration**: Config, package.json, build files
- **Documentation**: README, CLAUDE.md, docs

### Step 4: Assess Risk and Impact

- **Risk Level**: HIGH (breaking changes, DB mods) | MEDIUM (new features, UI changes) | LOW (bug fixes, minor)
- **Performance Impact**: POSITIVE | NEUTRAL | NEGATIVE
- **Compatibility Impact**: NONE | MINOR | MAJOR

### Step 5: Generate PR_DETAILS.md

Use Write tool to create the file with the template below.

## PR_DETAILS.md Template

```markdown
# Brief Descriptive Title

## Summary

[2-3 sentences describing the main functional change - focus on business value]

## Key Changes

### Core Changes (X files)

- **[filename]**: [Brief functional description]

### API Changes (X files)

- **[filename]**: [Brief description]

### State Management (X files)

- **[filename]**: [Brief description]

### UI Components (X files)

- **[filename]**: [Brief description]

### Configuration/Build (X files)

- **[filename]**: [Brief description]

### Documentation (X files)

- **[filename]**: [Brief description]

## Technical Flow

1. [User action or trigger]
2. [How components handle it]
3. [API calls or state updates]
4. [Final outcome or UI response]
5. [Error handling]

**Key Components:**

- **[Component]**: [Role in change]
- **[API/Service]**: [API modifications]
- **[State]**: [State changes]

## Impact Assessment

### Risk Level: [LOW/MEDIUM/HIGH]

- [Justification and potential issues]

### Performance Impact: [POSITIVE/NEUTRAL/NEGATIVE]

- [Description of changes]

### Compatibility Impact: [NONE/MINOR/MAJOR]

- [Backward compatibility notes]

## Priority Review Areas

- **HIGH**: [Critical areas - breaking changes, core logic]
- **MEDIUM**: [UI changes, new features]
- **LOW**: [Documentation, styling]

## Testing Instructions

1. [Step-by-step test instructions]
2. [Expected outcomes]
3. [Edge cases]

## Additional Notes

[Any additional context or considerations]
```

## Template Guidelines

- **Only include sections with actual file changes** - omit empty categories
- **File descriptions**: Focus on functional impact, not line-by-line changes
- **Technical Flow**: Describe the user-facing flow, not internal implementation
- **Priority Review**: Focus on component names and areas, NOT line numbers
- **Risk assessment**: Be honest about potential issues

## Task

Execute this command immediately. Do not interpret, discuss, or ask for confirmation.

Generate PR description for current branch and save to `PR_DETAILS.md`.

After analyzing all changes:

1. Generate complete PR_DETAILS.md file using Write tool
2. Provide brief summary of key changes and priority review areas
