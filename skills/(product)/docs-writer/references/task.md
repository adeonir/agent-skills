# Task -- Sprint Execution Item

## Workflow

```
drafting (direct)
```

No discovery needed. Tasks are concrete work items where the user already knows what needs to be done. Collect structured fields and draft.

## Process

Ask the user for the task details. If they provide a brief description, fill in reasonable defaults and present for review.

### Required Fields

1. **Title**: What needs to be done (action-oriented, starts with a verb)
2. **Description**: Additional context about the task
3. **Acceptance Criteria**: WHEN/THEN/SHALL conditions for completion

### Optional Fields (ask or use defaults)

4. **Status**: todo / in-progress / done (default: todo)
5. **Priority**: P1 / P2 / P3 (default: P2)
6. **Assignee**: Who is responsible (default: TBD)
7. **Estimate**: Time or story points (default: TBD)
8. **Sprint**: Which sprint or iteration (default: current)
9. **Labels**: Tags for categorization (default: none)
10. **Related Docs**: Links to related issues, stories, or specs

## Drafting

**USE TEMPLATE:** `templates/task.md`

Fill in fields from user input. For optional fields not provided, use defaults. Present draft for review before saving.

## Guidelines

- Task titles should be action-oriented: "Implement...", "Fix...", "Add...", "Update..."
- Acceptance criteria must be verifiable -- someone should be able to check each one as done or not done
- Keep tasks small enough to complete in a single sprint
- If a task is too large, suggest breaking it into subtasks

## Output

Save to: `.specs/docs/task-{name}.md`
