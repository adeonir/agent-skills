# Vault Structure

Recommended folder structure for the Obsidian vault when using session-notes.

## When to Use

- User asks about "vault structure", "how to organize", "folder setup"
- Setting up a new vault for the first time
- Reorganizing existing vault

## Recommended Structure

```
Vault/
├── Projects/
│   └── Project Name/
│       ├── project.md
│       ├── adr-*.md
│       ├── prd-*.md
│       └── tdd-*.md
├── Companies/
├── Challenges/
├── Brags/
├── Conversations/
├── Daily/
└── Templates/
    ├── project.md
    ├── company.md
    ├── challenge.md
    ├── brag.md
    ├── conversation.md
    ├── capture.md
    └── daily.md
```

## Folder Descriptions

| Folder | Purpose | Example Files |
|--------|---------|---------------|
| `Projects/` | One folder per project (Title Case), `project.md` + related docs | `Project Name/project.md` |
| `Companies/` | Job search tracking | `stripe-2025.md`, `figma-2024.md` |
| `Challenges/` | Interview take-homes | `stripe-system-design.md` |
| `Brags/` | Achievement logs | `2025-brags.md` |
| `Conversations/` | AI conversation notes | `refactoring-auth-flow.md` |
| `Daily/` | Journal entries | `2025-03-03.md` |
| `Templates/` | Templates for manual note creation via Obsidian | `daily.md`, `project.md` |

## Setup Commands

Verify vault and list existing folders:

```bash
# List available vaults
obsidian vaults verbose

# Show vault info
obsidian vault

# List existing folders
obsidian folders

# Verify a specific folder exists
obsidian folder path=Projects
```

Create initial structure by creating a note in each folder:

```bash
# Create a placeholder note in each folder to establish structure
obsidian create path="Projects/.gitkeep.md" content="placeholder"
obsidian create path="Companies/.gitkeep.md" content="placeholder"
obsidian create path="Challenges/.gitkeep.md" content="placeholder"
obsidian create path="Brags/.gitkeep.md" content="placeholder"
obsidian create path="Conversations/.gitkeep.md" content="placeholder"
```

Note: The `Daily/` folder is created automatically by the Daily Notes plugin.

## Alternative Structures

### By Year (for high volume)

```
Daily/
├── 2024/
├── 2025/
Projects/
├── 2024/
└── 2025/
```

### By Status (for many active projects)

```
Projects/
├── active/
│   └── Agent Skills/
└── archived/
    └── Old Project/
```

### Flat (simplest)

```
Vault/
├── Projects/
├── Companies/
├── Challenges/
├── Brags/
├── Conversations/
└── Daily/
```

## Guidelines

**DO:**
- Start simple, add complexity only when needed
- Use consistent naming (kebab-case)
- Keep folder depth shallow (max 2-3 levels)
- Use tags (#tag) for cross-cutting concerns

**DON'T:**
- Over-organize before you have content
- Create folders for single notes
- Use spaces in folder names
- Deep nesting (harder to navigate)

## Linking Strategy

Connect notes using wiki-links:

```markdown
# In Daily note
Worked on [[project-name]] today. See [[stripe-2025]] for context.

# In Company note
Technical challenge: [[stripe-system-design-url-shortener]]

# In Challenge note
Part of interview for [[stripe-2025]]
```

## Templates

Templates live in two places:

1. **Skill repo** (`templates/`) - source of truth, used by the agent to compose content
2. **Vault** (`Templates/`) - copies for manual use via Obsidian's Templates plugin
   and Daily Notes plugin

Configure Obsidian:
- **Settings > Templates > Template folder location**: `Templates`
- **Settings > Daily notes > Template file location**: `Templates/daily`

When templates in the skill repo are updated, sync changes to the vault copies.
The agent should remind the user to update vault templates when it detects
differences between the skill templates and the vault copies.
