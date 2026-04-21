# Write Basic Memory Notes

Create session and decision notes in Basic Memory. Uses BM MCP tools
directly — no dependency on other skills.

> **LOAD FIRST:** [mapping.md](mapping.md) -- provides BM project, BM path, and base tags

## When to Use

- When the resolved BM project is not `--`
- Runs after auto-memory, before Obsidian notes

## BM Syntax Rules

Basic Memory uses a distinct format from Obsidian. Do not mix them.

- **Observations**: `- [category] content #optional-tag` (brackets, not hashtags)
  - Category is arbitrary — any descriptive label in `[...]`
  - One fact per observation; be specific
  - Hashtags are optional metadata for cross-cutting concerns
- **Relations**: `- relation_type [[Target Note]]` (typed verb + wikilink)
  - Common types: `implements`, `requires`, `relates_to`, `part_of`,
    `extends`, `depends_on`, `replaces`, `contrasts_with`, `follows`,
    `expands`, `pairs_with`, `inspired_by`
  - Custom types are fine (snake_case by convention)
- **Frontmatter**: generated automatically by `write_note` from
  parameters — do not write it manually in the content string
- **Body**: free-form markdown. Write rich prose — background, motivation,
  analysis. Search retrieves chunks from body prose, so longer substantive
  context makes notes more discoverable.

## BM Tools

Call these directly — do not invoke any skill.

| Tool | Purpose |
|------|---------|
| `mcp__basic-memory__write_note` | Create new note (auto-generates frontmatter) |
| `mcp__basic-memory__edit_note` | Append, prepend, or find_replace in existing note |
| `mcp__basic-memory__read_note` | Read existing note before editing |
| `mcp__basic-memory__search_notes` | Search-before-create with query variations |
| `mcp__basic-memory__move_note` | Reorganize notes between directories |
| `mcp__basic-memory__build_context` | Traverse relations via `memory://` URLs |

### write_note signature

```
write_note(
  project="main",
  title="Note Title",
  directory="work/acme/sessions",
  note_type="session",
  tags=["tag1", "tag2"],
  content="Body prose...\n\n## Observations\n..."
)
```

Set `note_type` to match the note's role (`session`, `decision`). Enables
native BM filtering by type without relying on tags alone.

### edit_note operations

- `identifier`: permalink of the target note
  (e.g. `work/acme/sessions/2026-04-20-description`)
- `operation="append"` with `section="Observations"` adds a new observation
- `operation="find_replace"` with `find_text` / `content` updates in place
- `operation="prepend"` inserts at the top

### Search Before Create

Always search first. Duplicates fragment the knowledge graph.

Try multiple query variations (full name, abbreviations, keywords):

```
search_notes(query="2026-04-16", project="main")
search_notes(query="wrap-up refactor", project="main")
```

Decision tree:
- **Entity exists** → Update with `edit_note` using the permalink
- **Entity doesn't exist** → Create with `write_note`
- **Unsure** → Read the candidate with `read_note` first, then decide

## Workflow

### 1. Determine paths

Using mapping output:
- BM project: `bm.project` (typically `main`)
- Session directory: `{bm.path}/sessions/`
- Decision directory: `{bm.path}/decisions/`
- Base tags: `tags` (applied to every note, plus the note-type tag)

### 2. Check for existing session note

```
search_notes query="YYYY-MM-DD" project="{bm.project}"
```

If a session note exists for today's work, read it with `read_note` and
merge new information with `edit_note` using the permalink as identifier —
add new observations, update prose. Do not duplicate existing observations.
Otherwise create a new one in step 3.

### 3. Create session note

One note per session, carrying both facts and reasoning. Body prose is
free-form markdown above the structured sections. Write substantively —
background, motivation, what happened and why, trade-offs considered,
discoveries, and context for the next session.

```markdown
Prose context -- background, motivation, what happened and why, trade-offs,
discoveries, and reasoning. Free-form markdown, rich and substantive.
Include file paths, directory names, and technical specifics here.

## Decisions

- Decision + rationale + alternatives rejected

## Findings

- Technical discovery with specifics (values, edge cases, errors)

## Problems

- Problem + root cause + fix applied

## Next Context

- Unfinished work, next steps, blockers for next session

## Observations

- [outcome] Key outcome from the session
- [decision] Key decision condensed from Decisions section
- [finding] Key discovery condensed from Findings section
- [problem] Key problem condensed from Problems section
- [convention] Convention established
- [context] Background information

## Relations

- follows [[Previous Session Note]]
```

Write:

```
write_note(
  project="{bm.project}",
  title="YYYY-MM-DD — Description",
  directory="{bm.path}/sessions",
  note_type="session",
  tags=["session", ...base_tags, ...context_tags],
  content="Prose context...\n\n## Decisions\n..."
)
```

Rules:
- Observations use `[brackets]`, not `#hashtags`
- One fact per observation, be specific
- Prose body tells the story, observations distill the facts
- Omit empty sections (no empty Decisions, Findings, etc.)
- **`follows` relation**: list the sessions directory, find the most
  recent note before today's date. If no previous note exists, omit
  the relation
- Do not include file lists or obvious info from git history

### 4. Create decision notes (conditional)

If the session has a Decisions section with substantive content,
generate decision notes grouped by theme. Decision notes are
**not** 1:1 with sessions -- they are thematic, linked to the
session via `part_of`.

Skip this step if the session had no significant decisions.
Always create a decision note when the session defines a format,
convention, or reusable pattern that other agents need to reference.

```markdown
## Context

Free-form markdown -- this is the heart of the note, write
generously: background, motivation, history, analysis, reasoning,
trade-offs. What prompted this decision and why it matters.

## Decisions

### 1. Decision title

Justification with rationale embedded. Include alternatives
rejected and why. Add subsections, tables, or comparisons
as complexity demands.

## Observations

- [decision] Key decision condensed from Decisions section
- [rationale] Why this was chosen over alternatives
- [constraint] Limitation that influenced the decision

## Relations

- part_of [[Session Note Title]]
```

Write:

```
write_note(
  project="{bm.project}",
  title="Title — Decision Theme",
  directory="{bm.path}/decisions",
  note_type="decision",
  tags=["decision", ...base_tags, ...context_tags],
  content="## Context\n\n..."
)
```

Rules:
- Group by theme, not by session (one decision note per subject)
- Context and Decisions sections are required
- Additional sections (tables, comparisons, tiers) as needed
- Search BM first -- scan decision note titles for keyword overlap
  with the current topic. If a match is found, update that note
  via `edit_note` with its permalink instead of creating a new one
- Do not repeat full session content -- decisions go deeper on the
  specific choice, session covers the full context

## Guidelines

**DO:**
- Search before creating with `search_notes` to avoid duplicates
- Call BM MCP tools directly (`mcp__basic-memory__write_note`, etc.)
- Set `note_type` on every write (`session`, `decision`)
- Tag every note as `[note-type, ...base_tags, ...context_tags]` —
  `note-type` is one of `session`, `decision`; `base_tags` come from
  mapping output; `context_tags` are derived from the session content
  (work type, topics)
- Use `[brackets]` for observations (BM format)
- Use `- relation_type [[Target]]` for relations (BM format)
- Use permalinks as `identifier` for `edit_note`
- Update existing decision notes when the theme already exists
- Create decision notes for any format, convention, or reusable pattern —
  if another agent may need this information, it must exist as its own reference
- Link to entities in `entities/` when referencing technologies or tools
  (e.g., `uses [[Cloudflare]]`)
- Create new entity notes for technologies that appear in 2+ decision/session notes

**DON'T:**
- Invoke any skill — use BM MCP tools directly
- Use `#hashtags` for observations (that is Obsidian format)
- Use plain `[[wikilinks]]` without relation type (that is Obsidian format)
- Duplicate content between session and decision notes (session covers
  the full event, decision goes deeper on the specific choice)
- Write `# Heading` inside `content` — frontmatter already carries the title
