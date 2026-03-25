# Epic Tracker

Manage the delivery lifecycle from epic planning through story tracking to implementation handoff.

## Installation

```bash
npx skills add adeonir/agent-skills --skill epic-tracker
```

## What It Does

```mermaid
flowchart LR
    D[Discover] -->|check docs| C[Create]
    C -->|epic/story/bug/release| T[Track]
    T -->|update status| H[Handoff]
    H -->|suggest| SD[spec-driven]
```

| Phase | What Happens | Output |
|-------|-------------|--------|
| Discover | Check for existing PRD, brief, or context | Context for artifact creation |
| Create | Generate epic, story, bug, or release | Markdown artifact in `.artifacts/epics/` |
| Track | Update status, show overview | Updated frontmatter |
| Handoff | Suggest spec-driven or tracker sync | User chooses next step |

## Usage

```
"create epic" -- plan a new epic with stories, scope, and acceptance criteria
"create story" -- add a story to an existing epic
"report bug" -- document a defect with reproduction steps and severity
"create release" -- group stories across epics for delivery
"show roadmap" -- display delivery status overview
"mark done" -- update artifact status
"handoff" -- prepare story for spec-driven implementation
```

## Output

```
.artifacts/epics/
├── epic-name/
│   ├── epic.md
│   ├── story-name.md
│   └── bug-name.md
├── standalone/
│   └── bug-name.md
└── releases/
    └── release-name.md
```

## Integration

| Skill | Connection |
|-------|-----------|
| docs-writer | PRD and brief feed epic discovery |
| spec-driven | Stories and bugs feed implementation specs |
| brainstorming | Direction artifacts inform epic planning |
