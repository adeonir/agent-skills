# Slop Catalog

Bans and cues for the edit.

## Contents

- Bans
- Word and Phrase Cues
- Pattern Cues
- False Positives

## Bans

Change every match, a single one as well as a cluster. A ban wins over the voice the draft shows. It yields only to quotations, proper names, code, the grammar of the draft's language, and a supplied writing sample. Curly quotes and Title Case also yield to a house style.

**Em dashes.** Not a default rhythm crutch. The same applies to en dashes and hyphens used as dashes (" - ", "--"), and to parentheses that hold an aside in place of a dash. Replace every such dash or parenthetical aside with a period or a comma, a single one as well as a cluster. Keep a dash the grammar of the draft's language requires, such as the dash that opens a line of dialogue in Portuguese, a parenthesis that holds a definition, an abbreviation, or a reference, and punctuation matched to a supplied writing sample.

**Chat leftovers.** A greeting, praise, offer, or sign-off from a chat tool left in text that should stand alone: "Great question!", "Certainly!", "I hope this helps", "You're absolutely right", "Would you like me to…". Tool citation markers such as `oaicite`, `contentReference`, and `[cite: 1]`. Template text such as "I hope this message finds you well" or "[Describe the section here]". Remove the wrapper and keep the content. Never fill a placeholder; leave it and list it as open in What changed. Leave a link target unchanged and list a tracking parameter such as `utm_source=chatgpt.com` as open.

**Emphasis crutches.** "Full stop.", "Period.", "Let that sink in.", "Make no mistake", "This matters because", "Here's why that matters", "every. single. day.", and a single word in capitals for stress. They add no meaning. Delete them.

**Throat-clearing openers.** "Here's the thing," "Here's what I mean," "Here's how:" "Here's the breakdown:" "Let me be clear," "The uncomfortable truth is." Cut them and state the point.

**Faux-insight setups.** "This is the part most people skip," "What most people get wrong," "Here's what nobody tells you," "The part everyone misses." These flatter the writer as the lone expert. Cut the setup and make the claim stand on its own. "The part everyone misses: distribution is the real moat" becomes "Distribution is the main competitive advantage."

**Weasel attribution.** "Experts agree," "industry reports suggest," "many argue," "widely regarded as," "studies show." Name the source or cut the claim; never invent one. When the draft carries no source, cut the claim, list the cut in What changed, and invite the writer to restore it with a source.

**Binary contrasts.** "This is not X. It's Y." / "The question isn't X, it's Y." / "It's not just X but Y." / "stops being X and starts being Y" / "doesn't mean X, but actually Y" / "is about X but not Y" / "Stop X. Start Y." / "Y rather than X". The ban applies when nobody in the draft or among its readers holds X. State Y directly and drop the negation. "The question isn't the model. It's the eval." becomes "The eval matters more than the model."

**Stacked hedges.** "Could potentially," "might arguably," "in some cases it may." Keep at most one qualifier, and only when the uncertainty is real. "It could potentially be argued that the policy might affect outcomes" becomes "The policy may affect outcomes."

**Decorative formatting.** Decorative emoji in headings or body text, bold sprinkled mid-sentence for emphasis, bold on every proper noun or acronym, and headings in Title Case. Write headings in sentence case and keep the capitals of proper nouns.

**Curly quotes.** Typographic quotes and apostrophes (“ ” ‘ ’) in a target written with straight quotes, such as Markdown source, plain text, code comments, or English technical documentation. Use straight quotes there. Keep the quote marks the draft's language requires, such as « » or „ “, and the ones a supplied writing sample uses.

**Fake-profound kickers.** Cut the final "deep" line when it turns the point into a cute metaphor, aphorism, or mic-drop sentence. Do not rewrite it into a better metaphor. Do not preserve the rhythm. Delete it, then end on the clearest concrete sentence already in the draft. If the ending needs more closure, add a plain takeaway or next action.

**Summary-recap endings.** "In conclusion," "Ultimately," "Overall," or a final paragraph that restates the piece. The same applies to the fixed close "Despite its…, X faces several challenges" followed by a generic outlook. The preceding text already gave the summary. End on the last concrete point, takeaway, or next action instead.

## Word and Phrase Cues

Cut a word or phrase only when it is empty, inflated, part of a pattern cluster, or unsupported by context. Keep valid technical terms, factual qualifiers, quoted examples, proper names, and deliberate voice.

**High-risk words and phrases:** delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, paradigm shift, game changer, this is huge, this changes everything, tapestry, realm, beacon, multifaceted, meticulous, intricate, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving, crucial, pivotal, vibrant, enduring, interplay, showcase, underscore as a verb, garner, bolster, enhance, key as an adjective, additionally at the start of a sentence.

**Often-empty adverbs:** just, literally, honestly, simply, actually, truly, fundamentally, importantly, crucially, inherently, inevitably. Cut them when they add nothing. Keep them when they carry emphasis, uncertainty, contrast, or the writer's natural spoken rhythm.

**Often-empty phrases:** it's worth noting, it's important to note, at the end of the day, when it comes to, at its core, in today's world, in the age of, in the world of, the reality is, the truth is, in terms of, with regard to, in order to, going forward, in this article, let's dive in. Cut them when they delay the point. Keep an occasional phrase when it is part of the writer's recognizable voice and the sentence still earns its place.

**Lazy extremes:** every, always, never, everyone, everybody, nobody. They claim an authority the draft has not earned. Keep one when the draft can support it; otherwise name the specific case it stands for.

**Business jargon:** navigate becomes handle or address; unpack becomes explain or examine; lean into becomes accept or embrace; landscape becomes situation or field; double down becomes commit or increase; deep dive becomes analysis; take a step back becomes reconsider; moving forward becomes next; circle back becomes return to or revisit; on the same page becomes aligned or agreed.

**Stiff synonyms:** authored becomes wrote; relocated becomes moved; attempted becomes tried. Use the plain verb unless the formal one carries a real distinction.

**Abstract metaphor nouns:** substrate, wedge, vector, locus, vantage, nexus, primitive as a noun, bedrock, scaffolding as a metaphor, surface as a metaphor, paradigm, modality, gold-plating, ratchet as a metaphor, evacuate, endgame, north star, and flywheel. Replace them with the concrete mechanism, object, or action when they carry mood instead of meaning.

**Weak-verb adverbs:** significantly, deeply, effectively, seamlessly, meaningfully, thoughtfully, strategically, and carefully. Replace a weak verb and its adverb with a direct verb or a measure when the source supports one. Keep a modifier that adds real scope, manner, uncertainty, or emphasis.

## Pattern Cues

Change a match only when the context supports it.

**Colon reveals.** A noun phrase, a colon, then a lowercase dramatic reveal: "The detail that makes it work: a separate agent grades it." "The best part: it learns." Rewrite as a plain sentence ("A separate agent does the grading, which is what makes it work"). The same applies to a colon that joins two clauses mid-sentence in place of a period, a comma, or "because": "We moved the job to a queue: the API timed out" becomes "We moved the job to a queue because the API timed out." Use colons for lists, labels, examples, and quotes, never for fake drama or as a connector. Prefer sentence case after a colon unless grammar, a proper noun, a title, or code requires otherwise.

**Superficial analysis.** Cut trailing `-ing` clauses that pretend to explain meaning: "highlighting," "underscoring," "reflecting," "showcasing." "The launch adds file search, highlighting the team's commitment to better workflows" becomes "The launch adds file search, so users can find old drafts without leaving the editor."

**Importance puffery.** "Stands as a testament," "marks a pivotal moment," "plays a vital role," "solidifies its position," "underscores its significance," and lists of coverage that signal importance without a fact: "featured in," "independent coverage," "trade publications," "active social media presence." State the fact and let the reader judge whether it matters. "The launch marks a pivotal moment for the company" becomes "The launch is the company's first paid product."

**Interpretive metadiscourse.** Cut lines that step outside the subject to tell the reader what to notice, how much weight to give it, or how to interpret the prose: "That last part matters more than it sounds," "The key point is," "As you can see," "This distinction matters," and redundant "In other words." The same cut applies to lines that narrate the piece's own architecture: "The rest of this essay explains," "In this section, we'll," "As we'll see," "But that's another post," and lines about how the text was assembled: "compiled from," "anything unconfirmed is flagged rather than guessed." Keep a source credit the reader can follow. If the point is clear, delete the aside. Otherwise, replace it with support or facts already in the content.

**Fake-strong verbs.** Prefer "is" and "has" when they are clearer. "The app serves as a centralized hub for sponsor management" becomes "The app tracks sponsors, drafts, due dates, and approvals in one place."

**Feeling instead of mechanism.** Phrases such as "creates a sense of," "offers a powerful way to," "helps unlock," and "feels like" name an impression instead of an action or result. Replace them with behavior, mechanism, number, or consequence when the source supports it. Keep a real subjective judgment in personal or editorial prose.

**False agency.** An inanimate thing receives a human verb, which hides the person who acted: "a complaint becomes a fix," "a bet lives or dies in days," "the decision emerges," "the culture shifts," "the conversation moves toward," "the data tells us," "the market rewards." Name the human instead. "The team fixed it that week" is clearer than "the complaint becomes a fix." When no specific person fits, use "you" and name the action directly.

**Hidden actor.** A passive verb that hides who acted when the draft knows the actor and the actor matters: "mistakes were made," "the decision was taken to," "the release was delayed." Name the actor in an active sentence: "The platform team delayed the release." Keep the passive when the actor is unknown or irrelevant, or when the thing acted on is the subject, as in a procedure or a specification.

**Figurative verbs.** A verb used as a figure where a literal verb exists: "unlocks," "fuels," "breathes life into," "the parser chokes on," "the codebase fights you." Replace it with the literal action: "The parser fails on nested quotes." Keep conventional technical verbs such as "expects," "returns," "accepts," and "listens on," and keep figurative language that belongs to the writer's voice in personal or editorial prose.

**Metaphor in place of a claim.** A metaphor or aphorism that stands in for a claim the draft could state literally, anywhere in the text: "Shipping is a muscle," "Every line of code is a liability," "Speed is a feature." Replace it with the literal claim the draft supports, or cut it when the draft supports none. In technical, reference, legal, and factual prose, replace every one. In personal or editorial prose, keep a metaphor that belongs to the writer's voice. A metaphor in the final line falls under Fake-profound kickers.

**Narrator-from-a-distance.** Prose that reports on a scene without naming the actor or situation: "Nobody designed this," "People tend to," "This happens because," "This is why." Name the actor and situation. "You don't sit down one day and decide to work this way" is clearer than "Nobody designed this."

**Synonym cycling.** If the clear word is right, repeat it. Do not rotate terms for style. "The agent reviews the draft. The assistant scores the piece. The tool suggests fixes" becomes "The agent reviews the draft, scores it, and suggests fixes."

**Negative listing.** "Not a X. Not a Y. A Z." and the clipped tail ", no guessing" or "No X, no Y, just Z." Just say Z.

**Dramatic fragmentation.** "X. And Y. And Z." or "That's it. That's the whole thing." Use complete sentences.

**Telegraphic prose.** Sentences that drop the subject, the article, or the verb to compress the text: "Moved job to queue. Fixed parser bug. Works now." Write the whole sentence: "We moved the job to a queue and fixed the parser bug. The fix works now." A label, a table cell, a list item that is only a noun phrase, and a heading stay without a verb. Keep a fragment that is a trait of the writer's voice, and follow a supplied writing sample written in telegraphic style.

**Robotic rhythm.** Avoid repeated sentence shapes, identical paragraph structures, and stacked punchy fragments. Vary the shape only when it helps the point.

**Stacked claims.** One sentence chains independent clauses, each with its own subject, with ", and," ", which," or ", while": "We moved the job to a queue, which also let us add retries, and the dashboard now shows latency per region." Give each claim its own sentence. A cause, condition, contrast, or example attached to a claim is part of that claim and stays in its sentence, and so is a list of actions that share one subject. Keep a long chained sentence that is a trait of the writer's voice.

**Rhetorical setups.** "What if I told you...", "Think about it:", "Plot twist:", and self-answered "Question? Answer." pairs. Drop them and make the point.

**Deeper-truth setups.** "The deeper truth is," "The real lesson is," "The thing is," and "What this really means is." State the supported claim directly.

**Announced next point.** "Let's get into," "Let's unpack," "Let's look at," "Now, here's where it gets interesting," and similar narration of the next sentence. Start with the point or action instead.

**Heading repeats itself.** A heading states a point and the first sentence restates the same point in slightly different words. Keep the stronger version and begin with the next useful detail.

**Narrating a previous version.** "Earlier, I said," "As mentioned above," "In the previous section," and similar references to the draft's own history. Repeat a necessary term plainly or remove the pointer.

**Too many hyphenated pairs.** Repeated adjective pairs such as "clear, practical, and human-centered" or "fast-moving, high-impact, and end-to-end" create a polished cadence without adding detail. Keep a precise pair when it names a real distinction; otherwise use a fact or one exact adjective.

**Fake-candid opening.** "To be honest," "I'll be honest," "Let's be real," "I'll admit," and "Full disclosure" when the following sentence contains no personal admission or useful limitation. Remove the pose and keep the admission if it matters.

**Unsupported objection.** "You might be wondering," "Some people will say," or "Critics may argue" when the draft invents an objection only to answer it. State the answer directly. Keep a real objection when the text names it or needs to address it.

**Fake alternative.** "Either you get it or you don't," "There are two kinds of people," or an artificial two-option frame that hides a broader range. State the actual range or decision rule.

**False range.** "From X to Y" when X and Y are not two ends of a real scale: "from onboarding to billing to support," "from startups to sports teams." The frame claims coverage of everything in between. List the items, or name the group they belong to. Keep the frame when X and Y bound a real scale, such as sizes, dates, or versions.

**Forced triads.** Ideas arrive in threes to sound complete: "innovation, inspiration, and industry insights", or three parallel facts followed by a lesson. Keep three items when the meaning has three parts; otherwise keep the distinct ones.

**Promotional language.** "Nestled in the heart of," "boasts a," "renowned," "diverse array," "breathtaking," "must-visit," "rich" as a figure. The text reads like an advertisement. State what the thing is. "Nestled in the breathtaking hills, the town boasts a rich heritage" becomes "The town is in the hills."

**Vague connection.** "Was associated with," "in connection with," "was linked to" in place of the actual relation. Name the relation the source states: led, funded, worked for, wrote. When the source states none, keep the vague form and list it as open in What changed.

**Canned disclaimers.** "While specific details are limited," "based on available information," "not widely documented," often followed by a guess ("she likely grew up…"). State what the source does not show, or cut the sentence. Cut the guess. Keep a real limit the reader needs.

**Empty change report.** A summary of an edit that says what was kept or avoided instead of what changed: "Revised for clarity and flow," "while preserving the original meaning," "ensured adherence to the guidelines." Name what changed.

**Restating what the reader knows.** A reply that rebuilds the problem, the diagnosis, and the evidence the reader already has, with the answer in the last line. Lead with the answer and keep only the fact the reader lacks.

**Cliché imagery.** Stock fiction images: "flickered," "a voice barely above a whisper," "the air thick with the scent of," "eyes never leaving," "took a deep breath," "a low hum," "liminal," stock names such as Elara and Kael, and senses attached to abstractions ("sorrow tasted of metal"). Replace one with a detail the draft already gives, or with a plain statement of the action.

**Formatting slop.** Bullet lists where two sentences of prose would read better, lists where every item opens with a bold label and a colon, a bold label that restates its own line ("**Performance:** Performance improved"), arrows as bullets, a horizontal rule between every section, headers over two-sentence sections, and Markdown syntax in a target that does not render it. Use formatting to clarify structure, not to decorate the text. A bold lead-in that ends in a period and adds a new detail stays.

**Shorthand in prose.** Arrows, symbols, and chat abbreviations used as words in running prose: "->," "=>," "w/," "b/c," "&." Spell them out: "The job writes to the cache, then the worker reads it." Keep an acronym the draft defines or the field uses as standard, and keep shorthand inside code, commands, diagrams, and tables.

## False Positives

These limits apply to the cues.

- One formal word, punctuation mark, or pattern is not evidence by itself.
- Keep real limits, disclaimers, uncertainty, objections, alternatives, quotations, examples, proper names, and deliberate repetition.
- Keep technical uses of catalog words when they name a mechanism or field concept.
- Inspect the surrounding sentence and the pattern cluster before changing a word.
