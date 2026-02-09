# Log Injection

Add targeted debug logs at strategic points to capture runtime data.

## When to Use

- Investigation found suspected issues (50-69 confidence)
- Need runtime data to confirm root cause
- Silent errors or intermittent failures
- Complex data flow that needs tracing

## Log Format

Always use this format for consistency:

```javascript
console.log("[DEBUG] [file:line] description", { vars });
```

Components:

- `[DEBUG]` - Prefix for grep and cleanup
- `[file:line]` - Location for navigation
- `description` - What this log checks
- `{ vars }` - Relevant data (no sensitive info)

## Strategic Placement

### Decision Tree

```
Is function called?
├── No → Log at call sites
└── Yes → Log function entry
    ├── Has async operations?
    │   ├── Log before await (input/state)
    │   └── Log after await (result/error)
    ├── Has conditionals?
    │   └── Log which branch taken
    └── Has error handling?
        └── Log caught errors
```

### Placement Guide

| Location | Purpose | What to Log |
|----------|---------|-------------|
| Function entry | Confirm execution, capture args | Function name, key arguments |
| Before async | Check state before operation | Input data, current state |
| After async | Verify result | Response data, success/failure |
| Conditionals | Which branch taken | Condition value, path taken |
| Catch blocks | Error details | Error name, message, stack |
| State changes | Track mutations | Before/after values |
| Event handlers | User interactions | Event type, target data |

## Process

### Step 1: Identify Injection Points

Based on investigation findings, determine:

- Which files need logs
- What data to capture at each point
- How many logs (3-5 strategic points, not flooding)

### Step 2: Add Debug Logs

Insert logs using the standard format:

```javascript
// Example: Function entry
console.log("[DEBUG] [auth.ts:15] login called", { email, timestamp });

// Example: Before async
console.log("[DEBUG] [api.ts:42] fetching user", { userId });

// Example: After async
console.log("[DEBUG] [api.ts:45] user fetched", {
  user: data.user,
  status: response.status,
});

// Example: Error handling
console.log("[DEBUG] [service.ts:30] caught error", {
  name: err.name,
  message: err.message,
});
```

### Step 3: Report to User

```markdown
## Debug Logs Added ({count})

| Location | Purpose |
|----------|---------|
| {file}:{line} | {what it captures} |

Reproduce the bug and share console output.
```

### Step 4: Wait for User

Ask user to:

1. Reproduce the bug
2. Share console output
3. Describe what they observed

## Framework-Specific Patterns

### React/Next.js

```javascript
// Component lifecycle
console.log("[DEBUG] [Component.tsx:10] mount", { props, state });

// Effect execution
useEffect(() => {
  console.log("[DEBUG] [Component.tsx:15] effect run", { deps });
  return () => console.log("[DEBUG] [Component.tsx:17] cleanup");
}, [deps]);

// State updates (before)
console.log("[DEBUG] [Component.tsx:25] before setState", { current: state });
setState(newValue);

// Event handlers
console.log("[DEBUG] [Component.tsx:30] click handler", { event: e.target.dataset });
```

### Node.js/Express

```javascript
// Request handling
console.log("[DEBUG] [route.ts:10] request", {
  method: req.method,
  path: req.path,
  query: req.query,
  body: req.body, // Careful: may contain sensitive data
});

// Middleware execution
console.log("[DEBUG] [auth.ts:20] auth middleware", { user: req.user?.id });

// Database operations
console.log("[DEBUG] [db.ts:45] query", { sql: query.substring(0, 100) });
console.log("[DEBUG] [db.ts:47] query result", { rows: result.length });

// Error handling
console.log("[DEBUG] [error.ts:30] caught error", {
  name: err.name,
  message: err.message,
  stack: err.stack?.split('\n')[0],
});
```

### API Calls

```javascript
// Request start
console.log("[DEBUG] [api.ts:10] fetch start", { url, method });

// Request complete
console.log("[DEBUG] [api.ts:15] fetch done", {
  status: res.status,
  ok: res.ok,
  contentType: res.headers.get('content-type'),
});

// Response parsing
console.log("[DEBUG] [api.ts:20] response data", { data });
```

## What to Capture

### Always Useful
- Function entry/exit
- Async operation start/completion
- Error details (name, message)
- State before/after changes

### Sometimes Useful
- Function arguments (sanitized)
- API responses (truncated)
- User actions (event type)
- Timing information

### Never Capture
- Passwords, tokens, API keys
- PII (emails, phone numbers, SSN)
- Full credit card numbers
- Session IDs or auth cookies

## Analyzing Console Output

When user shares console output, look for:

| Pattern | Indicates | Next Step |
|---------|-----------|-----------|
| Log doesn't appear | Code path not executed | Check conditions, early returns |
| Unexpected value | Logic error | Trace value origin |
| Null/undefined | Missing data | Check upstream sources |
| Error in log | Exception caught | Analyze error context |
| Wrong order | Race condition | Check async timing |
| Repeated logs | Infinite loop | Check dependencies |

## Guidelines

1. **Only log what's needed** - no "just in case" logs
2. **Always use [DEBUG] prefix** - enables cleanup
3. **Never log sensitive data** - passwords, tokens, PII
4. **Include context** - file:line helps navigation
5. **Minimal logs** - 3-5 strategic points, not flooding
6. **Clean up after** - logs are temporary debugging aids
7. **Be specific** - "login failed" not "error occurred"

## Next Steps

After user provides console output:

- Analyze the runtime data
- Load [investigation.md](investigation.md) to continue investigation
- Find root cause with new evidence

## Task

Add targeted debug logs at strategic points based on investigation findings.

Ask user to reproduce the bug and share the console output.
