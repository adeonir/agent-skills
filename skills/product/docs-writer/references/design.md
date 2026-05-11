# Design Doc

Document high-level implementation strategy and key trade-offs for
ambiguous design problems.

## When to Use

When creating a design document for a software system before
implementation. Design docs document the high-level implementation
strategy and key design decisions with emphasis on the trade-offs that
were considered.

**Key principle:** The decision whether to write a design doc comes
down to whether the solution to the design problem is ambiguous —
because of problem complexity or solution complexity, or both. If it
is not, there is little value in going through the process of writing
a doc.

## When NOT to Write a Design Doc

- The solution is obvious with no meaningful trade-offs
- The doc would basically say "This is how we are going to implement it" without going into trade-offs, alternatives, and explaining decision-making
- Overhead of creating and reviewing outweighs the benefits
- Compatible with rapid prototyping and iteration (though prototyping can be part of design doc creation)

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally:
> `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

```
discovery --> analysis --> drafting
```

### Phase 1: Discovery

Load [discovery.md](discovery.md) for shared interview patterns and
critical posture.

**Check Existing Context:**

Look for existing PRD at `.artifacts/docs/prd.md`.

If found: read and extract product context as starting input.

| PRD Section | Feeds Design Doc |
|-------------|------------------|
| Problem Statement | Context & Scope |
| Goals & Metrics | Goals / Non-Goals |
| Scope (MoSCoW) | Design scope |
| User Journeys | Data flow scenarios |
| NFRs | Cross-cutting concerns |

When PRD exists, ask which scope this design covers — the full system or
a specific component.

If no PRD exists: start discovery from scratch.

**Discovery Topics:**

#### Topic 1: System Overview

**Opening questions:**

- What is being built at a high level?
- What problem does it solve?
- What constraints shape the design? (technical, business, regulatory)
- What is explicitly out of scope?

**Deepen when:**

- No constraints mentioned → "Are there technical limitations? Team size constraints? Regulatory requirements?"
- Scope is vague → "What are the boundaries of this system?"
- Missing context → "How does this fit into the existing technical landscape?"

**Sufficient when:**

- Clear overview with problem context
- Constraints are identified
- Scope boundaries are defined

#### Topic 2: Architecture & Design

**Opening questions:**

- What is the high-level architecture?
- What external services does this integrate with?
- What are the key design decisions and trade-offs?
- How does data flow through the system?

**Deepen when:**

- No integration points mentioned → "Does this read from or write to any existing system?"
- Architecture is hand-waved → "How does the rest of the system handle similar problems?"
- No trade-offs discussed → "What options were considered? Why this choice?"

**Sufficient when:**

- Architecture direction is clear
- External services and integrations are identified
- Key trade-offs are documented
- Data flows can be diagrammed

#### Topic 3: Cross-Cutting Concerns

**Opening questions:**

- What security concerns exist?
- Are there regulatory requirements? (LGPD, GDPR, HIPAA, etc.)
- How will the system be monitored?
- What testing approach is planned?

**Deepen when:**

- Security ignored → "How is authentication handled? What about data at rest?"
- Compliance hand-waved → "What specific regulations apply?"
- Observability missing → "How will you know if the system is working?"

**Sufficient when:**

- Security approach is defined
- Compliance requirements are identified (or explicitly none)
- Observability strategy is clear

### Phase 2: Analysis

Synthesize discovery into technical analysis:

1. Map system boundaries and external integrations
2. Design system context diagram
3. Identify key design decisions and evaluate alternatives
4. Document trade-offs explicitly
5. Identify cross-cutting concerns
6. Present analysis to user for feedback before drafting

**Architecture Evaluation:**

For key decisions, consider:

- Complexity vs. maintainability
- Performance vs. development speed
- Flexibility vs. simplicity
- Build vs. buy
- Vendor lock-in vs. managed services

### Phase 3: Drafting

Use the template below. Load [quality.md](quality.md) before presenting
the draft to the user.

## Design Doc Template

ALWAYS use this exact template structure:

````markdown
---
name: {{document-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: draft
sources: []
---

# Design Doc: {{System Name}}

## 1. Context & Scope

{{What is being built and the landscape where it exists. This isn't a requirements doc — keep it succinct. The goal is that readers are brought up to speed, but some previous knowledge can be assumed and detailed info can be linked to. This section should be entirely focused on objective background facts.}}

---

## 2. Goals & Non-Goals

### Goals

- **{{Goal name}}:** {{Measurable objective the system must achieve}}
- **{{Goal name}}:** {{Measurable objective the system must achieve}}

### Non-Goals

- {{Thing that could reasonably be a goal but is explicitly chosen not to be a goal. Note: non-goals aren't negated goals like "The system shouldn't crash", but rather things that could reasonably be goals. A good example would be "ACID compliance" — when designing a database, you'd certainly want to know whether that is a goal or non-goal.}}

---

## 3. Design

### Overview

{{High-level implementation strategy and key design decisions with emphasis on the trade-offs that were considered during those decisions.}}

### System Context Diagram

```mermaid
{{System-context diagram showing the system as part of the larger technical landscape. This allows readers to contextualize the new design given its environment that they are already familiar with.}}
```

### APIs

{{If the system exposes an API, sketch it out here. Withstand the temptation to copy-paste formal interface or data definitions — focus on the parts that are relevant to the design and its trade-offs.}}

### Data Storage

{{If the system stores data, discuss how and in what rough form. Again, avoid copy-pasting complete schema definitions — focus on the parts relevant to design trade-offs.}}

### Data Flow

```mermaid
{{Optional: Sequence or flow diagram showing how data moves through the system for key scenarios}}
```

---

## 4. Alternatives Considered

{{This section lists alternative designs that would have reasonably achieved similar outcomes. The focus should be on the trade-offs that each respective design makes and how those trade-offs led to the decision to select the current design.}}

| Decision | Chosen | Rejected | Reasoning |
|----------|--------|----------|-----------|
| {{what was decided}} | {{what was chosen}} | {{what was rejected}} | {{trade-offs and why this choice}} |
| {{what was decided}} | {{what was chosen}} | {{what was rejected}} | {{trade-offs and why this choice}} |

---

## 5. Cross-Cutting Concerns

{{Ensure cross-cutting concerns such as security, privacy, and observability are taken into consideration. These are often relatively short sections that explain how the design impacts the concern and how the concern is addressed.}}

### Security & Privacy

- {{Security concern and how it is addressed}}
- {{Auth/authz approach}}
- {{Data protection strategy}}

### Observability

- {{Monitoring approach}}
- {{Logging strategy}}
- {{Alerting critical paths}}

### Compliance

- {{Regulatory requirements and how they are met}}
- {{Data handling policies}}

---

## 6. References

- {{Link to PRD, if exists}}
- {{Link to relevant ADRs}}
- {{Link to external documentation or prior art}}
````

## Design Doc Schema

6 sections matching the template:

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 1. Context & Scope | What is being built and the landscape | Topic 1 |
| 2. Goals & Non-Goals | Measurable objectives and explicit exclusions | Topic 1 (or PRD) |
| 3. Design | High-level approach, diagrams, APIs, data | Topic 2 |
| 4. Alternatives Considered | Decision, choice, rejected option, reasoning | Analysis |
| 5. Cross-Cutting Concerns | Security, privacy, observability, compliance | Topic 3 |
| 6. References | Related docs, ADRs, PRDs, external links | All phases |

## Guidelines

- Focus on trade-offs — this is the primary value of a design doc
- Keep it informal — don't follow strict guidelines if another form makes more sense
- Include system-context diagrams — essential for contextualization
- Document alternatives considered — shows why the selected solution is best
- Address cross-cutting concerns — security, privacy, observability
- Keep it sufficiently detailed but short enough to be read (10-20 pages for larger projects, 1-3 pages for mini design docs)
- Update the doc when implementation reveals shortcomings

**On Diagrams:**

- Use Mermaid for version control friendliness
- System-context diagram is highly recommended
- Data flow diagrams help for complex scenarios
- Keep diagrams focused on design decisions, not exhaustive documentation

## Anti-Pattern: Implementation Manual Without Trade-offs

A doc that says "this is how we are going to implement it" without
covering alternatives, trade-offs, or decision rationale is not a
design doc — it's a task list. The value of a design doc is the
reasoning behind the choice. If there are no meaningful trade-offs,
skip the doc.

## Design Doc Lifecycle

1. **Creation and rapid iteration:** Write the doc, share with close collaborators, iterate based on feedback
2. **Review:** Share with wider audience, incorporate feedback
3. **Implementation and iteration:** Update when reality reveals issues
4. **Maintenance and learning:** Serve as entry point for future engineers

**Rule of thumb:** If the designed system hasn't shipped yet, definitely
update the doc when changes are needed.

## Output

Save to: `.artifacts/docs/design.md`

Note: Design docs are informal documents and don't follow strict
guidelines. The template provides a useful structure, but adapt it to
what makes sense for the particular project.
