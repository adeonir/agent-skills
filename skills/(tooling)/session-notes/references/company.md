# Create Company Note

Track job applications and interview process for a company.

## When to Use

- User says "document company", "job application", "applied to", "interview with"
- User wants to track status of job applications
- User mentions company names in context of job search

## Workflow

1. **Gather company info**
   - Company name
   - Position/role applied for
   - Application date
   - Current status (applied, screening, interview, offer, rejected)
   - Tech stack (technologies used)

2. **Generate filename**
   - Title Case with year for uniqueness: `{{Company Name}} {{Year}}.md`
   - Example: "Stripe" -> `Stripe 2025.md`

3. **Check if exists**
   ```
   search_notes query="Stripe 2025" path="Companies/"
   ```

4. **Create or update**
   - If new: compose content following `templates/company.md` structure
   - If exists: read with `read_note`, then append new Timeline row with `patch_note`

5. **Write note**
   New note:
   ```
   write_note path="Companies/Stripe 2025.md" content="..."
   ```
   Append Timeline row:
   ```
   read_note path="Companies/Stripe 2025.md"
   patch_note path="Companies/Stripe 2025.md" oldString="..." newString="..."
   ```

## Guidelines

**DO:**
- Update the existing company note when re-applying to the same company
- Link to challenge notes for interview stages with technical detail
- Track reasons for rejection (if known)
- Create separate challenge notes for technical interview stages
- Confirm application status with the user before recording it
- Redact sensitive info (recruiter contact, compensation) unless the user explicitly consents

**DON'T:**
- Create duplicate notes for the same company + year (contrasts: update existing note)
- Include sensitive info like recruiter contact or compensation without permission (contrasts: redact unless user consents)
- Assume application status (contrasts: confirm with the user)

## Next Steps

- User may want to create challenge note for technical interviews
- User may want to update brag document with learnings
