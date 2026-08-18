# Load Handoff

Read the consolidated `.artifacts/HANDOFF.md` so the current session resumes with prior context.

## When to Use

- User invokes a load trigger ("resume session", "load handoff", "continue from last") at session start or mid-session
- Another workflow needs the current handoff as input

## Workflow

1. If `.artifacts/HANDOFF.md` is absent, empty, or contains neither `Focus` nor `Next step`, return no output.
2. Read the whole file into working context.
3. Report `Focus` and `Next step`.

## Guidelines

- Do not print the document in full unless asked — reading it already puts it in context
- Do not clear after load; clear is a separate explicit op
- Flag the gap when either `Focus` or `Next step` is missing, then continue with what is present
