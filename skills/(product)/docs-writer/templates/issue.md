---
name: {{issue-name}}
subtype: {{bug/enhancement/chore/spike}}
status: open
priority: {{critical/high/medium/low}}
severity: {{blocker/major/minor/trivial -- bugs only}}
reporter: {{reporter}}
assignee: {{assignee}}
labels: {{labels}}
created: {{YYYY-MM-DD}}
---

# Issue: {{Title}}

## Description

{{Clear description of the issue. What is happening? What should be happening?}}

## Steps to Reproduce *(bugs only)*

1. {{First action that leads to the issue}}
2. {{Next step in the reproduction flow}}
3. {{Final step where the issue manifests}}

**Expected Behavior:** {{What should happen according to the spec or user expectation}}

**Actual Behavior:** {{What actually happens, including any error messages}}

## Environment *(bugs only)*

| Field | Value |
|-------|-------|
| Browser | {{e.g., Chrome 122}} |
| OS | {{e.g., macOS 15}} |
| Device | {{e.g., Desktop / iPhone 15}} |
| Version | {{App version or commit hash}} |
| Environment | {{Production / Staging / Local}} |

## Screenshots / Logs

{{Attach screenshots, screen recordings, or relevant log output}}

```
{{Error logs or stack trace if applicable}}
```

## Impact

{{Who is affected? How many users? What is the business impact?}}

## Proposed Solution *(if known)*

{{Describe the proposed fix or enhancement approach, or "To be investigated"}}

## Acceptance Criteria

- [ ] {{Condition that must be true for this issue to be considered resolved}}
- [ ] {{Another verifiable condition}}

## Related

- **Related Issues:** {{Links to related issues, or "None"}}
- **User Story:** {{Link to parent story, or "None"}}
- **PR:** {{Link to fix PR, or "Pending"}}
