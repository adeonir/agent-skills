---
name: storytelling
description: "Creates or revises the story and experience direction of a site from the materials that exist: the central thesis, the tension, the arc of moments, the pacing, the order of the moments, and the role of interaction, motion, video, or scroll. Use when a site needs one idea tying content, visual, and interaction together, when pages feel generic or disconnected, or when storytelling, narrative direction, or scrollytelling comes up. Not for visual identity, wireframes, page layout, final copy, building the experience, code review, or auditing a built UI."
---

# Storytelling

## Quick start

Create or revise the story and experience direction of a site in one document, `docs/design/storytelling.md`, from whatever materials the project already holds. The document states intent: what the visitor should feel and understand at each moment and the order the moments arrive in. The skill builds nothing.

```text
materials → state → assess → concept → arc → experience → recommend → document
              └ no project site: skip assess
```

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Load the context
- [ ] Step 2: Assess the current experience
- [ ] Step 3: Define the concept
- [ ] Step 4: Shape the arc
- [ ] Step 5: Direct the experience
- [ ] Step 6: Recommend
- [ ] Step 7: Write the document
- [ ] Step 8: Report
```

**Step 1. Load the context.** Load [context.md](references/context.md). Find the materials, settle the role of each site, and detect the state the work starts from. Done when each material found has a kind, each site has a role, and the state is known.

**Step 2. Assess the current experience.** When a project site exists, describe what it delivers today: read the code for structure and content, and render it for what only the rendered page shows — pacing, scroll behavior, and how sections connect. For each section in visitor order, what it communicates and whether it connects to the previous one or stands apart. Observations only; no concept exists yet to judge against. When rendering fails, ask the user how to proceed; on continuing without a render, assess from the code and record what could not be assessed and why. Without a project site, skip this step. Done when every section has an observation, or the step was skipped.

**Step 3. Define the concept.** Write the thesis, the tension, and the feeling from the materials and the assessment. Where a material already states the message, the audience, or the objectives, use them and add only what the materials lack. A prior document's concept is the starting claim: confirm, adjust, or replace it. Done when all three entries are written.

- Thesis: one sentence the experience asserts.
- Tension: what the visitor believes or feels on arrival that the experience must change.
- Feeling: what the visitor feels and understands on leaving.

**Step 4. Shape the arc.** Order the moments from tension to resolution, across one page or several. Each moment names what the visitor should feel or understand and its pace: peak (the moment that carries the weight of the story) or breather (the room before or after a peak). Neighboring moments alternate their pace; two neighbors share a pace only when the intent of the second says why. Each moment also names what leads to the next: what it leaves in the visitor that pulls them on, such as a question left open or a promise the next moment keeps; the last moment names what it leaves the visitor to do. When the arc spans pages, group the moments under the page that carries them; for a page a visitor can land on directly, name what it carries from the arc, such as the tension restated, so the story holds for that visitor. The story sets the number of moments; merge two moments that carry the same intent. Done when every moment has an intent, a pace, and a lead to the next, neighbors alternate or the intent justifies the repeat, every moment sits under a page when the arc spans pages, and no two moments share an intent.

**Step 5. Direct the experience.** Name each place an interaction earns a role in the story, and the visual mood the story needs, in words. Name the moments where movement (motion, video, or scroll) serves the story and the role at each, such as revealing in stages or holding the scroll; a story that needs none says so and gives the reason. If the arc or the experience cannot carry the concept, return to Step 3. Done when every Experience entry is written and the arc and the experience carry the concept.

**Step 6. Recommend.** When a project site was assessed or a visual identity exists, record what to preserve, what to reinterpret, and any conflict between the visual identity and the concept or the current experience. Recommendations stay in the document; the skill edits no existing artifact, code, or identity. Done when each recommendation names its subject, or the section is None because neither exists.

**Step 7. Write the document.** Read [storytelling.md](assets/storytelling.md) and follow its structure; its MUST NOT list names what never appears in the document. State each entry as it stands, in present tense. When a prior document exists, revise it in place: keep every section the new materials do not touch and re-check each recorded claim against them. Set `Status:` to `draft` when the content changes; only the user sets `agreed`. Set `Created:` on the first write and `Updated:` on every write, on the line under the title. Then re-read the written document against each MUST NOT entry; if one is violated, fix the entry, returning to the step that produced it when the fix changes its content. Done when the document is written and no MUST NOT entry is violated.

**Step 8. Report.** Report the path, what the document holds in one to three sentences — what changed, on a revision — and the open questions it carries. Never paste the document. Done when the report is sent.

## Host metadata

`agents/openai.yaml` carries the display name and short description for hosts that show skills; no step loads it.

## Guidelines

- Ask one question per message, and only when discovery or the concept needs the answer. Record an unanswered item under Open Questions instead of guessing.
