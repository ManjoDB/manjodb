# Research note: the competitive landscape

**Date:** 2026-11-15. **Status:** research input for the product gate (plan §26) and for positioning. **Relates to:** `ManjoDB-Grand-Plan.md` §1.5, §8.12, §23, §29; `research/scaling-path.md`; `research/developer-adoption-strategy.md`.

**Evidence rules.** Facts below come from the sources listed at the end, checked 2026-11-15. A figure that a vendor reports about itself is marked *vendor claim*. Where sources disagree or I could not verify something, the table says so rather than guessing. This is a landscape snapshot, not a benchmark: no competitor has been run or measured.

## 1. Summary

1. **Neo4j is the incumbent.** It leads DB-Engines' graph ranking (score 47.32 in a March 2026 snapshot, a popularity measure, not a quality measure) [C1]. Its Community Edition is GPLv3 and single-node; clustering and online backup are Enterprise features [C2, C3].
2. **OrientDB is still releasing, but its commercial era is over.** The Wikipedia infobox shows 3.2.58 dated 2026-11-09 [C4], and Maven Central listed 3.2.57 on 2026-10-06 [C5]. SAP stopped commercial support in 2021, its creator then started ArcadeDB, and Sonatype treats OrientDB as sunset for its own product [C4, C6, C7]. Details in §3.
3. **The field has a continuity problem.** In the last three years: Kùzu was archived (Oct 2025), Gel's company shut down (Dec 2025), Dgraph changed owners again (Oct 2025), and Redis relicensed twice. Several others moved to source-available licenses (§4.1–4.2).
4. **Scale-out is mostly gated or early.** Neo4j clustering is Enterprise-only; its new 100 TB-class sharding is an early-access program and keeps the graph topology on one shard; Memgraph's Raft-based HA is listed under its Enterprise tier (§4.3).
5. **"AI-native" is already crowded** (SurrealDB 3.0, FalkorDB, ArcadeDB, Neo4j all pitch AI memory or GraphRAG), so it cannot be ManjoDB's differentiator by itself (§4.5).
6. **Developers' default database is PostgreSQL** (55.6–58.2% usage and about 65.5–66% admiration in the 2025 Stack Overflow survey; sources differ on the exact figures) [C20]. ManjoDB should be positioned beside PostgreSQL, not against it.

## 2. The field at a glance

| Product | Model and query language | License | Scale-out | Health and ownership signal (verified) |
| --- | --- | --- | --- | --- |
| **Neo4j** | Native property graph; Cypher, with GQL-aligned features [C2] | Community: GPLv3. Enterprise: commercial [C2, C3] | Enterprise clustering [C2]. Infinigraph property sharding, early access (§4.3) [C8, C9] | Market leader; vendor-backed |
| **OrientDB** | Multi-model (graph, document, object, key-value); SQL with graph extensions, Gremlin [C4] | Apache 2.0 [C4] | Not verified in this pass | Community-maintained; 3.2.58 on 2026-11-09 [C4]; see §3 |
| **ArcadeDB** | Multi-model; Cypher, Gremlin, OrientDB SQL, and more [C10] | Apache 2.0 [C10] | Not verified in this pass | Created by OrientDB's founder after leaving SAP [C4, C10]; version 26.7.1 reported 2026-07-01 (one listing; verify on GitHub) |
| **Memgraph** | In-memory property graph; Cypher | Community: BSL 1.1. Enterprise: commercial [C11] | Raft-based HA listed under Enterprise in the README [C11] | Active; verify the current feature split |
| **FalkorDB** | Property graph on the Redis module system; successor to RedisGraph | SSPLv1 [C12] | Not verified in this pass | v4.20.1 reported July 2026 (one listing) |
| **Kùzu** | Embedded, columnar property graph; Cypher | MIT; repository **archived Oct 2025** [C13] | Not applicable | Forks: LadybugDB (v0.17.1, June 2026) and Bighorn (Kineviz) [C13, C14] |
| **Dgraph** | Native graph; GraphQL-flavored and DQL | Apache 2.0 from v25 [C15] | Distributed (design not re-verified here) | Sold to Istari Digital by Hypermode, Oct 2025 [C15, C16] |
| **ArangoDB** | Multi-model; AQL | Source: BSL 1.1. Community binaries: Community License, free up to 100 GB for production commercial use (wording differs between sources) [C17] | Sharding (not re-verified here) | Vendor-backed; license terms contested |
| **SurrealDB** | Multi-model; SurrealQL | Not re-verified in this pass | Distributed mode (not re-verified here) | Series A extension of $23M in Feb 2026, $44M raised in total; 3.0 released Feb 2026; vendor claims 2.3M downloads and 31k GitHub stars [C18] |
| **TypeDB** | Typed, polymorphic database; TypeQL | MPL 2.0 per the repository [C19] | Not verified in this pass | 3.0 (a Rust rewrite) released Dec 2024 [C19] |
| **NebulaGraph / TigerGraph** | Native distributed graphs | NebulaGraph: Apache 2.0. TigerGraph: commercial (DB-Engines) [C21] | Both listed as sharded (DB-Engines) [C21] | Not examined in depth |
| **Apache AGE** | openCypher inside PostgreSQL | Apache 2.0 | Inherits PostgreSQL | Active (1.7 and 1.8 for PG 17 and 18); Azure offers it as GA [C22] |
| **Amazon Neptune** | Managed property graph and RDF | Managed service | Managed | Pricing not verified here (secondary sources disagreed) |
| **Spanner Graph** | Graph on Spanner; GQL and SQL/PGQ | Managed service | Managed | Google's docs claim conformance to the minimal features of both standards [C23] |
| **Gel (ex-EdgeDB)** | Not a pure graph DB; a schema-first layer on PostgreSQL | Open source | Not applicable | **Company shut down:** announced 2025-12-02, cloud off by 2026-01-31, team joined Vercel [C24] |

## 3. OrientDB in depth

**What it is.** A Java multi-model database: graph, document, object, and key-value in one engine. Relationships are stored as direct record pointers ("RIDs"), so traversal follows pointers instead of joining [C4]. Its query language is SQL extended with graph traversal, plus Gremlin [C4]. License is Apache 2.0 [C4].

**History.** Luca Garulli wrote it in 2010, as a Java rewrite of an earlier C++ product, and OrientDB LTD sponsored it from 2012 [C4]. CallidusCloud bought the company in 2017, and SAP's acquisition of CallidusCloud was announced in January 2018 [C4]. In September 2021 Garulli left SAP and started ArcadeDB, after SAP stopped commercial support for OrientDB; in December 2024 its R&D lead, Andrii Lomakin, started a fork called YouTrackDB in JetBrains' GitHub organization. Both of those two points rest on self-published sources, so treat them as reported, not audited [C4].

**Where it stands.** Patch releases continue (3.2.57 on 2026-10-06 and 3.2.58 on 2026-11-09, per two sources) [C4, C5]. But Sonatype's release notes say that as of 2026-01-09 OrientDB is "officially sunset" for Nexus Repository, which used it as an embedded store. That is one vendor's support decision, not a project statement [C7]. The practical reading: usable and maintained by the community, with no vendor behind it.

**What I could not verify.** How OrientDB's distributed (multi-master) mode works and how well it holds up. The sources I could read do not cover it. I will not claim anything about it.

**What it teaches ManjoDB.**

1. **Direct-pointer adjacency is not new, and not a differentiator.** OrientDB and Neo4j both store relationships as pointers. ManjoDB's adjacency design (§10.3) should be justified by measurements on the reference workloads, not by "native graph storage".
2. **Multi-model breadth did not protect it.** Graph, document, key-value, and object models in one engine did not keep a corporate sponsor interested, and two forks followed. A narrow, well-explained product is more defensible than a wide one.
3. **Governance matters as much as technology.** The code stayed Apache 2.0 throughout, yet the community split three ways (OrientDB, ArcadeDB, YouTrackDB). A permissive license alone does not create a stable project. Neutral governance, a maintainer plan, and explicit continuity commitments do (see `developer-adoption-strategy.md`).
4. **A sponsor's exit is the main risk, not a competitor's feature.** OrientDB is the clearest case in the graph market of strong technology outliving its commercial home.

**Competitive posture toward OrientDB and ArcadeDB.** ArcadeDB is the active successor, Apache 2.0, and broad. It is a legitimate baseline for the usability study and benchmarks (§6). ManjoDB should not market against OrientDB itself: its users are a small, specific audience, and "we are better than the abandoned one" is not an identity.

## 4. Patterns in the evidence

### 4.1 Ownership and sustainability failures

| Project | What happened | Date |
| --- | --- | --- |
| Kùzu | Repository archived; creator Kùzu Inc. reportedly acquired by Apple (via an EU filing) [C13, C25] | Oct 2025 |
| Gel | Company shut down; team to Vercel for Python work; $19M raised; open-source code remains [C24] | Dec 2025 |
| Dgraph | Moved from Hypermode to Istari Digital; new owner says it wants Dgraph "a maintained open source project" but its roadmap was still unsettled [C15, C16] | Oct 2025 |
| OrientDB | SAP ended commercial support; creator and an R&D lead each started a fork [C4] | 2021, 2024 |

The recurring shape: a venture-backed or acquired single-company project, excellent engineering, and then a change in the sponsor's plans. The community survives only if someone forks.

### 4.2 License churn and gating

| Product | License position |
| --- | --- |
| Neo4j | Community GPLv3; clustering and online backup are Enterprise [C2, C3] |
| Memgraph | Community BSL 1.1; Raft-based HA listed as Enterprise [C11] |
| ArangoDB | Source under BSL 1.1; free production use capped at 100 GB under the Community License; sources disagree on exactly how the cap is measured [C17] |
| FalkorDB | SSPLv1, which the OSI does not recognize as open source [C12] |
| Redis | SSPL in March 2024, then the Valkey fork under the Linux Foundation, then AGPLv3 in May 2025; commentary says trust did not fully recover [C26, C27] |
| Apache-2.0 or MIT | OrientDB, ArcadeDB, Dgraph (from v25), Apache AGE, NebulaGraph, Kùzu (MIT, archived) |

**Implication.** Many graph databases gate high availability, backup, or size behind commercial terms. A project that publishes a license it will not change, and gates none of correctness, backup, or recovery, occupies a position few competitors can credibly claim. It only counts if it holds for years (see §5, and licensing options in `developer-adoption-strategy.md`).

### 4.3 Scale-out is gated, early, or partial

- **Neo4j Infinigraph** [C8, C9]: launched September 2025, claims 100 TB-plus scale (vendor claim, no independent benchmark found). It splits the cluster into one **graph shard** holding topology (nodes, relationships, labels, IDs) as a single Raft group, and **property shards** holding property values spread by hash. Traversal runs on the graph shard; property values are fetched in batches at the end of a query. The property-shard count is fixed at creation, with no automatic rebalancing in the first version, and the property-sharding feature was in an early access program. Neo4j itself calls it "not a one-size-fits-all solution".
- **Memgraph**: HA is listed under Enterprise [C11].
- **NebulaGraph and TigerGraph**: DB-Engines lists both as sharded [C21]; I did not examine their designs.
- **Key point for ManjoDB:** the best-resourced vendor's answer to scale-out is *not* a fully partitioned graph. It keeps the topology on one replicated shard and shards the bulky property data. That is also the cheapest staged path for ManjoDB (see `scaling-path.md`).

### 4.4 Standards

ISO/IEC 39075:2024 (GQL) is published [C28], and Google says Spanner Graph supports the minimal conformance features of both GQL and SQL/PGQ [C23]. PostgreSQL removed its SQL/PGQ implementation from the version 19 beta, citing reliability (plan Appendix B). Neo4j supports Cypher and GQL-aligned features [C2]. **Implication:** a standard exists and large vendors are moving toward it. This reinforces the plan's §8.12 position that the engine IR must be independent of the surface language, and that a GQL front end is a live option if MQL loses the usability study.

### 4.4b Benchmarks

The Linked Data Benchmark Council (LDBC) publishes the Social Network Benchmark and audited results exist for SNB Interactive, the most recent I found dated December 2025 (Huawei Cloud's Graph Engine Service). Its FinBench had no audited results yet, and audits require LDBC membership and a certified auditor [C29, C30]. **Implication:** LDBC datasets and workloads are the credible way to produce comparable numbers. ManjoDB can run LDBC workloads internally long before any audit.

### 4.5 AI positioning is crowded

SurrealDB 3.0 markets agent memory and "context graphs" [C18]; FalkorDB markets GraphRAG [C12]; ArcadeDB is listed as an MCP server in at least one directory [C10]; Neo4j markets vectors in the graph [C8]. **Implication:** "AI-native" is table stakes. ManjoDB's defensible AI angle is *safety and verifiability* (validate loop, preview then apply, scoped tokens, no bypass), which is a claim that has to be demonstrated, not asserted (plan §18).

### 4.6 The default database is PostgreSQL

PostgreSQL leads usage and admiration in the 2025 Stack Overflow survey [C20], and PostgreSQL itself offers recursive queries (plan [P1]) and extensions (Apache AGE). **Implication:** the first sentence of ManjoDB's pitch must say when to *keep* PostgreSQL (plan §1.5, §2).

## 5. Where ManjoDB can differentiate, and where it cannot

| Dimension | What the field looks like | ManjoDB's candidate claim (a hypothesis) | Evidence needed |
| --- | --- | --- | --- |
| **Continuity and trust** | Archives, shutdowns, owner changes, license reversals (§4.1–4.2) | A permissive license it will not change, neutral governance, and no gating of backup, recovery, or integrity | Published license and governance commitments; years of keeping them |
| **Correctness and integrity** | Constraints vary by edition and product | Endpoint-typed relationships, RESTRICT deletes, restore-verified backups, specified semantics | Lifecycle suite, crash tests, bug-injection exercise (plan H3) |
| **Developer experience** | Cypher incumbent; SQL-flavored and multi-model alternatives | A TypeScript-first schema with generated migrations, typed query signatures, precise diagnostics | Usability study and time-to-first-query (see adoption note) |
| **Evidence in answers** | Results are usually rows or paths | Edge identity and witness paths in every answer | Task correctness against baselines |
| **Operability** | Often a server plus ecosystem; HA and backup gated | One binary, one data directory, verified restore | Pilot interviews, restore drills |
| **AI safety** | Everyone pitches AI | Preview then apply writes, validator loop, scoped tokens | LLM authoring evaluation (plan §18.7) |

**Where ManjoDB should not compete before it has evidence:** breadth of features, ecosystem size, current scale, raw speed, GQL compatibility, and a "No. 1 by popularity" claim. Neo4j and PostgreSQL win all of those today.

**One unverified opening, to check before claiming it.** I found no graph database whose primary workflow is a code-first TypeScript schema with generated migrations, which is the Drizzle-style experience. That absence is from limited searching, not a survey. Verify it before it appears in any copy.

## 6. Baselines to include in the product gate

| Baseline | Why | Notes |
| --- | --- | --- |
| **PostgreSQL** recursive CTEs | The default and the plan's required relational baseline (plan §23) | Tuned, with cycle handling |
| **Apache AGE** | The "graph inside PostgreSQL" option [C22] | Tests whether an extension is enough |
| **Neo4j** (Community) | The incumbent; Cypher/GQL subset for the usability study (plan §8.12) | License is GPLv3; run as a separate process only |
| **ArcadeDB** | The active OrientDB lineage, Apache 2.0, broad | Good second graph baseline |
| **Memgraph** or **LadybugDB** | Optional: an in-memory server, and an embedded graph (the Kùzu fork lineage) | Include if the embedded wedge is pursued (see `developer-adoption-strategy.md`) |

## 7. Open questions

1. How do OrientDB and ArcadeDB handle distribution today, and how reliable is it? (Not verifiable from the sources read.)
2. SurrealDB's current license and scale-out design, which I did not re-verify.
3. Neo4j's current Community-versus-Enterprise feature split, including constraints and online backup, from its own comparison page.
4. Whether any graph database already offers a TypeScript-first schema and migration workflow.
5. Real-world adoption numbers (downloads, deployments) from independent sources. The figures above are mostly vendor claims.

## Sources

- **[C1]** DB-Engines, *Graph DBMS ranking* (German page, March 2026 snapshot: Neo4j 47.32; another snapshot showed 50.15, undated). <https://db-engines.com/en/ranking/graph+dbms>
- **[C2]** Neo4j, *Operations Manual: Introduction* (Community and Enterprise editions); Neo4j, *Label expression predicates* (Cypher/GQL conformance). <https://neo4j.com/docs/operations-manual/current/introduction/>; <https://neo4j.com/docs/cypher-manual/25/expressions/predicates/label-expression-predicates/>
- **[C3]** Neo4j community discussion, *Neo4j Community Edition limitations (deep dive)*. Secondary; not authoritative. <https://community.neo4j.com/t/neo4j-community-edition-limitations-deep-dive/71005>
- **[C4]** Wikipedia, *OrientDB* (retrieved 2026-11-11; several statements carry "citation needed" tags). <https://en.wikipedia.org/wiki/OrientDB>
- **[C5]** Maven Central listing for OrientDB 3.2.57 (2026-10-06), as reported in search results. <https://mvnrepository.com/artifact/com.orientechnologies/orientdb-distributed>
- **[C6]** OrientDB GitHub releases. <https://github.com/orientechnologies/orientdb/releases>
- **[C7]** Sonatype, *Nexus Repository 3.70.0 release notes* (OrientDB sunset for Nexus, 2026-01-09). <https://help.sonatype.com/en/sonatype-nexus-repository-3-70-0-release-notes.html>
- **[C8]** Neo4j, *Infinigraph* announcement and architecture post (the post's date metadata and byline disagree: 2026-06-04 vs 2025-09-03). <https://neo4j.com/blog/graph-database/infinigraph-scalable-architecture/>; <https://neo4j.com/press-releases/neo4j-launches-infinigraph/>
- **[C9]** Neo4j, *Property sharding in Infinigraph*. <https://neo4j.com/blog/graph-database/property-sharding-infinigraph/>
- **[C10]** ArcadeDB GitHub repository; DB-Engines ArcadeDB page (rewrite note); a DEV.co listing for the latest release. <https://github.com/ArcadeData/arcadedb>; <https://db-engines.com/en/system/ArcadeDB%3BGraphDB%3BNeo4j>
- **[C11]** Memgraph GitHub README (license split, HA under Enterprise); DB-Engines Memgraph page (BSL 1.1). <https://github.com/memgraph/memgraph>
- **[C12]** FalkorDB, *License* (SSPLv1). <https://docs.falkordb.com/references/license>
- **[C13]** The Register, *KuzuDB abandoned*, 2025-10-14. <https://www.theregister.com/2025/10/14/kuzudb_abandoned/>
- **[C14]** dbdb.io, *LadybugDB*. <https://dbdb.io/db/ladybugdb>
- **[C15]** Hypermode, *The future of Dgraph is open, serverless and AI-ready* (single Apache 2 license from v25); Istari Digital acquisition notice. <https://hypermode.com/blog/the-future-of-dgraph-is-open-serverless-and-ai-ready>
- **[C16]** Dgraph community forum, *Dgraph, Welcome to Istari*. <https://discuss.dgraph.io/t/dgraph-welcome-to-istari/20021>
- **[C17]** ArangoDB, *Evolving ArangoDB's licensing model for a sustainable future*. Sources disagree on how the 100 GB limit is measured; read the license text before relying on it. <https://arango.ai/?p=2755>
- **[C18]** SurrealDB, *Raises $23M Series A extension*; SiliconANGLE coverage, 2026-02-17. Company-reported numbers. <https://surrealdb.com/blog/surrealdb-raises-23m-series-a-extension-to-power-the-ai-native-database-era>
- **[C19]** TypeDB repository and *TypeDB 3.0 is now live*. <https://github.com/vaticle/typedb>; <https://typedb.com/blog/typedb-3-0-is-now-live>
- **[C20]** Stack Overflow, *2025 Developer Survey: Technology*. Secondary write-ups quote 55.6% or 58.2% usage for PostgreSQL, so read the official tables for exact figures. <https://survey.stackoverflow.co/2025/technology/>
- **[C21]** DB-Engines, NebulaGraph and TigerGraph comparison pages (license and partitioning). <https://db-engines.com/en/system/NebulaGraph%3BNeo4j%3BTigerGraph>
- **[C22]** Apache AGE coverage (ODBMS.org, July 2026); Microsoft, *Generally available: graph database support in Azure Database for PostgreSQL*. <https://www.odbms.org/2026/07/apache-age/>; <https://techcommunity.microsoft.com/blog/adforpostgresql/-/4413894>
- **[C23]** Google, *Spanner Graph and ISO standards*. Vendor's own conformance statement. <https://docs.cloud.google.com/spanner/docs/graph/iso-standards>
- **[C24]** Gel, *Gel joins Vercel* (2025-12-02); Vercel, *Investing in the Python ecosystem*. <https://www.geldata.com/p/sunset>; <https://vercel.com/blog/investing-in-the-python-ecosystem>
- **[C25]** PuppyGraph, *What is KùzuDB* (reports the Apple acquisition via an EU Digital Markets Act filing). <https://www.puppygraph.com/blog/what-is-kuzudb>
- **[C26]** InfoQ, *Redis adds AGPL license*, 2025-05. <https://www.infoq.com/news/2025/05/redis-agpl-license>
- **[C27]** Percona, *Community erosion post license change*. <https://www.percona.com/blog/community-erosion-post-license-change-quantifying-the-power-of-open-source/>
- **[C28]** ISO/IEC 39075:2024 (GQL), published April 2024. <https://webstore.iec.ch/publication/94107>
- **[C29]** LDBC, *Social Network Benchmark* and audited results. <https://www.ldbcouncil.org/benchmarks/snb>
- **[C30]** LDBC, *Financial Benchmark (FinBench)*. <https://ldbcouncil.org/benchmarks/finbench>

**Limitations.** Several rows rest on search snippets, vendor pages, or Wikipedia, and say so. Facts marked "not verified in this pass" were not checked and must be confirmed before they appear in public copy. No competitor was installed, run, or benchmarked, and nothing here is a performance comparison.
