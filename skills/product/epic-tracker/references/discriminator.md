# Artifact Type Discriminator

Choose the artifact type for a unit of work — Bug, Story, or Task — from one shared rule.

## When to Use

Before creating an artifact when the trigger does not already name the type, or when a create flow suspects the work belongs to a different type. The create refs ([story.md](story.md), [task.md](task.md), [bug.md](bug.md)) point here on their type-redirect paths.

## Decision

Most specific first — the Jira Story/Task/Bug split:

1. **Defect** — does it fix behavior that already exists and is broken? → **Bug**
2. **User-value slice** — does it deliver a demonstrable slice of user value, with acceptance criteria that satisfy a requirement? → **Story**
3. **Anything else actionable** — enabling, technical, research, tooling, or docs, measured by a Definition of Done with no acceptance criteria → **Task**

## Decision Tree

```text
Does the behavior already exist and is broken?
├ yes → Bug
└ no  → Does it deliver demonstrable user value with acceptance criteria?
        ├ yes → Story
        └ no  → Is it actionable work measured by a Definition of Done?
                ├ yes → Task
                └ no  → Ask the user
```

## Identities

| Type | Is | Carries |
|------|----|---------|
| Bug | a defect in existing behavior | repro steps, severity, environment |
| Story | a demonstrable slice of user value | acceptance criteria (Given/When/Then) + Satisfies requirement |
| Task | general actionable work | Definition of Done, no acceptance criteria |

## Notes

- **Story vs Task is form, not audience.** A Story is a demonstrable user-value slice with acceptance criteria; everything else actionable is a Task, even when user-adjacent. A horizontal building block with no demonstrable user outcome is a Task, not a Story.
- **Example — password reset.** "Set a new password from a reset link" is a Story: demonstrable on its own, carries acceptance criteria. "Add the password_resets table" or "stand up the mail queue" is a Task: a horizontal building block the story needs but that shows the user nothing on its own.
- **Anti-pattern — task dressed as story.** "Send a welcome email" is a Task if the user outcome is not observable on its own. "Complete onboarding and receive a welcome email" is a Story because the user sees the result.
- **Bug vs Task.** A Bug fixes broken existing behavior; a Task builds or changes something that is not a defect.
- **Bug vs missing expected behavior.** If the behavior was specified or delivered before and now fails, it is a Bug. If it was never implemented, it is a Story (or a Task if it is purely enabling work).
- **When to escalate to Epic.** If the work is too large for one Story and naturally groups multiple Stories, it is an Epic candidate — not a big Story or a big Task.

## When Still Unclear

Ask the user when:

- The work feels like half Bug, half Story.
- Something "should work" but was never implemented.
- The user describes a solution, not the problem or outcome.
- The same work could be framed as enabling a feature (Task) or as the feature itself (Story).
