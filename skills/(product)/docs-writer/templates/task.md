---
name: {{task-name}}
type: task
status: todo
priority: {{critical/high/medium/low}}
assignee: {{assignee}}
estimate: {{hours or story points}}
due_date: {{YYYY-MM-DD}}
parent: {{link to user story, epic, or issue}}
---

# Task: {{Title}}

## Description

{{Clear description of what needs to be done and why. Be specific and actionable.}}

## Subtasks

- [ ] {{First discrete unit of work}}
- [ ] {{Next step in the implementation}}
- [ ] {{Final step to complete the task}}

## Technical Details

{{Implementation details, relevant files, approach, or patterns to follow}}

### Files to Modify

- `{{path/to/file}}` -- {{What to change and why}}
- `{{path/to/file}}` -- {{What to change and why}}

### Approach

1. {{First implementation step}}
2. {{Next step building on the previous}}
3. {{Final step to complete the approach}}

## Acceptance Criteria

- [ ] **Given** {{precondition}}, **When** {{action}}, **Then** {{expected result}}
- [ ] **Given** {{precondition}}, **When** {{action}}, **Then** {{expected result}}

## Dependencies

- {{Blocker or prerequisite that must be resolved first, or "None"}}

## Notes

{{Any additional context, edge cases, or things to watch out for}}

## Related

- **Story:** {{Link to parent user story, or "None"}}
- **Issue:** {{Link to related issue, or "None"}}
- **PR:** {{Link to implementation PR, or "Pending"}}
