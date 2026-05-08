# Phase Transitions

Protocol for moving between phases and managing session context.

## When to Use

At the end of each phase (specify, design, tasks, implement) before starting
the next. Also referenced when deciding whether to dispatch sub-agents.

## Between Phases

Each phase should run in a clean context window. A polluted window (used for
early phases and then for implementation) grows large and increases
hallucination risk.

```
finish phase -> [offer dump] -> clean window* -> start next phase
                                                   ...
                                                 (more phases)
                                                   ...
                               end of session -> end-of-session wrap-up (reads dump)
```

(*clean window only if user accepts the dump)

1. Complete the current phase and write its artifacts to disk
2. Offer the user a context transition -- suggest appending a session summary
   to `.artifacts/.session-dump.md` (decisions, discoveries, blockers, open
   items, phase completed, next phase); each phase appends, building a
   cumulative record. This is opt-in: if the user declines, continue in the
   current window without clearing
3. If accepted: clear the context window
4. Start the next phase in a clean window, loading only the artifacts it needs

The session dump is ephemeral — the end-of-session wrap-up reads it
to compose notes, then the file is disposable. It is not a project
artifact.

## Sub-Agent Dispatch

When activities run in full form (auto-sizing decides), they can dispatch
to sub-agents for context isolation. Disk artifacts are the handoff for
discovery and execution sub-agents -- they don't return findings through
the context. Plan sub-agents are read-only by harness contract: they
return structured slot fillers (tables, lists, rows) that the main agent
composes into the artifact via the canonical template. Inline forms
(quick mode, Medium scope) run without dispatch.

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

## Session Dump Template

Each phase appends one block to `.artifacts/.session-dump.md`. ALWAYS
use this exact template structure:

````markdown
## {{YYYY-MM-DD HH:MM}} — {{phase}}

**Feature:** {{ID}}-{{name}}
**Status transition:** {{from}} → {{to}}

**Decisions:**
- {Key decisions made this phase, beyond what is captured in artifacts. Write "none" if all decisions already live in spec.md / design.md.}

**Discoveries:**
- {Anything found that is not already in spec.md / design.md / tasks.md. Write "none" if no out-of-artifact findings.}

**Blockers:**
- {Open blockers preventing the next phase; otherwise "none".}

**Open items:**
- {Questions or follow-ups for the next phase; otherwise "none".}

**Next phase:** {{next phase or "done"}}
````
