# Finish Branch

Prepare, merge, and clean up a branch after work is complete.

## When to Use

When the branch is ready to merge -- PR is approved, or work is done on a
solo project without PRs. This is the final step in the git workflow.

## Workflow

### Step 1: Gather Context

```bash
git branch --show-current
git log {base}..HEAD --oneline
git rev-list --left-right --count {base}...HEAD
```

Check for open PR:

```bash
gh pr list --head $(git branch --show-current) --state open
```

### Step 2: Check If Branch Needs Updating

Compare current branch with base:

```bash
git fetch origin {base}
git rev-list --left-right --count origin/{base}...HEAD
```

If base is ahead (branch diverged):
- Inform user: "Branch is {N} commits behind {base}."
- Ask: "Update before merging? (rebase / squash / merge / skip)"

If up to date: skip to Step 4.

### Step 3: Update Branch

Execute the method chosen by the user:

**Rebase:**

```bash
git rebase origin/{base}
```

Replays commits on top of base. Results in linear history. If conflicts,
inform user and help resolve.

**Squash:**

```bash
git rebase -i origin/{base}
# or
git reset --soft origin/{base}
git commit
```

Combines all branch commits into one. Ask user for the squash commit message.
Follow commit conventions from [commit.md](commit.md).

**Merge base into branch:**

```bash
git merge origin/{base}
```

Preserves full history. If conflicts, inform user and help resolve.

After updating, force push to update the remote branch:

```bash
git push --force-with-lease
```

### Step 4: Merge

**If PR exists (default):**

Ask user which merge method to use:

| Method | Command | Result |
|--------|---------|--------|
| Merge commit | `gh pr merge --merge` | Preserves all commits + merge commit |
| Squash | `gh pr merge --squash` | Single commit on base |
| Rebase | `gh pr merge --rebase` | Replays commits on base (linear) |

Pass a custom subject citing the PR ID (the default GitHub merge message, e.g. `Merge pull request #19 from adeonir/chore/foundation`, is not acceptable).

Subject format: `{type}: {description} (#{pr-number})` -- follows conventional commit style from [commit.md](commit.md), with PR ID appended.

```bash
gh pr merge {pr-number} --{method} --subject "{type}: {description} (#{pr-number})"
```

For `--squash` and `--merge`, also pass `--body` with contextual bullets when relevant. For `--rebase`, no subject/body is needed (original commits are replayed).

**If no PR (solo project, merge direct):**

```bash
git switch {base}
git merge {branch}
git push origin {base}
```

### Step 5: Cleanup

Delete the branch locally and remotely:

```bash
git switch {base}
git pull origin {base}
git branch -d {branch}
git push origin --delete {branch}
```

Confirm: "Branch `{branch}` merged into `{base}` and deleted."

## Guidelines

**DO:**
- Always ask before updating or merging -- never auto-merge
- Use `--force-with-lease` (not `--force`) when force pushing
- Confirm the merge method with the user
- Pass a custom subject citing the PR ID on merge commits
- Delete both local and remote branch after merge is confirmed

**DON'T:**
- Force push without `--force-with-lease` (contrasts: use --force-with-lease)
- Merge without checking if branch is up to date (contrasts: always ask before merging)
- Use the default `Merge pull request #N from {branch}` message (contrasts: custom subject with PR ID)
- Delete branch before merge is confirmed (contrasts: delete after merge is confirmed)
- Skip cleanup -- stale branches accumulate (contrasts: delete both local and remote after merge)

## Error Handling

- PR not found: ask if user wants to merge directly or create PR first
- Conflicts during rebase/merge: inform user, help resolve, continue
- Branch already merged: inform user, offer to clean up
- Protected base branch: inform user, suggest PR if direct merge fails
- Force push rejected: inform user to check branch protection rules
