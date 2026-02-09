# Log Cleanup

Remove all debug logs after debugging is complete.

## When to Use

- Fix has been verified and bug is resolved
- User explicitly requests cleanup
- Before committing changes to version control
- Debug session is complete

## Process

### Step 1: Find Debug Logs

Search for all `[DEBUG]` logs in the codebase:

```bash
grep -rn '\[DEBUG\]' . --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx'
```

### Step 2: Remove Logs

Remove each debug log statement:

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

Run the grep command again to confirm no logs remain:

```bash
grep -rn '\[DEBUG\]' . --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx'
```

Expected output: No matches found.

### Step 4: Report to User

```markdown
## Cleanup Complete

Removed {count} debug logs from:

- {file}: {count} logs
- {file}: {count} logs
```

## Manual Verification

User can check for remaining logs anytime:

```bash
grep -rn '\[DEBUG\]' . --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx'
```

## Guidelines

1. **Remove all [DEBUG] logs** - don't leave any behind
2. **Don't remove other logs** - only those with [DEBUG] prefix
3. **Verify after cleanup** - confirm no logs remain
4. **Cleanup is automatic** - part of normal debug workflow
5. **Safe to cleanup anytime** - debug logs are temporary only

## Task

Remove all `[DEBUG]` logs from the codebase.

Report how many logs were removed and from which files.
