# Roadmap Management

Manage project roadmap and feature planning.

## When to Use

- Planning upcoming features
- Prioritizing work
- Updating feature status

## Process

### Step 1: Load Current Roadmap

Read `.artifacts/project/ROADMAP.md`.

### Step 2: Parse Input

User may want to:
- Add new feature to roadmap
- Update feature priority
- Move feature between sprint/backlog
- Update feature status

### Step 3: Update Roadmap

**Add feature:**

```markdown
| {name} | planned | {P1/P2/P3} |
```

**Update status:**
- planned → in-progress → done

### Step 4: Save

Write updated ROADMAP.md.

### Step 5: Report

Show current roadmap summary.

## Roadmap Format

```markdown
# Roadmap

## Current Sprint

| Feature | Status | Priority |
|---------|--------|----------|
| auth | in-progress | P1 |

## Backlog

| Feature | Priority |
|---------|----------|
| payments | P1 |
| notifications | P2 |
```

## Error Handling

- Roadmap not found: Create from template
- Invalid priority: Suggest P1/P2/P3
