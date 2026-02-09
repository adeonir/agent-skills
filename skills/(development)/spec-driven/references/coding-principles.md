# Coding Principles

Behavioral principles for implementation. Load before writing any code.

## Core Principles

| Principle | Description |
|-----------|-------------|
| Simplicity first | Write the simplest code that satisfies the requirement |
| Surgical changes | Modify only what is necessary, leave unrelated code untouched |
| Goal-driven | Every change must trace back to a requirement or acceptance criterion |
| Follow existing patterns | Match the project's conventions exactly (naming, imports, error handling) |
| Verify before moving on | Run quality gates after each task, fix issues immediately |

## Anti-Patterns

| Anti-Pattern | What It Looks Like | Instead |
|--------------|--------------------|---------|
| Over-engineering | Adding abstractions for one use case | Write concrete code, extract later if needed |
| Premature abstraction | Creating helpers/utils for single callers | Inline the logic, refactor when a pattern emerges |
| Unnecessary refactoring | Cleaning up code outside the task scope | Only touch files listed in the plan |
| Speculative features | Adding config options "just in case" | Implement exactly what the spec requires |
| Gold plating | Adding extra error handling, logging, or comments beyond requirements | Match the project's existing level of detail |

## Decision Framework

Before writing code, ask:

1. Is this change required by a spec requirement?
2. Does the plan specify this file/component?
3. Am I following the project's existing pattern for this?
4. Is this the minimal change that satisfies the task?

If any answer is "no", reconsider the change.
