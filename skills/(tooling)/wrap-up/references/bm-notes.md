# Write Basic Memory Notes

Create session, debrief, and decision notes in Basic Memory.

> **LOAD FIRST:** [mapping.md](mapping.md) -- provides BM project and prefix

## When to Use

- When the resolved BM project is not `--`
- Runs after auto-memory, before Obsidian notes

## Workflow

### 1. Determine paths

Using mapping output:
- Session directory: `{bm_prefix}{project}/sessions/`
- Debrief directory: `{bm_prefix}{project}/debriefs/`
- Decision directory: `{bm_prefix}{project}/decisions/`
- BM project: from mapping table

### 2. Check for existing session note

Search BM for a session note with today's date and similar topic:

```
search_notes query="YYYY-MM-DD" project="{bm_project}"
```

If a session note exists for today's work, read it and merge new
information — add new observations, update prose. Do not duplicate
existing observations. Then proceed to step 4 (debrief).
If no session note exists, create one in step 3.

### 3. Create session note

Use `write_note` following the memory-notes skill format (no
template in wrap-up -- the example below is format guidance):

The body context is free-form markdown between the heading and
the Observations section. Write substantively -- background,
motivation, what happened and why. Reasoning and trade-offs
belong in the debrief, not here.

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

Rules:
- Observations use `[brackets]`, not `#hashtags`
- One fact per observation, be specific
- Prose body tells the story, observations distill the facts
- Omit empty sections
- **`follows` relation**: list the sessions directory, find the most
  recent note before today's date. If no previous note exists, omit
  the relation

### 4. Create debrief note

Always create a debrief. Use `write_note` with extended format:

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
- Search before creating to avoid duplicates
- Use BM skills (write_note, search_notes, edit_note)
- Link debrief to session note with `expands` relation
- Be detailed in debrief -- this is the deep knowledge record
- Update existing decision notes when the theme already exists
- Create decision notes for any format, convention, or reusable pattern -- if another agent may need this information, it must exist as its own reference

**DON'T:**
- Use #hashtags in observations (BM uses [brackets])
- Duplicate content between session and debrief (session is facts, debrief is reasoning, paths, and technical specifics)
- Reuse the session title for the debrief -- each must have its own descriptive title
- Duplicate content between debrief and decision notes (debrief covers the session, decision goes deeper on the specific choice)
