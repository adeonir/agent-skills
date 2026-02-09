# Baseline Discovery

Document current behavior for brownfield features.

## Purpose

For features that modify existing code, understand what the system currently does from a user perspective (not implementation details).

## When to Use

- Feature type is `brownfield` (modifies existing code)
- Creating spec for improvement/refactoring of existing functionality

## Process

### Step 1: Extract Keywords from Description

**Brownfield indicators:**
- "improve", "refactor", "fix", "optimize"
- "extend", "add to", "modify", "update"
- "melhorar", "refatorar", "corrigir", "otimizar"

**Greenfield indicators:**
- "create", "new", "implement from scratch"
- "criar", "novo", "implementar do zero"

### Step 2: Search Codebase for Related Code

Extract technical terms from description (e.g., "cache", "auth", "payment").

```bash
# Find files by name
find . -name "*{term}*" -type f

# Find files containing term
grep -r "{term}" --include="*.ts" --include="*.js" -l
```

### Step 3: Determine Type

| Keywords | Code Found | Type | Action |
|----------|------------|------|--------|
| Greenfield | No | greenfield | Proceed |
| Greenfield | Yes | Ask user | Clarify intent |
| Brownfield | No | Ask user | Clarify intent |
| Brownfield | Yes | brownfield | Proceed with baseline |
| Unclear | No | greenfield | Default to new |
| Unclear | Yes | Ask user | Clarify intent |

**If ambiguous, ask:**
```
Found related code in: src/cache/redis.ts, src/cache/memory.ts
Is this:
1. New feature (greenfield) - not related to existing code
2. Change to existing code (brownfield)
```

### Step 4: Analyze Current Behavior

For brownfield features, understand from user perspective:

**What users can currently do:**
- Current capabilities
- Current workflows
- Current limitations

**What needs to change:**
- Missing functionality
- Performance issues
- Usability problems

### Step 5: Document Baseline

Add to spec.md (high-level behavior only):

```markdown
## Baseline

Current state based on codebase analysis.

### Current Behavior

- Users can currently do X
- System behaves like Y
- Limitation: Z

### Gaps / Limitations

- Missing: A
- Problem: B
- Improvement needed: C
```

**Important:** Describe BEHAVIOR, not implementation:
- ✅ "Cache expires after fixed time, requires manual refresh"
- ❌ "Cache uses Redis with TTL of 3600s in src/cache/redis.ts"

## Content Rules

| Include | Exclude |
|---------|---------|
| What users can do | File paths |
| Current limitations | Function names |
| Behavior gaps | Code snippets |
| User-facing issues | Technical implementation |

## Examples

**Good baseline:**
```markdown
### Current Behavior
- Password reset sends email with permanent link
- No expiration on reset links
- Users can request multiple resets simultaneously

### Gaps / Limitations
- Links never expire (security risk)
- No rate limiting on reset requests
- No confirmation that email was sent
```

**Bad baseline:**
```markdown
### Current Behavior
- Uses SendGrid API in src/email.ts:45
- resetToken stored in PostgreSQL users table
- Token generated with uuidv4()
```

## Integration with Codebase Mapping

**baseline-discovery.md**: Micro view - behavior relevant to this feature
**codebase-mapping.md**: Macro view - overall codebase structure

They complement each other:
- Use codebase-mapping for general patterns
- Use baseline-discovery for specific feature context
