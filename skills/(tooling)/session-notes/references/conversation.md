# Conversation Note

Save conversations with AI tools as structured Obsidian notes with prose context.

## When to Use

- User says "save conversation", "save this chat", "session summary"
- User wants to record insights from an AI conversation
- End of a productive session worth documenting
- User pastes or describes a conversation from another AI tool

## Workflow

1. **Identify source**
   If running inside Claude Code, assume `claude-code` automatically.
   Otherwise, ask user which tool the conversation is from.
   Ask one question at a time -- never batch source and destination together.

2. **Compose the note**
   Write in prose -- capture the reasoning and context behind decisions,
   not a transcript. The note should read naturally weeks later.

   - **Body**: rich prose paragraph(s) explaining what was discussed, why it
     mattered, and what came out of it
   - **Key Decisions**: prose describing each decision and its rationale
   - **Insights**: prose describing findings, learnings, or realizations
   - **Open Questions**: bullet list of unresolved items
   - **Observations**: `#category content` syntax for Obsidian indexing
   - **Relations**: `[[wikilinks]]` to related notes -- omit if none exist

   For `claude-code`: compose from the current session context.
   For other sources: ask user to paste or describe key points.

3. **Determine destination**
   Ask if the conversation relates to an existing project.
   - Related to project: `Projects/{{Project Name}}/{{Topic}}.md`
   - Standalone: `Conversations/{{Topic}}.md`

4. **Generate filename**
   Title Case: `{{Topic}}.md`

5. **Check if exists**
   ```
   search_notes query="{{topic}}" path="{{destination folder}}"
   ```
   If related note exists, ask to append or create new.

6. **Write note**
   ```
   write_note path="{{destination}}/{{Topic}}.md" content="..."
   ```

## Guidelines

**DO:**
- Write prose, not bullet dumps -- decisions and insights deserve context
- Focus on reasoning and outcomes, not a play-by-play
- Link to related project/daily notes with `[[wikilinks]]`
- Include source in frontmatter for searchability

**DON'T:**
- Include the full conversation transcript (summarize in prose)
- Assume the conversation source without asking
- Include sensitive information (API keys, credentials, personal data)
- Write bullet-only notes without prose context

## Next Steps

- Insights may feed into daily notes
- Decisions may become project documentation or brag entries
