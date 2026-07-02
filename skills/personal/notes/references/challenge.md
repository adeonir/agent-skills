# Create Challenge Note

Document technical challenges from interview processes.

## When to Use

- User says "technical challenge", "take-home", "coding interview",
  "system design"
- User mentions interview problems or assignments
- User wants to record solutions to technical problems

## Vault Resolution

Load [mapping.md](mapping.md) first to resolve vault root via the 3-tier
fallback (local symlink → global pointer → bootstrap).

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

4. **Compose content** using the template below.

5. **Write note**

   ```
   write_note path="Challenges/Stripe/System Design URL Shortener.md" content="..."
   ```

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{challenge-slug}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: {{pending / completed / submitted / feedback-received}}
sources: []
company: {{company}}
stack:
  - {{technology}}
tags:
  - challenge
  - interview
  - {{dynamic tags based on content}}
---
# {{Challenge Description}}

{{What the challenge was about, the constraints (time, tools, scope),
and the environment. Include the initial reaction and how the problem
was framed before diving in. Paraphrase — do not copy proprietary
challenge text verbatim.}}

## Approach

{{How the problem was approached — thought process, trade-offs considered}}

## Solution

{{The solution — code, architecture, diagrams (mermaid)}}

## Learnings

- {{what was learned}}
- {{what could be done differently}}

## Observations

- #technique {{approach or pattern used}}
- #complexity {{time/space complexity if algorithmic}}
- #feedback {{feedback received, if any}}
- #lesson {{key takeaway}}

## Relations

- [[{{Related Note}}]]
````

## Guidelines

- Include the solution approach and thought process
- Document what was learned, even from failures
- Note time and space complexity for algorithms (inside Solution section)
- Include diagrams for system design (using mermaid)
- Record feedback received in the Learnings section
- Paraphrase proprietary challenge text — never copy verbatim

## Anti-Pattern: Skipping Failed Attempts

Failed challenges contain the most useful learnings — they reveal which
assumptions broke and what would be tried differently. Documenting only
successes turns the brag/challenge log into a vanity record. Capture
both.
