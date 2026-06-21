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
| Any pending | Stop — wait for CI to finish |
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

If behind: **always ask** the user which update method to use (rebase / squash / merge / skip). Do not persist this decision — the right answer depends on the branch's history each time.

Apply the chosen method:

```bash
# rebase
git rebase origin/{base}

# squash
git reset --soft origin/{base}
git commit -m "$(cat <<'EOF'
{type}: {description}
EOF
)"

# merge base into branch
git merge origin/{base}
```

The squash path collapses the branch into one commit — give it a message with
the same conventional-commit discipline as a fresh commit. Never leave `git
commit` bare; an empty `-m` opens an editor that stalls a non-interactive run.

If conflicts: help the user resolve, then continue.

After updating, refresh the remote branch:

```bash
git push --force-with-lease
```

A force-push replaces the state CI ran against and starts a fresh run, so the
earlier pass no longer reflects what will merge. Re-run the **CI Status** check
above on the new state before proceeding.

#### PR Mergeable State

```bash
gh pr view {pr-number} --json mergeable,mergeStateStatus,reviewDecision
```

| Field | Required value |
|-------|----------------|
| `mergeable` | `MERGEABLE` |
| `mergeStateStatus` | `CLEAN` — see the table below for the other states |
| `reviewDecision` | `APPROVED` when branch protection requires review |

`mergeStateStatus` carries what the other two fields miss — read it, do not
discard it. It is the field that catches a branch that fell behind or a check
that is still settling after a sync:

| `mergeStateStatus` | Action |
|--------------------|--------|
| `CLEAN` | Proceed |
| `BEHIND` | Base moved ahead — loop back to Branch Sync, then re-check |
| `BLOCKED` | Required review or check unmet — stop and surface |
| `DIRTY` | Conflicts — stop and surface |
| `UNSTABLE` | A check is still pending or failing — stop and wait, do not race |
| `UNKNOWN` | GitHub is still computing mergeability — wait and re-query |

If not mergeable: stop and surface the specific blocker (conflicts, missing approval, blocked by protection).

### Step 4: Merge

Compose subject and body:

- **Subject** — `{type}: {description} (#{pr-number})`. Conventional commit style from [commit.md](commit.md) with the PR ID appended.
- **Body** — contextual bullets describing motivation or impact; omit for trivial merges.

```bash
gh pr merge {pr-number} --{method} --subject "{type}: {description} (#{pr-number})" --body "{body}"
```

For `--rebase`, subject and body are not used (the original commits are replayed onto base).

If `gh pr merge` exits non-zero: stop and surface the error.

### Step 5: Confirm Merge Landed

`gh pr merge` exits as soon as GitHub accepts the merge request, but the merge commit and the `{base}` ref pointer are populated asynchronously. Pulling immediately can race the propagation and surface a stale intermediate state (linear history when the convention expected a merge commit, or a missing commit altogether). Confirm the merge commit OID is published before cleanup.

Poll the PR's `mergeCommit.oid` until non-empty (cap at ~10 attempts, ~1s between):

```bash
for i in {1..10}; do
  oid=$(gh pr view {pr-number} --json mergeCommit -q .mergeCommit.oid)
  [ -n "$oid" ] && break
  sleep 1
done
[ -n "$oid" ] || { echo "merge commit not published after 10s — surface and stop"; exit 1; }
```

Store the returned `oid` as `{merge-oid}` for the next step's verification.

### Step 6: Cleanup

```bash
git switch {base}
git fetch origin {base}
git pull --ff-only origin {base}
```

After the pull, verify the local tip matches the API-reported merge commit OID. If they diverge, the pull picked up an intermediate state — re-fetch once more and re-check. The `git reset --hard` below is a deliberate, bounded exception to the usual confirm-before-reset rule: it discards only the stale local `{base}` pointer so it matches the authoritative remote, with no working-tree changes at risk — the prior steps only switched to and pulled `{base}`, never a branch carrying uncommitted work.

```bash
local_oid=$(git rev-parse {base})
if [ "$local_oid" != "{merge-oid}" ]; then
  git fetch origin {base} && git reset --hard origin/{base}
  local_oid=$(git rev-parse {base})
fi
[ "$local_oid" = "{merge-oid}" ] || { echo "local {base} did not converge on {merge-oid} — surface and stop"; exit 1; }
```

When the method is `merge`, also assert the tip has two parents:

```bash
parent_count=$(git cat-file -p HEAD | grep -c '^parent ')
[ "$parent_count" -eq 2 ] || { echo "expected merge commit (2 parents), got $parent_count — surface and stop"; exit 1; }
```

Then delete the branches. Use `-D`, not `-d`: after a squash or rebase merge the
branch's commits are never ancestors of `{base}`, so `-d`'s safety check refuses
the delete even though the merge landed. That safety is already redundant here —
Step 5's published OID and the tip check above prove the merge is in `{base}`.

```bash
git branch -D {branch}
git push origin --delete {branch}
```

If the repo has `deleteBranchOnMerge` enabled, the remote `--delete` will report the branch already gone — that is expected, not an error.

Confirm: "PR #{pr-number} merged into `{base}` (`{merge-oid}`) and branch deleted."

## Guidelines

**DO:**
- Resolve the PR number from the current branch; ask only when no open PR exists for it
- Infer the merge method from recent base history before asking the user
- Stop on CI pending — do not race the merge
- After a sync force-push, re-check CI and gate on `mergeStateStatus` (stop on `BEHIND`/`BLOCKED`/`UNSTABLE`) — `mergeable` alone misses a stale or settling state
- Always ask the update method when the branch is behind, per merge
- Pass a custom subject citing the PR ID on merge commits
- Use `--force-with-lease` (not `--force`) when force pushing
- Poll `gh pr view --json mergeCommit` until the OID is populated before pulling — `gh pr merge` exits before propagation
- Verify the local `{base}` tip equals the API-reported merge OID after pulling; re-fetch once if it diverges
- For `--merge` method, confirm HEAD has two parents before deleting branches
- Delete both local and remote branch after the cleanup pull succeeds

**DON'T:**
- Merge while CI is pending
- Pull immediately after `gh pr merge` without confirming the merge commit OID is published — the API races propagation and the pull can land on an intermediate state
- Trust the `gh pr merge` exit code alone as proof of completion — the exit code only confirms GitHub accepted the request
- Use the default `Merge pull request #N from {branch}` message
- Force push without `--force-with-lease`
- Persist the branch-update method
- Skip cleanup — stale branches accumulate

## Error Handling

- On base branch and user gave no PR number: ask for the number
- No open PR for current branch: stop and inform user
- CI failed or pending: stop and surface; do not proceed
- Local tests fail (no CI configured): stop
- Branch behind base with conflicts during update: help resolve, then continue
- PR not mergeable (conflicts, missing approval, blocked): stop and surface the specific blocker
- `gh pr merge` exits non-zero: surface the error and stop — do not proceed to cleanup
- `mergeCommit.oid` still empty after the poll window (~10s): surface and stop — something blocked the merge server-side
- Cleanup pull fails as non-fast-forward: merge did not land as expected; surface and stop
- Local `{base}` tip differs from `mergeCommit.oid` after the fallback re-fetch: surface and stop — do not delete branches
- HEAD has fewer parents than the method requires (expected 2 for `--merge`): surface and stop — the merge applied as a different method than intended
