# Create Transcription Note

Save meeting, course, lecture, or standup transcription notes to the vault.

## When to Use

- User says "transcription", "meeting notes", "standup notes", "lecture notes"
- User pastes or shares a transcription from Granola, Otter, or similar tools
- User wants to save course module notes, workshop notes, or webinar notes

## Workflow

1. **Identify context**
   Ask the user what kind of content this is (meeting, standup, course, lecture,
   workshop, webinar). Ask one question at a time.

2. **Receive the transcription**
   The user pastes or provides the transcription content. This content is the
   body of the note and must not be modified, reformatted, summarized, or
   rewritten. Preserve it exactly as provided.

3. **Compose the note**
   Use `templates/session.md` as the structural base with these overrides:

   - **Frontmatter**: use `type: transcription` instead of `type: session`.
     Tags are derived from the transcription content
   - **Title (H1)**: `YYYY-MM-DD -- Description` (same as session template)
   - **Body**: paste the transcription content verbatim after the H1. Do not
     add a `## Summary` or any other heading before the transcription content
   - **Observations**: `#category content` entries derived from the
     transcription content -- concepts, decisions, tools, or techniques
     mentioned
   - **Relations**: `[[wikilinks]]` to related notes in the vault -- only if
     they exist. Check before linking

   The agent reads the transcription to generate tags, observations, and
   relations, but never modifies the transcription text itself.

4. **Determine destination**
   Ask the user where to save the note. If the user specifies a path, use it.
   If not, default to `Meetings/` at the vault root.

5. **Generate filename**
   `YYYY-MM-DD -- Description.md` where Description is a short title
   derived from the content (Title Case, sanitized).

6. **Check if exists**
   ```
   search_notes query="Description" path="{destination}/"
   ```
   If a note with the same date and topic exists, ask to append or create new.

7. **Write note**
   ```
   write_note path="{destination}/YYYY-MM-DD -- Description.md" content="..." frontmatter={...}
   ```

## Guidelines

**DO:**
- Preserve the transcription content exactly as provided
- Generate tags from the transcription content (topics, tools, concepts)
- Generate observations by reading the transcription (key insights, decisions)
- Ask one question at a time
- Include source link at the bottom if the user provides one

**DON'T:**
- Edit, reformat, summarize, or rewrite the transcription content
- Add section headings inside the transcription body
- Create observations or tags about topics not present in the transcription

## Error Handling

- No transcription provided: ask user to paste or share the content
- Ambiguous context: ask user to clarify what kind of content it is
- Destination folder missing: create it on first write

## Next Steps

- Transcription insights may feed into daily notes
- Course transcriptions may link to project notes when applying learnings
- Meeting decisions may become decision notes
