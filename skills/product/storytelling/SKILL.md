---
name: storytelling
description: "Creates or revises the story and experience direction of a site from the materials that exist: the central thesis, the tension, the arc of moments, the pacing, and the role of interaction, motion, video, or scroll. Use when a site needs one idea tying content, visual, and interaction together, when pages feel generic or disconnected, or when storytelling, narrative direction, or scrollytelling comes up. Not for visual identity, wireframes, page layout, final copy, building the experience, code review, or auditing a built UI."
---

# Storytelling

## Quick start

Create or revise the story and experience direction of a site in one document, `docs/design/storytelling.md`, from whatever materials the project already holds. The document states intent: what the visitor should feel and understand at each moment, never how the page is arranged or built. Every entry is a suggestion the builder may contest. The skill builds nothing.

```text
materials → state → assess → concept → arc → experience → recommend → document
              └ no project site: skip assess
```

1. **Load [context.md](references/context.md)** — find the materials, settle the role of each site, and detect the state the work starts from.
2. **Assess the current experience** — when a project site exists, load [assessment.md](references/assessment.md) and describe what the experience delivers today. The assessment stays descriptive; no concept exists yet to judge it against.
3. **Define the concept** — write the thesis, the tension, and the feeling from the materials and the assessment. Where a material already states the message, the audience, or the objectives, use them and add only what the materials lack. A prior document's concept is the starting claim: confirm, adjust, or replace it. Present the concept as a claim and wait for the user to accept, adjust, or reject it before shaping the arc.
   - Thesis: one sentence the experience asserts.
   - Tension: what the visitor believes or feels on arrival that the experience must change.
   - Feeling: what the visitor feels and understands on leaving.
4. **Shape the arc** — order the moments from tension to resolution. Each moment names what the visitor should feel or understand and how the story paces there: pause (the visitor lingers), hold (steady), or accelerate (the story quickens). The story sets the number of moments; merge two moments that carry the same intent.
5. **Direct the experience** — name the rhythm across the arc, each place an interaction earns a role in the story, and the visual mood the story needs, in words. Decide whether movement (motion, video, or scroll) serves the story and give the reason; a story that needs none says so.
6. **Recommend** — when a project site was assessed or a visual identity exists, record what to preserve, what to reinterpret, and any conflict between the visual identity and the concept or the current experience. Recommendations stay in the document; the skill edits no existing artifact, code, or identity.
7. **Write the document** — read [storytelling.md](assets/storytelling.md). Its MUST NOT list names what stays out and never appears in the document. State each entry as it stands, in present tense, never the exchange or deliberation that reached it; a revision writes the new state, never the change. Nothing from the conversation enters the document: no "as discussed", "the user accepted", "we agreed". When a prior document exists, revise it in place: keep every section the new materials do not touch and re-check each recorded claim against them. Set `status` to `draft` when the content changes; only the user sets `agreed`. Set `created` on the first write and `updated` on every write.

## Guidelines

- Describe intent per moment, never arrangement: no section order, grid, or wireframe.
- Leave the look to the visual identity: palette, typeface, and tokens stay out.
- Leave the mechanism to the builder: timing, easing, scroll length, renderer, library, and assets stay out.
- Ask one question per message, and only when discovery or the concept needs the answer. Record an unanswered item under Open Questions instead of guessing.
- Back every claim about the current experience with a capture or a code location; without evidence it is an open question.
