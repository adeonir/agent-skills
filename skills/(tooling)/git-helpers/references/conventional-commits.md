# Conventional Commits

Standard for writing consistent, meaningful commit and PR messages.

## Commit Types

| Type | Use when |
|------|----------|
| `feat` | Adding new functionality |
| `fix` | Fixing a bug |
| `refactor` | Restructuring code without changing behavior |
| `chore` | Maintenance tasks, dependencies, configs |
| `docs` | Documentation changes |
| `test` | Adding or updating tests |
| `style` | Code style changes |
| `perf` | Performance improvements |
| `ci` | CI/CD configuration changes |
| `build` | Build system or external dependencies |

## Message Format

```
type: concise description in imperative mood

- Optional: key change 1
- Optional: key change 2
```

## Format Rules

1. **Use imperative mood**: "add", "fix", "implement" (not "added", "fixes")
2. **Be concise**: First line under 72 characters
3. **Focus on WHAT**: Describe the change and the observable behavior from the user's perspective
4. **Follow project conventions**: Check AGENTS.md or CLAUDE.md for explicit commit rules first. Only fall back to `git log --oneline -10 --no-merges` if no rules are documented. When analyzing the log, distinguish between regular commits and PR/merge commits, as they may follow different conventions. Only use scope if the project's guidelines explicitly require it for regular commits
5. **No file names**: Don't mention specific files in the message
6. **No versions**: Don't mention package versions
7. **No attribution**: Never add Co-Authored-By or similar lines
8. **No future references**: Don't mention upcoming work or architectural reasoning
9. **Diff only**: Base the message exclusively on the actual diff — never on conversation context, prior discussion, or assumptions

## Body Guidelines

Optional. When included, explain HOW the change was implemented from a developer's perspective.

- 1 to 5 bullet points
- Complex change needs explanation
- Breaking change needs documentation
- No file names or paths

## Examples

**Good:**

```
feat: add user authentication flow

- Support email/password login
- Add session management
- Include remember me option
```

```
fix: resolve token refresh race condition
```

```
refactor: extract validation logic into shared utilities
```

**Bad:**

```
feat: Added authentication and updated src/auth.ts

Updated lodash to 4.17.21 for security.
Co-Authored-By: AI Assistant
```
