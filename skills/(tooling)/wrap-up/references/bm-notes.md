# Write Basic Memory Notes

Create session, debrief, and decision notes in Basic Memory. Uses BM MCP
tools directly — no dependency on other skills.

> **LOAD FIRST:** [mapping.md](mapping.md) -- provides BM project and prefix

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
- **Body**: free-form markdown between `# Heading` and `## Observations`.
  Write rich prose — background, motivation, analysis. Search retrieves
  chunks from body prose, so longer substantive context makes notes more
  discoverable.
- The `title` parameter must match the `# Heading` in the content

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
  folder="ventures/pensefy/sessions",
  tags=["tag1", "tag2"],
  content="# Note Title\n\nBody prose...\n\n## Observations\n..."
)
```

### edit_note operations

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
- **Entity exists** → Update with `edit_note`
- **Entity doesn't exist** → Create with `write_note`
- **Unsure** → Read the candidate with `read_note` first, then decide

## Workflow

### 1. Determine paths

Using mapping output (all notes go to BM project `main`):
- Session directory: `{bm_prefix}{project}/sessions/`
- Debrief directory: `{bm_prefix}{project}/debriefs/`
- Decision directory: `{bm_prefix}{project}/decisions/`
- BM project: always `main`

### 2. Check for existing session note

```
search_notes query="YYYY-MM-DD" project="main"
```

If a session note exists for today's work, read it with `read_note`
and merge new information with `edit_note` — add new observations,
update prose. Do not duplicate existing observations. Then proceed
to step 4 (debrief). If no session note exists, create one in step 3.

### 3. Create session note

Body context is free-form markdown between the heading and the
Observations section. Write substantively — background, motivation,
what happened and why. Reasoning and trade-offs belong in the
debrief, not here.

```markdown
# YYYY-MM-DD — Description

Prose context -- what happened and what was done. Facts and outcomes
only, not reasoning or trade-offs (those belong in the debrief).
Rich and substantive, not just bullet points.

## Observations

- [outcome] Key outcome from the session
- [decision] Decision made with rationale
- [convention] Convention established
- [context] Background information

## Relations

- follows [[Previous Session Note]]
```

Write:

```
write_note(
  project="main",
  title="YYYY-MM-DD — Description",
  folder="{bm_prefix}{project}/sessions",
  tags=["session"],
  content="# YYYY-MM-DD — Description\n\n..."
)
```

Rules:
- Observations use `[brackets]`, not `#hashtags`
- One fact per observation, be specific
- Prose body tells the story, observations distill the facts
- Omit empty sections
- **`follows` relation**: list the sessions directory, find the most
  recent note before today's date. If no previous note exists, omit
  the relation

### 4. Create debrief note

Always create a debrief. Call `write_note` directly:

```markdown
# YYYY-MM-DD — What was learned/decided (not the session title)

## Context

Deeper than session note. Include reasoning, trade-offs
considered, discoveries, and context for next session. Free-form
markdown -- this is the heart of the note, write generously:
background, motivation, history, analysis, reasoning, trade-offs.
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

- [summary] 1-3 sentence summary of the session
- [decision] Key decision condensed from Decisions section
- [finding] Key discovery condensed from Findings section
- [problem] Key problem condensed from Problems section

## Relations

- expands [[Session Note Title]]
```

Rules:
- Debrief title must differ from session title -- session describes
  **what was done**, debrief describes **what was learned/decided**
- Example: session `2026-03-25 — Decision Notes and Vault Restructure`,
  debrief `2026-03-25 — Template Consistency and Format Decisions`
- Omit empty sections (no empty Decisions, Findings, etc.)
- Observations condense the sections above into atomic facts
- **`expands` relation**: links to the session note from step 3. If no
  session note was created (no meaningful content), omit the relation
- Focus on reasoning, discoveries, and specifics
- Do not include file lists or obvious info from git history

### 5. Create decision notes (conditional)

If the debrief has a Decisions section with substantive content,
generate decision notes grouped by theme. Decision notes are
**not** 1:1 with sessions -- they are thematic, linked to the
session via `part_of`.

Skip this step if the session had no significant decisions.
Always create a decision note when the session defines a format,
convention, or reusable pattern that other agents need to reference.

```markdown
# Title — Decision Theme

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

Rules:
- Group by theme, not by session (one decision note per subject)
- Context and Decisions sections are required
- Additional sections (tables, comparisons, tiers) as needed
- Search BM first -- scan decision note titles for keyword overlap
  with the current topic. If a match is found, update that note
  instead of creating a new one
- Do not repeat debrief content -- decisions go deeper on the
  specific choice, debrief covers the full session

## Guidelines

**DO:**
- Search before creating with `search_notes` to avoid duplicates
- Call BM MCP tools directly (`mcp__basic-memory__write_note`, etc.)
- Use `[brackets]` for observations (BM format)
- Use `- relation_type [[Target]]` for relations (BM format)
- Link debrief to session note with `expands` relation
- Be detailed in debrief — this is the deep knowledge record
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
- Duplicate content between session and debrief (session is facts,
  debrief is reasoning, paths, and technical specifics)
- Reuse the session title for the debrief — each must have its own
  descriptive title
- Duplicate content between debrief and decision notes (debrief covers
  the session, decision goes deeper on the specific choice)
