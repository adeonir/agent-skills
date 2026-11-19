---
name: storytelling
description: "Creates or revises the story and experience direction of a site from the materials that exist: the central thesis, the tension, the arc of moments, the pacing, the order of the moments, and the role of interaction, motion, video, or scroll. Use when a site needs one idea tying content, visual, and interaction together, when pages feel generic or disconnected, or when storytelling, narrative direction, or scrollytelling comes up. Not for visual identity, wireframes, storyboards, page layout, final copy, building the experience, code review, or auditing a built UI."
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

**Step 1. Load the context.** Load [context.md](references/context.md). Find the materials, settle the role of each site, and detect the state the work starts from. Done when each material found has a kind, each site has a role, the state is known, and, with a project site, the work is marked evolve or new vision from the request or the user's answer.

**Step 2. Assess the current experience.** When a project site exists, describe what it delivers today: read the code in the repository for structure and content, and when the user supplied an address for the site, also render that address for what only the rendered page shows — pacing, scroll behavior, and how sections connect. Never start a server to render. For each section in visitor order, what it communicates and whether it connects to the previous one or stands apart, tagged with its source: `(rendered)` or `(code)`. Observations only; no concept exists yet to judge against. When no address was supplied or the address does not render, record what could not be assessed and why. Without a project site, skip this step. Done when every section has a tagged observation and, without a render, the limit is recorded, or the step was skipped.

**Step 3. Define the concept.** Write the thesis, the tension, and the feeling from the materials, and from the assessment only when the work evolves the current site. Where a material already states the message, the audience, or the objectives, use them and add only what the materials lack. A prior document's concept is the starting claim: confirm, adjust, or replace it. Done when all three entries are written.

- Thesis: one sentence the experience asserts.
- Tension: what the visitor believes or feels on arrival that the experience must change.
- Feeling: what the visitor feels and understands on leaving.

**Step 4. Shape the arc.** Order the moments from tension to resolution, across one page or several. Each moment names what the visitor should feel or understand and its pace: peak (the moment that carries the weight of the story) or breather (the room before or after a peak). Neighboring moments on the same page alternate their pace; two neighbors share a pace only when the intent of the second says why. Each moment also names what leads to the next: what it leaves in the visitor that pulls them on, such as a question left open or a promise the next moment keeps; the last moment names what it leaves the visitor to do. When the arc spans pages, group the moments under the page that carries them; for every page after the first, name what it carries from the arc, such as the tension restated, so the story holds for a visitor who lands there directly. The story sets the number of moments; merge two moments that carry the same intent. Done when every moment has an intent, a pace, and a lead to the next, neighbors alternate or the intent justifies the repeat, every moment sits under a page and every page after the first carries an entry when the arc spans pages, and no two moments share an intent.

**Step 5. Direct the experience.** Name each place an interaction earns a role in the story: what the visitor does, in words of intent, and what it makes them feel or understand, such as "the visitor undoes a step and feels that nothing is lost"; never a control, a widget, or a feature. Name the visual mood the story needs, in words. Name the moments where movement (motion, video, or scroll) serves the story and the role at each, such as revealing in stages or holding the scroll; a story that needs none says so and gives the reason. If the arc or the experience cannot carry the concept, return to Step 3. Done when every Experience entry is written and the arc and the experience carry the concept.

**Step 6. Recommend.** When a project site was assessed or a visual identity exists, record what to preserve, what to reinterpret, and any conflict between the visual identity and the concept or the current experience. Recommendations stay in the document; the skill edits no existing artifact, code, or identity. Done when each recommendation names its subject, or the section is None because neither exists.

**Step 7. Write the document.** Read [storytelling.md](assets/storytelling.md) and follow its structure; its MUST NOT list names what never appears in the document. State each entry as it stands, in present tense. When a prior document exists, revise it in place: keep every section the new materials do not touch and re-check each recorded claim against them. Set `Status:` to `draft` when the content changes; only the user sets `agreed`. Set `Created:` on the first write and `Updated:` on every write, in the list under the title. Then run `python3 <this-skill>/scripts/check_storytelling.py docs/design/storytelling.md`, with `<this-skill>` resolved to the directory this `SKILL.md` was read from. Fix every ERROR; for each WARN on neighbors that share a pace, make the intent of the second say why or alternate the pace. Re-run until it reports no ERROR. Then re-read the document against the MUST NOT entries the script cannot check: a layout, grid, or wireframe described in words, a named typeface or palette, final copy, requirements or features, sibling artifact names outside References, the same fact in two sections, and the history of a decision. When a fix changes the content of an entry, return to the step that produced it. Done when the script reports no ERROR and the re-read finds no MUST NOT entry violated.

**Step 8. Report.** Report the path, what the document holds in one to three sentences — what changed, on a revision — and the open questions it carries. Never paste the document. Done when the report is sent.

## Host metadata

`agents/openai.yaml` carries the display name and short description for hosts that show skills; no step loads it.

## Guidelines

- Ask one question per message, and only when discovery or the concept needs the answer. Record an unanswered item under Open Questions instead of guessing.
