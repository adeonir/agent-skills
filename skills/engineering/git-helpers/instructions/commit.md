# Commit

Create a conventional commit shaped to the project's conventions from the actual changes.

## Load first

Read [message-sourcing.md](../references/message-sourcing.md) before writing anything — it carries where the words come from, the diction bar, and the two shapes of slop this subject must avoid.

## Reading the change

Read `git status --short` to plan staging. Once staging is complete, read `git diff --cached`. Never diff before staging is complete: unstaged changes pollute the message with content that will not land.

## Staging

Stage by name the files that belong to this change — never a blind `git add -A`, never a file containing secrets. Respect `.gitignore`: never `git add -f` an ignored path — ignored files (build output, local scratch, secrets) are excluded on purpose; if a file you mean to stage is ignored, stop and surface it, staging only on explicit user confirmation. If files are already staged, flag them before adding more; `git add .` is only for an explicit "stage everything". When the user says "only staged", commit the existing index as-is.

## One commit, one type

Run the mixed-type check on the staged diff before writing — not optional: if the diff mixes unrelated change types (a feature plus an unrelated fix), flag it and ask whether to split. On accept, unstage the unrelated files and commit them separately; on decline, pick the primary type.

Split only when the types fall on file boundaries. When one file carries both, the split is no longer available: never stage selected hunks to manufacture it, because every commit built that way asserts a file state that never existed on disk and was never read. Say the commit mixes types, pick the primary one, and commit it whole.

## Format Rules

1. **Imperative mood**: write the subject as a command — "add", "fix", "move", never "added" or "fixes".
2. **Human readable**: Write the subject so a teammate understands it without opening the diff. Prefer descriptions that tell the story of the change — what actually moved and why it matters — over abstract framing. The first reads like a story; the second like a release-note abstraction:
   - `refactor: make db and auth per-request for d1 binding`
   - `refactor: swap client and adapter for d1 pattern`

   The filler vocabulary to avoid is in the loaded reference; the table below applies it to a subject.
3. **The subject carries the whole *what***: it names the user-observable effect, and it is the only place the *what* lives. Keep out *where* (file names, paths, the location touched) and *how* (mechanics, specific values, counts, package versions) — those live in the diff and the code. This holds even when a single file is the whole change: name what the edit does (`docs: document the install steps`), not the file it lands in.
4. **Follow project conventions**: Documented rules (AGENTS.md / CLAUDE.md) win over everything here. Otherwise match the log, as the form pass below sets out. User can override (e.g. "add scope `auth`", "drop the scope").
5. **No attribution**: Never add Co-Authored-By or similar lines
6. **No future references**: Don't mention upcoming work or architectural reasoning
7. **Breaking changes**: mark a change breaking (`type!:` or a `BREAKING CHANGE:` footer, per project style) when the diff alters observable behavior for a consumer, however small. A one-line change that alters what a caller observes is breaking; a large refactor that preserves behavior is not — the observable contract decides, not the diff size.

## Anti-Pattern: AI-slop subject

Both shapes of slop applied to a commit subject:

| AI-slop | Human |
|---------|-------|
| `feat: enhance error handling` | `feat: retry failed uploads` (the count stays in the code) |
| `refactor: streamline auth logic` | `refactor: move token refresh into the request interceptor` |
| `chore: pin node to 20 in CI` | `ci: pin node version` (the exact version stays in the config) |
| `feat: implement user authentication functionality` | `feat: add password login` |
| `fix: ensure proper token refresh behavior` | `fix: refresh tokens before they expire` |

## Body

**Default to no body.** The subject carries the *what*, and most commits stop there.

A body is earned by one observation, made against the staged diff before any of it is written: name the wrong action a reader holding the diff would take without it — reverts the change, reapplies it badly, re-fixes the same bug, reaches again for the mechanism this one rules out. No wrong action to name, no body. A reader understanding less is not a wrong action, and taking it for one is what puts a body on every commit. The observation is the gate, never a trim applied afterwards, because a body written first and justified second always finds its justification.

The observation finds one of two things:

- **The previous behavior was a problem the changed lines do not show.** *A problem, not merely a difference.* Nearly every change has a problem behind it, and the diff usually shows that problem plainly, so having one settles nothing on its own. Ask whether the changed lines already carry it.
- **A constraint binds the solution** — a compatibility requirement, a limitation worked around, a tradeoff forced on you.

**One sentence.** Write the fact the observation found — the problem the diff does not show, or the constraint — and stop. Never pair them as the problem and then why this solution: that arc retells the session behind the change, which is the leak the body exists to keep out. Never bullets either: a list opens empty slots that ask to be filled, and filling them turns the message into a transcript of the diff. A commit doing so many separable things that you want to enumerate them is a commit to split.

The rationale is not a finding. The reader already holds the change, so the reasoning that led to it — the discarded alternative, the design justification, why this solution beat the other one — retells the conversation instead of arming them. Neither are the files touched, the mechanics, the values, versions, or counts.

When the user asks to reevaluate or fix a bloated body, do not silently delete it. Cut it to what the observation supports first. Drop the body entirely when the observation finds nothing, and tell the user that is what you did and why.

## Matching the project's form

With the message drafted, read `git log --oneline -10 --no-merges` and adjust the draft to the form the log establishes: scope usage (`type(scope):` vs `type:`) and which scopes exist, subject casing, the type vocabulary in use, the language the messages are written in, and any trailing reference the merge style appends (`(#42)`). Never add or strip a form element against it.

The log sets form only. It never sets what the subject says.

## Examples

Most commits are subject-only:

```text
fix: resolve token refresh race condition
```

```text
refactor: extract validation logic into shared utilities
```

```text
chore(auth): rotate signing key
```

A body when the previous behavior was a problem the diff does not show:

```text
fix: read the config once at startup

A deploy that rewrote the config while the process ran served two different
configs to requests in the same second.
```

A body when a constraint binds the solution:

```text
refactor: pin the tokenizer to the sync API

The async path drops surrogate pairs on flush, so the sync call stays until
that lands upstream.
```

**Bad — a body that inventories the diff.** One line per file operation, which is what the diff already is:

```text
ci: consolidate workflows

- replace four workflow files with one
- add needs to chain jobs
- remove old lint.yml, test.yml, build.yml, typecheck.yml
- update deploy.yml to chain smoke
```

The previous behavior *was* a problem, so this commit earns a body — but the body must say the problem, not re-list the hunks:

```text
ci: consolidate workflows

Four independent workflows each re-installed the toolchain, so a lint failure
still paid for the full test and build run.
```

## Committing

Commit runs the project's hooks (lint, tests, secret scans) — never `--no-verify`, `--no-gpg-sign`, or any bypass flag; never `--amend`. If a hook fails, fix the cause and make a new commit — the failed commit did not land, so a new commit is the only forward path. Confirm the commit landed — if the files still show as pending, stop and tell the user. Report the subject and body in chat, not the diff.
