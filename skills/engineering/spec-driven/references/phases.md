# Sub-Agent Dispatch

Protocol for dispatching sub-agents during phase execution.

## When to Use

Referenced from each phase ref (specify, design, tasks, implement)
when deciding whether and how to dispatch sub-agents for context
isolation.

## Workflow

Dispatch is for full-form (Large/Complex) activities -- auto-sizing decides.
Disk artifacts are the handoff for discovery and execution sub-agents -- they
don't return findings through the context. Plan sub-agents are read-only by
harness contract: they return structured slot fillers (tables, lists, rows)
that the main agent composes into the artifact via the canonical template.

At **Medium**, design and tasks run inline -- the research, exploration, and
Plan sub-agents are not dispatched. The implement sub-agent is still dispatched
per invocation (it isolates the implement+verify cycle, not planning). Quick
mode runs entirely without dispatch.

## Dispatch Map

Full dispatch instructions live in each reference that uses them:

| Sub-agent | Defined in |
|-----------|-----------|
| Research sub-agents (one per unknown topic) | [design.md](design.md) Step 5 |
| Codebase exploration sub-agent | [design.md](design.md) Step 6 |
| Design Plan sub-agent | [design.md](design.md) Step 10 |
| Tasks Plan sub-agent | [tasks.md](tasks.md) Step 4 |
| Implement sub-agent | [implement.md](implement.md) Step 4 |

Research and exploration sub-agents in design.md run in the same
dispatch turn (independent). The Design Plan sub-agent runs after
exploration artifacts exist. The Tasks Plan sub-agent runs after
design.md exists. The implement sub-agent runs after design/tasks
artifacts exist.
