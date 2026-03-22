# Log Injection

Add targeted debug logs at strategic points to capture runtime data.

## When to Use

As a technique during investigation, when static analysis alone cannot confirm
the root cause and runtime data is needed. Not every debugging session requires
log injection -- use it when confidence is in the 50-69 range and runtime
evidence would raise it above 70.

## Log Format

Always use the `[DEBUG]` prefix for grep and cleanup. Adapt the format to the project language:

| Language | Format |
|----------|--------|
| JavaScript/TypeScript | `console.log("[DEBUG] [file:line] description", { vars });` |
| Python | `print(f"[DEBUG] [file:line] description {vars}")` |
| Go | `fmt.Printf("[DEBUG] [file:line] description %v\n", vars)` |
| Rust | `eprintln!("[DEBUG] [file:line] description {:?}", vars);` |
| Ruby | `puts "[DEBUG] [file:line] description #{vars.inspect}"` |

Components:

- `[DEBUG]` - Prefix for grep and cleanup (required, all languages)
- `[file:line]` - File path and line number for navigation (e.g., `[cache.js:12]`). Never use function names in place of line numbers
- `description` - What this log checks
- `vars` - Relevant data (no sensitive info)

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

## Workflow

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

## Common Patterns

### Component Lifecycle (React, Vue, Svelte)

Log on mount, effect execution, state changes, and event handlers.

### HTTP Handlers (Express, FastAPI, Gin)

Log request entry (method, path, sanitized body), middleware execution, and response status.

### Database Operations

Log query (truncated), result count, and errors. Never log full query params that may contain user data.

### API Calls

Log request start (url, method), response status, and parsed data shape.

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

**DO:**
- Only log what is needed to confirm or deny the hypothesis
- Always use `[DEBUG]` prefix for grep and cleanup
- Include `[file:line]` context for navigation
- Keep to 3-5 strategic injection points
- Clean up after debugging -- logs are temporary aids
- Use specific descriptions: "login failed" not "error occurred"

**DON'T:**
- Add "just in case" logs
- Log sensitive data (passwords, tokens, PII)
- Flood the output with excessive log points
- Leave debug logs in production code

## Error Handling

- File is read-only or generated: inform user and suggest alternative location
- Language not listed in log format table: adapt the [DEBUG] prefix pattern to the language's print/log function
- Too many injection points needed: focus on the most critical 3-5

## Next Steps

After user provides console output:

- Analyze the runtime data
- Load [investigation.md](investigation.md) to continue investigation
- Find root cause with new evidence
