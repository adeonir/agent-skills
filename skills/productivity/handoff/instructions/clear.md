# Clear Handoff

Empty `.artifacts/HANDOFF.md` so the next session starts without prior context.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Check the file exists
- [ ] Step 2: Empty the file
- [ ] Step 3: Report
```

**Step 1. Check the file.** If `.artifacts/HANDOFF.md` is absent, return no output and stop. Done when the file is confirmed present, or nothing is returned.

**Step 2. Empty.** Write empty content to the file. Never delete it — an empty file reads as missing on the next load, and writing avoids a Bash permission prompt. Done when the file exists and holds no content.

**Step 3. Report.** Report the path and that the handoff was cleared. Done when the report names the path.
