# Create Challenge Note

Document technical challenges from interview processes.

## When to Use

- User says "technical challenge", "take-home", "coding interview", "system design"
- User mentions interview problems or assignments
- User wants to record solutions to technical problems

## Workflow

1. **Gather challenge info**
   - Company (if part of interview process)
   - Brief description
   - Tech stack
   - Time constraints
   - Current status (pending, completed, submitted, feedback received)

2. **Generate folder and filename**
   - Folder: company or context name in Title Case under `Challenges/`
   - Filename: Title Case describing the challenge
   - Pattern: `Challenges/{{Company}}/{{Type Topic}}.md`
   - Examples:
     - `Challenges/Stripe/System Design URL Shortener.md`
     - `Challenges/Algo/Binary Tree Traversal.md`
     - `Challenges/Figma/React Component Library.md`

3. **Check if exists**
   ```
   search_notes query="System Design URL Shortener" path="Challenges/"
   ```

4. **Compose content**
   Build the note content following `templates/challenge.md` structure.
   Populate Relations with the company note link if part of an interview
   process. Include any other related notes mentioned by the user.

5. **Write note**
   ```
   write_note path="Challenges/Stripe/System Design URL Shortener.md" content="..."
   ```

## Guidelines

**DO:**
- Ask one question at a time -- never batch multiple questions
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
