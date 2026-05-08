# Checklist

Generate `.agents/codebase/checklist.md` — post-task validation steps based on the project's tooling.

## When to Use

- Sub-agent dispatched during codebase summary fan-out
- User explicitly asks to refresh `checklist.md` after tooling changes (new linter, formatter, etc.)

## Scope

Verification steps to run after completing a task: type checking, linting, formatting, testing, code generation, pre-commit hooks. Commands come from the project's actual scripts and tooling — never invented.

## Reading Priorities

1. `package.json` `scripts` (or equivalent: `Makefile`, `pyproject.toml`, `Justfile`, `composer.json`)
2. Pre-commit config (`.husky/`, `.pre-commit-config.yaml`, `lefthook.yml`)
3. CI config (`.github/workflows/`, `.gitlab-ci.yml`) — pull standard validation steps
4. Lint/format config (`.eslintrc`, `.prettierrc`, `biome.json`, `ruff.toml`)
5. TypeScript / type-check config (`tsconfig.json`)

## Source Boundary

Document commands the project actually exposes. If `npm run typecheck` exists, document it; if not, document `tsc --noEmit` only when the user clearly uses that pattern. Do not invent generic commands.

## Output

Save to `.agents/codebase/checklist.md`. Update existing on re-run (merge, never overwrite).

## Template

ALWAYS use this exact template structure:

````markdown
---
project: {{project-name}}
created: {{YYYY-MM-DD}}
---

# Checklist

Run after completing a task:

## Code Quality
- [ ] `{{type check command}}`
- [ ] `{{lint command}}`
- [ ] `{{format command}}`

## Testing
- [ ] `{{test staged/changed files command}}`

## Generation (if applicable)
- [ ] `{{codegen command}}`

## Verification
- [ ] No type errors
- [ ] No lint errors
- [ ] Tests pass
- [ ] Code is formatted
````

## Guidelines

- Use the project's actual script names (e.g., `npm run lint`, not generic `eslint .`)
- Omit sections that don't apply (e.g., no Generation section if no codegen exists)
- Keep the checklist tight — this gets read every task
