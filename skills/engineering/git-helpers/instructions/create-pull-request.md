# Create Pull Request

Push the current branch and open a pull request shaped to the project's conventions.

## Load first

Read [message-sourcing.md](../references/message-sourcing.md) before writing the title or body — it carries where the words come from, the diction bar, and the two shapes of slop.

## Contents

- Rules for every run
- Workflow

## Rules for every run

1. Use the GitHub channel the project's AGENTS.md or CLAUDE.md records as primary, the GitHub MCP server or `gh`, and the other channel when the primary fails; when the project records none, use whichever is available. The MCP tools are `GitHub:list_pull_requests` and `GitHub:create_pull_request`; the `gh` equivalents are `gh pr list --head {branch} --state open` and `gh pr create`. Use Git commands for local repository operations. `{branch}` is the current branch.
2. Push before opening the pull request: the API resolves the head ref on the remote, so a branch that exists only locally cannot be a pull request head.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Name the base
- [ ] Step 2: Check the guards: branch differs from the base, no open pull request
- [ ] Step 3: Push the branch
- [ ] Step 4: Write the title and body from the branch diff
- [ ] Step 5: Open the pull request. If the remote lacks the branch, return to Step 3
- [ ] Step 6: Report the title, URL, and base
```

**Step 1. Resolve the base.** Use the base the user named. Otherwise the repo default (fall back to `main`). Done when `{base}` is named.

**Step 2. Check the guards.**

```bash
git branch --show-current
gh pr list --head {branch} --state open --json number,url
```

Stop when `{branch}` is `{base}`: a pull request needs a separate head branch. If the branch already has an open pull request, do not open a second one — surface it and ask whether to update it. Done when `{branch}` differs from `{base}` and has no open pull request.

**Step 3. Push.**

```bash
git push -u origin HEAD
```

Done when the push succeeds and the remote has `{branch}`.

**Step 4. Write the title and body.** Write the body from the branch diff and commit log against the base — the *what*. Beyond what the loaded reference allows, the body draws only on the base branch (scope) and explicit user directives: a title override, an issue to close, or a *why* the user stated.

Sections are earned, not mandatory. Always write the Summary. Add **Changes** only when the pull request has several distinct changes worth listing. Add **Test Plan** only when there is reviewer-runnable behavior. A trivial pull request (a typo, a one-line fix) is often just a Summary and `Closes #N`.

Here is a sensible default format, but use your best judgment:

````markdown
## Summary

{what changed and why, in a short paragraph a reviewer reads at a glance}

## Changes

- {meaningful change in imperative mood — the curated set, not a file-by-file transcript; 3-7 items at most}

## Test Plan

1. `{command}` — {what the reviewer observes}

Closes #{issue-number}
````

**Summary — glanceable.** 1-3 short sentences at the diction bar in the loaded reference. Lead with what the branch does or fixes, then only the *why* the reviewer needs:

| AI-slop Summary | Plain Summary |
|-----------------|---------------|
| This PR enhances the authentication flow to ensure robust token handling and streamline the user experience. | Refresh access tokens before they expire so a long-lived tab stops forcing a full sign-in. |
| Implements comprehensive error handling functionality across the upload pipeline. | Retry failed uploads and surface a clear error when retries are exhausted. |

**Test Plan — reviewer-facing, not machine gates.** The section most often filled with the wrong thing. List commands that exercise *this* pull request's behavior, each paired with what the reviewer observes:

- `curl localhost:3000/api/orders/42` — returns 404 with `{"error":"not found"}`
- submit the login form with a blank password — inline "required" error appears

Skip whole-project gates (`npm test`, `tsc`, `npm run build`): they pass regardless of the diff and CI already runs them. If the pull request has no reviewer-runnable behavior (a pure internal refactor), say so in one line.

**Title.** Same bar as a commit subject: conventional type, human-readable *what*, no *where*/*how* leakage. Prefer the primary commit's subject when the branch is one commit; otherwise write a fresh subject that covers the branch.

Leave these out of the body — a reviewer reads it to understand the diff, so anything the diff does not show reads as noise or invention:

- Session narrative — discussions, plans, or decisions the diff does not show
- Alternatives debated in chat or rejected approaches
- Future work, follow-ups, or roadmap references
- Run-specific results — test counts, scores, or measured values
- Whole-project gates run for ceremony rather than to exercise the diff
- Implementation internals in the outcome — symbol names or which path ran; state only what the reviewer observes
- Attribution lines

Done when the title and body trace to the branch diff and carry none of the omitted items above.

**Step 5. Open the pull request.** Open the pull request with the base, title, and body above; omit any null section (`## Changes`, `## Test Plan`, `Closes #N`). If the call fails because the remote lacks `{branch}`, return to Step 3. Done when the call returns the pull request URL.

**Step 6. Report.** Report the pull request title and URL in chat — not the full body. Name the base in the report so a wrong base is visible right away. Done when the report carries the title, the URL, and the base.
