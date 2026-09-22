# Dimensions

What to look for in each dimension, and where the primary source of each one lives.

## When to Use

Loaded to pick the dimensions a question touches and to know which source settles each one. Open only the dimensions the question needs; a dimension the question does not touch stays out of the report.

## Product

| Dimension | Look for | Primary source |
| --- | --- | --- |
| Domain | How the field works, its vocabulary, its actors, the flow the product enters | Standards bodies, regulators, the field's own documentation, a practitioner material the user supplies |
| Audience | Who has the problem, what they need, how they solve it today, what they say about it | Interviews and support records the user supplies, the audience's own forums and reviews, published surveys with a named method |
| Competitors and similar products | What each one offers, charges, promises, and leaves out; how it positions itself | The product's own site, pricing page, documentation, changelog, and interface |
| Visual and functional references | Interfaces, flows, and interaction patterns already solving the same job | The product itself, its design documentation, its public component library |
| Market patterns | Conventions the audience expects, defaults the field has settled on, what recent entrants changed | Several products showing the same convention, a standard, a platform guideline |
| Constraints | Legal, regulatory, platform, accessibility, brand, and contractual limits | The law or regulation, the platform's policy and review guidelines, the standard, the contract the user supplies |
| Materials | Facts, decisions, figures, and contradictions inside what the user supplied | The material itself, with its author named |

## Code

| Dimension | Look for | Primary source |
| --- | --- | --- |
| Behavior | What the code does today along the path the question names | The repository: definitions, callers, configuration, tests, data boundaries |
| History | Why the behavior exists and when it changed, only where it explains the present | Commit messages, pull requests, decision records in the repository |
| Dependencies | What each library, framework, protocol, platform, or service involved guarantees, at the version the repository uses | Official documentation and source of the dependency, matched to the version in the lockfile or manifest |
| Integration surfaces | Where new work would meet the existing code: patterns, conventions, comparable implementations | The repository |
| Constraints | Limits set by the runtime, the platform, the provider, or the dependency | Official documentation, the platform's policy, the repository's own configuration |

## Sources to prefer

- The owner of a fact over a report about it.
- The page a search result points to over its snippet.
- A source with a named author, method, or date over one without.
- The version the repository uses over the latest version, when they differ; record the difference.
- Several independent sources for a market pattern; one product is an example, never a pattern.

## Sources to mark

- A competitor's claim about itself is primary for what it offers and secondary for how well it works.
- A review, a post, or a talk is secondary even when its author is credible; record the author.
- A survey without a named method, sample, or date is secondary and its figures carry that mark.
- A model's own knowledge with no opened source is an inference, never a fact.
