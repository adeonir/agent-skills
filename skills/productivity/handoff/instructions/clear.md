# Clear Handoff

Empty `.artifacts/HANDOFF.md` so the next session starts without prior context.

## Workflow

1. If `.artifacts/HANDOFF.md` is absent, return no output.
2. Write empty content to the file. Never delete it — an empty file reads as missing on the next load, and writing avoids a Bash permission prompt.
3. Report that the handoff was cleared.
