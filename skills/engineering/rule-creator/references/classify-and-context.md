# Classify and Context

Gates that run before rendering a new rule. Classification decides whether the input deserves a rule at all. Context check decides whether the rule makes sense in this project.

## When to Use

Loaded by the create mode in SKILL.md. Not used by list, edit, extract, or delete.

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

Do not write a partial rule file when refusing.

## Project context check

After classification passes, validate the rule against the actual project state.

### Checks in order

1. **Stack mismatch.** Read `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or equivalent to identify the stack. If the rule names a stack the project does not use ("use Rust naming conventions" in a Node project), flag and ask whether to proceed.
2. **Duplicate topic.** List `.claude/rules/`. If a file matches the intended topic, read it. If it already covers the instruction, tell the user and exit. If it covers an adjacent topic, propose appending an H2 section instead of creating a new file.
3. **CLAUDE.md contradiction.** Read `CLAUDE.md` (and `.claude/CLAUDE.md` if present). If the rule contradicts an existing instruction there, flag both passages and ask the user which wins.

Flag findings as a short list and let the user decide. Do not silently override. Verifiability is checked separately in the final gate before write — see [rule-format.md](rule-format.md).

## Scope decision

The decision is between **global** (no frontmatter, applies to every file Claude touches) and **path-scoped** (`paths:` frontmatter, applies only when Claude reads files matching the glob).

### Signal vocabulary

**Path signals** (default to path-scoped when any are present):

- File extension mentioned: `.ts`, `.tsx`, `.py`, `.go`, `.rs`, `.md`, `.sql`, etc.
- Directory mentioned: `src/`, `tests/`, `app/api/`, etc.
- Framework or library tied to a directory: "React components", "API handlers", "Django models", "Next.js pages"
- Scope phrase: "when working with X", "in the API code", "for tests"

**Global signals** (default to global when none of the above apply):

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

Prefer brace expansion (`{ts,tsx}`) over multiple array entries when extensions share a parent.

Always validate the glob: it must use forward slashes and standard glob syntax. Reject backslashes or shell-specific expansions.

## When to ask vs infer

| Situation | Action |
|-----------|--------|
| Input has clear path signal | Infer path-scoped, render frontmatter, no question |
| Input has no path signal | Infer global, no question |
| Input ambiguous between two globs | Ask once with two options |
| Stack mismatch detected | Ask before proceeding |
| Duplicate topic detected | Ask append vs new |
| CLAUDE.md contradiction | Ask which wins |

Never ask more than necessary. Each question is a cost.
