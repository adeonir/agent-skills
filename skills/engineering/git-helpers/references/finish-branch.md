# Finish Branch

Merge a GitHub pull request and clean up the branch.

## When to Use

When ready to merge a PR — approved, CI green, ready to ship. GitHub-based workflow only; requires `gh` CLI.

## PR state

!`gh pr list --head $(git branch --show-current) --state open --json number,title,baseRefName`

## Workflow

### Step 1: Identify PR

Read the **PR state** block above. It contains the open PR (if any) for the current branch with `number`, `title`, and `baseRefName`. If that block is missing or shows the raw command (shell injection disabled), run `gh pr list --head $(git branch --show-current) --state open --json number,title,baseRefName` yourself to get the same data.

If the list is empty (user is on the base branch, or the current branch has no open PR): ask the user for the PR number, then fetch its metadata:

```bash
gh pr view {pr-number} --json number,title,baseRefName
```

Use `baseRefName` from the response (or from the injected list) as `{base}` for the rest of the workflow.

### Step 2: Resolve Merge Method

```bash
git config --get git-helpers.merge-method
```

If a value is returned (`squash`, `merge`, or `rebase`), use it directly —
skip the rest of this step.

If no value is set, infer from recent merges on base:

```bash
git log origin/{base} -10 --format='%P %s'
```

| Pattern | Method |
|---------|--------|
| Two parents (two SHAs in `%P`) | `merge` |
| One parent, subject ends in `(#N)` | `squash` |
| One parent, no PR ID in subject | `rebase` |

If at least 3 of the last entries agree, persist and use that method:

```bash
git config --local git-helpers.merge-method {method}
```

If ambiguous or no merge history, ask the user, then persist:

```bash
git config --local git-helpers.merge-method {method}
```

| Method | Result |
|--------|--------|
| `merge` | Preserves commits + merge commit (parent count 2) |
| `squash` | Single commit on base |
| `rebase` | Replays original commits (linear history) |

### Step 3: Sync and Verify

```bash
git fetch origin {base}
git rev-list --left-right --count origin/{base}...HEAD
```

If the branch is behind, rebase automatically:

```bash
git rebase origin/{base}
```

If rebase conflicts: surface and stop — inform the user to resolve and re-run.

After a successful rebase, refresh the remote branch:

```bash
git push --force-with-lease
```

Gather branch context for Step 4:

```bash
git log origin/{base}..HEAD --oneline
git diff origin/{base}...HEAD
```

Verify mergeability:

```bash
gh pr view {pr-number} --json mergeStateStatus -q .mergeStateStatus
```

| `mergeStateStatus` | Action |
|--------------------|--------|
| `CLEAN` | Proceed |
| `BLOCKED` | Stop and surface — review or check unmet |
| `DIRTY` | Stop and surface — conflicts |
| `UNSTABLE` | Stop and wait — CI still settling |
| `UNKNOWN` | Wait and re-query |

### Step 4: Merge

Spawn an isolated Agent with only the following as input — no conversation
context passes through:

1. PR title and number from Step 1
2. Branch diff and commit log gathered in Step 3

Instruct the agent to return a structured object:

```json
{
  "subject": "string ({pr-title} (#{pr-number}) if conventional, generated otherwise)",
  "body": ["contextual bullet describing motivation or impact"]
}
```

Use `null` for `body` when the subject is self-sufficient. The subject uses the
PR title directly when it follows `type: description` convention; the agent
generates a conforming subject only when it does not.

```bash
gh pr merge {pr-number} --{method} --subject "{subject}" --body "{body}"
```

Omit `--body` when `body` is null.

For `--rebase`, subject and body are not used (the original commits are replayed
onto base).

If `gh pr merge` exits non-zero: stop and surface the error.

### Step 5: Confirm Merge Landed

`gh pr merge` exits before GitHub propagates the merge commit. Confirm the PR reached `MERGED` state before pulling:

```bash
gh pr view {pr-number} --json state -q .state
```

If state is not `MERGED`, wait a moment and retry once. If still not `MERGED`, surface and stop.

### Step 6: Cleanup

```bash
git switch {base}
git pull --ff-only origin {base}
```

If the pull fails as non-fast-forward, the merge has not propagated — surface and stop.

Delete the branches. Use `-D`, not `-d`: after a squash or rebase merge the branch's commits are not ancestors of `{base}`, so `-d` refuses the delete even though the merge landed.

```bash
git branch -D {branch}
git push origin --delete {branch}
```

If the repo has `deleteBranchOnMerge` enabled, the remote `--delete` will report the branch already gone — that is expected, not an error.

Confirm: "PR #{pr-number} merged into `{base}` and branch deleted."

## Guidelines

**DO:**
- Resolve the PR number from the current branch; ask only when no open PR exists for it
- Read merge method from `git config --get git-helpers.merge-method`; infer and persist on first run
- Always ask the update method when the branch is behind
- Pass a custom subject citing the PR ID on merge commits
- Use `--force-with-lease` (not `--force`) when force pushing
- Confirm `MERGED` state before pulling in Step 5 — `gh pr merge` exits before propagation
- Delete both local and remote branch after the cleanup pull succeeds

**DON'T:**
- Pull immediately after `gh pr merge` without confirming `MERGED` state
- Use the default `Merge pull request #N from {branch}` message
- Force push without `--force-with-lease`
- Persist the branch-update method
- Skip cleanup — stale branches accumulate

## Error Handling

- On base branch and user gave no PR number: ask for the number
- No open PR for current branch: stop and inform user
- Branch behind base with conflicts during update: help resolve, then continue
- `gh pr merge` exits non-zero: surface the error and stop — do not proceed to cleanup
- State not `MERGED` after retry: surface and stop
- Cleanup pull fails as non-fast-forward: surface and stop
