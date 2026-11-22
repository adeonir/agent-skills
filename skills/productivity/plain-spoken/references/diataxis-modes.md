# Diataxis Modes

Pick one documentation mode before writing a document, and keep the document in that mode.

## When to Use

Read before writing or rewriting documentation: a tutorial, a guide, a README section, a reference page, or a conceptual page. Skip for an answer in a conversation, an incident report, or a specification.

## Pick the mode

Write one document in one mode. When the content needs a second mode, split it into a second document and link to it.

- **Tutorial** — the reader learns by doing. State what the reader will build. Make every step produce a visible result, and say what the reader should see. Give an explanation one clause and a link.
- **How-to** — the reader reaches a goal. Assume the reader is competent. Write actions only, and allow forks for different setups. Name the guide by the task: "Rotate the signing key".
- **Reference** — the reader looks up a fact. Describe only. Keep the text dry, complete, and certain. Mirror the structure of the thing described: one entry per flag, per endpoint, or per field.
- **Explanation** — the reader wants to understand why. Cover one bounded topic. Give the context: design decisions, history, constraints, and alternatives. State an opinion here and in no other mode.

## Headings

- Write each heading so it carries the point, in sentence case.
- Use one h1 per page, and never skip a heading level.
