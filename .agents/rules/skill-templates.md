---
paths:
  - "skills/**/*.md"
---

## Copyable Templates in Assets

**Impact: MEDIUM**

A copyable output template lives at `assets/*`. Keep a short format example inline when the agent should read it as instruction rather than copy it as an output file. One reference or instruction owns each template and routes to it explicitly; never add a `templates/` directory or reuse one template across workflows.

**Incorrect:**

```text
skill-name/templates/spec.md
```

**Correct:**

```text
skill-name/assets/spec.md
skill-name/references/specify.md   # routes to the copyable asset
```

## Mark Template Rigidity

**Impact: MEDIUM**

Every template states its expected behavior explicitly: strict with `ALWAYS use this exact template structure:` or flexible with `Here is a sensible default format, but use your best judgment:`. An unmarked template leaves the agent guessing how much it may adapt.

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
