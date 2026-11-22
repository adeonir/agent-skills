# Merge Pull Request

Merge a GitHub pull request.

## Load first

Read [message-sourcing.md](../references/message-sourcing.md) before writing the merge subject — it carries where the words come from, the diction bar, and the two shapes of slop. Resolve bundled script paths from this skill's installed directory.

## Contents

- Rules for every run
- Workflow

## Rules for every run

1. Use the GitHub channel the project's AGENTS.md or CLAUDE.md records as primary, the GitHub MCP server or `gh`, and the other channel when the primary fails; when the project records none, use whichever is available. The MCP tools are `GitHub:pull_request_read` and `GitHub:merge_pull_request`; the `gh` command is shown at each step. Use Git commands for local repository operations.
2. Target the pull request by `{pr-number}` in every command, never by the current branch or `HEAD`: the current branch may be the base.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Name the pull request, base, and branch
- [ ] Step 2: Resolve the merge method
- [ ] Step 3: Verify the merge state is CLEAN. If it is UNKNOWN or UNSTABLE, wait and verify again
- [ ] Step 4: Merge. The command must exit zero
- [ ] Step 5: Confirm the state is MERGED
- [ ] Step 6: Clean up: local base matches the remote, local branch deleted
- [ ] Step 7: Report what ran
```

**Step 1. Identify the pull request.** Run this first — it identifies the pull request for the current branch:

```bash
gh pr list --head $(git branch --show-current) --state open --json number,title,baseRefName,headRefName
```

Take `number`, `title`, `baseRefName`, and `headRefName` from the output. If it is empty (on the base branch, or no open pull request), ask the user for the pull request number and fetch its metadata:

```bash
gh pr view {pr-number} --json number,title,baseRefName,headRefName
```

Use `baseRefName` as `{base}` and `headRefName` as `{branch}` for the rest of the workflow. Done when `{pr-number}`, `{base}`, and `{branch}` are named.

**Step 2. Resolve the merge method.**

```bash
git config --get git-helpers.merge-method
```

If a value is returned (`squash`, `merge`, or `rebase`), use it as `{method}` and skip to the record step at the end of this step.

If no value is set, infer from recent merges on base:

```bash
git log origin/{base} -10 --format='%P %s'
```

| Pattern | Method |
|---------|--------|
| Two parents (two SHAs in `%P`) | `merge` |
| One parent, subject ends in `(#N)` | `squash` |
| One parent, no pull request ID in subject | `rebase` |

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

Whatever path resolved `{method}`, record the rule:

```bash
python3 <this-skill>/scripts/merge-method.py {method}
```

The script maintains one `## Merge method` section in the repository's instruction file: one sentence, the merge rule itself. Re-running with the resolved method changes nothing. If the script exits non-zero, surface the error; the instruction file stays untouched on failure. Done when `{method}` is one of `squash`, `merge`, or `rebase`, and the script exited zero.

**Step 3. Sync and verify.**

```bash
git fetch origin {base}
gh pr view {pr-number} --json mergeable --jq .mergeable
```

If `mergeable` is `CONFLICTING`, rebase. The rebase rewrites the branch commits and overwrites the remote branch, so rebase only on explicit user confirmation; on decline, stop here. Any other value: skip the rebase.

```bash
gh pr checkout {pr-number}
git rebase origin/{base}
```

Resolve each conflict with the user, then continue the rebase. If a conflict cannot be resolved, abort and stop.

After a successful rebase, refresh the remote branch:

```bash
git push --force-with-lease
```

Gather branch context for Step 4:

```bash
gh pr view {pr-number} --json commits --jq '.commits[].messageHeadline'
gh pr diff {pr-number}
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

Done when `mergeStateStatus` is `CLEAN`. On any other value, act as the table says; after waiting, return to the verify command above.

**Step 4. Merge.** Write the merge commit from the pull request title and branch context. The subject is `{type}: {description} (#{pr-number})` — never the default `Merge pull request #N from {branch}`, which strips intent and conventional commit type. Take `{type}: {description}` from the pull request title when it follows that shape; generate a conforming one only when it does not, at the bar the loaded reference sets. Add a body only when the subject is not self-sufficient — one short sentence stating what the branch solves, never a list of its commits or the session behind them, and traced to the branch diff.

Merging writes to `{base}` and closes the pull request. Proceed once Step 3 confirms `mergeStateStatus` is `CLEAN`. Ask the user only when something is inconsistent: a non-`CLEAN` status, a failing check, or anything else Step 3 surfaces.

```bash
gh pr merge {pr-number} --{method} --subject "{subject}" --body "{body}"
```

A merge through `GitHub:merge_pull_request` takes the subject as `commit_title`, the body as `commit_message`, and the method as `merge_method`. Pass `--body ""` when there is no body — omitting the flag makes `gh` fill the body with the branch commit messages. For `--rebase`, subject and body are unused (the original commits are replayed onto base). If `gh pr merge` exits non-zero, stop and surface the error. Done when `gh pr merge` exits zero.

**Step 5. Confirm the merge landed.** `gh pr merge` exits before GitHub propagates the merge commit. Confirm the pull request reached `MERGED` state:

```bash
gh pr view {pr-number} --json state -q .state
```

If state is not `MERGED`, wait a moment and retry once. If still not `MERGED`, surface and stop. Done when the state is `MERGED`.

**Step 6. Clean up.**

```bash
git switch {base}
git fetch origin {base}
git merge --ff-only origin/{base}
```

If the merge fails as non-fast-forward, the merge has not propagated; surface it and go to Step 7.

Delete `{branch}` remotely and locally without asking. Step 5 confirmed the pull request is `MERGED`, so its work is on `{base}`. Delete the remote branch first: skip when nothing is listed, and surface the error otherwise.

```bash
git ls-remote --heads origin {branch}
git push origin --delete {branch}
```

Delete `{branch}` locally when it still exists. Use `-D`: after a squash or rebase merge the branch commits are not ancestors of `{base}`, and `git branch -d` refuses.

```bash
git branch --list {branch}
git branch -D {branch}
```

Skip the delete when the first command prints nothing.

Done when the local `{base}` matches `origin/{base}` and `{branch}` no longer exists locally and on the remote.

**Step 7. Report.** Confirm what ran, naming the branches deleted: "Pull request #{pr-number} merged into `{base}`; local branch `{branch}` deleted", adding "and the remote branch" only when it existed on the remote. When Step 6 stops before the deletes, confirm "Pull request #{pr-number} merged into `{base}`". Done when the report states what ran.
