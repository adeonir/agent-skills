# Notes

Structured note creation for Obsidian.

## What It Does

```mermaid
flowchart TD
    T[User Request] --> D{Note Type}
    D -->|Project| P[Create Project Note]
    D -->|Challenge| H[Create Challenge Note]
    D -->|Brag| B[Update Brag Document]
    D -->|Transcription| TR[Save Transcription]
    D -->|Company| CO[Track Company]
    P --> M[Obsidian CLI]
    H --> M
    B --> M
    TR --> M
    CO --> M
    M --> N[Note in Vault]
```

| Note Type | Output |
|-----------|--------|
| Project | Full project documentation (overview, goals, architecture) in `<obsidian.path>/<Project Name>/<Project Name> Overview.md` |
| Challenge | Technical interview challenge (take-home, system design) in `Challenges/<Company>/<Type Topic>.md` |
| Brag | Achievement tracking for performance reviews in `Brags/YYYY.md` or `Brags/YYYY Qn.md` |
| Transcription | Meeting, 1:1, feedback session, lecture, or course in `Meetings/<Description>.md` or `Courses/<Description>.md` |
| Company | Job application tracking (timeline, status, decision) in `Companies/<Company>/<Role> — <Company>.md` |

## Usage

```text
create project note for checkout-refactor
record technical challenge from Stripe interview
add brag: reduced latency by 40%
save transcription from yesterday's 1:1
track company application — Stripe Senior Frontend
```

## Output

Notes are created in the Obsidian vault following this structure:

```text
Vault/
├── <obsidian.path>/
│   └── <Project Name>/
│       └── <Project Name> Overview.md
├── Challenges/
├── Brags/
├── Meetings/
├── Courses/
└── Companies/
```

## Requirements

- Obsidian desktop app with its built-in CLI (`obsidian`). The CLI works only while the app runs. The Obsidian MCP server is the fallback when the CLI binary is missing or the app is closed; a plain file write into the vault is the last resort when both channels are unavailable. The skill never opens the app or focuses its window.
- Python 3, standard library only, for the bundled scripts
- An Obsidian vault. On the first project note in a repo the skill creates the registry at `~/.config/wrap-up/projects.yml` when absent and asks for the project entry.

## FAQ

**Q: How do filenames handle special characters?** A: Characters the OS rejects or Obsidian links break on (`/ \ : * ? " < > | # ^ [ ] %`) are removed. Accented characters are kept. All filenames are Title Case.

**Q: What if a note with the same name exists?** A: The skill detects duplicates via the vault search and asks whether to append, choose a new name, or cancel.

**Q: Can the skill update existing notes?** A: Yes. Read + patch updates existing notes in place. Templates apply only to new note creation.

**Q: Does it open or focus the Obsidian app?** A: No. When the app is closed, the skill writes through the Obsidian MCP server instead of the CLI.

**Q: How are wikilinks validated?** A: Before adding a wikilink, the skill verifies the target file exists. Orphan wikilinks (pointing to missing files) create empty files at the vault root and are avoided.
