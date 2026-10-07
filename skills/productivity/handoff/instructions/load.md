# Load Handoff

Read the consolidated `.artifacts/HANDOFF.md` so the current session resumes with prior context.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Check the file exists and holds content
- [ ] Step 2: Read the whole file
- [ ] Step 3: Check load-bearing claims
- [ ] Step 4: Report
```

**Step 1. Check the file.** If `.artifacts/HANDOFF.md` is absent or empty, report that no handoff exists and stop. Done when the file holds content, or the absence is reported.

**Step 2. Read.** Read the whole file into working context. Flag a missing `Focus` or `Current state`, then continue with the available context. Done when the whole file is read and every missing required section is flagged.

**Step 3. Check claims.** Check load-bearing claims against current evidence before acting, starting with those marked `unverified`. Treat a claim you could not check as unverified. Done when each load-bearing claim is confirmed, corrected, or treated as unverified.

**Step 4. Report.** Report `Focus` and the relevant current state, constraints, and open threads, and the next action inferred from them; never require a prescribed next step. Never print the handoff in full unless asked — reading it already puts it in context. Done when the report carries the focus, the claims that failed the check, the open threads, and the inferred next action.
