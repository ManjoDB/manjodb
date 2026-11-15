# Research note: scaling beyond a single node

**Date:** 2026-11-15. **Status:** recommendation, proposes changes to plan §10.2, §13, §28. **Relates to:** `ManjoDB-Grand-Plan.md` §1.4, §2, §10, §11, §16.5, §28; `research/competitive-landscape.md`.

## 1. The question, and the short answer

*"Why settle on a single-node graph database? I want to expand more."*

**Short answer.** Single-node is the first *stage* of a path, not the ceiling. The plan should stage it for three reasons:

1. **The expensive, risky parts of distribution are hard to do early.** Consensus, failover, partitioning, and distributed transactions are each multi-year engineering problems. A small team that starts there risks never shipping a database that is correct on one machine, which is the thing every later stage depends on.
2. **The reference workloads are small by database standards.** Dependency inventories, lineage graphs, and access graphs run at about 10^4–10^7 edges (plan §3). One node with replicas covers them, and the plan's first users do not need sharding.
3. **The best-funded competitor does not fully partition the graph either.** Neo4j's 100 TB-class design keeps the topology on one replicated shard and spreads only the property data (§2). That points to a cheaper path than general graph partitioning.

**But the plan should not read as a ceiling.** Cheap decisions made now keep every later stage open, and some are very hard to retrofit (§4). The plan's §2 and §28 are updated to say this.

## 2. What the market shows about scale-out

| Product | Approach | Status and caveats |
| --- | --- | --- |
| **Neo4j Infinigraph** | One **graph shard** holds topology (nodes, relationships, labels, IDs) as a **single Raft group** with failover and secondaries. **Property shards** hold property values, spread by hash. Traversal runs on the graph shard; property values are fetched in batches at the end of the query. Writes go through the graph shard's Raft group and propagate to property shards by transaction logs [G1, G2] | Launched September 2025. Claims 100 TB-plus (vendor claim, no independent benchmark found). Property shard count is fixed at creation; no automatic rebalancing in the first version; property sharding described as an early-access program; Neo4j says it is not for every workload [G2] |
| **Neo4j clustering** | Enterprise Edition feature; Community is single-node [G3] | Vendor documentation |
| **Memgraph** | Raft-based coordination and failover, listed under Enterprise [G4] | Verify the current feature split |
| **NebulaGraph, TigerGraph** | Sharded native graphs (DB-Engines) [G5] | Designs not examined here |
| **OrientDB** | Described in the literature as distributed and multi-master | **Not verified** from the sources I read; no claims made |
| **Hiqlite** | An example in the OpenRaft README: an embeddable, highly available, Raft-based SQLite [G6] | Shows Raft can be embedded; not a graph |

**The pattern.** Nobody in this list sells a freely partitioned, general-purpose graph as the default. The industry's most credible 2025 answer shards the *bulk* (properties and vectors) and keeps the *structure* together. That works when the topology fits one Raft group, which holds for most application graphs.

**A caution about building a graph on a distributed key-value store.** A competitor's article argues that a graph over an external key-value store pays a network round trip per hop and leaves graph modeling and transactions to the application [G7]. That is a competitor's view, but the mechanism is real. ManjoDB's plan puts the graph layer on an *embedded, local* key-value store (plan §10.1), which has no network hop. A *remote* distributed store (FoundationDB, TiKV) would reintroduce the hop and a second system to operate, which conflicts with the one-binary goal (plan H4). So those stores stay a research experiment (§4, item 5), not a plan.

## 3. A staged path

| Stage | Product | Adds | Depends on | Open questions | Evidence gate |
| --- | --- | --- | --- | --- | --- |
| **S0** | Single-node database (plan v0.1 to 1.0) | Everything in the plan | — | — | Plan §26 gates |
| **S1** | **Replicated** database: one primary, read replicas | Log shipping from a logical commit log; read scale; faster restore; cold standby | A stable commit log and `commit_seq` (§4) | Replica lag semantics; snapshot installation; how read-your-writes is requested | Replica converges to primary on the randomized-history suite; documented lag metric |
| **S2** | **Highly available** database | Automatic failover through a tested consensus library | S1 | Ordering of consensus log, local commit, and client acknowledgement; no acknowledged write lost across failover | Jepsen-style fault testing; acknowledged-write survival under partition and crash |
| **S3** | **Managed single-node or HA service** | Provisioning, credentials, backups, metrics, billing | S0, ideally S2 | Tenant isolation; restore and deletion lifecycles | Operational drills (plan §28) |
| **S4** | **Property and payload sharding**, in the style of Infinigraph (topology on one replicated group, bulky values sharded) | Scale beyond one machine's storage when properties dominate | S2 | Fixed versus rebalanceable shard counts; cross-shard latency on property fetch; backup and restore across shards | Pilot with a graph whose properties, not topology, outgrow one node |
| **S5** | **Partitioned graph** (topology itself sharded) | Scale beyond one machine's topology | S4 | Partitioning that preserves traversal locality; distributed snapshots; cross-shard transactions | A concrete customer-driven case; not scheduled |

Each stage is a separate product with its own thesis and RFC set (plan §28). **S0 to S2 are plausible for a small team.** S3 is largely conventional engineering. **S4 is the realistic scale-out path.** S5 is still a research problem.

**Consistency words to use from the start.** *Serializable on the primary.* On replicas: *bounded-stale* by default, or *read-your-writes* by passing a commit-position token. PostgreSQL's 19 beta added a WAIT command for read-your-writes on replicas [G8], which is the same idea in another system and a sign the mechanism is mainstream.

## 4. Decide now to keep the path open

These choices are cheap today and costly to retrofit after data and clients exist. Each is a proposal for an RFC, not a decision.

1. **Write a logical commit log.** In the same substrate transaction as each write document, append one entry: `L/{commit_seq}` holding the request ID, principal, and the *changeset* (created, updated, and removed objects with their final values). It is the one primitive that serves replication (S1), the outbound change feed (plan §16.5), incremental backup and point-in-time recovery, audit, and cache invalidation. Use a *changeset* log, not a statement log, so a replica never has to re-plan a query and reach a different result. **Cost:** extra write amplification, to be measured in experiment S3 (plan §10.6). **Retention:** bounded, with compaction after replicas and consumers have caught up.
2. **Return `commit_seq` everywhere.** Every write receipt and read result carries a monotonic `commit_seq` (this replaces or augments the diagnostic `snapshot` field in plan §8.8). Reserve a request parameter and capability, such as `read.min_commit_seq.v1`, so a client can ask a replica for "at least this commit". Today it is always satisfied; reserving it now means no protocol change later.
3. **Reserve partition bits in IDs.** Keep `NodeId` and `EdgeId` as opaque 64-bit values, never reused (already planned), and reserve the top 12 bits as a *partition field* that is zero until sharding exists. That leaves about 4.5 × 10^15 IDs per partition and lets S4/S5 allocate IDs per shard without renumbering. **Cost:** none today. **Needs RFC-0001** because it affects the storage format.
4. **Keep write documents deterministic.** MQL v0.1 has no clock or random functions; time and randomness enter only as parameters. Keep it that way. With a changeset log this is not strictly required, but it keeps statement-level replication and replay (for tests and the reference evaluator) possible.
5. **Keep the substrate trait narrow, and add a feasibility experiment.** The graph layer already uses only ordered get, put, delete, range scan, snapshots, and write transactions (plan §10.1). Add an *experiment*, not a commitment: **S5-substrate**, which prototypes the same trait on a distributed transactional store (FoundationDB or TiKV) to measure per-hop latency. It exists to confirm or kill the hop-latency concern in §2 with data.
6. **Treat "single writer" as a capability, not a protocol assumption.** The protocol is already stateless (plan §13.1). Do not add features that assume one process exists, such as server-held transactions or process-local ordering tokens exposed to clients.
7. **Do not promise multi-node behavior in documentation until a stage ships.** No "scales horizontally" language; state the current stage and the next stage plainly.

## 5. Consensus library risk

OpenRaft is a widely used Rust Raft library, and its README lists embedded uses such as Hiqlite [G6]. But its current crate line is a 0.10 alpha series, and the alpha documentation says the API is unstable [G9]. Many downstream projects build on the 0.9 line. **Implications:**

- Do not choose a consensus library in M0. Revisit at S2, with fault-injection results.
- Wrap whatever is chosen behind a small trait, as with the substrate.
- Never implement Raft or any consensus protocol in-house (plan §28).

## 6. What would change this recommendation

| Signal | Action |
| --- | --- |
| Two or more pilot teams need high availability before they will adopt | Pull S1 and S2 forward in the roadmap; keep v0.1 scope unchanged |
| A pilot's *properties* outgrow one node (for example large attached evidence), while topology fits | Prototype S4 early; it is the best-supported path in §2 |
| A pilot's *topology* outgrows one node (roughly 10^9 edges or more, workload-dependent) | Open S5 as research, and reconsider the distributed-substrate experiment |
| The logical commit log costs too much write amplification (experiment S3) | Fall back to substrate-level replication for S1, and revisit the change feed's design |
| All pilots run on one node comfortably through 1.0 | Keep S0 to 1.0 as planned; spend the effort on adoption (`developer-adoption-strategy.md`) |

## 7. Plan changes made alongside this note

- **§2 Non-goals:** the distributed line now says single-node is a *stage*, with the path in §28.
- **§10.2:** adds the `L/{commit_seq}` key family as a candidate.
- **§8.8 and §13.4:** results and receipts carry `commit_seq`.
- **§28:** adds a "decide now" list and a staged table, and keeps the existing research tracks.
- **`PRODUCT.md`:** removes "does not compete on distribution" in favor of "sequenced after 1.0".

## Sources

- **[G1]** Neo4j, *Infinigraph: scalable architecture* (post metadata and byline disagree on its date). <https://neo4j.com/blog/graph-database/infinigraph-scalable-architecture/>
- **[G2]** Neo4j, *Property sharding in Infinigraph* (graph shard as a single Raft group; fixed property-shard count; early access). <https://neo4j.com/blog/graph-database/property-sharding-infinigraph/>
- **[G3]** Neo4j, *Operations Manual: Introduction* (Enterprise adds clustering and online backup). <https://neo4j.com/docs/operations-manual/current/introduction/>
- **[G4]** Memgraph GitHub README (Enterprise HA). <https://github.com/memgraph/memgraph>
- **[G5]** DB-Engines, NebulaGraph and TigerGraph pages (partitioning method: sharding). <https://db-engines.com/en/system/NebulaGraph%3BNeo4j%3BTigerGraph>
- **[G6]** OpenRaft repository README (downstream users including Hiqlite). <https://github.com/databendlabs/openraft>
- **[G7]** TigerGraph, *Building a graph database on a key-value store?* (a competitor's argument). <https://www.tigergraph.com/blog/building-a-graph-database-on-a-key-value-store/>
- **[G8]** PostgreSQL, *PostgreSQL 19 Beta 4 Released* (WAIT command for read-your-writes replication). <https://www.postgresql.org/about/news/postgresql-19-beta-4-released-3386/>
- **[G9]** docs.rs, *openraft 0.10.0-alpha.32* (unstable-API note). <https://docs.rs/crate/openraft/0.10.0-alpha.32>

**Limitations.**

- Vendor scale claims (100 TB-plus) are unverified and no independent benchmarks were found.
- Competitor architectures other than Neo4j's were not examined in depth.
- The ID-bit reservation, the changeset-log format, and the `commit_seq` semantics are design proposals that need RFC-level review and measurement. None is a result.
