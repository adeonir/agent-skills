# Commit Conventions

Conventional commit message format for the commit that closes a task boundary.

## When to Use

When building the message for a task commit in [implement.md](../instructions/implement.md) — the default 1 task = 1 commit boundary, and any grouped or split boundary noted in `tasks.md ## Commit Boundary Notes`. It defines the message only; staging, branching, pushing, and pull requests are out of scope.

## Sourcing

The message summarizes the boundary just closed. The agent making the commit already implemented and verified the work, so it builds the message from the boundary's tasks (their `Done when` and intent) and the actual changes made. There is no separate diff-reading pass — reproduce facts from what was written, never invented.

## Commit types

| Type | Use when |
|------|----------|
| `feat` | Adding new functionality |
| `fix` | Fixing a bug |
| `refactor` | Restructuring code without changing behavior |
| `test` | Adding or updating tests |
| `docs` | Documentation changes |
| `style` | Code style changes |
| `perf` | Performance improvements |
| `build` | Build system or external dependencies |
| `ci` | CI/CD configuration changes |
| `chore` | Maintenance tasks, dependencies, configs |

## Format rules

1. **Imperative mood** — "add", "fix", "implement" (not "added", "fixes").
2. **Concise subject** — ~72 characters, a soft ceiling.
3. **Human readable** — write the subject so a teammate understands it without opening the code. Tell the story of what moved and why it matters, not an abstract framing. `refactor: make db and auth per-request for d1 binding` reads like a story; `refactor: swap client and adapter for d1 pattern` reads like a release-note abstraction. See the AI-slop anti-pattern for the filler vocabulary to avoid.
4. **The subject carries the whole *what*** — it names the user-observable effect, and it is the only place the *what* lives. Keep file names, paths, mechanics, and specific values out (they live in the diff). One exception: when the file *is* the change (`docs: update README`), naming it is clearer than abstracting it.
5. **Match project style** — documented project rules win over everything here. Otherwise read the project log for one thing only: its scope usage (`type(scope):` vs `type:`). Do not add or strip scope against the established style. The log does not set the shape of the message; this reference does. A prompt directive overrides.
6. **No attribution, no future references** — never add Co-Authored-By or mention upcoming work.
7. **Breaking changes** — mark a change breaking (`type!:` or a `BREAKING CHANGE:` footer, per project style) when it alters observable behavior for a consumer, however small the diff. A one-line fix that changes what a caller observes is breaking; a large refactor that preserves behavior is not — the observable contract decides, not the diff size.

## Template

ALWAYS use this exact template structure:

```text
type(scope): subject

Prose body, when there is one.
```

Omit the blank line and body when the subject already says everything — the common case. Omit `(scope)` when the project style is scopeless. Neither subject nor body carries an AC reference: the identifier names an artifact, not the change.

## Body guidelines

**The body is never an inventory of what changed.** The subject already carries the *what*. The body states the problem with the previous behavior, then why this solution — prose, in one or two short paragraphs. Not bullets: a list opens empty slots that ask to be filled, and filling them turns the message into a transcript of the work.

**Most task commits have no body at all.** A body exists in exactly two cases:

- **The previous behavior was a problem** the change does not show on its face. *A problem, not merely a difference.* A rename, a doc edit, a new file that simply did not exist before — nothing was broken, so there is nothing to explain and the subject is the whole commit.
- **A constraint binds the solution** — a compatibility requirement, a limitation worked around, a tradeoff the task forced. A reader who does not know it reverts the change or reapplies it badly.

Neither case is about *listing* the work. A boundary that closes so many separable things that you want to enumerate them is a boundary that should have been split — say so instead of padding the body with bullets.

Never in the body: the reasoning that led to the change (the rationale, the discarded alternative, the design justification), the files touched, mechanics, values, counts, AC or task IDs. The rationale is the most seductive of these — it *feels* like a *why*, but it binds nothing: it retells the implementation session instead of arming the reader.

## Anti-Pattern: AI-slop subject

AI-slop has two opposite shapes, and "just be concrete" pushes out of the first and straight into the second. Watch for both.

**Shape 1 — empty abstraction.** The subject names a filler word instead of the thing that moved: filler verbs (*enhance, streamline, leverage, optimize* when nothing was measured), filler adjectives (*robust, comprehensive, seamless*), abstract nouns standing in for the real object (*logic, functionality, handling, behavior*).

**Shape 2 — fake concreteness.** Over-correcting yields a subject that reads like a release note:

- Specific values are *how*, not *what* — `retry failed uploads three times` → `retry failed uploads`; the count stays in the code.
- Prose locators are *where* — `... in CI` → drop it; the `ci:` scope already carries it.
- Reference codes are *where* handles, not *what* — `ADR-002`, `AC-2`, `#42`. The identifier names an artifact, not the change; describe what the change does, not its ID. Keep the code only when the repo's log references artifacts by it.

A human subject is terse and structural — it names what moved, in the developer's own shorthand, at topic altitude.

| AI-slop | Human |
|---------|-------|
| `feat: enhance error handling` | `feat: retry failed uploads` |
| `refactor: streamline auth logic` | `refactor: move token refresh into the request interceptor` |
| `chore: pin node to 20 in CI` | `ci: pin node version` |

## Examples

Most task commits are subject-only:

```text
feat(checkout): reject expired credit cards
```

```text
fix: resolve token refresh race condition
```

```text
refactor: extract validation logic into shared utilities
```

A body when the previous behavior was a problem — the problem, then why this solution:

```text
fix(checkout): read the config once at startup

Every request re-parsed the config from disk, so a deploy that rewrote the
file mid-flight served two different configs within the same second. Reading
at startup makes the process's view of the config immutable for its lifetime.
```

A body when a constraint binds the solution:

```text
refactor(parser): pin the tokenizer to the sync API

The async path drops surrogate pairs on flush, so the sync call stays until
that lands upstream — do not "modernize" this back.
```

**Bad — a body that inventories the work**, which is what the task list and the diff already are:

```text
feat(checkout): reject expired credit cards

- add an expiry check to the payment validator
- surface the rejection on the card field
- cover the branch in the payment tests
- covers AC-2
```

Nothing was broken and nothing binds the solution — the feature simply did not exist. No body:

```text
feat(checkout): reject expired credit cards
```

## Scope

This reference carries the message format only. It does **not** cover staging strategy, branch handling, pushing, or pull requests. Commits run hooks normally: never `--no-verify`, never `--amend`. Fixes are always a new commit.
