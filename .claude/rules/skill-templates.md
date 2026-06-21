---
paths:
  - "skills/**/*.md"
---

## Inline Templates, One Per Reference

**Impact: MEDIUM**

A template lives inline in the reference that uses it, one template per
reference, with no reuse across references and no `templates/` directory. A
shared template folder couples references and drifts from the prose that
depends on it.

**Incorrect:**

```text
skill-name/templates/spec.md
```

**Correct:**

```text
skill-name/references/specify.md   # the spec template lives inline here
```

## Mark Template Rigidity

**Impact: MEDIUM**

Every template states its expected behavior explicitly: strict with `ALWAYS
use this exact template structure:` or flexible with `Here is a sensible
default format, but use your best judgment:`. An unmarked template leaves the
agent guessing how much it may adapt.

**Incorrect:**

```markdown
Use this template:

## Summary
{{...}}
```

**Correct:**

```markdown
ALWAYS use this exact template structure:

## Summary
{{...}}
```
