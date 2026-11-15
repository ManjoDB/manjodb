# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Delegated for brand work: logo files are hand-authored SVG, and the brand sheet is a single static HTML page. The product itself is specified in `ManjoDB-Grand-Plan.md`: a Rust engine and `manjo` binary, plus TypeScript client and schema packages. Nothing is implemented yet.

## Users

The first users are backend and platform engineers who own an inventory of services, datasets, permissions, or evidence. That inventory already lives in PostgreSQL, YAML, or event streams. These engineers currently maintain traversal code or recursive SQL to answer impact and explanation questions, such as "if this service fails, what is affected, and why?". The second audience is AI agents and the developers who wire agents to databases, through MCP, skills, and validators.

## Product Purpose

ManjoDB is a single-node, graph-native database for applications that must answer *what is connected to what, and why*. It stores directed, typed relationships with identity and returns evidence (which edges produced an answer), not just yes/no. Success means:

- correct answers with less application code;
- fewer integrity bugs than a well-built relational baseline;
- an operational burden teams accept, usually as a rebuildable projection beside their system of record.

## Positioning

ManjoDB is a small, precise relationship database with:

- an explicit, readable query language (MQL: one clause per hop, words for direction);
- evidence-preserving results;
- enforced graph integrity (endpoint-typed relationships, safe deletes, unique business keys);
- AI-native contracts (validator loop, MCP profiles) that never bypass the database's safety model.

It deliberately does not compete on raw speed or analytics. Scale-out is sequenced after 1.0 (single node, then replicas, then HA, then sharding; see `research/scaling-path.md`), not excluded.

## Operating Context

Developers use ManjoDB from a terminal (`manjo` CLI and shell), from TypeScript code, through a schema DSL (inspired by Drizzle's ergonomics), and through AI coding agents. Studio, a database IDE, comes later. Documentation, error pages, and the npm/GitHub presence are where most first impressions happen.

## Capabilities and Constraints

- Pre-implementation. The whole product is a proposed architecture (`ManjoDB-Grand-Plan.md`, revision 4.1).
- Everything is planned as **open source**. No closed-source or commercial code is planned (confirmed 2026-10-03).
- No benchmarks, customers, adoption numbers, or performance claims exist. Never fabricate them.

## Brand Commitments

- **Names:** umbrella brand **Manjo**; database **ManjoDB**; tagline "Relationships, first."; query language **MQL**; CLI `manjo`; npm scope `@manjodb/*` (proposed, not yet secured).
- **Name origin:** "Manjo" is the nickname of a friend of the founder (from her surname, Manjavidze). She is fond of deep mathematics, which is where the idea came from. "ManjoDB" also rhymes with MongoDB.
- **Voice:** precise and trustworthy. Engineering-serious, the tone of a database you would trust with your data.
- **References the founder named as inspiration:** GraphQL, MongoDB, and Drizzle ORM.
- **Binding visual constraint volunteered by the founder:** pink or purple as the brand color family.

## Evidence on Hand

Only the architecture plan and the research notes in `research/`. There are no customers, testimonials, benchmarks, logos, or press. Any demonstration data must be labeled synthetic.

## Product Principles

1. Correctness before everything that comes after it: integrity, durability, and restore-verified backups are the product.
2. Explicit over implicit: direction, identity, and multiplicity are always visible.
3. Measured claims only: hypotheses stay hypotheses until evidence exists.
4. One canonical way: one language, one mutation pipeline, one contract for every client and every agent.
5. Small and maintainable: scope is sequenced to what a small team can keep correct.

## Accessibility & Inclusion

Diagnostics, docs, and tools must work with keyboard and screen readers, and must never encode meaning in color alone. Documentation is planned in Georgian and English. Code keywords are never translated.
