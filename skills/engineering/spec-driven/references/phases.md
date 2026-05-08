# Sub-Agent Dispatch

Protocol for dispatching sub-agents during phase execution.

## When to Use

Referenced from each phase ref (specify, design, tasks, implement)
when deciding whether and how to dispatch sub-agents for context
isolation.

## Workflow

When activities run in full form (auto-sizing decides), they can dispatch
to sub-agents for context isolation. Disk artifacts are the handoff for
discovery and execution sub-agents -- they don't return findings through
the context. Plan sub-agents are read-only by harness contract: they
return structured slot fillers (tables, lists, rows) that the main agent
composes into the artifact via the canonical template. Inline forms
(quick mode, Medium scope) run without dispatch.

## Dispatch Map

Full dispatch instructions live in each reference that uses them:

| Sub-agent | Defined in |
|-----------|-----------|
| Research sub-agents (one per unknown topic) | [design.md](design.md) Step 5 |
| Codebase exploration sub-agent | [design.md](design.md) Step 6 |
| Design Plan sub-agent | [design.md](design.md) Step 10 |
| Tasks Plan sub-agent | [tasks.md](tasks.md) Step 4 |
| Implement sub-agent | [implement.md](implement.md) Step 5 |

Research and exploration sub-agents in design.md run in the same
dispatch turn (independent). The Design Plan sub-agent runs after
exploration artifacts exist. The Tasks Plan sub-agent runs after
design.md exists. The implement sub-agent runs after design/tasks
artifacts exist.
