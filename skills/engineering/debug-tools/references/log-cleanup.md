# Log Cleanup

Remove all debug logs after debugging is complete.

## When to Use

When the `[DEBUG]` logs added during a session have to come out of the code.

## Workflow

### Find Debug Logs

Search for all `[DEBUG]` logs in the codebase:

```bash
grep -rn '\[DEBUG\]' . --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' --include='*.py' --include='*.go' --include='*.rs' --include='*.rb' --include='*.mjs' --include='*.cjs' --include='*.vue' --include='*.svelte'
```

### Remove Logs

Remove each debug log statement. Only lines carrying the `[DEBUG]` prefix are in scope — the project's own logging stays untouched, however stray it looks. A near-miss prefix (`[debug]`, `[DEBUG ]`) is reported and removed only on user confirmation. In generated or compiled output, rebuild instead of editing.

### Verify Removal

Re-run the grep command from Find Debug Logs. Expected output: no matches.

### Report

Report the files cleaned, how many logs were removed in one to three sentences, and any near-miss prefix left for the user to confirm. Never paste the removed lines.
