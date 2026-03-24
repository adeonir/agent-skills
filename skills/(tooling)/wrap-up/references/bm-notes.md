# Write Basic Memory Notes

Create session and debrief notes in Basic Memory.

> **LOAD FIRST:** [mapping.md](mapping.md) -- provides BM project and prefix

## When to Use

- When the resolved BM project is not `--`
- Runs after auto-memory, before Obsidian notes

## Workflow

### 1. Determine paths

Using mapping output:
- Session directory: `{bm_prefix}{project}/sessions/`
- Debrief directory: `{bm_prefix}{project}/debriefs/`
- BM project: from mapping table

### 2. Check for existing session note

Search BM for a session note with today's date and similar topic:

```
search_notes query="YYYY-MM-DD" project="{bm_project}"
```

If a session note exists for today's work, skip to step 4 (debrief).
If no session note exists, create one in step 3.

### 3. Create session note

Use `write_note` with the BM standard format:

```markdown
# YYYY-MM-DD — Description

Prose context -- background, motivation, what happened and why.
Rich and substantive, not just bullet points.

## Observations

- [outcome] Key outcome from the session
- [decision] Decision made with rationale
- [convention] Convention established
- [context] Background information

## Relations

- follows [[Previous Session Note]]
```

Rules:
- Observations use `[brackets]`, not `#hashtags`
- One fact per observation, be specific
- Prose body tells the story, observations distill the facts
- Omit empty sections

### 4. Create debrief note

Always create a debrief. Use `write_note` with extended format:

**USE TEMPLATE:** `templates/debrief.md`

```markdown
# YYYY-MM-DD — Description

Prose context -- deeper than session note. Include reasoning,
trade-offs considered, discoveries, and context for next session.

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
- [decision] Key decisions (condensed from Decisions section)
- [finding] Key discoveries (condensed from Findings section)
- [problem] Key problems (condensed from Problems section)

## Relations

- expands [[YYYY-MM-DD — Session Note Title]]
```

Rules:
- Omit empty sections (no empty Decisions, Findings, etc.)
- Observations condense the sections above into atomic facts
- The `expands` relation links to the session note from step 3
- Focus on reasoning, discoveries, and specifics
- Do not include file lists or obvious info from git history

## Guidelines

**DO:**
- Search before creating to avoid duplicates
- Use BM skills (write_note, search_notes, edit_note)
- Link debrief to session note with `expands` relation
- Be detailed in debrief -- this is the deep knowledge record

**DON'T:**
- Use #hashtags in observations (BM uses [brackets])
- Create a debrief if the session had no meaningful content
- Duplicate content between session and debrief (session is facts, debrief is reasoning)
