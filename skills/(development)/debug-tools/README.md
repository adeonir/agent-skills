# Debug Tools

Iterative debugging workflow with confidence scoring and targeted log injection.

## Installation

```bash
npx skills add adeonir/agent-skills --skill debug-tools
```

## What It Does

Five-phase debugging workflow that helps find and fix bugs systematically:

```mermaid
flowchart TD
    A[Investigate] --> B{Root cause found?}
    B -->|Yes >=70%| C[Propose Fix]
    B -->|No 50-69%| D[Inject Logs]
    B -->|No <50%| A
    D --> E[User reproduces bug]
    E --> F[Analyze output]
    F --> A
    C --> G[Apply fix]
    G --> H{Bug fixed?}
    H -->|Yes| I[Cleanup]
    H -->|No| A
    I --> J[Done]
```

**Phase 1: Investigate** - Analyze code to find root cause with confidence scoring
**Phase 2: Inject Logs** - Add targeted `[DEBUG]` logs to capture runtime data
**Phase 3: Propose Fix** - Suggest minimal fix based on evidence
**Phase 4: Verify** - Confirm the fix resolves the issue
**Phase 5: Cleanup** - Automatically remove all debug logs

## Usage

```
# Start debugging
debug this issue
investigate why the login is failing
trace this error

# Add debug logs
add debug logs to trace the data flow
inject logs to see what's happening

# Cleanup logs
remove debug logs
cleanup debug statements
```

### How It Works

**Investigation** analyzes code looking for error sources, data flow issues, state mutations, race conditions, API contract violations, and timing problems. Findings are scored 0-100: >= 70 is reported as probable cause, 50-69 suggests logs to confirm, < 50 is not reported.

**Log Injection** adds 3-5 strategic `[DEBUG]` logs at function entry points, before/after async operations, conditional branches, and catch blocks. Never logs sensitive data. Supports JS/TS, Python, Go, Rust, Ruby, Vue, Svelte, and more.

**Fix and Verify** proposes a minimal fix in diff format, requires user approval, and loops back if the fix doesn't resolve the issue.

**Cleanup** automatically removes all `[DEBUG]` logs after verification.

## Requirements

- Git (for code analysis)

## FAQ

**Q: When should I use debug-tools vs code review?**
A: Use debug-tools for runtime issues and unexpected behavior. Use code review for static analysis of code changes.

**Q: What if the first fix doesn't work?**
A: The workflow loops back to investigation. New logs may be added, or a different root cause is explored.

**Q: Are debug logs left in my code?**
A: No. Cleanup is automatic after fix verification. You can also request cleanup anytime.

**Q: Do I need specific tools for this to work?**
A: No. The skill adapts to whatever tools are available. Runtime inspection and browser debugging tools enhance the experience, but are not required.

**Q: What confidence score is considered "good enough" to propose a fix?**
A: >= 70 confidence with clear evidence. Lower scores suggest adding logs to gather more data.
