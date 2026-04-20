# Create Pull Request

Push current branch and create Pull Request via `gh` cli.

## When to Use

When pushing a branch and creating a pull request.

## Workflow

### Step 1: Check gh cli Availability

```bash
which gh
```

If not available, stop and inform user to install `gh` cli.

### Step 2: Detect Base Branch

If not specified, default to `main`. User can override via prompt.

```bash
git show-ref --verify --quiet refs/heads/main && echo main
```

### Step 3: Gather Context

```bash
git branch --show-current
git log {base}..HEAD --oneline
git diff {base}...HEAD --stat
git diff {base}...HEAD
```

### Step 4: Analyze Changes

- Review commits and diff
- Determine appropriate PR type

### Step 5: Preview and Confirm

Compose the PR title and body. Show the PR title, body, and base branch for
user confirmation before executing.

**Title:** `type: concise description` or `type(scope): concise description`
(lowercase, imperative mood)

**Body:** **USE TEMPLATE:** `templates/pull-request.md`

### Step 6: Push and Create PR

```bash
git push -u origin $(git branch --show-current)
gh pr create --title "type: concise description" --body "$(cat <<'EOF'
{PR body from template}
EOF
)"
```

Output the PR URL when done.

## Guidelines

**DO:**
- Preview the PR title and body before pushing
- Use imperative mood in PR title and changes list
- Include `Closes #N` when there is a related issue
- Keep the changes list to 3-7 key items, from the user's perspective
- Write the PR body in neutral voice (no attribution)
- Everything in English

**DON'T:**
- Push without explicit user confirmation (contrasts: preview before pushing)
- List every file changed (contrasts: 3-7 key items)
- Include implementation details (contrasts: user's perspective)
- Add attribution lines to the PR body (contrasts: neutral voice)

## Error Handling

- gh cli not available: stop and inform user to install it
- No remote configured: inform user to set up a remote first
- Branch already has open PR: inform user and ask if they want to update it
- Push rejected: inform user to pull first
