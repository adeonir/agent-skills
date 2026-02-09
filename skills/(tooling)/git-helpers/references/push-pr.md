# Push PR

Push current branch and create Pull Request via `gh` cli.

## Process

### Step 1: Check gh cli Availability

```bash
which gh
```

If not available, stop and inform user to install `gh` cli.

### Step 2: Detect Base Branch

If not specified:

```bash
for branch in development develop main master; do
  git show-ref --verify --quiet refs/heads/$branch && echo $branch && break
done
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

### Step 5: Push and Create PR

```bash
git push -u origin $(git branch --show-current)
gh pr create --title "type: description" --body "$(cat <<'EOF'
Brief summary of what this PR does (2-3 sentences max).

## Changes

- Key change 1
- Key change 2
- Key change 3
EOF
)"
```

Output the PR URL when done.

## PR Format

Load [conventional-commits.md](conventional-commits.md) for commit types and message format rules.

**Title:** `type: concise description` or `type(scope): concise description`

**Body:**

```markdown
Brief summary of what this PR does (2-3 sentences max).

## Changes

- Key change 1
- Key change 2
- Key change 3
```

**Additional Guidelines:**

- Keep changes list to 3-5 key items
- No risk assessment or testing instructions in PR body
- Scope in title is allowed - both `feat:` and `feat(scope):` are valid

## Task

Execute this command immediately. Do not interpret, discuss, or ask for confirmation.

Push current branch and create PR using `gh pr create`.

Output the PR URL when done.
