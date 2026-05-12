# Testing

Generate `.agents/codebase/testing.md` — test infrastructure, patterns, mocking approach, and coverage gaps.

## When to Use

- Sub-agent dispatched during codebase summary fan-out
- User explicitly asks to refresh `testing.md` after test setup changes

## Scope

Test framework, file naming and location, structural patterns (describe/it nesting), mocking approach, fixtures and helpers, coverage gaps if detected. All evidence comes from actual test files.

## Reading Priorities

1. Test config (jest.config, vitest.config, pytest.ini, etc.)
2. Sample test files across types and quantities:
   - Small (<30 source files): 2-3 tests
   - Medium (30-100 source files): 3-5 tests (unit, integration, e2e)
   - Large (>100 source files): 5-8 tests across types
3. Diversity: unit, integration, e2e; happy path, edge cases, error handling

Prefer AST-aware tooling (e.g., `smart-explore`) over full `Read` when scanning test files larger than 300 lines — same structural signal at a fraction of the tokens.

## Source Boundary

Read actual test files — do not infer patterns from framework documentation. If the project uses jest with custom matchers, document the custom matchers, not jest's defaults.

## Output

Save to `.agents/codebase/testing.md`. On re-run, follow [merge-policy.md](merge-policy.md).

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources:
  - {{file-path-actually-read}}
  - {{file-path-actually-read}}
---

# Testing

## Infrastructure

| Aspect | Detail |
|--------|--------|
| Framework | {{jest/vitest/etc}} |
| Command | {{npm test/etc}} |
| Location | {{test directory pattern}} |
| Naming | {{test file naming convention}} |

## Patterns

### Test Structure

```{{lang}}
// Source: {{test-file-path}}
{{code example showing describe/it structure, setup/teardown}}
```

### Mocking

```{{lang}}
// Source: {{test-file-path}}
{{code example showing mocking approach}}
```

### Fixtures / Helpers

```{{lang}}
// Source: {{test-file-path or helper-path}}
{{code example showing fixture or helper pattern}}
```

## Reference Tests

| File | What It Tests | Why It's a Good Reference |
|------|---------------|--------------------------|
| {{test file}} | {{what it covers}} | {{what pattern it demonstrates}} |

## Coverage Gaps

{{Areas with missing or insufficient test coverage, if detected during scan}}
````

## Guidelines

- Read tests; do not list them
- Pick reference tests that demonstrate the cleanest version of each pattern
- Coverage Gaps section: include only when actual gaps were observed, omit otherwise
- Populate `sources:` with every file actually read; empty list is not acceptable
