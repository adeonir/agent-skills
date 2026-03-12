# Create Project Note

Create structured documentation for a project in the Obsidian vault.

## When to Use

- User says "create project", "new project note", "document project"
- User mentions PRD, Design Doc, ADR, or architecture documentation
- User wants to track project decisions, scope, or learnings

## Workflow

1. **Confirm vault**
   ```bash
   obsidian vaults verbose
   ```
   Ask user which vault if multiple exist. Use `vault=<name>` in subsequent
   commands to target the correct vault.

2. **Gather project info**
   - Project name
   - Brief summary (1-2 sentences)
   - Tech stack

3. **Generate folder and filename**
   - Folder: Title Case (e.g., "Checkout Refactor" -> `Projects/Checkout Refactor/`)
   - Main file: always `Overview.md` (avoids redundancy with folder name)
   - Related docs (ADR, PRD, Design Doc): follow docs-writer naming or user-defined

4. **Check if exists**
   ```bash
   obsidian search query="Checkout Refactor" path="Projects/Checkout Refactor"
   ```
   If exists, ask to append, choose new name, or cancel.

5. **Compose content**
   Build the note content following `templates/project.md` structure.
   Populate Documents section only with links that exist or that the user
   wants to create. Populate References with related notes if mentioned.

6. **Preview and confirm**
   Display the full note content and target file path to the user.
   Ask for confirmation before writing. Accept edits if suggested.

7. **Write note**
   Check if Obsidian CLI is available:
   ```bash
   which obsidian
   ```
   If available, create with CLI:
   ```bash
   obsidian create path="Projects/Checkout Refactor/Overview.md" content="{{composed content}}" silent
   ```
   Use `open` instead of `silent` if the user wants to see the note in Obsidian immediately.
   If CLI is not available, fall back to Write tool to create the file
   directly at the vault path (ask user for vault path on first use).

## Next Steps

- User may want to create linked docs (e.g., ADR, Design Doc) via docs-writer skill
- User may want to create a company note if this is for a job application
