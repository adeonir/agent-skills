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
4. **What and why, never where or how** — carry the user-observable effect and the why; keep file names, paths, mechanics, and specific values out (they live in the diff). One exception: when the file *is* the change (`docs: update README`), naming it is clearer than abstracting it.
5. **Match project style** — follow the project log's scope usage (`type(scope):` vs `type:`); do not add or strip scope against the established style. A prompt directive overrides.
6. **No attribution, no future references** — never add Co-Authored-By or mention upcoming work.
7. **Breaking changes** — mark a change breaking (`type!:` or a `BREAKING CHANGE:` footer, per project style) when it alters observable behavior for a consumer, however small the diff. A one-line fix that changes what a caller observes is breaking; a large refactor that preserves behavior is not — the observable contract decides, not the diff size.

## Template

ALWAYS use this exact template structure:

```text
type(scope): subject

- body bullet 1
- body bullet 2
```

Omit the blank line and body when the subject already says everything. Omit `(scope)` when the project style is scopeless. The subject states what was done, without AC references; the body may cite the ACs covered when useful.

## Body guidelines

The body makes the commit self-sufficient — a reader understands the change from the message alone. Write it as a **curated mini-changelog**, not a hunk-by-hunk transcript:

- 1 to 5 bullets — the *meaningful* changes, grouped; drop incidental edits.
- Start each bullet with a lowercase imperative verb ("- add", "- remove").
- Fold in the *why* where the changes alone don't carry it.

A curated bullet can still smuggle literal instance data — an exact value in parentheses, a proper noun, a quoted copy string. Strip it when the bullet's structural description already carries the meaning; keep a literal only when it *is* the change (a config value whose number is the decision). It is the subject's fake-concreteness trap (Shape 2), applied to bullets.

A change that spans files leaks the diff's redundancy when each bullet restates the shared substance once per file. State the substance once — in the subject or the primary bullet — and let each sibling bullet say what *its* file did, not re-list the shared decision.

A trivial change needs no body.

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

```text
feat(checkout): reject expired credit cards

- reject cards past their expiry at payment time
- covers AC-2
```

```text
fix: resolve token refresh race condition
```

```text
refactor: extract validation logic into shared utilities
```

## Scope

This reference carries the message format only. It does **not** cover staging strategy, branch handling, pushing, or pull requests. Commits run hooks normally: never `--no-verify`, never `--amend`. Fixes are always a new commit.
