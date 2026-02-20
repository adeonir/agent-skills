# Archive

Consolidate feature documentation and cleanup.

## When to Use

- Feature is complete (status: done)
- Ready to document for future reference

## Process

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

### Step 4: Update CHANGELOG.md

Add entry to `.artifacts/project/CHANGELOG.md`:

```markdown
## {YYYY-MM-DD}

### Added

- {User-visible capability from this feature}

### Changed

- {Modified behavior}
```

**No feature IDs in changelog entries.** Use dates only, no spec references.

**Good entries:**
- "Added TOTP-based two-factor authentication"
- "Modified login flow to support optional 2FA"

**Bad entries:**
- "001: Added authentication" (references feature ID)
- "Implemented T001-T005" (references tasks)
- "Added totp.ts file" (implementation detail)

### Step 5: Ask About Cleanup

```
Archive complete. Remove working directory?
- Yes: Delete .artifacts/features/{ID}-{name}/
- No: Keep for reference
```

If yes:
- Remove `.artifacts/features/{ID}-{name}/`
- Update ROADMAP.md status

### Step 6: Report

Inform user:
- Archived to: `docs/features/{name}.md`
- CHANGELOG.md updated
- Cleanup: {done/kept}

## Error Handling

- Not done: Suggest `validate` first
- Docs dir missing: Create
