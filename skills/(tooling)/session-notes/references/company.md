# Create Company Note

Track job applications and interview process for a company.

## When to Use

- User says "document company", "job application", "applied to", "interview with"
- User wants to track status of job applications
- User mentions company names in context of job search

## Workflow

1. **Confirm vault**
   ```bash
   obsidian vaults verbose
   ```

2. **Gather company info**
   - Company name
   - Position/role applied for
   - Application date
   - Current status (applied, screening, interview, offer, rejected)
   - Tech stack (technologies used)

3. **Generate filename**
   - Title Case with year for uniqueness: `{{Company Name}} {{Year}}.md`
   - Example: "Stripe" -> `Stripe 2025.md`

4. **Check if exists**
   ```bash
   obsidian search query="Stripe 2025" path=Companies
   ```

5. **Create or update**
   - If new: create with template
   - If exists: append new row to Timeline table

6. **Preview and confirm**
   Display the full note content (or the new Timeline row to append) and
   target file path to the user. Ask for confirmation before writing.
   Accept edits if suggested.

7. **Write note**
   Check if Obsidian CLI is available:
   ```bash
   which obsidian
   ```
   If available, compose content following `templates/company.md` structure
   and create with CLI:
   ```bash
   obsidian create path="Companies/Stripe 2025.md" content="# Senior Engineer -- Stripe" silent
   ```
   For appending a Timeline row to an existing note:
   ```bash
   obsidian append path="Companies/Stripe 2025.md" content="| 2025-03-18 | Technical | System design, see [[Stripe System Design]] |"
   ```
   Use `open` instead of `silent` if the user wants to see the note in Obsidian immediately.
   If CLI is not available, fall back to Write tool to create the file
   directly at the vault path (ask user for vault path on first use).

## Guidelines

**DO:**
- Update existing company note if re-applying to same company
- Link to challenge notes for interview stages with technical detail
- Track reasons for rejection (if known)
- Create separate challenge notes for technical interview stages

**DON'T:**
- Create duplicate notes for same company + year
- Include sensitive info (recruiter personal contact without permission)
- Assume status - always confirm with user
- Include compensation details (sensitive information)

## Next Steps

- User may want to create challenge note for technical interviews
- User may want to update brag document with learnings
