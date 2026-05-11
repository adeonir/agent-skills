# Create Project Note

Create structured documentation for a project in the Obsidian vault.

## When to Use

- User says "create project", "new project note", "document project"
- User wants to track project scope or learnings
- Depends on mapping output (`{VaultFolder}` resolution); load
  [mapping.md](mapping.md) first

## Workflow

1. **Gather project info**
   - Project name
   - Brief summary (1-2 sentences)
   - Tech stack

2. **Generate folder and filename**
   - Folder: `{VaultFolder}/{Project Name}/` in Title Case
   - Main file: `{Project Name} Overview.md` (filenames must be unique
     across the vault for Obsidian wikilinks to work)

3. **Check if exists**

   ```
   search_notes query="Checkout Refactor Overview" path="{VaultFolder}/"
   ```

   If exists, ask to append, choose new name, or cancel.

4. **Compose content** using the template below.

5. **Write note**

   ```
   write_note path="{VaultFolder}/Checkout Refactor/Checkout Refactor Overview.md" content="..."
   ```

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-slug}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources: []
stack:
  - {{technology}}
tags:
  - project
  - {{dynamic tags based on content}}
---
# {{Project Name}} Overview

{{What this project is, why it exists, what problem it solves. Include
the constraints, trade-offs, and context that shaped the approach —
enough that someone reading this note later understands the full picture
without needing to ask.}}

## Goals

- {{goal 1}}
- {{goal 2}}

## Learnings

- {{what worked well}}
- {{what didn't work}}
- {{what to remember next time}}

## Observations

- #decision {{key technical or product decision}}
- #stack {{technology choice and rationale}}
- #risk {{known risk or concern}}

## Relations

- [[{{Related Note}}]]
````

Context prose between H1 and Goals is required. Goals is required. All
other sections are optional — include only when the user mentions
relevant content. Omit empty sections.

## Output Path

```
{VaultFolder}/{Project Name}/{Project Name} Overview.md
```

## Guidelines

- Use `search_notes` to check for existing project notes before creating
- Populate Relations only with verified existing notes

## Error Handling

- Project note already exists: ask to append, choose new name, or cancel
- Vault folder unresolved: load [mapping.md](mapping.md), bootstrap if needed
