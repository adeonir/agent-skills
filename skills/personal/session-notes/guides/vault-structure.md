# Vault Structure

Recommended folder structure for the Obsidian vault when using session-notes.

## When to Use

- User asks about "vault structure", "how to organize", "folder setup"
- Setting up a new vault for the first time
- Reorganizing existing vault

## Recommended Structure

```
Vault/
├── {VaultFolder}/
│   └── Project Name/
│       ├── Project Name Overview.md
│       └── Sessions/
│           └── YYYY-MM-DD — Description.md
├── Companies/
├── Challenges/
├── Brags/
├── Conversations/
├── Meetings/
└── Daily/
```

## Folder Descriptions

| Folder | Purpose | Example Files |
|--------|---------|---------------|
| `{VaultFolder}/` | One folder per project (Title Case), `{Name} Overview.md` + Sessions/ | `Project Name/Project Name Overview.md` |
| `Companies/` | Job search tracking | `Stripe 2025.md`, `Figma 2024.md` |
| `Challenges/` | Interview take-homes | `Stripe/System Design.md` |
| `Brags/` | Achievement logs | `Brags 2025.md` |
| `Conversations/` | AI conversation notes | `Refactoring Auth Flow.md` |
| `Meetings/` | Transcription notes (meetings, courses, lectures) | `2026-04-02 -- Intro Testes Automatizados.md` |
| `Daily/` | Activity logs | `2025-03-03.md` |

## Setup

Verify vault structure:

```
list_directory path="/"
```

Create initial structure by writing a placeholder note in each folder:

```
write_note path="Companies/.gitkeep.md" content="placeholder"
write_note path="Challenges/.gitkeep.md" content="placeholder"
write_note path="Brags/.gitkeep.md" content="placeholder"
write_note path="Conversations/.gitkeep.md" content="placeholder"
```

Project folders are created on demand when the first note is written.
The vault folder depends on the project category (see wrap-up mapping table).

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
├── Meetings/
└── Daily/
```

## Guidelines

**DO:**
- Start simple, add complexity only when needed
- Use consistent naming (Title Case)
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
Worked on [[Project Name]] today. See [[Stripe 2025]] for context.

# In Company note
Technical challenge: [[System Design URL Shortener]]

# In Challenge note
Part of interview for [[Stripe 2025]]
```

