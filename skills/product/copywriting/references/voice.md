# Voice and Proof

Voice axes, register bias, and the proof hierarchy. This craft keeps written copy sounding like someone and earning trust. The cross-referenced slop catalog of dead words, dead structures, and machine tells lives in [anti-patterns.md](anti-patterns.md).

## When to Use

Loaded by the write, refresh, and revoice workflows to set or hold a target voice that fits intent before copy lands in `copy.yaml`, and by critique and audit to judge voice and proof. Applies to any surface; calibrate intensity by context.

## Voice Axes

Pick a point on each axis and hold it across the copy.

- **Formal / Casual:** "We architect distributed systems" vs "We build the big backend that doesn't fall over."
- **Reserved / Bold:** "Comfortable at scale" vs "Handles ten million transactions a day."
- **Earnest / Dry:** "We love helping teams ship" vs "We get paid to make slow teams less slow."
- **Plain / Playful:** straight delivery vs well-placed wit. One good line beats five attempts.

## Register sets the voice

Register sets the voice, never the shape. The surface function decides what the copy must do ([surface-functions.md](surface-functions.md)). A brand register on an informational surface still explains: it does not open with the reader's outcome or close with an ask.

Register is the posture: **brand** (the words are the product) or **product** (the words serve the task). Set or confirm it, and read the matching file ([brand.md](brand.md) / [product.md](product.md)) when establishing or changing it; it calibrates the axes above:

- **Brand:** distinctive and confident; bolder in headlines, scannable in body, and action-oriented in CTAs when the surface has one. A personal site leans first person, present tense ("I build", not "Builds").
- **Product:** concise, calm, instructional; verbs first, no hype.

Read copy out loud. If it sounds like a brochure where it should instruct, or flat where it should sell, the register is wrong.

## Finding the Voice

When the voice is undefined, pull a sample the author already wrote (a post, an email, a talk transcript). That cadence is the starting point. Confirm any stated voice back in one line ("confident but warm") and use it as a filter for every line. Honor cliché allergies; words the author refuses are a voice signal.

Set the voice once and record it under `voice` in `copy.yaml`: the line, axis points, and refused words. Later sessions use that record instead of deriving a voice from the current copy. Voice must fit confirmed intent. Change it only through revoice, when the user asks.

## Proof Hierarchy

Show credibility, do not assert it. Strongest to weakest:

1. **Numbers:** "Cut deploy time from 40 minutes to 4."
2. **Named clients or employers:** "Built billing at Acme Pay."
3. **Specific projects:** "Rewrote the matching engine"; link if public.
4. **Quotes from real people:** real names and titles.
5. **Awards or recognition:** only if still current.
6. **Talks, writing, open source:** link the actual thing.
7. **Years of experience:** weakest; use only when nothing above exists.

Use this hierarchy for claims about capability, quality, or outcomes. A factual description of a subject, role, process, or project needs accurate context, not an invented result. If the strongest proof for a claim is item 6-7, the copy needs better proof, not more adjectives.

### Outward vs Inward

Confidence points outward (to the work or outcome); bragging points inward (to the person).

| Inward (arrogant) | Outward (confident) |
|---|---|
| "We are world-class engineers" | "We ship production Rails at Acme, Globex, Initech" |
| "Best-in-class design" | "Two projects won Site of the Day" |

A testimonial that could apply to anyone is not proof. "Great to work with" → "The only team we trust to touch our payment code." Cut glowing, keep specific.

## Dead language

The dead words, hollow structures, and machine tells to strip are catalogued as rules with fail/pass examples in [anti-patterns.md](anti-patterns.md). Hold the voice here; cut the slop there.
