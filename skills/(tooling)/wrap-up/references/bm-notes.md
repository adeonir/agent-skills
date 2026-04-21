# Write Basic Memory Notes

Create session notes in Basic Memory. Uses BM MCP tools directly —
no dependency on other skills.

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

Set `note_type="session"`. Enables native BM filtering by type without
relying on tags alone.

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

## Guidelines

**DO:**
- Search before creating with `search_notes` to avoid duplicates
- Call BM MCP tools directly (`mcp__basic-memory__write_note`, etc.)
- Set `note_type="session"` on every write
- Tag every note as `[session, ...base_tags, ...context_tags]` —
  `base_tags` come from mapping output; `context_tags` are derived
  from the session content (work type, topics)
- Use `[brackets]` for observations (BM format)
- Use `- relation_type [[Target]]` for relations (BM format)
- Use permalinks as `identifier` for `edit_note`
- Capture decisions inline in the session `## Decisions` section with
  `[decision]` observations — thematic discovery happens via observation
  search, not via dedicated notes
- Link to entities in `entities/` when referencing technologies or tools
  (e.g., `uses [[Cloudflare]]`)
- Create new entity notes for technologies that appear in 2+ session notes

**DON'T:**
- Invoke any skill — use BM MCP tools directly
- Use `#hashtags` for observations (that is Obsidian format)
- Use plain `[[wikilinks]]` without relation type (that is Obsidian format)
- Create dedicated decision notes — decisions live inline in sessions
- Write `# Heading` inside `content` — frontmatter already carries the title
