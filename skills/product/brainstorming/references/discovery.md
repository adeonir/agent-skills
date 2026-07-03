# Discovery -- Understand the Problem Space

Map the territory before exploring it. Understand what exists, what is missing,
and what matters.

## When to Use

First phase of every brainstorming session. Auto-loaded when brainstorming triggers.

## Path Detection

Classify entry state from the user's input.

**Greenfield** — no concrete idea or plan yet. Exploratory framing,
open questions, requests to map a space from scratch.

**Relentless** — an idea or plan already exists at any maturity.
Requests to challenge, validate, refine, pivot, or audit committed
thinking. The `/brainstorming deep` argument forces this path.

Do not announce the path as a label or headline. Lead directly with a proposed
interpretation that reflects the detected path. User can redirect at any point.

Greenfield: open with your read of the situation, invite correction.
Relentless: open by acknowledging the committed direction, then probe the
core assumption behind it. Do not repeat "stress-test" or "pressure-test" as
labels throughout the response — acknowledge the mode once if at all, then
focus on the substance.

The proposed interpretation with its redirect invite is the complete first turn.
Do not add a second question after the interpretation. End on the invite
("Is that right?" / "Is that a fair read?") and wait for the response.

## Workflow

Never assume context. Always interview before generating alternatives.
Brainstorming discovery maps the space of possibilities before any
direction exists — different from skills that refine an already-chosen
idea.

Interview is adaptive, not scripted. Walk the decision tree: each answer reveals
which branch to explore next. Resolve dependencies between decisions before
advancing — don't ask B until A is settled if B depends on A.

### Interview Approach

**Proposed interpretation:** Don't ask cold open-ended questions. Propose your
read of the situation, let the user confirm or redirect. This unsticks vague
thinking faster than neutral questioning.

Example: "It sounds like the core problem is X — is that right, or is it
more like Y?"

**Codebase exploration:** When a question about current state can be answered
by reading the code, explore the codebase instead of asking. State what you
found before moving on.

Example: Instead of "What does the current onboarding flow look like?" →
explore the codebase, then: "I found the current flow in `src/onboarding/` —
it has 3 steps with drop-off tracking on step 2. Does that match your
understanding?"

Extract the current-state answer, not the code: file paths, symbols, and
implementation detail inform your understanding but do not cross into the
brainstorm artifact, which stays at the problem-and-direction level.

**Always carry a recommendation:** Never ask a cold, open-ended question. Every
turn states your read — either an interpretation with its redirect invite ("It
sounds like X — is that right?") or a question paired with your recommended
answer ("Gate on role or on plan? I'd gate on role, because the plan can change
mid-session — agree?"). A question without a POV pushes the work the interview
exists to do back onto the user.

**One question at a time:** Never batch questions. One interpretation, or one
question-with-recommendation — not both. The turn ends on its invite ("is that
right?" / "agree?"). Do not add a second question after it.

**Summarize before advancing:** Before moving to the next topic, summarize
what was learned and confirm with the user.

### Adaptive Deepening

Probe further when answers are:

| Signal | Response |
|--------|----------|
| Vague | Propose an interpretation: "It sounds like X — is that right?" |
| Assumed | Ask for evidence: "How do you know? What data supports this?" |
| Conflated | Separate: "Those sound like two different things. Which one matters more?" |
| Solution-first | Redirect: "Before the solution — what problem or opportunity do you see?" |
| Overly broad | Narrow: "Who specifically? Which case matters most?" |

### Path Differences

**Greenfield path:** Adaptive deepening applies. When the user genuinely
doesn't know, mark as TBD and move on. Not all unknowns block advancement.

**Relentless path:** Push once more before accepting any TBD on Topics 1 and 2.
"You said you're not sure — what's your best guess, even if uncertain?" Only
mark TBD after a genuine second attempt. Topic 3 (success criteria) follows
greenfield rules — genuine uncertainty there is acceptable.

### Topics

#### Topic 1: Context and Motivation

Walk the decision tree for this topic: start with what triggered this brainstorm,
then resolve dependent branches (current state, timing) in the order they emerge.

**Opening branch:** What triggered this brainstorm?

Depending on the answer, explore dependent branches:
- Triggered by a problem: What is the current state? Who is affected? How often?
- Triggered by an opportunity: What changed to make this possible now? What exists today?
- Triggered by a constraint: What does that constraint prevent? What would removing it enable?

**Codebase trigger:** If the discussion touches existing features, systems, or
flows — explore the codebase to map current state before asking the user about it.

**Deepen when:**
- Vague motivation: "Something feels off" → propose: "It sounds like [X] is causing friction — is that right?"
- Solution-first: user describes what to build → redirect: "Before the solution — what problem or opportunity do you see?"
- Assumed urgency: "We need this ASAP" → ask what happens if you wait a month
- No current state: user jumps to the future → explore codebase or ask what exists today

**Sufficient when:**
- Clear trigger or motivation articulated
- Current state understood (what exists, what does not)
- Timing rationale clear or explicitly unknown

**TBD weight:** High. A TBD on motivation means diverge has no anchor. Relentless
path: push once more before accepting. Greenfield path: flag the gap explicitly
before advancing.

#### Topic 2: Constraints and Boundaries

Walk the decision tree for this topic: start with what is off the table, then
resolve dependent branches (what must be preserved, who has veto power) based
on answers.

**Opening branch:** What is definitely off the table?

Depending on the answer, explore dependent branches:
- Technical constraints: What does that rule out? What does it still allow?
- Budget/time constraints: Does that change the scope of what's worth exploring?
- "No constraints": probe — budget? timeline? team size? technical stack? political?

**Deepen when:**
- "No constraints" → "What would your manager/team/users reject?"
- Hidden constraints → "What would make this dead on arrival?"
- Contradictory constraints → surface the tension, ask which takes priority
- Only hard constraints mentioned → ask about soft preferences too

**Sufficient when:**
- Hard constraints identified (non-negotiable boundaries)
- Soft constraints identified (preferences that can flex)
- Key stakeholders named or explicitly noted as absent

**TBD weight:** High. Constraint TBDs mean diverge generates infeasible alternatives.
Relentless path: push once more before accepting. Greenfield path: flag explicitly —
note which alternatives may be affected.

#### Topic 3: Success Criteria

Walk the decision tree for this topic: start with what success looks like, then
resolve dependent branches (how to evaluate, what failure looks like).

**Opening branch:** If this brainstorm succeeds, what do you walk away with?

Depending on the answer, explore dependent branches:
- Output-focused: How will you evaluate the chosen direction?
- Feeling-focused ("I'll know it when I see it"): ask for one concrete signal
- Multiple criteria: Which one wins when they conflict?

**Deepen when:**
- "I will know it when I see it" → ask for one concrete signal
- Multiple competing criteria → ask which one wins when they conflict
- No measurable outcome → "If we revisit in 3 months, how do we judge this?"
- Only positive criteria → ask what failure looks like too

**Sufficient when:**
- At least one concrete success signal defined
- Decision criteria clear enough to evaluate alternatives against
- User understands what "done" means for this brainstorm (a direction, not a plan)

**TBD weight:** Low. Genuine uncertainty on success criteria is acceptable —
diverge often clarifies what "good" looks like. Mark TBD, carry forward to
converge for evaluation.

### Quality Gate

Before advancing to diverge, confirm:

- [ ] Motivation is understood (why now, what triggered this)
- [ ] Current state is mapped (what exists today — from codebase or user)
- [ ] Hard constraints are identified
- [ ] Success criteria defined or explicitly TBD (carried forward to converge)
- [ ] Open TBDs logged with topic and weight
- [ ] User has confirmed the summary

Present a summary and confirm before advancing to diverge. Only proceed after
confirmation.

## Guidelines

**DO:**
- Detect entry state and reflect it in how you open — not as a label, but as framing
- Propose your interpretation, let the user confirm or redirect
- Explore the codebase when current-state questions can be answered that way
- Walk the decision tree within each topic — let answers drive the next branch
- Push once more on Topics 1 and 2 TBDs before accepting on relentless path
- Log open TBDs with their topic weight before advancing

**DON'T:**
- Follow scripted question lists regardless of answers
- Ask any question without attaching your recommended answer — every turn
  carries a POV, whether an interpretation or a question-with-recommendation
- Ask about current state when the codebase can answer it
- Accept motivation or constraint TBDs without a second push on relentless path
- Move past the quality gate without user confirmation
- Add a second question after the interpretation invite
- Repeat "stress-test" or "pressure-test" as labels throughout the response
