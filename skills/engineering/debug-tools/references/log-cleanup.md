# Log Cleanup

Remove all debug logs after debugging is complete.

## When to Use

When the `[DEBUG]` logs added during a session have to come out of the code.

## Workflow

Resolve `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose that directory, stop and report an environment problem. Run every command from the project root.

### Find Debug Logs

Run `python3 <this-skill>/scripts/debug_logs.py find`. It lists every `[DEBUG]` statement with its full line span, including a call split across lines, and skips dependency and build directories.

### Remove Logs

Run `python3 <this-skill>/scripts/debug_logs.py remove`. It deletes every listed span and reports what is left:

- **Held back** — the statement shares its line with other code, or its brackets never close. Remove the `[DEBUG]` call by hand and leave the surrounding code intact.
- **Near-miss prefix** (`[debug]`, `[DEBUG ]`) — report it and remove it only on user confirmation.

Only `[DEBUG]` statements are in scope; the project's own logging stays untouched, however stray it looks. In generated or compiled output, rebuild instead of editing.

### Verify Removal

Re-run `find`; it exits 0 when no `[DEBUG]` statement is left. Then run the project's syntax or type check when it has one. If either fails, return to Remove Logs.

### Report

Report the files cleaned, how many logs were removed in one to three sentences, and any near-miss prefix left for the user to confirm. Never paste the removed lines.
