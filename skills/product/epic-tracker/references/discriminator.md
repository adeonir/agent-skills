# Artifact Type Discriminator

Choose the artifact type for a unit of work — Bug, Story, or Task — from one shared rule.

## When to Use

Before creating an artifact when the trigger does not already name the type, or when a create flow suspects the work belongs to a different type. This ref is the single home for the rule that decides between them; a create ref states what its own type is and points here rather than re-deriving the split. The create refs ([story.md](../instructions/story.md), [task.md](../instructions/task.md), [bug.md](../instructions/bug.md)) point here on their type-redirect paths.

## Decision

Most specific first — the Story/Task/Bug split:

1. **Defect** — does it fix behavior that already exists and is broken? → **Bug**
2. **User-value slice** — does it deliver a demonstrable slice of user value, an outcome the user observes on its own? → **Story**
3. **Anything else actionable** — enabling, technical, research, tooling, or docs, where no user observes an outcome of its own → **Task**

## Decision Tree

```text
Does the behavior already exist and is broken?
├ yes → Bug
└ no  → Does the user observe an outcome of its own?
        ├ yes → Story
        └ no  → Is it actionable work with a statable done-condition?
                ├ yes → Task
                └ no  → Ask the user
```

## Identities

| Type | Is | Carries |
|------|----|---------|
| Bug | a defect in existing behavior | repro steps, severity, environment |
| Story | a demonstrable slice of user value | acceptance criteria (Given/When/Then), each carrying `Satisfies` when a parent epic declares the requirement |
| Task | general actionable work | Definition of Done, no acceptance criteria; a done-condition carries `Satisfies` when it discharges a requirement no story can |

## Notes

- **Story vs Task is the observable outcome, not the audience.** A Story delivers something a user sees happen; everything else actionable is a Task, even when user-adjacent. Work being *about* users does not make it a Story — a horizontal building block with no outcome of its own is a Task however close to the user it sits.
- **The shape follows the type; it never picks it.** A Story states its outcome as Given/When/Then acceptance criteria, a Task states its as a Definition of Done — consequences of the choice above, not tests for it. Writing no acceptance criteria does not turn a user-observable slice into a Task, and adding them does not turn enabling work into a Story.
- **Example — password reset.** "Set a new password from a reset link" is a Story: demonstrable on its own, carries acceptance criteria. "Add the password_resets table" or "stand up the mail queue" is a Task: a horizontal building block the story needs but that shows the user nothing on its own.
- **Anti-pattern — task dressed as story.** "Send a welcome email" is a Task if the user outcome is not observable on its own. "Complete onboarding and receive a welcome email" is a Story because the user sees the result.
- **No epic to sit under is not a type signal.** A demonstrable user-value slice with no theme to group it is a standalone Story, not a Task — an Epic groups Stories, it never qualifies them. Downgrading the slice to a Task to give it a parent is the inverse of the anti-pattern above.
- **Bug vs Task.** A Bug fixes broken existing behavior; a Task builds or changes something that is not a defect.
- **Bug vs missing expected behavior.** If the behavior was specified or delivered before and now fails, it is a Bug. If it was never implemented, it is a Story (or a Task if it is purely enabling work).
- **When to escalate to Epic.** If the work is too large for one Story and naturally groups multiple Stories, it is an Epic candidate — not a big Story or a big Task.

## When Still Unclear

Ask the user when:

- The work feels like half Bug, half Story.
- Something "should work" but was never implemented.
- The user describes a solution, not the problem or outcome.
- The same work could be framed as enabling a feature (Task) or as the feature itself (Story).
