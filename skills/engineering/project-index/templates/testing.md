---
project: {{project-name}}
created: {{YYYY-MM-DD}}
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
