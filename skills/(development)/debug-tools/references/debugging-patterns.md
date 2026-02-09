# Debugging Patterns

Common debugging patterns, log formats, and bug categories by framework.

## Log Patterns by Framework

### React/Next.js

```javascript
// Lifecycle
console.log("[DEBUG] [Component.tsx:10] mount", { props });

// Effect
useEffect(() => {
  console.log("[DEBUG] [Component.tsx:15] effect run", { deps });
  return () => console.log("[DEBUG] [Component.tsx:17] cleanup");
}, [deps]);

// State updates
console.log("[DEBUG] [Component.tsx:25] before setState", { current: state });
```

### Node.js/Express

```javascript
// Request handling
console.log("[DEBUG] [route.ts:10] request", {
  method: req.method,
  path: req.path,
});

// Error handling
console.log("[DEBUG] [service.ts:30] caught error", {
  name: err.name,
  message: err.message,
});

// Database operations
console.log("[DEBUG] [db.ts:45] query result", { rows: result.length });
```

### API Calls

```javascript
// Request start
console.log("[DEBUG] [api.ts:10] fetch start", { url, method });

// Request complete
console.log("[DEBUG] [api.ts:15] fetch done", {
  status: res.status,
  ok: res.ok,
});

// Response data
console.log("[DEBUG] [api.ts:20] response data", { data: await res.json() });
```

## Common Bug Patterns

| Pattern | Symptom | Check |
|---------|---------|-------|
| Null access | "Cannot read property X of undefined" | Optional chaining, defaults |
| Race condition | Works sometimes, fails randomly | Async ordering, state timing |
| Stale closure | Using old values in callbacks | useCallback deps, event bindings |
| API mismatch | Data not displaying | Response shape, null handling |
| Silent error | Nothing happens | Empty catch blocks, missing error state |
| Infinite loop | App freezes | Dependency arrays, state updates |
| Memory leak | Performance degrades over time | Event listeners, subscriptions |
| Timing issue | Works in dev, fails in prod | Timing assumptions, async/await |

## Confidence Scoring Reference

| Score | Meaning | Action |
|-------|---------|--------|
| >= 70 | High (>= 70) | Report as probable cause |
| 50-69 | Medium (50-69) | Suggest logs to confirm |
| < 50 | Low (< 50) | Do not report |

## MCP Integration (Optional)

| MCP | Provides |
|-----|----------|
| console-ninja | Runtime values, test status, coverage |
| chrome-devtools | Network inspection, browser console, DOM state |
| serena | Semantic code analysis, symbol references |
| context7 | Documentation search, debugging patterns |

## When to Debug vs When NOT to

**Use debug-tools:**

- Unexpected behavior
- Silent errors
- Intermittent failures
- Issues requiring runtime data

**Don't use debug-tools:**

- Syntax errors (linter resolves)
- Type errors (TypeScript resolves)
- Obvious bugs in diff (use code review)

## Task

Load this reference when user asks about:

- Debug log formats
- Common bug patterns
- Framework-specific debugging
- Confidence scoring guidelines
