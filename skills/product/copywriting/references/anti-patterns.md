# Anti-Patterns

Catalog of copy failure modes — the dead language, hollow structures, and
machine tells that make writing read as generic or AI-generated. Each rule
pairs a recognizable failure with the smallest fix and a fail/pass example.

## When to Use

Composed by the `write`, `refresh`, and `revoice` workflows to avoid known
failure shapes while authoring, and by `critique` / `audit` as the failure-mode
lens when judging existing copy. This file owns the slop catalog; voice and
proof craft live in [voice.md](voice.md), prose tightening in
[editing-sweeps.md](editing-sweeps.md), clarity craft in
[ux-writing.md](ux-writing.md).

## Categories

Jump-table — each links to its rule section below.

- [Dead Words](#dead-words) — marketing adjectives and verbs the eye slides off
- [Dead Structures](#dead-structures) — hollow rhetorical shapes that perform insight
- [Punctuation and Rhythm](#punctuation-and-rhythm) — machine cadence tells
- [AI Copy Tells](#ai-copy-tells) — reflex openers, closers, and template phrasing
- [Proof and Claim Failures](#proof-and-claim-failures) — claims that assert instead of show

## Rule Template

ALWAYS use this exact template structure:

````markdown
### {rule-id-kebab-case}
**Category:** {category name from above}
**Severity:** {error | warning}
**Check:** {prose description of what to detect — one or two sentences}
**Fix:** {what to do instead}
**Example fail:**
```text
{minimal copy line that triggers the rule}
```
**Example pass:**
```text
{minimal copy line that satisfies the rule}
```
````

## Two Kinds of Check

A rule's Check is one of two kinds, and critique and audit treat them
differently:

- **Deterministic** — the Check reduces to a presence or a count: a listed word
  appears, a known opener matches, more than one em-dash in a paragraph. It has
  a definite answer — scan for it; it either fires or it does not.
- **Perceptual** — the Check needs a holistic read: "performs insight",
  "could sit on any competitor's page", "reads as a template". Weigh it by eye;
  reasonable readers can disagree at the margin.

Copy tells skew perceptual. Even a rule that looks deterministic is really about
a shape, not a string: the same hollow frame reappears reworded and in any
language, so a literal-string blocklist catches the example and never the
family. Learn the shape. write avoids both kinds while drafting; critique and
audit report both.

## Dead Words

### dead-marketing-words
**Category:** Dead Words
**Severity:** warning
**Check:** Copy leans on marketing adjectives and hype verbs that every site
uses — passionate, results-driven, innovative, cutting-edge, world-class,
best-in-class, seamless, robust, synergy, holistic, disruptive, game-changing;
verbs leverage, unlock, elevate, supercharge, empower, revolutionize, transform.
The reader's eye slides off them because they carry no information.
**Fix:** Replace the word with the specific thing and what was done about it — a
named outcome, a number, a concrete detail. The replacement is a fact, not a
warmer adjective.
**Example fail:**
```text
We're a passionate, results-driven team leveraging cutting-edge tech.
```
**Example pass:**
```text
We cut deploy time from 40 minutes to 4 for 30 engineering teams.
```

### dead-phrases
**Category:** Dead Words
**Severity:** warning
**Check:** Stock filler phrases that announce nothing — "in today's fast-paced
world", "welcome to our site", "we are committed to excellence", "Let's connect",
"the fact of the matter is", "needless to say", "at this moment in time",
"let's dive in".
**Fix:** Delete the phrase. If a real next step hid behind it ("Let's connect"),
name the actual action ("Book a 20-minute call").
**Example fail:**
```text
In today's fast-paced world, we are committed to excellence. Let's connect.
```
**Example pass:**
```text
Book a 20-minute call and see your pipeline in your own data.
```

## Dead Structures

Dead words are vocabulary; these are *shapes*. A line can use only plain words
and still read as machine-written, because its skeleton is a rhetorical template
carrying no information.

### empty-antithesis
**Category:** Dead Structures
**Severity:** warning
**Check:** A contrast scaffold that sounds profound and says nothing — it sets
up a thing, negates it, then pivots to a grander thing. The negated half is a
strawman the reader never proposed; the pivot half is abstract enough to mean
anything. Recognize the move however it is worded: "not X, but Y", "it's not
about X, it's about Y", "more than X, it's Y".
**Fix:** Delete the false setup and state the real thing, anchored to a concrete
detail only this writer could say. If stripping the antithesis leaves nothing,
the line had nothing — write the actual claim.
**Example fail:**
```text
Switching to code wasn't a detour, it was a natural evolution.
```
**Example pass:**
```text
I switched to code and kept designing. Now I do both on one screen.
```

### inflated-rule-of-three
**Category:** Dead Structures
**Severity:** warning
**Check:** A triad where the third item is filler for rhythm, not information —
"design, code, and purpose", "faster, smarter, better". The cadence does the
work; the third word means nothing.
**Fix:** Keep only the items that carry weight. Two specific things beat three
where one is padding.
**Example fail:**
```text
We bring design, engineering, and passion to every project.
```
**Example pass:**
```text
We design and build the product; you ship it the same quarter.
```

### portentous-reframe
**Category:** Dead Structures
**Severity:** warning
**Check:** A one-line restatement of the previous sentence dressed as a
revelation — "And that changes everything." It adds no fact; it performs
significance.
**Fix:** Cut the reframe, or replace it with the concrete consequence it gestures
at.
**Example fail:**
```text
We rebuilt the matching engine. And that changes everything.
```
**Example pass:**
```text
We rebuilt the matching engine; searches that took 8 seconds now take 200ms.
```

## Punctuation and Rhythm

### em-dash-density
**Category:** Punctuation and Rhythm
**Severity:** warning
**Check:** More than one em-dash in a paragraph. The mark manufactures a dramatic
pause the sentence did not earn; density is the giveaway, not the single mark.
**Fix:** Default to a comma, period, or colon. Reach for an em-dash only for a
genuine aside, and rarely — at most one per paragraph.
**Example fail:**
```text
Our tool — built for teams — saves time — so you ship faster.
```
**Example pass:**
```text
Our tool saves teams time, so you ship faster.
```

### robotic-parallelism
**Category:** Punctuation and Rhythm
**Severity:** warning
**Check:** Every bullet or sentence in a group shares the same grammatical shape
and length — "Boost your X. Improve your Y. Enhance your Z." The uniform cadence
reads as generated.
**Fix:** Vary the rhythm. Let one line run long and the next land short; break
the verb-object lockstep where the content wants it.
**Example fail:**
```text
Boost your output. Improve your focus. Enhance your workflow.
```
**Example pass:**
```text
Get more done. Your day stops fragmenting into 30 open tabs.
```

## AI Copy Tells

Reflex phrasing copy reaches for because "marketing pages do this", not because
the message asked.

### borrowed-frame-opener
**Category:** AI Copy Tells
**Severity:** warning
**Check:** An opener that borrows a stock frame to set a scene — "Imagine a
world where…", "Picture this:", "In a world of…", "We live in an age where…".
The frame is generic; the reader has read it a thousand times.
**Fix:** Open on the reader's actual problem or the concrete outcome, in their
words.
**Example fail:**
```text
Imagine a world where your team never misses a deadline.
```
**Example pass:**
```text
Your sprint slips because nobody sees the blocker until standup.
```

### reveal-hook
**Category:** AI Copy Tells
**Severity:** warning
**Check:** A teaser that promises a payoff instead of stating it — "But here's
the thing…", "The best part?", "Here's the kicker:", "And it gets better."
**Fix:** State the payoff directly. The drama device delays the only sentence
that carried information.
**Example fail:**
```text
And the best part? It sets up in under five minutes.
```
**Example pass:**
```text
It sets up in under five minutes — no config file.
```

### whether-youre-list
**Category:** AI Copy Tells
**Severity:** warning
**Check:** A "whether you're A, B, or C" sweep that tries to address everyone and
so addresses no one — "Whether you're a startup, an enterprise, or a solo
founder…".
**Fix:** Name the one reader this copy is for. Breadth that names no one persuades
no one.
**Example fail:**
```text
Whether you're a startup, an agency, or a Fortune 500, we've got you covered.
```
**Example pass:**
```text
For Series A teams whose first data hire hasn't started yet.
```

## Proof and Claim Failures

### unsubstantiated-superlative
**Category:** Proof and Claim Failures
**Severity:** error
**Check:** A superlative or ranking claim with nothing behind it — "the best",
"#1", "industry-leading", "world-class" — stated as fact the reader is asked to
take on trust.
**Fix:** Replace the claim with the proof that would earn it — a number, a named
client, an award still current. See the proof hierarchy in [voice.md](voice.md).
If no proof exists, drop the claim rather than assert it.
**Example fail:**
```text
The industry's #1 best-in-class analytics platform.
```
**Example pass:**
```text
Analytics that 2,800 teams check before their Monday standup.
```

### inward-bragging
**Category:** Proof and Claim Failures
**Severity:** warning
**Check:** Confidence pointed inward at the person or company ("we are
world-class engineers") instead of outward at the work or outcome.
**Fix:** Point the claim outward — to what was shipped, for whom, with what
result. See outward vs inward in [voice.md](voice.md).
**Example fail:**
```text
We are world-class engineers who care deeply about quality.
```
**Example pass:**
```text
We ship production Rails at Acme, Globex, and Initech.
```

### generic-claim
**Category:** Proof and Claim Failures
**Severity:** warning
**Check:** A claim so broad it could appear on any competitor's page unchanged —
"we help businesses grow", "solutions that scale". It specifies no who, no how,
no how much.
**Fix:** Specify the reader, the mechanism, and the magnitude. If the line could
sit on a rival's site, it has no point of view.
**Example fail:**
```text
We help businesses grow with solutions that scale.
```
**Example pass:**
```text
We get DTC brands to a 3x return on ad spend in 90 days.
```

### feature-without-benefit
**Category:** Proof and Claim Failures
**Severity:** warning
**Check:** A feature stated with no bridge to why the reader should care — the
"so what" is missing.
**Fix:** Add the bridge ("…which means…") so the feature lands as an outcome.
**Example fail:**
```text
Real-time sync across all your devices.
```
**Example pass:**
```text
Real-time sync across your devices, so you start on your phone and finish on
your laptop without losing a word.
```
