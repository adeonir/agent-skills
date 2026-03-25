# Handoff

Suggest next steps for implementing a story or fixing a bug. Bridge
between epic-tracker (what) and spec-driven (how).

## When to Use

- User says "handoff", "implement story", "start story"
- A story or bug is ready for implementation
- User wants to move from planning to execution

## Workflow

### 1. Identify Artifact

1. If user specifies a story or bug, load it
2. If not specified, show stories/bugs with status "planned" or
   "in-progress" and ask which one
3. Read the artifact's acceptance criteria and context

### 2. Prepare Context

Gather context for the handoff:

- Story/bug title and description
- Acceptance criteria (these become spec-driven's requirements)
- Parent epic context (scope, rabbit holes)
- Related references (PRD, design doc)

### 3. Suggest Next Steps

Present options to the user:

**Option A: Hand off to spec-driven**

Suggest using spec-driven to create a feature spec from the story:

```
Use spec-driven to specify this story:
"create feature {story-name}: {brief description}"
```

The story's acceptance criteria feed directly into the spec's
requirements. The story's rabbit holes inform the spec's constraints.

**Option B: Sync to external tracker**

If the user mentions a tracker (Linear, GitHub Issues, Jira):

- Note that the artifact is structured for 1:1 mapping
- Suggest manual creation in the tracker using the artifact as source
- Epic-tracker does not implement sync -- this is a future integration

**Option C: Mark as in-progress**

If the user wants to start working without spec-driven:

- Update the artifact's status to "in-progress"
- Remind that acceptance criteria should be verified when done

### 4. Update Status

After handoff, suggest updating the artifact status to "in-progress"
if not already.

## Guidelines

**DO:**
- Always show the acceptance criteria during handoff
- Suggest spec-driven as the primary implementation path
- Include parent epic context for broader understanding
- Let the user choose the handoff path

**DON'T:**
- Auto-trigger spec-driven -- always suggest, never invoke
- Implement tracker sync -- only describe the mapping
- Hand off stories without acceptance criteria -- ask to add them first
- Skip status update after handoff

## Error Handling

- Story has no acceptance criteria: ask user to define them before
  handoff
- Story status is "done": warn that it's already completed
- Story status is "blocked": warn and ask if the blocker is resolved
- Spec-driven not installed: suggest manual implementation, note that
  spec-driven would provide structured workflow
