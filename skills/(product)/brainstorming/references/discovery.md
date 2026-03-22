# Discovery -- Understand the Problem Space

Map the territory before exploring it. Understand what exists, what is missing,
and what matters.

## When to Use

First phase of every brainstorming session. Auto-loaded when brainstorming triggers.

## Workflow

Never assume context. Always interview before generating alternatives. Unlike
docs-writer discovery (which refines an existing idea), brainstorming discovery
maps the space of possibilities before any direction exists.

Adaptive interview, not scripted. Start each topic with opening questions,
evaluate answers against sufficiency criteria, deepen when signals appear,
and move on when criteria are met. Summarize understanding before advancing
to the next topic.

### Adaptive Deepening

Probe further when answers are:

| Signal | Response |
|--------|----------|
| Vague | Ask for specifics: "Can you give a concrete example?" |
| Assumed | Ask for evidence: "How do you know? What data supports this?" |
| Conflated | Separate concepts: "Those sound like two different things. Which one matters more?" |
| Solution-first | Redirect to problem: "Before the solution -- what problem or opportunity do you see?" |
| Overly broad | Narrow down: "Who specifically? Which case matters most?" |

### Question Principles

- Open-ended first, specific later
- Never suggest answers (avoid leading)
- Build follow-ups on what the user actually said, not a script
- Summarize understanding before moving to the next topic
- One question at a time -- never batch multiple questions in a single message

### Topics

#### Topic 1: Context and Motivation

**Opening Questions:**

- What triggered this brainstorm? What happened or changed?
- What is the current situation? What exists today?
- Why now? What makes this the right time to explore?

**Deepen When:**

- Vague motivation: "Something feels off" -- ask for a specific moment or trigger
- Solution-first: user describes what to build -- redirect to what problem or
  opportunity they see
- Assumed urgency: "We need this ASAP" -- ask what happens if you wait a month
- No current state: user jumps to the future -- ask what exists today and what
  is working or not working

**Sufficient When:**

- Clear trigger or motivation articulated
- Current state understood (what exists, what does not)
- Timing rationale clear or explicitly unknown

#### Topic 2: Constraints and Boundaries

**Opening Questions:**

- What is definitely off the table? (technical, budget, time, political)
- What must be preserved? (existing systems, user expectations, brand)
- Who are the stakeholders? Who has veto power?

**Deepen When:**

- "No constraints" -- probe: budget? timeline? team size? technical stack?
- Hidden constraints -- "What would your manager/team/users reject?"
- Contradictory constraints -- surface the tension, ask which takes priority
- Only hard constraints mentioned -- ask about preferences and soft boundaries

**Sufficient When:**

- Hard constraints identified (non-negotiable boundaries)
- Soft constraints identified (preferences that can flex)
- Key stakeholders named or explicitly noted as absent

#### Topic 3: Success Criteria

**Opening Questions:**

- If this brainstorm succeeds, what do you walk away with?
- How will you know the chosen direction is right?
- What would make you confident enough to move forward?

**Deepen When:**

- "I will know it when I see it" -- ask for one concrete signal
- Multiple competing criteria -- ask which one wins when they conflict
- No measurable outcome -- "If we revisit in 3 months, how do we judge if
  this was the right call?"
- Only positive criteria -- ask what failure looks like too

**Sufficient When:**

- At least one concrete success signal defined
- Decision criteria clear enough to evaluate alternatives against
- User understands what "done" means for this brainstorm (a direction, not a plan)

### Quality Gate

Before advancing to diverge, confirm:

- [ ] Motivation is understood (why now, what triggered this)
- [ ] Current state is mapped (what exists today)
- [ ] Hard constraints are identified
- [ ] Success criteria defined (how to evaluate alternatives)
- [ ] User has confirmed the summary

Present a summary and confirm before advancing to diverge. Only proceed after
confirmation.

## Guidelines

**DO:**
- Start every brainstorm with discovery regardless of how clear the idea seems
- Adapt question depth to the complexity of the subject
- Mark unknowns as TBD rather than inventing constraints
- Challenge vague or assumed answers before moving on

**DON'T:**
- Skip discovery because the user seems to have a direction
- Ask all questions at once (one topic at a time)
- Assume constraints that were not stated
- Move past the quality gate without user confirmation

## Next Steps

Load [diverge.md](diverge.md) to generate alternatives.
