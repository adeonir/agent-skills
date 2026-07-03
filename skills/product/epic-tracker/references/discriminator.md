# Artifact Type Discriminator

Choose the artifact type for a unit of work — Bug, Story, or Task — from one
shared rule.

## When to Use

Before creating an artifact when the trigger does not already name the type,
or when a create flow suspects the work belongs to a different type. The
create refs ([story.md](story.md), [task.md](task.md), [bug.md](bug.md))
point here on their type-redirect paths.

## Decision

Most specific first — the Jira Story/Task/Bug split:

1. **Defect** — does it fix behavior that already exists and is broken? →
   **Bug**
2. **User-value slice** — does it deliver a demonstrable slice of user value,
   with acceptance criteria that satisfy a requirement? → **Story**
3. **Anything else actionable** — enabling, technical, research, tooling, or
   docs, measured by a Definition of Done with no acceptance criteria → **Task**

## Identities

| Type | Is | Carries |
|------|----|---------|
| Bug | a defect in existing behavior | repro steps, severity, environment |
| Story | a demonstrable slice of user value | acceptance criteria (Given/When/Then) + Satisfies requirement |
| Task | general actionable work | Definition of Done, no acceptance criteria |

## Notes

- **Story vs Task is form, not audience.** A Story is a demonstrable
  user-value slice with acceptance criteria; everything else actionable is a
  Task, even when user-adjacent. A horizontal building block with no
  demonstrable user outcome is a Task, not a Story.
- **Bug vs Task.** A Bug fixes broken existing behavior; a Task builds or
  changes something that is not a defect.
