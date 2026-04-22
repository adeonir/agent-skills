# Architecture

Map components, data flow, and patterns based on resolved requirements
and trade-off decisions.

## When to Use

Load after all trade-off decisions are confirmed. Do not produce architecture
diagrams before key decisions are resolved.

## Component Mapping

Identify the building blocks of the system:

1. **Entry points**: where requests or events originate (API gateway, message
   broker, event source, scheduled trigger)
2. **Services or modules**: units of logic that process, transform, or
   coordinate data
3. **Storage**: databases, object stores, caches, queues — one entry per
   distinct store
4. **External dependencies**: third-party APIs, identity providers, CDNs,
   notification services

For each component, state:
- What it does (one sentence)
- What it receives and what it produces
- Which trade-off decision determined its inclusion

## Text Diagram Format

Use ASCII block diagrams. Boxes for components, arrows for data flow,
labels on arrows for the operation type.

```
[Client] --> [API Gateway] --> [Auth Service]
                  |
                  v
            [App Service] --> [Primary DB]
                  |               |
                  v               v
            [Queue]         [Read Replica]
                  |
                  v
            [Worker] --> [Object Store]
```

Rules:
- Left-to-right or top-to-bottom layout
- Label arrows when the operation type is not obvious
- Group components by layer (client, gateway, service, storage)
- Async flows use `-->` with a note, not a different arrow type

## Data Flow Narratives

After the diagram, describe the main flows in prose:

**Happy path**: step-by-step through the diagram for the primary use case.
**Failure path**: what happens when a component is unavailable.
**Scale path**: how the system handles a 10x increase in load.

Keep each narrative to 3-5 steps. If a flow needs more, it signals a
missing component or an architecture that is too complex for the requirements.

## Patterns

State the architectural pattern explicitly. Common patterns and when they fit:

| Pattern | Fits when |
|---------|-----------|
| Monolith | Small team, single deployment unit, low operational overhead priority |
| Modular monolith | Growing team, domain boundaries clear, not yet at service-scale |
| Microservices | Independent scaling needs, team autonomy priority, operationally mature |
| Event-driven | Loose coupling required, async processing dominant, audit trail needed |
| CQRS | Read and write patterns diverge significantly, reporting load is high |
| Read replica | Read-heavy workload, geographic distribution, reporting queries |
| Queue-based worker | Background processing, rate limiting, decoupled producers/consumers |

Multiple patterns can apply. Name all that are present.

## Observability Notes

For each component, note the minimum observable signals:

- **Metrics**: what to measure (request rate, error rate, latency, queue depth)
- **Logs**: what to record (request ID, user ID, error context)
- **Traces**: where distributed tracing should span (across service boundaries)

## Quality Gate

Before loading `output.md`, verify:

- [ ] All resolved decisions are reflected in the component list
- [ ] Data flow is traceable from entry point to storage
- [ ] Failure paths are documented for critical flows
- [ ] Architectural pattern is named
- [ ] Observability signals are identified

## Next Steps

Present the architecture to the user for confirmation. When approved,
load [output.md](output.md) to produce the system brief.
