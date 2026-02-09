# Session State Management

Manage persistent memory across sessions using STATE.md.

## When to Use

- Recording decisions
- Logging blockers
- Capturing learnings
- Syncing with persistent storage

## Process

### Step 1: Load Current State

Read `.specs/project/STATE.md`.

### Step 2: Load Existing Context

If persistent storage is available (memory files, project context, prior session data):
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

### Step 4: Sync to Persistent Storage

If persistent storage is available:
- Push new entries
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

## Persistent Storage Integration

When available, STATE.md acts as local cache:

1. Query persistent storage first
2. Merge with local state
3. Update both sources
4. Local file ensures portability

## Error Handling

- File not found: Create from template
- Storage unavailable: Use local file only
- Sync conflict: Prioritize newer timestamps
