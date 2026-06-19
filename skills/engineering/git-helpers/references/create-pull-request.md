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

**The branch diff and commit log are the single source of truth.** Agents
tend to drag session narrative into PR bodies — block that instinct.
Features discussed, plans drafted, alternatives debated in conversation
are not content unless the diff shows them.

**Discard for content generation:**

- Prior conversation narrative and agent intuition about the work
- Future work, follow-ups, or roadmap context from the session

**Retain:**

- The `{base}...HEAD` diff and commit subjects from Step 3
- Explicit user directives about the PR itself — title override, base
  branch, issue number to close. They shape format and metadata, not
  invented content.

Based only on those sources:

- Review commits and diff
- Determine appropriate PR type

### Step 5: Preview and Confirm

Compose the PR title and body. Show the PR title, body, and base branch for
user confirmation before executing.

**Title:** `type: concise description` or `type(scope): concise description`
(lowercase, imperative mood)

**Body:** Use the template below.

## PR Body Template

ALWAYS use this exact template structure:

````markdown
## Summary

{{What changed and why, derived from the diff and commit log (2-3 sentences)}}

**Type:** {{bug fix | new feature | refactor | breaking change | documentation | configuration}}

## Changes

- {{Key change in imperative mood}}

{3-7 items describing the key changes, each in imperative mood}

## Test Plan

{{Commands a reviewer can run to verify, each paired with its expected
outcome — not the results you measured this run (no test counts, scores,
or specific fixes).}}

1. `{{command}}` — {{expected outcome}}
2. `{{command}}` — {{expected outcome}}

Closes #{{issue-number}}
````

The body MUST NOT contain:

- Session narrative — discussions, plans, or decisions from the
  conversation that the diff does not show
- Alternatives debated in chat or rejected approaches
- Future work, follow-ups, or roadmap references
- Run-specific results in the Test Plan — test counts, scores, or measured
  values; list reproducible commands and their expected outcomes instead
- Attribution lines

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
- Push without explicit user confirmation
- List every file changed
- Include implementation details
- Add attribution lines to the PR body

## Error Handling

- gh cli not available: stop and inform user to install it
- No remote configured: inform user to set up a remote first
- Branch already has open PR: inform user and ask if they want to update it
- Push rejected: inform user to pull first
