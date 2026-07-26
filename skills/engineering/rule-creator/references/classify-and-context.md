# Classify and Context

Gates that run before rendering a new rule. Classification decides whether the input deserves a rule at all, the context check whether the rule makes sense where it will land, and the destination decision picks the level and the scope.

## When to Use

Loaded by the create mode in SKILL.md, and by the extract mode when it runs these gates per approved section. Not used by list, edit, or delete.

## Classifier

The input must be **declarative** (a standing constraint Claude should follow). Anything else routes elsewhere.

### Decision table

| Pattern in the input | Verdict |
|----------------------|---------|
| Numbered steps, "first X then Y", explicit ordering, conditional branches | Procedural → recommend authoring a skill, exit |
| Lifecycle trigger ("before commit", "on save", "after edit", "pre-push") | Hook territory → recommend a hook, exit |
| Time-bound task ("today", "for this PR", "this one time") | One-off → refuse, suggest doing the work directly |
| Declarative convention ("always use X", "never Y", "X must Z", "prefer A over B") | Rule → proceed |

When the input is ambiguous, ask one targeted question:

> "Is this a standing convention or a one-off task?"

Do not auto-proceed when ambiguous.

### Refusal script

When the classifier rejects, output the verdict plainly and stop:

> "This reads as a multi-step workflow. Rules describe standing
> constraints, not procedures. Recommend authoring a skill for this
> instead. Continue there?"

Do not write a partial rule file when refusing, and do not invoke the recommended skill or hook workflow automatically — the user confirms and re-invokes.

## Context check

Rules live at two levels, and a rule at either level may already cover the input. Validate against both, whichever level the new rule targets.

| Level | Directory | Reaches |
|-------|-----------|---------|
| user | `~/.claude/rules/` | every project on the machine |
| project | `.claude/rules/` | this repository |

Project rules load after user rules and take priority.

### Resolving a memory file

A `CLAUDE.md` at either level may hold its content behind `@path` imports — a one-line `CLAUDE.md` importing `AGENTS.md` carries every line of that file. Resolve imports before reading or measuring: follow each `@path` up to four hops, and skip any `@path` inside a code span or fenced block, which is literal text that never loads.

### Checks in order

1. **Stack mismatch.** Project level only. Read `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or equivalent to identify the stack; if the rule names a stack the project does not use, flag and ask whether to proceed. Skip at user level — a rule spanning every project is not bound to the current one's stack.
2. **Duplicate topic.** List both rules directories recursively. Topic identity is the path relative to the rules directory, so `frontend/testing.md` and `backend/testing.md` are distinct topics. If a file matches the intended topic, read it: already covered → tell the user and exit; adjacent topic → propose appending an H2 section instead of a new file.
3. **Contradiction.** Read the memory files at both levels with imports resolved — `AGENTS.md` / `CLAUDE.md` and `.claude/CLAUDE.md` in the project, `~/.claude/CLAUDE.md` at user level — plus the rules at the other level. If the rule contradicts an instruction there, flag both passages and ask which wins. When the conflict crosses levels, name the winner: project.

Flag findings as a short list and let the user decide. Do not silently override. Verifiability is checked separately in the final gate before write — see [rule-format.md](rule-format.md).

## Destination decision

Two independent axes.

| Axis | Values | Materializes as |
|------|--------|-----------------|
| Level | user / project | the directory written to |
| Scope | unconditional / path-scoped | absence or presence of `paths:` frontmatter |

**user + path-scoped is unavailable.** Path-scoped user rules are not documented as supported and are reported to be ignored, so a path signal resolves the level to project. A user-level rule is always unconditional.

### Level

**User signals:** "all my projects", "every project", "always", "user-level", or a personal tooling or workflow preference naming no repository.

**Project signals:** the input names a stack, directory, or framework of the current repository, or says "this project", "here", "in this repo". A path signal is a project signal.

**No signal → ask.** Never infer the level from the content of the rule; writing to `~/.claude/rules/` reaches every project on the machine.

When the rule belongs to several projects but not all of them, neither level fits — symlink one file into each project instead:

```bash
ln -s ~/shared-claude-rules/security.md .claude/rules/security.md
```

Symlinks in a rules directory are resolved and loaded normally, and a circular link is detected rather than followed.

### Scope

**Path signals** (path-scoped):

- File extension mentioned: `.ts`, `.tsx`, `.py`, `.go`, `.rs`, `.md`, `.sql`, etc.
- Directory mentioned: `src/`, `tests/`, `app/api/`, etc.
- Framework or library tied to a directory: "React components", "API handlers", "Django models", "Next.js pages"
- Scope phrase: "when working with X", "in the API code", "for tests"

**Unconditional signals** (no `paths:` block):

- Universal stylistic conventions: "indentation", "naming", "imports"
- Cross-cutting concerns: "security", "logging", "error handling"
- Workflow conventions: "before committing", "test before merging" (note: these may also be hook candidates — re-check classifier)

### Glob shape

When path-scoped, infer the most specific glob from the signal:

| Signal | Glob |
|--------|------|
| "TypeScript files" | `**/*.ts` |
| "TypeScript and TSX" | `**/*.{ts,tsx}` |
| "API handlers under src/api" | `src/api/**/*.{ts,tsx}` |
| "React components" | `src/components/**/*.tsx` |
| "Python tests" | `tests/**/*.py` |

Prefer brace expansion (`{ts,tsx}`) over multiple array entries when extensions share a parent. Each brace group multiplies the expanded pattern count, and a rule's whole `paths` list shares one budget of 1,000 expanded patterns — a list that exceeds it is used unexpanded, and its literal braces match nothing.

Always validate the glob: forward slashes, standard glob syntax, no backslashes or shell-specific expansions. A `[` opens a bracket expression, so one that cannot be read as such matches nothing — escape a literal bracket as `\[`.

When the signal is ambiguous between two globs, ask once with both options. A clear scope signal is inferred without a question. Each question is a cost.
