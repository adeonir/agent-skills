# Finish Branch

Merge a GitHub pull request and clean up the branch.

## When to Use

When ready to merge a PR — approved, CI green, ready to ship. GitHub-based workflow only; requires `gh` CLI.

## PR state

!`gh pr list --head $(git branch --show-current) --state open --json number,title,baseRefName`

## Workflow

### Step 1: Identify PR

Read the **PR state** block above for the current branch's open PR (`number`, `title`, `baseRefName`). If it is missing or shows the raw command (injection disabled), run it yourself. If empty (on the base branch, or no open PR), ask the user for the PR number and fetch its metadata:

```bash
gh pr view {pr-number} --json number,title,baseRefName
```

Use `baseRefName` as `{base}` for the rest of the workflow.

### Step 2: Resolve Merge Method

```bash
git config --get git-helpers.merge-method
```

If a value is returned (`squash`, `merge`, or `rebase`), use it directly — skip the rest of this step.

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

Write the merge commit from the PR title and branch context, never the conversation. The subject uses the PR title when it follows `type: description`; generate a conforming one only when it does not. Add a body bullet only when the subject is not self-sufficient — and trace it to the branch diff.

```bash
gh pr merge {pr-number} --{method} --subject "{subject}" --body "{body}"
```

Omit `--body` when there is none. For `--rebase`, subject and body are unused (the original commits are replayed onto base). If `gh pr merge` exits non-zero, stop and surface the error.

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

- Resolve the PR from the current branch; ask only when none is open for it
- Read merge method from `git config --get git-helpers.merge-method`; infer and persist on first run, but never persist the branch-update method
- Confirm `MERGED` before pulling — `gh pr merge` exits before propagation
- Force push only with `--force-with-lease`; delete with `-D` (squash/rebase leave commits that are not ancestors of base)
- Use a custom merge subject citing the PR ID, never the default GitHub message

## Error Handling

- On base branch and user gave no PR number: ask for the number
- No open PR for current branch: stop and inform user
- Branch behind base with conflicts during update: help resolve, then continue
- `gh pr merge` exits non-zero: surface the error and stop — do not proceed to cleanup
- State not `MERGED` after retry: surface and stop
- Cleanup pull fails as non-fast-forward: surface and stop
