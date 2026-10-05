# Commit Conventions

Conventional commit message format for the commit that closes a task boundary.

## When to Use

When building the message for a task commit in [implement.md](../instructions/implement.md) — the default 1 task = 1 commit boundary, and any grouped or split boundary noted in `tasks.md ## Commit Boundary Notes`. It defines the message only; which files to stage, branching, pushing, and pull requests are out of scope.

## Sourcing

The message summarizes the boundary just closed. Stage the boundary's files, read `git diff --cached`, and commit, in three separate commands; never write the message before the staged diff was read. The staged diff alone settles what changed: drop any claim about a change it does not show. The boundary's tasks (their `Done when` and intent) supply at most the problem or constraint a body states.

Commits run hooks normally: never `--no-verify`, never `--amend`. A failed hook means the commit did not land: fix the cause and make a new commit. Confirm the commit landed before reporting it; if the files still show as pending, stop and report. Fixes are always a new commit.

## Format rules

1. **Imperative mood** — "add", "fix", "move" (not "added", "fixes").
2. **Human readable** — write the subject so a teammate understands it without opening the code. Tell the story of what moved and why it matters, not an abstract framing. `refactor: make db and auth per-request for d1 binding` reads like a story; `refactor: swap client and adapter for d1 pattern` reads like a release-note abstraction. See the AI-slop anti-pattern for the filler vocabulary to avoid.
3. **The subject carries the whole *what*** — it names the user-observable effect, and it is the only place the *what* lives. Keep file names, paths, mechanics, and specific values out (they live in the diff). This holds even when a single file is the whole change: name what the edit does (`docs: document the install steps`), not the file it lands in.
4. **Match project style** — documented project rules win over everything here. Otherwise read `git log --oneline -10 --no-merges` for the project's message form: scope usage (`type(scope):` vs `type:`) and which scopes exist, subject casing, the type vocabulary in use, the language the messages are written in, and any trailing reference the merge style appends (`(#42)`). Match what the log establishes — never add or strip a form element against it. The log sets form only. It never sets the bar for what the subject says; this reference does, however sloppy the log reads. A prompt directive overrides.
5. **No attribution, no future references** — never add Co-Authored-By or mention upcoming work.
6. **Breaking changes** — mark a change breaking (`type!:` or a `BREAKING CHANGE:` footer, per project style) only when the diff makes an existing consumer incompatible with an established, observable contract. Name the affected consumer and the concrete incompatibility in the return summary. A changed internal artifact format or documentation example alone does not establish a breaking change, and neither does a fix that existing consumers still work with.

## Diction

The bar for the subject and the body. It governs word choice, never length or register; the format rules and the body guidelines set those.

- Prefer short, familiar words over corporate ones (`use` not `utilize`, `fix` not `ensure`).
- Keep one term for one concept in the same message — do not rotate synonyms for variety.
- Use active voice: name what the change does, not what "was updated".
- Put one main point in each sentence, and lead with the change or the problem — never `This commit…`, `In order to…`.
- In the body, repeat the noun when `it`, `this`, or `that` could point at more than one thing, and break noun clusters into plain relations (`timeout for the database connection`). A subject keeps the developer's terse shorthand instead.
- Keep every condition, limit, exception, and stated uncertainty the source carries — a shorter message never drops one.
- Use no idiom, metaphor, or slang, and no abbreviation the reader cannot expand from the diff or the project.

## Template

ALWAYS use this exact template structure:

```text
type(scope): subject

Prose body, when there is one.
```

Omit the blank line and body when the subject already says everything — the common case. Omit `(scope)` when the project style is scopeless. Neither subject nor body carries an AC or task ID: the identifier names an artifact, not the change.

## Body guidelines

**Most task commits have no body at all.** A body exists in exactly two cases:

- **The previous behavior was a problem** the change does not show on its face. *A problem, not merely a difference.* A rename, a doc edit, a new file that simply did not exist before — nothing was broken, so there is nothing to explain and the subject is the whole commit.
- **A constraint binds the solution** — a compatibility requirement, a limitation worked around, a tradeoff the task forced.

**One sentence.** State the fact — the problem the change does not show, or the constraint — and stop. Never pair them as the problem and then why this solution: that arc retells the implementation session, which is what the body exists to keep out. Never bullets either: a list opens empty slots that ask to be filled, and filling them turns the message into a transcript of the work. A boundary that closes so many separable things that you want to enumerate them is a boundary that should have been split.

Never in the body: the reasoning that led to the change (the rationale, the discarded alternative, the design justification), the conversation that asked for it ("as discussed", "per the user"), the files touched, mechanics, values, or counts. The rationale is the most seductive of these — it *feels* like a *why*, but it binds nothing: it retells the implementation session instead of arming the reader.

**The order.** Write the subject, run both tests below against the staged diff, and write the sentence only once both pass. Never draft a sentence and then judge whether it stays: a body written first and justified second always finds its justification.

**Test 1 — does the diff already answer it?** Read the staged diff alone and ask what problem it solves. If the changed lines answer, there is no body.

**Test 2 — substitution.** Put another commit of the same type in front of the candidate sentence and read it again. A sentence that stays true does not describe this commit, and it goes: `The request crashed instead of returning an error` stays true for most fixes; `A deploy that rewrote the config while the process ran served two different configs in the same second` is true of one commit only.

## Anti-Pattern: AI-slop subject

AI-slop has two opposite shapes, and "just be concrete" pushes out of the first and straight into the second. Watch for both.

**Shape 1 — empty abstraction.** The subject names a filler word instead of the thing that moved. The tells cluster in a small vocabulary:

- Filler verbs: *enhance, streamline, leverage, utilize, facilitate, revamp* — plus *optimize* when nothing was measured, *ensure, enable, provide, implement* when the work just adds or changes code, *introduce, support* with no concrete object, and *improve, update, tweak, rework* unless paired with a concrete object
- Filler adjectives: *robust, comprehensive, seamless, proper, modern*
- Abstract nouns standing in for the real object: *logic, functionality, handling, behavior, mechanism, capability, configuration, infrastructure*
- Corporate phrasing that pretends to explain: *in order to, with the goal of, this allows users to, making it possible to*

**Shape 2 — fake concreteness.** Over-correcting yields a subject that reads like a release note:

- Specific values are *how*, not *what* — `retry failed uploads three times` → `retry failed uploads`; the count stays in the code.
- Prose locators are *where* — `... in CI` → drop it; the `ci:` scope already carries it.
- Reference codes are *where* handles, not *what* — `ADR-002`, `#42`. The identifier names an artifact, not the change; describe what the change does, not its ID. Keep the code only when the repo's log references artifacts by it.

A human subject is terse and structural — it names what moved, in the developer's own shorthand, at topic altitude.

| AI-slop | Human |
|---------|-------|
| `feat: enhance error handling` | `feat: retry failed uploads` |
| `refactor: streamline auth logic` | `refactor: move token refresh into the request interceptor` |
| `chore: pin node to 20 in CI` | `ci: pin node version` |
| `feat: implement user authentication functionality` | `feat: add password login` |
| `fix: ensure proper token refresh behavior` | `fix: refresh tokens before they expire` |

## Examples

Most task commits are subject-only, like every *Human* subject in the table above.

A body when the previous behavior was a problem the change does not show:

```text
fix(checkout): read the config once at startup

A deploy that rewrote the config while the process ran served two different
configs to requests in the same second.
```

A body when a constraint binds the solution:

```text
refactor(parser): pin the tokenizer to the sync API

The async path drops surrogate pairs on flush, so the sync call stays until
that lands upstream.
```

**Bad — a body that inventories the work**, which is what the task list and the diff already are:

```text
feat(checkout): reject expired credit cards

- add an expiry check to the payment validator
- surface the rejection on the card field
- cover the branch in the payment tests
- covers AC-2.1
```

Nothing was broken and nothing binds the solution — the feature simply did not exist. No body.
