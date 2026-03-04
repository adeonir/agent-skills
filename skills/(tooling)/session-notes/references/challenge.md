# Create Challenge Note

Document technical challenges from interview processes.

## When to Use

- User says "technical challenge", "take-home", "coding interview", "system design"
- User mentions interview problems or assignments
- User wants to record solutions to technical problems

## Workflow

1. **Confirm vault**
   ```bash
   obsidian vaults verbose
   ```

2. **Gather challenge info**
   - Company (if part of interview process)
   - Challenge type (algorithm, system design, take-home, live coding)
   - Brief description
   - Technologies involved
   - Time constraints
   - Current status (pending, completed, submitted, feedback received)

3. **Generate filename**
   - Descriptive kebab-case: `{{company}}-{{type}}-{{topic}}.md`
   - Examples:
     - `stripe-system-design-url-shortener.md`
     - `algo-binary-tree-traversal.md`
     - `figma-react-component-library.md`

4. **Check if exists**
   ```bash
   obsidian search query="stripe-system-design" path=Challenges
   ```

5. **Compose content**
   Build the note content following `templates/challenge.md` structure.
   Populate References with the company note link if part of an interview
   process. Include any other related notes mentioned by the user.

6. **Preview and confirm**
   Display the full note content and target file path to the user.
   Ask for confirmation before writing. Accept edits if suggested.

7. **Write note**
   Check if Obsidian CLI is available:
   ```bash
   which obsidian
   ```
   If available, compose content and create with CLI:
   ```bash
   obsidian create path="Challenges/stripe-system-design-url-shortener.md" content="{{composed content}}" silent
   ```
   Use `open` instead of `silent` if the user wants to see the note in Obsidian immediately.
   If CLI is not available, fall back to Write tool to create the file
   directly at the vault path (ask user for vault path on first use).

## Guidelines

**DO:**
- Include your solution approach and thought process
- Document what you learned, even if failed
- Note time complexity and space complexity for algorithms (inside Solution section)
- Include diagrams for system design (using mermaid)
- Record feedback received (if any, in Learnings section)

**DON'T:**
- Copy proprietary challenge text verbatim (paraphrase)
- Share solutions publicly without permission
- Skip documenting failed attempts (they're valuable learning)

## Next Steps

- User may want to link to company note
- User may add to brag document if challenge was particularly difficult
