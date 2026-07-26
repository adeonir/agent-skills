# Log Cleanup

Remove all debug logs after debugging is complete.

## When to Use

Cleanup happens automatically after a fix is verified, or on explicit user request. Run cleanup before committing changes to version control.

- Fix has been verified and bug is resolved
- User explicitly requests cleanup
- Before committing changes to version control
- Debug session is complete

## Workflow

### Step 1: Find Debug Logs

Search for all `[DEBUG]` logs in the codebase:

```bash
grep -rn '\[DEBUG\]' . --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' --include='*.py' --include='*.go' --include='*.rs' --include='*.rb' --include='*.mjs' --include='*.cjs' --include='*.vue' --include='*.svelte'
```

### Step 2: Remove Logs

Remove each debug log statement. Only lines carrying the `[DEBUG]` prefix are in scope — the project's own logging stays untouched, however stray it looks.

```javascript
// Before cleanup
function calculateTotal(items) {
  console.log("[DEBUG] [cart.ts:15] calculateTotal called", { items });
  const total = items.reduce((sum, item) => sum + item.price, 0);
  console.log("[DEBUG] [cart.ts:17] calculated total", { total });
  return total;
}

// After cleanup
function calculateTotal(items) {
  const total = items.reduce((sum, item) => sum + item.price, 0);
  return total;
}
```

### Step 3: Verify Removal

Re-run the grep command from Step 1. Expected output: no matches.

### Step 4: Report to User

```markdown
## Cleanup Complete

Removed {count} debug logs from:

- {file}: {count} logs
- {file}: {count} logs
```

## Error Handling

- No [DEBUG] logs found: inform user cleanup is already done
- Logs in generated or compiled files: suggest rebuilding instead of manual cleanup
- Partial match (prefix variation): report and ask user to confirm removal
