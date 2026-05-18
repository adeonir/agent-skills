# Finish Branch

Merge a GitHub pull request and clean up the branch.

## When to Use

When ready to merge a PR -- approved, CI green, ready to ship. GitHub-based workflow only; requires `gh` CLI.

## Workflow

### Step 1: Identify PR

```bash
gh pr list --head $(git branch --show-current) --state open --json number,title,baseRefName
```

If the list is empty (user is on the base branch, or the current branch has no open PR): ask the user for the PR number, then fetch its metadata:

```bash
gh pr view {pr-number} --json number,title,baseRefName
```

Use `baseRefName` from the response as `{base}` for the rest of the workflow.

### Step 2: Resolve Merge Method

Infer the project's convention from recent merges on base:

```bash
git log origin/{base} -10 --format='%P %s'
```

| Pattern in recent entries | Method |
|---------------------------|--------|
| Two parents (two SHAs in `%P`) | `merge` |
| One parent, subject ends in `(#N)` | `squash` |
| One parent, no PR ID in subject | `rebase` |

If at least 3 of the last entries agree, use that method. If ambiguous or the base has no merge history, ask the user.

| Method | Result |
|--------|--------|
| `merge` | Preserves commits + merge commit (parent count 2) |
| `squash` | Single commit on base |
| `rebase` | Replays original commits (linear history) |

### Step 3: Preflight Checks

#### CI Status

```bash
gh pr checks {pr-number}
```

| State | Action |
|-------|--------|
| All passed | Proceed |
| Any failed | Stop and surface |
| Any pending | Stop -- wait for CI to finish |
| No checks configured | Run local tests instead |

If no CI is configured, run the project's test suite:

```bash
# Use whichever applies: npm test / pnpm test / pytest / cargo test / go test ./...
```

Local tests failed: stop.

#### Branch Sync

```bash
git fetch origin {base}
git rev-list --left-right --count origin/{base}...HEAD
```

If behind: **always ask** the user which update method to use (rebase / squash / merge / skip). Do not persist this decision -- the right answer depends on the branch's history each time.

Apply the chosen method:

```bash
# rebase
git rebase origin/{base}

# squash
git reset --soft origin/{base}
git commit

# merge base into branch
git merge origin/{base}
```

If conflicts: help the user resolve, then continue.

After updating, refresh the remote branch:

```bash
git push --force-with-lease
```

#### PR Mergeable State

```bash
gh pr view {pr-number} --json mergeable,mergeStateStatus,reviewDecision
```

| Field | Required value |
|-------|----------------|
| `mergeable` | `MERGEABLE` |
| `reviewDecision` | `APPROVED` when branch protection requires review |

If not mergeable: stop and surface the specific blocker (conflicts, missing approval, blocked by protection).

### Step 4: Merge

Compose subject and body:

- **Subject** -- `{type}: {description} (#{pr-number})`. Conventional commit style from [commit.md](commit.md) with the PR ID appended.
- **Body** -- contextual bullets describing motivation or impact; omit for trivial merges.

```bash
gh pr merge {pr-number} --{method} --subject "{type}: {description} (#{pr-number})" --body "{body}"
```

For `--rebase`, subject and body are not used (the original commits are replayed onto base).

If `gh pr merge` exits non-zero: stop and surface the error.

### Step 5: Cleanup

```bash
git switch {base}
git pull --ff-only origin {base}
git branch -d {branch}
git push origin --delete {branch}
```

The fast-forward pull proves the merge landed on the remote -- if it fails, the merge did not land and the cleanup itself surfaces the failure.

If the repo has `deleteBranchOnMerge` enabled, the remote `--delete` will report the branch already gone -- that is expected, not an error.

Confirm: "PR #{pr-number} merged into `{base}` and branch deleted."

## Guidelines

**DO:**
- Resolve the PR number from the current branch; ask only when no open PR exists for it
- Infer the merge method from recent base history before asking the user
- Stop on CI pending -- do not race the merge
- Always ask the update method when the branch is behind, per merge
- Pass a custom subject citing the PR ID on merge commits
- Use `--force-with-lease` (not `--force`) when force pushing
- Trust the `gh pr merge` exit code; let the cleanup pull surface late failures
- Delete both local and remote branch after the cleanup pull succeeds

**DON'T:**
- Merge while CI is pending (contrasts: wait for CI to finish)
- Cross-check the merge against local `origin/{base}` refs (contrasts: trust `gh pr merge` exit code)
- Use the default `Merge pull request #N from {branch}` message (contrasts: custom subject with PR ID)
- Force push without `--force-with-lease` (contrasts: use --force-with-lease)
- Persist the branch-update method (contrasts: always ask per merge)
- Skip cleanup -- stale branches accumulate (contrasts: delete both local and remote after merge)

## Error Handling

- On base branch and user gave no PR number: ask for the number
- No open PR for current branch: stop and inform user
- CI failed or pending: stop and surface; do not proceed
- Local tests fail (no CI configured): stop
- Branch behind base with conflicts during update: help resolve, then continue
- PR not mergeable (conflicts, missing approval, blocked): stop and surface the specific blocker
- `gh pr merge` exits non-zero: surface the error and stop -- do not proceed to cleanup
- Cleanup pull fails as non-fast-forward: merge did not land as expected; surface and stop
