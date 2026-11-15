# Research note: becoming developers' first choice

**Date:** 2026-11-15. **Status:** strategy proposal; every target below is a hypothesis to test, not a prediction. **Relates to:** `PRODUCT.md`, `ManjoDB-Grand-Plan.md` §1, §14, §18, §25–§26, §29; `research/competitive-landscape.md`; `research/scaling-path.md`; `DESIGN.md`.

## 1. What "No. 1" can honestly mean

Two facts frame the goal:

- **Neo4j leads the graph category** in DB-Engines' ranking (47.32 in a March 2026 snapshot) [D1]. A ranking built from popularity signals cannot be overtaken by a project that does not yet exist.
- **PostgreSQL is developers' default database**: 55.6–58.2% usage and about 65.5–66% admiration among 2025 Stack Overflow respondents (sources quote slightly different figures) [D2]. Most teams that need a graph already run PostgreSQL.

So "No. 1 overall" is not a plan. What *is* achievable, and what the evidence from other databases supports, is **being the best choice for a defined job, then expanding outward**:

> **Target position (hypothesis):** the first choice for engineers who need to *explain* relationships (impact, lineage, provenance, access) from TypeScript and agent-driven code, and who need a database they can trust to still exist, still be open, and still restore.

"First choice" is then measured on dimensions ManjoDB controls (§5), not on stars or download counts. Stars and downloads are reported, but never used as success criteria, because they can be bought, gamed, or inflated by hype.

## 2. What other databases and developer tools teach

| Project | What worked | What to be careful of | Source |
| --- | --- | --- | --- |
| **MongoDB** | A document model that matched how developers already thought; open source from the start; engineers at developer events ("thousands of small interactions") | Early critics called it a toy that lost data and could not do transactions, and multi-document transactions arrived only in 4.0 (2018). The CEO's own diagnosis: it "had won the developer heart but not the enterprise wallet" | [D3, D4] |
| **Drizzle ORM** | Schema in TypeScript, a SQL-close style, zero runtime dependencies (good for serverless and edge); 2026 comparisons recommend it for SQL-comfortable teams | Migration tooling is simpler than a competitor's. Reportedly its core team now works for PlanetScale, a sponsor-funded model | [D5] |
| **PostgreSQL** | Reliability and extensibility; a permissive license; community governance | Slow to adopt features it cannot make correct; it removed SQL/PGQ from its v19 beta for reliability (plan Appendix B) | [D2] |
| **Redis and Valkey** | The Valkey fork, a Linux Foundation project, attracted contributors quickly after Redis moved to SSPL in 2024 (18 contributors in the first month, growing to 49, per Percona) | Redis returned to AGPLv3 in 2025, yet commentary says trust did not recover. A license reversal is a lasting cost | [D6, D7] |
| **Kùzu, Gel, Dgraph, OrientDB** | Strong engineering or developer experience | Company-backed projects stalled or changed hands (see competitive note §4.1). A good product does not guarantee continuity | [C13, C24, C15, C4] in the competitive note |

**Lessons that follow:**

1. **Developer experience wins the first adopters; trust keeps them.** MongoDB shows both halves. ManjoDB's correctness-first plan matches the trust half; it must also deliver the experience half.
2. **Reputation for durability is slow to earn and fast to lose.** Do not use the word "durable" without the fault model (plan §11.3), and never ship a "preview" that loses data quietly.
3. **License changes are the most expensive mistake.** The permanent answer is to decide early, with counsel, and write it down as a commitment (§6).
4. **Sponsorship is a real model, and a real risk.** Drizzle's reported sponsor arrangement and Gel's shutdown are opposite ends. ManjoDB needs an explicit sustainability plan (§7).

## 3. The candidate identity

The brand already says *precise and trustworthy* (`PRODUCT.md`), and the Commit Lanes mark draws a relationship as a branch and a merge. The strategy should make that identity true in behavior. Five pillars, each backed by something checkable:

| Pillar | What it means | What proves it |
| --- | --- | --- |
| **Shows its work** | Every answer carries the edges that produced it; `explain` maps every clause to an operator | Evidence columns, witness paths, plan viewer |
| **Precise** | Semantics are specified, errors are typed, and diagnostics say how to fix the query | Spec corpus, usability study, error registry |
| **Open for good** | A license that will not change, no gated correctness or recovery features, neutral governance | Published commitments (§6); years of keeping them |
| **Boring to operate** | One binary, one data directory, verified restore | Backup-restore drills, `manjo check`, pilot interviews |
| **Safe for agents** | AI is an untrusted client; previews before writes; scoped tokens | LLM evaluation, MCP profile tests (plan §18) |

**Candidate one-line positions to test with developers** (not decided; wording needs real feedback):

- *"The graph database that shows its work."*
- *"Relationships, first."* (the current tagline: it describes the architecture, not the benefit)
- *"Graph queries you can read, and answers you can trace."*

The tagline question is cheap to test: show each line to 10 to 15 engineers from the target audience and ask what they think the product does.

## 4. Beachheads and expansion

A **beachhead** is the first narrow group the product serves better than anything else. A product earns the next group only after the first is happy.

| Order | Beachhead | Why | Competitive pressure | What it must prove |
| --- | --- | --- | --- | --- |
| **1** | **Dependency impact and lineage**, as a projection beside PostgreSQL | The plan's reference workloads (Appendix D). Small data, high pain. Low adoption cost because nothing migrates | PostgreSQL recursive queries, Apache AGE, Neo4j | H1–H4 in plan §1.2 |
| **2** | **Embedded graph for TypeScript and Rust apps** (the "SQLite for graphs" slot) | Kùzu was archived (Oct 2025) and its forks are community-run; an embedded engine also removes the "another process" objection (plan H4) | LadybugDB and Bighorn (Kùzu lineage), SQLite-based approaches | A small, stable embedded API; Node.js binding quality |
| **3** | **Agent memory and provenance** | Matches the plan's AI-native design | **Crowded:** SurrealDB, FalkorDB, Neo4j, ArcadeDB (competitive note §4.5) | Only worth entering with the *safety* differentiator, demonstrated |
| **4** | Access and entitlement *explanation* (not enforcement) | Plan D3 and D5 | Dedicated authorization services | A clear non-enforcement boundary |

**Order of expansion beyond use cases** follows `scaling-path.md`: replicas, HA, managed service, property sharding.

The embedded beachhead is a new proposal, and it should be tested before it is committed. It is attractive because it is a *vacant, recently orphaned slot*, but it adds a per-platform support surface (native builds) that a small team has to maintain. Treat it as plan experiment E-embedded: prototype the Node.js binding in M5, and decide with pilot feedback.

## 5. What "first choice" is measured by

All targets are **proposals** to be fixed in the M0 RFCs before data is collected.

| Stage | Metric | Candidate target | How measured |
| --- | --- | --- | --- |
| **Try** | Time from "I heard of it" to a first successful query on sample data | Under 5 minutes, no account, one command | Timed sessions with new users |
| **Try** | Install friction | One download or one `npm` install; no external services | Install log; support questions |
| **Learn** | Task correctness on the plan's task set (Appendix C3) without help | At least 80% on basic tasks after the short tutorial (plan §26) | Usability study |
| **Learn** | Diagnostics: repair rate from error messages alone | To be set from pilot data | Think-aloud tasks |
| **Adopt** | Time to a first useful answer from the user's *own* data | Under one working day, including import | Pilot teams |
| **Adopt** | Correctness versus the baseline | Equal answers on the reference workloads; fewer invalid states accepted | Plan §23 and the bug-injection exercise |
| **Trust** | Restore verification | 100% of releases pass backup, restore, check, and corpus equivalence | CI and release gate |
| **Trust** | Continuity | Published license and governance commitments unchanged across releases | Public record |
| **Advocate** | Unprompted recommendations among pilot teams | Counts, reported with quotes | Pilot interviews |

**Not targets:** GitHub stars, download counts, conference talks, and press mentions. Report them, but never optimize for them.

**On credibility of performance claims.** The industry's neutral instrument is LDBC's benchmarks, whose audited results exist for the Social Network Benchmark Interactive workload (most recent found: December 2025), while FinBench has none yet [D8, D9]. ManjoDB can run LDBC datasets and workloads internally from M2, publish the raw results, and consider an audit only when it is worth the cost and membership requirement.

## 6. Open source, license, and trust

`PRODUCT.md` records that everything is open source. The plan (§29) leaves the *license itself* undecided. Evidence from the field says this decision is the single most important trust signal, and the most expensive to reverse.

| Option | Open source (OSI)? | Examples in the field | Trade-off |
| --- | --- | --- | --- |
| **Apache-2.0** | Yes | OrientDB, ArcadeDB, Dgraph (v25), Apache AGE, NebulaGraph | Maximum adoption and an explicit patent grant. A cloud provider can host it without contributing back |
| **MIT** | Yes | Kùzu (archived) | Simpler text, no patent grant |
| **MPL-2.0** | Yes | TypeDB | File-level copyleft: changes to MPL files stay open, while larger works can be combined with other code |
| **AGPL-3.0** | Yes | Redis 8 (one of its options) | Network copyleft deters hosted forks, and many companies avoid it |
| **GPLv3** | Yes | Neo4j Community | Strong copyleft; compatible with an enterprise upsell, which the field shows leads to feature gating |
| **BSL 1.1, SSPL, similar** | **No** (source-available) | Memgraph, ArangoDB, FalkorDB | Protects against hosted competition. The field shows it costs community trust |

**Candidate recommendation (needs qualified legal advice, which plan §29 already requires):**

1. **Apache-2.0** for all code, because the plan's strategy is adoption and trust, and the field's biggest trust injuries came from restriction and reversal.
2. **A written commitment** in the repository: the license will not be changed to a source-available license; backup, restore, integrity checking, and high availability are never gated behind a paid tier.
3. **DCO instead of a CLA** for contributions, so contributors keep their copyright and a unilateral relicensing becomes impractical. This is the strongest structural guard against a Redis-style reversal.
4. **Trademark policy** that protects the names (ManjoDB, Manjo, MQL, the mark) from confusing use, while permitting forks under other names. It is how the project defends its identity without restricting the code.
5. **Neutral governance as a goal.** Once there are multiple maintainers or sponsors, consider a neutral foundation (for example the Linux Foundation, which hosts Valkey and now MCP). Not before there is something to govern.

**Trade-off to accept openly.** Apache-2.0 lets a large cloud provider run ManjoDB as a service. The sustainability section below is the answer, not a restrictive license.

## 7. Sustainability: the unsolved problem

The field's failures are *continuity* failures (competitive note §4.1). "Everything open source" answers the trust question but not the funding question. Options, none yet chosen:

| Model | Evidence | Fit |
| --- | --- | --- |
| **Managed hosting** (open core cloud, with no gated features) | MongoDB's and Neo4j's model | Needs S3 (scaling note), which is far off |
| **Sponsor employs maintainers** | Drizzle's core team reportedly employed by PlanetScale [D5] | Tied to a sponsor's priorities, as Gel showed from the other side |
| **Foundation and donations** | Valkey under the Linux Foundation [D6] | Requires a visible project first |
| **Consulting, support, training** | Common for open-source infrastructure | Scales with people, not users |
| **Venture funding** | Gel ($19M raised) shut down; SurrealDB raised $44M in total [D10, C18] | High pressure to monetize, which drives license changes |

**Recommendation:** treat sustainability as an explicit workstream, with a decision at the product gate (plan §26) and a rule that no revenue model may require gating correctness or recovery features. Do not take venture funding before the license and governance commitments in §6 are public and enforceable.

## 8. What to build to earn adoption

Concrete work, ordered by what the evidence suggests matters most. This is a proposal list, not a schedule.

1. **A first-five-minutes experience.** One command to install, one to start, one to load a sample graph, one to see the first answer. Time it, and treat anything over five minutes as a bug.
2. **Docs that are tested.** Every example executes in CI (plan §29). A gallery of the reference workloads with synthetic data.
3. **An in-browser playground** running the reference evaluator (a proposed addition to plan §29), so people can try MQL with no install. The reference evaluator is already a planned permanent component (plan §9.1), which makes this comparatively cheap.
4. **The TypeScript schema workflow** (plan §7.4): the part that most resembles what developers loved about Drizzle. Make `manjo schema diff` and typed query signatures excellent before anything else in the SDK.
5. **Diagnostics as a product feature.** Error messages that name the fix, documented per code. This is where usability evidence is strongest (plan Appendix C).
6. **Migration paths in.** Importers from PostgreSQL and CSV with `--validate-only`; a Neo4j export-to-JSONL recipe (only if the competitor's export format permits it); and an honest "when to stay on PostgreSQL" page.
7. **Public trust artifacts.** The license commitment, the fault model, the restore-drill results, and the roadmap with its kill criteria. Publishing the criteria for stopping is itself a signal of seriousness.
8. **Community basics.** A friendly issue tracker, "good first issue" labels, a code of conduct, and a response-time commitment for security reports.

## 9. Risks and anti-goals

- **Do not claim "No. 1", "fastest", or "most trusted".** Earn the evidence first (plan evidence rules).
- **Do not chase the incumbent's breadth.** Neo4j and PostgreSQL win on breadth; ManjoDB wins, if at all, on a narrow job done more clearly and more trustworthily.
- **Do not chase GQL or Cypher compatibility early.** Keep the engine IR independent of the surface language (plan §8.12) and decide after the usability study. A compatibility layer is a large, permanent cost.
- **Beware hype categories.** SurrealDB has raised $44M and markets AI heavily [C18]; a small project cannot win a marketing contest and does not need to.
- **Beware vanity metrics.** Stars and downloads do not measure the five pillars.
- **The biggest risk is sustainability** (§7), not technology.

## 10. Next experiments

| ID | Experiment | Decides |
| --- | --- | --- |
| **A1** | Tagline test with 10–15 target engineers (§3) | Positioning words |
| **A2** | First-five-minutes timing on a prototype CLI (M1 onward) | Install and onboarding design |
| **A3** | Pilot interviews with 3–5 teams (plan M2), asking about license trust, an extra process, and HA needs | Beachhead order; whether S1 or S2 move earlier (scaling note §6) |
| **A4** | Embedded Node.js binding prototype (M5) | Whether the embedded beachhead is worth its support cost |
| **A5** | Legal review of license, DCO, and trademark policy | The license decision (plan §29) |
| **A6** | Sustainability options paper | A funding model before 1.0 |
| **A7** | Verify the "no TypeScript-first graph schema workflow exists" observation (competitive note §5) | Whether it can appear in public copy |

## Sources

- **[D1]** DB-Engines, *Graph DBMS ranking*. <https://db-engines.com/en/ranking/graph+dbms>
- **[D2]** Stack Overflow, *2025 Developer Survey: Technology* (PostgreSQL usage and admiration; secondary write-ups quote slightly different percentages). <https://survey.stackoverflow.co/2025/technology/>
- **[D3]** MongoDB, *From niche NoSQL to enterprise powerhouse*. <https://mongodb.com/company/blog/from-niche-nosql-enterprise-powerhouse-story-mongodbs-evolution>
- **[D4]** Sequoia Capital, *MongoDB with Dev Ittycheria: how an early pivot catalyzed an open source movement*. <https://sequoiacap.com/podcast/crucible-moments-mongodb>
- **[D5]** MakerKit, *Drizzle vs Prisma ORM in 2026*; the claim that Drizzle's core team works for PlanetScale appears in a 2026 comparison and is unverified here. <https://makerkit.dev/blog/tutorials/drizzle-vs-prisma>
- **[D6]** Percona, *Community erosion post license change: quantifying the power of open source* (Valkey contributor counts). <https://www.percona.com/blog/community-erosion-post-license-change-quantifying-the-power-of-open-source/>
- **[D7]** InfoQ, *Redis adds AGPL license*. <https://www.infoq.com/news/2025/05/redis-agpl-license>
- **[D8]** LDBC, *Social Network Benchmark*. <https://www.ldbcouncil.org/benchmarks/snb>
- **[D9]** LDBC, *Financial Benchmark (FinBench)*. <https://ldbcouncil.org/benchmarks/finbench>
- **[D10]** Gel, *Gel joins Vercel* (2025-12-02). <https://www.geldata.com/p/sunset>
- Competitive-note sources ([C#]) are listed in `research/competitive-landscape.md`.

**Limitations.**

- This is strategy from public evidence, not market research. No developers were interviewed, and no adoption data for ManjoDB exists.
- Several cited facts come from vendor posts or secondary write-ups, and the table marks which.
- The license and governance recommendations are not legal advice and need qualified counsel before any commitment is published.
- Every target in §5 is a proposal to be set and tested.
