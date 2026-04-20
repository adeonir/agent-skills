# Create Project Note

Create structured documentation for a project in the Obsidian vault.

## When to Use

- User says "create project", "new project note", "document project"
- User wants to track project scope or learnings

## Workflow

1. **Gather project info**
   - Project name
   - Brief summary (1-2 sentences)
   - Tech stack

2. **Generate folder and filename**
   - Folder: `{VaultFolder}/{Project Name}/` in Title Case
   - The vault folder depends on the project category. Load
     [mapping.md](mapping.md) to resolve it.
   - Main file: `{Project Name} Overview.md` (filenames must be unique across the
     vault for Obsidian wikilinks to work)

3. **Check if exists**
   ```
   search_notes query="Checkout Refactor Overview" path="{VaultFolder}/"
   ```
   If exists, ask to append, choose new name, or cancel.

4. **Compose content**
   Build the note content following `templates/project.md` structure.
   Populate Relations with related notes if mentioned.

5. **Write note**
   ```
   write_note path="{VaultFolder}/Checkout Refactor/Checkout Refactor Overview.md" content="..."
   ```

## Content Structure

Context prose between H1 and Goals is required. Goals is required. All other
sections are optional -- include only when the user mentions relevant content.
Omit empty sections.

## Output Path

```
{VaultFolder}/{Project Name}/{Project Name} Overview.md
```

The `{VaultFolder}` depends on the project category. Load
[mapping.md](mapping.md) to resolve it.

## Guidelines

**DO:**
- Use `search_notes` to check for existing project notes before creating

**DON'T:**
- Create duplicate project notes
- Populate sections with placeholder content

## Next Steps

- User may want to create a company note if this is for a job application
