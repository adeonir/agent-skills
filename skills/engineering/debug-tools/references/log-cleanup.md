# Log Cleanup

Remove all debug logs after debugging is complete.

## When to Use

When the `[DEBUG]` logs added during a session have to come out of the code.

## Workflow

Resolve `<this-skill>` to the directory the `SKILL.md` was read from; if the host does not expose that directory, stop and report an environment problem. Run every command from the project root.

### Find Debug Logs

Run `python3 <this-skill>/scripts/debug_logs.py find`. It lists removable `[DEBUG]` log calls, held marker candidates, and near-miss prefixes, including calls split across lines. It skips dependency and build directories.

### Remove Logs

Run `python3 <this-skill>/scripts/debug_logs.py remove`. It removes only recognized, standalone parenthesized calls: JavaScript/TypeScript `console` logging methods, Python `print`, Go `fmt.Print` variants, Rust `println!` and `eprintln!`, and Ruby `puts`. It reports what is left:

- **Held back** — shared lines, unclosed brackets, unsupported call forms, comments, or non-log data. Inspect the source; remove only confirmed debug calls by hand and preserve surrounding code and non-log markers. A `[DEBUG]` string alone does not establish a log call.
- **Near-miss prefix** (`[debug]`, `[DEBUG ]`) — report it and remove it only on user confirmation.

Only `[DEBUG]` statements are in scope; the project's own logging stays untouched, however stray it looks. In generated or compiled output, rebuild instead of editing.

### Verify Removal

Re-run `find`; it exits 0 when no exact marker candidate remains and 1 when removable calls or held candidates remain. Review held candidates individually; preserve confirmed non-log content and report those markers instead of deleting them to force exit 0. If any debug call remains, return to Remove Logs. Then run the project's syntax or type check when it has one; fix any cleanup damage before reporting completion.

### Report

Report the files cleaned, how many logs were removed in one to three sentences, and any near-miss prefix left for the user to confirm. Never paste the removed lines.
