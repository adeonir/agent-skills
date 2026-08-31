# Rule Format

Template and conventions for rule files. Every rule produced by the create or edit mode uses this format. Required and optional sections are marked.

## When to Use

Loaded to render a rule and to verify one: by create and extract after the gates pass, and by edit when applying a change.

## Template

Here is a sensible default format, but use your best judgment:

````markdown
---
paths:
  - "[glob]"
---

## [Rule title]

**Impact: HIGH|MEDIUM|LOW**

[One paragraph: what the rule enforces and why it matters.]

<!-- Optional: include when the rule has independent principles to list. -->
### Principles

- [principle]

<!-- Optional: include the pair when a concrete contrast helps verify the rule. -->
**Incorrect:**

```[language]
[bad example]
```

**Correct:**

```[language]
[good example]
```

Reference: [label](url)
````

Omit the `paths:` frontmatter block entirely when the rule is unconditional. Omit the `Reference:` line when no canonical source applies.

## Section rules

### Title

- One H2 (`## [Rule title]`) per rule
- Title is a noun phrase describing the constraint, not a verb command
- Examples: `Type Aliases for Object Shapes`, `No Implicit Any`, `Test File Placement`
- Avoid: `Use type instead of interface` (verb-led), `Types` (too broad)

### Impact line

Required. Exactly one of `HIGH`, `MEDIUM`, `LOW`.

| Level | Use when |
|-------|----------|
| HIGH | Bug-prone code, security risk, data loss, breaks production |
| MEDIUM | Consistency, maintainability, team conventions |
| LOW | Style, formatting, cosmetic preference |

Impact is the author's judgment. When unsure, write MEDIUM. Do not omit the line.

### Explanation paragraph

- One paragraph, two to four sentences
- States the constraint and the reason
- No preamble, no motivation history, no acknowledgments
- No "this rule ensures..." filler; state the constraint directly

### Principles

- Optional. Add bullets when the rule has independent principles that are clearer as a list than in the paragraph.
- Keep each bullet to one constraint or one type of information.

### Incorrect / Correct blocks

- Optional. Add the pair when a concrete contrast helps a reviewer verify the rule.
- Include both blocks or neither
- Use the same language tag in both blocks (`typescript`, `python`, `bash`, etc.) — every fenced block declares its language
- Examples must be minimal: the smallest snippet that demonstrates the contrast
- Avoid unrelated noise (imports, setup, comments) unless they are the point of the rule
- The contrast between Incorrect and Correct must be visible at a glance

### Reference line

- Optional
- One link per rule, to a canonical source (official docs, RFC, style guide)
- Drop if no canonical reference exists; do not fabricate one
- Do not link to internal docs that move or rot

## Frontmatter

- `paths` is an array, even with a single entry
- Quote every glob value
- Multiple entries in the array only when brace expansion does not fit (different parent directories)
- Unconditional rule: no frontmatter at all — do not write an empty `---` block
- A user-level rule is always unconditional, so it never carries a `paths:` block

## Multi-rule files

A topic file groups related rules. Each rule is its own H2.

Example structure (`testing.md`):

````markdown
## Test File Placement

**Impact: MEDIUM**

[paragraph]

**Incorrect:** ...
**Correct:** ...

## Test Naming

**Impact: LOW**

[paragraph]

**Incorrect:** ...
**Correct:** ...
````

Rules:

- All rules in one file share the same `paths:` scope (if any) — a topic file is one frontmatter block at the top, not per-rule
- If two rules need different scopes, they belong in different files
- Order rules by impact: HIGH first, then MEDIUM, then LOW
- No H1 in rule files; the filename serves as the topic identifier

## Verifiability checklist

Before writing, every rule must pass three checks:

- [ ] Has an action verb in the explanation paragraph (use, prefer, validate, reject, never, always, etc.)
- [ ] Cites a specific tool, file pattern, or syntax — not a vague "code quality" gesture ("format code properly", "write good tests" fail here)
- [ ] A reviewer reading a diff could point at a line and say "this violates the rule"

Fail any check → rewrite before saving.

## Example

Path-scoped, HIGH, with reference:

````markdown
---
paths:
  - "src/api/**/*.ts"
---

## Validated Input on API Handlers

**Impact: HIGH**

Every API handler validates its request body with Zod before touching the
database. Skipping validation lets malformed input reach the schema layer
and corrupts data.

**Incorrect:**

```typescript
export async function POST(req: Request) {
  const body = await req.json()
  return db.users.create({ data: body })
}
```

**Correct:**

```typescript
export async function POST(req: Request) {
  const body = userCreateSchema.parse(await req.json())
  return db.users.create({ data: body })
}
```

Reference: [Zod — Basic usage](https://zod.dev/?id=basic-usage)
````
