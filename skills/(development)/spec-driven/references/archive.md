# Archive

Consolidate feature documentation and cleanup.

## When to Use

- Feature is complete (status: done)
- Ready to document for future reference

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load All Artifacts

Read:
- `spec.md`
- `plan.md`
- `tasks.md`
- `git log` (for implementation notes)

### Step 3: Generate Consolidated Doc

**USE TEMPLATE:** `templates/archive.md`

Generate archive doc following the template structure:
- Summary
- What Was Built
- Technical Decisions
- Implementation Notes
- Lessons Learned

Create at `docs/features/{name}.md` (no ID in filename).

### Step 4: Ask About Cleanup

```
Archive complete. Remove working directory?
- Yes: Delete .artifacts/features/{ID}-{name}/
- No: Keep for reference
```

If yes:
- Remove `.artifacts/features/{ID}-{name}/`

### Step 5: Report

Inform user:
- Archived to: `docs/features/{name}.md`
- Cleanup: {done/kept}

## Guidelines

- Don't archive features with open or in-progress tasks
- Always generate the consolidated doc before cleanup
- Include implementation decisions and lessons learned in the archive
- Don't delete feature directory without user confirmation

## Error Handling

- Not done: Suggest `validate` first
- Docs dir missing: Create
