# Create Project Note

Create structured documentation for a project in the Obsidian vault.

## When to Use

- User says "create project", "new project note", "document project"
- User mentions PRD, Design Doc, ADR, or architecture documentation
- User wants to track project decisions, scope, or learnings

## Workflow

1. **Gather project info**
   - Project name
   - Brief summary (1-2 sentences)
   - Tech stack

2. **Generate folder and filename**
   - Folder: Title Case (e.g., "Checkout Refactor" -> `Projects/Checkout Refactor/`)
   - Main file: always `Overview.md` (avoids redundancy with folder name)
   - Related docs (ADR, PRD, Design Doc): follow docs-writer naming or user-defined

3. **Check if exists**
   ```
   search_notes query="Checkout Refactor" path="Projects/"
   ```
   If exists, ask to append, choose new name, or cancel.

4. **Compose content**
   Build the note content following `templates/project.md` structure.
   Populate Documents section only with links that exist or that the user
   wants to create. Populate References with related notes if mentioned.

5. **Write note**
   ```
   write_note path="Projects/Checkout Refactor/Overview.md" content="..."
   ```

## Next Steps

- User may want to create linked docs (e.g., ADR, Design Doc) via docs-writer skill
- User may want to create a company note if this is for a job application
