# Load Handoff

Read the consolidated `.artifacts/HANDOFF.md` so the current session resumes with prior context.

## Workflow

1. If `.artifacts/HANDOFF.md` is absent or empty, return no output.
2. Read the whole file into working context.
3. Check load-bearing claims against current evidence before acting. Treat stale or unverified claims as unverified.
4. Report `Focus` and the relevant current state, constraints, and open threads.

## Guidelines

- Do not print the document in full unless asked — reading it already puts it in context
- Do not clear after load; clear is a separate explicit op
- Infer the next action from the focus and current context; do not require a prescribed next step
- Flag missing `Focus` or `Current state`, then continue with the available context
