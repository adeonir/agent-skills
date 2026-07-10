# Rule Format

Template and conventions for rule files. Every rule produced by the create or edit mode uses this format. The template is strict.

## When to Use

Loaded by the create mode after classification and context checks pass, and by the edit mode when applying changes.

## Template

ALWAYS use this exact template structure:

````markdown
---
paths:
  - "<glob>"
---

## <Rule Title>

**Impact: HIGH|MEDIUM|LOW**

<One paragraph: what the rule enforces and why it matters.>

**Incorrect:**

```<lang>
<bad example>
```

**Correct:**

```<lang>
<good example>
```

Reference: [<label>](<url>)
````

Omit the `paths:` frontmatter block entirely when the rule is global. Omit the `Reference:` line when no canonical source applies.

## Section rules

### Title

- One H2 (`## <Title>`) per rule
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

### Incorrect / Correct blocks

- Both are required; never one without the other
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

Path-scoped rule frontmatter:

```yaml
---
paths:
  - "src/**/*.ts"
  - "src/**/*.tsx"
---
```

Or with brace expansion:

```yaml
---
paths:
  - "src/**/*.{ts,tsx}"
---
```

Global rule: no frontmatter at all. Do not write an empty `---` block.

Frontmatter rules:

- `paths` is an array, even with a single entry
- Globs use forward slashes
- Quote every glob value
- Multiple globs in the array when brace expansion does not fit (different parent directories)

## Multi-rule files

A topic file groups related rules. Each rule is its own H2.

Example structure (`testing.md`):

````markdown
## Test File Placement

**Impact: MEDIUM**

<paragraph>

**Incorrect:** ...
**Correct:** ...

## Test Naming

**Impact: LOW**

<paragraph>

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
- [ ] Cites a specific tool, file pattern, or syntax — not a vague "code quality" gesture
- [ ] A reviewer reading a diff could point at a line and say "this violates the rule"

Fail any check → rewrite before saving.

## Examples

### Global, MEDIUM, with reference

````markdown
## Type Aliases for Object Shapes

**Impact: MEDIUM**

Use `type` for object shapes; reserve `interface` for declaration
merging. Mixing both for the same concept fragments the codebase and
forces readers to learn two equivalent dialects.

**Incorrect:**

```typescript
interface User { id: string name: string }
```

**Correct:**

```typescript
type User = { id: string name: string }
```

Reference: [TypeScript handbook — Type Aliases](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-aliases)
````

### Path-scoped, HIGH, no reference

````markdown
---
paths:
  - "src/api/**/*.ts"
---

## Validated Input on API Handlers

**Impact: HIGH**

Every API handler validates its request body with Zod before
touching the database. Skipping validation lets malformed input
reach the schema layer and corrupts data.

**Incorrect:**

```typescript
export async function POST(req: Request) { const body = await req.json() return db.users.create({ data: body }) }
```

**Correct:**

```typescript
export async function POST(req: Request) { const body = userCreateSchema.parse(await req.json()) return db.users.create({ data: body }) }
```
````
