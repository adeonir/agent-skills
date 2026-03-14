---
name: {{document-name}}
created: {{YYYY-MM-DD}}
---

# Design Doc: {{System Name}}

## 1. Context & Scope

{{What is being built and the landscape where it exists. This isn't a requirements doc—keep it succinct. The goal is that readers are brought up to speed, but some previous knowledge can be assumed and detailed info can be linked to. This section should be entirely focused on objective background facts.}}

---

## 2. Goals & Non-Goals

### Goals

- **{{Goal name}}:** {{Measurable objective the system must achieve}}
- **{{Goal name}}:** {{Measurable objective the system must achieve}}

### Non-Goals

- {{Thing that could reasonably be a goal but is explicitly chosen not to be goals. Note: non-goals aren't negated goals like "The system shouldn't crash", but rather things that could reasonably be goals. A good example would be "ACID compliance"—when designing a database, you'd certainly want to know whether that is a goal or non-goal.}}

---

## 3. Design

### Overview

{{High-level implementation strategy and key design decisions with emphasis on the trade-offs that were considered during those decisions.}}

### System Context Diagram

```mermaid
{{System-context diagram showing the system as part of the larger technical landscape. This allows readers to contextualize the new design given its environment that they are already familiar with.}}
```

### APIs

{{If the system exposes an API, sketch it out here. Withstand the temptation to copy-paste formal interface or data definitions—focus on the parts that are relevant to the design and its trade-offs.}}

### Data Storage

{{If the system stores data, discuss how and in what rough form. Again, avoid copy-pasting complete schema definitions—focus on the parts relevant to design trade-offs.}}

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
