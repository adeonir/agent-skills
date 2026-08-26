---
name: git-helpers
allowed-tools: Bash(git:*) Bash(gh:*) Read
description: "Git workflow helper for conventional commits, pull request creation, and pull request merging. Use when committing staged or unstaged changes, opening or pushing pull requests, or merging a pull request. Not for code review, acceptance-criteria verification, visual design review, general branch management, or session wrap-up."
---

# Git Helpers

Git workflow with conventional commits, pull requests, and pull request merges.

## Triggers

- **Commit changes** ("commit this", "create commit", "ready to commit", "all done") → [commit.md](references/commit.md)
- **Push and open PR** ("push this", "create PR", "open pull request", "ready to push") → [create-pull-request.md](references/create-pull-request.md)
- **Merge pull request** ("merge PR", "merge pull request", "ready to merge") → [finish-branch.md](references/finish-branch.md)

## Workflow

```text
commit → create-pull-request → merge-pull-request
```

Each step is independent. Use any workflow in isolation or chain them together.

## Tool Selection

For GitHub operations, check for an available qualified GitHub MCP tool first. Use it when available; use `gh` CLI only as the fallback. Use local Git commands for repository operations.

## Anti-Pattern: Conversation-Driven Messages

Writing a commit, PR, or merge message from chat context produces fabricated quotes, rejected approaches presented as fact, and restated diff content. The diff is the single source of *what* changed; the conversation supplies at most an explicit *why* the user stated. Before writing, trace every line back to a hunk in the diff — a line that names a change the diff does not show came from the conversation, so drop it.

## Guidelines

**Plain prose** — the word-choice bar for every message this skill writes: commit subject and body, PR title and body, merge subject and body. It governs diction, never length or register; each reference sets those for the message it owns.

- Prefer short, familiar words over corporate ones (`use` not `utilize`, `fix` not `ensure`).
- Keep one term for one concept in the same message — do not rotate synonyms for variety.
- Use active voice: name what the change does, not what "was updated".
- Put one main point in each sentence, and lead with the change or the problem — never `This commit…`, `This PR…`, `In order to…`.
- In prose, repeat the noun when `it`, `this`, or `that` could point at more than one thing, and break noun clusters into plain relations (`timeout for the database connection`). A subject keeps the developer's terse shorthand instead.
