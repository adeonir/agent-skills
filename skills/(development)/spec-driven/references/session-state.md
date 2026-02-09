# Session State Management

Manage persistent memory across sessions using STATE.md and optional MCP memory bank.

## When to Use

- Recording decisions
- Logging blockers
- Capturing learnings
- Syncing with MCP memory bank

## Process

### Step 1: Load Current State

Read `.specs/project/STATE.md`:

```bash
cat .specs/project/STATE.md
```

### Step 2: Check MCP Memory Bank

If MCP memory bank is available:
- Query for relevant context
- Merge with local STATE.md
- Identify new entries to sync

### Step 3: Update State

Based on user input, update appropriate section:

**Recording a Decision:**

```markdown
| {YYYY-MM-DD} | {Decision} | {Context} |
```

**Logging a Blocker:**

```markdown
| {YYYY-MM-DD} | {Blocker description} | active/resolved |
```

**Capturing a Learning:**

```markdown
| {YYYY-MM-DD} | {Learning} | {Source feature} |
```

### Step 4: Sync to MCP Memory Bank

If MCP available:
- Push new entries to memory bank
- Tag with project context

### Step 5: Save STATE.md

Write updated content back to file.

## State.md Format

```markdown
# State

## Decisions

| Date | Decision | Context |
|------|----------|---------|
| 2024-01-15 | Use JWT for auth | Scalability requirements |

## Blockers

| Date | Blocker | Status |
|------|---------|--------|
| 2024-01-16 | Waiting for API keys | active |

## Learnings

| Date | Learning | Source |
|------|----------|--------|
| 2024-01-14 | Next.js middleware needs special config | 001-auth |
```

## MCP Memory Bank Integration

When available, STATE.md acts as local cache:

1. Query memory bank first
2. Merge with local state
3. Update both sources
4. Local file for portability

## Error Handling

- File not found: Create from template
- MCP unavailable: Use local file only
- Sync conflict: Prioritize newer timestamps
