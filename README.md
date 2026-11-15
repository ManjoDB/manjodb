# ManjoDB

**Relationships, first.**

A graph-native database for tracing what's connected, and why.

> **Status: design stage.** Nothing is implemented or released. There is no code, binary, or package yet, and every interface in these documents is a proposal.

## The idea

ManjoDB is planned as a single-node graph database for questions like "if this service fails, what is affected?", "which dashboards depend on this column?", and "why does this user have access?". The design goals are:

- **Readable queries.** MQL is a small query language in which each hop names its source, relationship type, and direction.
- **Answers that show their work.** Results carry the edges that produced them.
- **Integrity.** Typed relationships, safe deletes, and unique business keys, enforced by the database.
- **Boring operations.** One binary, one data directory, and backups that are verified by restoring them.
- **Safe for AI agents.** Agents go through the same validation, authorization, and audit path as people.

None of these is a measured result. The plan states each one as a hypothesis, with the evidence that would confirm or reject it.

## What is in this repository

| Path | What it is |
| --- | --- |
| [`ManjoDB-Grand-Plan.md`](ManjoDB-Grand-Plan.md) | The architecture plan (revision 4.5) |
| [`research/`](research/) | Research notes: MQL syntax, repository structure, the competitive landscape, the scaling path, and adoption strategy |
| [`brand/`](brand/) | The Commit Lanes logo files and brand sheet |
| [`PRODUCT.md`](PRODUCT.md), [`DESIGN.md`](DESIGN.md) | Product context and the design system for the brand |

## Planned stack

A Rust engine and `manjo` CLI, TypeScript client and schema packages, and an Nx monorepo. See §5 of the plan.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

The license does not grant any right to use the names ManjoDB, Manjo, or MQL, or the logo, as trademarks (Apache-2.0 §6). A trademark policy is planned.

## Community

- [CONTRIBUTING.md](CONTRIBUTING.md): what helps most at the design stage, and how to propose a change.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): the Contributor Covenant 2.1.
- [SECURITY.md](SECURITY.md): how to report a vulnerability privately. Please do not open a public issue for one.
