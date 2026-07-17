# Create Transcription Note

Save meeting, 1:1, feedback, course, lecture, or standup transcription notes to the vault. Body content is preserved verbatim.

## When to Use

- User says "transcription", "meeting notes", "1:1 notes", "feedback notes", "standup notes", "lecture notes", "course notes"
- User pastes or shares a transcription from Granola, Otter, or similar
- User wants to save course module notes, workshop notes, or webinar notes

## Vault Resolution

Load [mapping.md](mapping.md) first to resolve vault root via the 3-tier fallback (local symlink → global pointer → bootstrap).

## Workflow

1. **Identify context.** Ask the user what kind of content this is (meeting with client, peer-dev sync, 1:1, feedback session, course, lecture, workshop, webinar, standup).

2. **Receive the transcription.** The user pastes or provides the transcription content. This content is the body of the note and must not be modified, reformatted, summarized, or rewritten. Preserve it exactly as provided.

3. **Compose the note** using the template below. The transcription body replaces `{{verbatim transcription}}`. Generate tags, observations, and relations from the transcription content; the body itself passes through unchanged.

4. **Determine destination.** Ask the user where to save. If unspecified, default to `Meetings/` at the vault root for meeting/1:1/feedback, `Courses/` for course/lecture/workshop content.

5. **Generate filename.** `Description.md` where Description is a short title derived from the content (Title Case, sanitized). No date prefix in the filename — date lives in frontmatter.

6. **Check if exists**

   ```text
   Obsidian:search_notes query="Description" path="{destination}/"
   ```

If a note with the same topic exists, ask to append or create new.

7. **Write note**

   ```text
   Obsidian:write_note path="{destination}/Description.md" content="..." frontmatter={...}
   ```

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{transcription-slug}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources: []
date: {{YYYY-MM-DD}}
context: {{meeting / 1:1 / feedback / standup / lecture / course / workshop / webinar}}
tags:
  - transcription
  - {{context-tag}}
  - {{dynamic tags based on content}}
---
# {{Description}}

{{verbatim transcription — preserve exactly as provided}}

## Observations

- #{{category}} {{insight, decision, tool, or technique mentioned}}

## Relations

- [[{{Related Note}}]]
````

## Guidelines

- Preserve the transcription content exactly as provided
- Generate tags from the transcription content (topics, tools, concepts)
- Generate observations by reading the transcription (key insights, decisions)
- Include source link at the bottom if the user provides one
- Verify wikilinks point to existing notes before adding them

## Anti-Pattern: Editorial Polish

Reformatting, summarizing, or rewriting the transcription destroys its value as a verbatim record. The body is a primary source — observations and tags are derived data layered on top, not replacements.

## Anti-Pattern: Inventing Observations

Observations must come from the transcription content. Do not infer topics, tools, or decisions that were not actually discussed. When the content is sparse, fewer observations is correct.

## Error Handling

- No transcription provided: ask user to paste or share the content
- Ambiguous context: ask user to clarify what kind of content it is
- Destination folder missing: create it on first write
