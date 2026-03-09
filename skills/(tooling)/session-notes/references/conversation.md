# Conversation Note

Save conversations with AI tools (Claude Code, claude.ai, ChatGPT, Gemini, etc.)
as structured Obsidian notes.

## When to Use

- User says "save conversation", "save this chat", "session summary"
- User wants to record insights from an AI conversation
- End of a productive session worth documenting
- User pastes or describes a conversation from another AI tool

## Workflow

1. **Confirm vault**
   ```bash
   obsidian vaults verbose
   ```

2. **Identify source**
   If running inside Claude Code, assume `claude-code` automatically.
   Otherwise, ask user which tool the conversation is from:
   - `claude-code` - current session (agent has full context)
   - `claude-ai` - user provides content (paste or describe)
   - `chatgpt` - user provides content
   - `gemini` - user provides content
   - `other` - user provides content

3. **Compose the note**
   - For `claude-code`: summarize from the current session context.
     Focus on what was discussed, decisions made, insights, and open questions.
   - For other sources: ask user to paste the conversation or describe
     the key points. Structure the content into the template sections.

4. **Determine destination**
   Ask if the conversation is related to an existing project.
   - If related to a project: save inside the project folder
     - Path: `Projects/{{Project Name}}/{{Topic}}.md`
   - If standalone: save in `Conversations/`
     - Path: `Conversations/{{Topic}}.md`

5. **Generate filename**
   - Title Case: `{{Topic}}.md`
   - Examples:
     - `Landing Page Stack.md` (inside `Projects/Pensefy/`)
     - `React Performance Patterns.md` (inside `Conversations/`)

6. **Check if exists**
   ```bash
   obsidian search query="{{topic}}" path="{{destination folder}}"
   ```
   If a related note exists, ask to append or create new.

7. **Preview and confirm**
   Display the full note content and target file path to the user.
   Ask for confirmation before writing. Accept edits if suggested.

8. **Write note**
   Check if Obsidian CLI is available:
   ```bash
   which obsidian
   ```
   If available, compose content following `templates/conversation.md` structure
   and create with CLI:
   ```bash
   obsidian create path="{{destination folder}}/{{filename}}" content="{{composed content}}" silent
   ```
   If CLI is not available, ask user for the output path on first use,
   then fall back to Write tool to create the file directly.

## Guidelines

**DO:**
- Focus on decisions, insights, and actionable outcomes
- Keep summaries concise (not a transcript)
- Link to related project/daily notes with `[[wikilinks]]`
- Use the correct source tag for searchability

**DON'T:**
- Include the full conversation transcript (summarize instead)
- Assume the conversation source without asking
- Include sensitive information (API keys, credentials, personal data)
- Write without previewing and getting user confirmation first

## Next Steps

- Insights may feed into daily notes
- Decisions may become project documentation or brag entries
