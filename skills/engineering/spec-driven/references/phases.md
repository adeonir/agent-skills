# Subagent Dispatch

Protocol for dispatching subagents during phase execution.

## When to Use

Referenced from each phase ref (specify, design, tasks, implement)
when deciding whether and how to dispatch subagents for context
isolation.

## Workflow

Dispatch is for full-form (Large/Complex) activities -- auto-sizing decides.
Disk artifacts are the handoff for discovery and execution subagents -- they
don't return findings through the context. Plan subagents are read-only by
harness contract: they return structured slot fillers (tables, lists, rows)
that the main agent composes into the artifact via the canonical template.

At **Medium**, design and tasks run inline -- the research, exploration, and
Plan subagents are not dispatched. The implement subagent is still dispatched
per invocation (it isolates the implement+verify cycle, not planning). Quick
mode runs entirely without dispatch.

## Dispatch Map

Full dispatch instructions live in each reference that uses them:

| Subagent | Defined in |
|-----------|-----------|
| Research subagents (one per unknown topic) | [design.md](design.md) Step 5 |
| Codebase exploration subagent | [design.md](design.md) Step 6 |
| Design Plan subagent | [design.md](design.md) Step 10 |
| Tasks Plan subagent | [tasks.md](tasks.md) Step 4 |
| Implement subagent | [implement.md](implement.md) Step 4 |

Research and exploration subagents in design.md run in the same
dispatch turn (independent). The Design Plan subagent runs after
exploration artifacts exist. The Tasks Plan subagent runs after
design.md exists. The implement subagent runs after design/tasks
artifacts exist.
