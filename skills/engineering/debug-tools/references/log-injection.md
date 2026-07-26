# Log Injection

Add targeted debug logs at strategic points to capture runtime data.

## When to Use

As a technique during investigation, when static analysis alone cannot confirm the root cause and runtime data is needed. Not every debugging session requires log injection -- use it when reading the code cannot show the mechanism, and only observing the running system can.

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
- `description` - What this log checks, stated specifically: "login failed", not "error occurred"
- `vars` - Relevant data (no sensitive info)

## Strategic Placement

### Decision Tree

```text
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

- Which files need logs — never a generated or read-only file, where the log is lost on the next build; log the source that produces it, or the nearest caller
- What data to capture at each point
- How many logs (3-5 strategic points, not flooding)

### Step 2: Add Debug Logs

Insert each log in the project's language using the standard format, at the locations the Placement Guide names.

### Step 3: Report What Was Added

```markdown
## Debug Logs Added ({count})

| Location | Purpose |
|----------|---------|
| {file}:{line} | {what it captures} |
```

### Step 4: Collect the Output

Run the reproduction and read the output. Ask the user for it only when the repro is out of reach from here — it needs their credentials, their device, a manual interaction, or an environment this session cannot enter. Then name the steps to run and ask for the output plus what they observed.

## What to Capture

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

## Performance and Memory Leak Instrumentation

For performance regressions, slowdowns, or leaks, plain console logs are not enough -- inject measurements that quantify what is happening over time.

| Symptom | Instrumentation | What to Log |
|---------|----------------|-------------|
| Slow operation | Wrap with `performance.now()` / `time.time()` | Elapsed ms before and after |
| Memory leak | Snapshot listener/subscription counts | Count before and after suspect flow |
| Re-render storm | Counter at render entry | Increment on each call, log per second |
| Resource bloat | Sample heap or process memory | Reading before/after and delta |
| Loop suspicion | Iteration counter | Total iterations, time per iteration |

Capture before/after pairs so the delta is obvious from the output. A single absolute number rarely answers "is this growing?".

## Analyzing Console Output

In the collected output, look for:

| Pattern | Indicates | Next Step |
|---------|-----------|-----------|
| Log doesn't appear | Code path not executed | Check conditions, early returns |
| Unexpected value | Logic error | Trace value origin |
| Null/undefined | Missing data | Check upstream sources |
| Error in log | Exception caught | Analyze error context |
| Wrong order | Race condition | Check async timing |
| Repeated logs | Infinite loop | Check dependencies |
