# Independent Critics

Judge each built part through three separate views of its rendered result.

## When to Use

Read before creating critic agents or interpreting their verdicts.

## Isolation

Create a new agent for each critic and each round without the builder's conversation history. Use a fresh-context option when the environment provides one. If native agents cannot isolate context, use a separate process only when the available tools and permissions support it. Report the limitation if neither route works; three self-reviews do not replace independent critics.

Write each critic's instructions for the current target. Send only its assigned basis and the relevant rendered evidence. Keep source files, the builder's explanation, the A/B provenance map, and the other verdicts out of its context. Run the three critics in parallel when supported, then wait for all three.

## Roles and verdicts

| Critic | Receives | Judges |
| --- | --- | --- |
| Request | User's objective and rendered result | Whether the result fulfills the request; ignore aesthetics |
| Design system | Agreed design system and rendered result | Observable adherence to the system; ignore whether it looks attractive |
| Visual | Reference criteria and blind A/B evidence | Whether the result beats the reference on the stated mechanisms; ignore request fulfillment |

Each critic returns `APPROVED` or `REJECTED`, the observed evidence for the verdict, and at most one largest gap. Approve only when the evidence supports that critic's assigned basis; insufficient evidence cannot support approval. Do not assign numeric scores. The visual critic chooses A or B; approve only when it chooses the result. A tie is a rejection. The coordinator keeps the A/B map and translates the visual verdict after the critic returns it.

When no design system exists, settle an explicit basis for the design-system critic before construction. Do not present an ungrounded verdict as one of three approvals.
