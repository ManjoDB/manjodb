# Research note: repository structure, now and after growth

**Date:** 2026-10-03; **updated 2026-11-15 (Nx adopted).** **Status:** recommendation for M0 (plan §25). **Relates to:** `ManjoDB-Grand-Plan.md` §5.3–5.4, §14, §18.8, §25.2, §27, §29; `PRODUCT.md` (everything open source, confirmed 2026-10-03; Nx monorepo, confirmed 2026-11-15).

> **Decision, 2026-11-15:** the monorepo is an **Nx workspace**. The first version of this note recommended a `justfile`, with a later upgrade to moon. That recommendation is **superseded**. The seam design (§3.1–3.2) is unchanged: Nx is how the seams are *enforced and built*. The workspace design is in §3.3, the trade-offs are in §3.4, and the facts it rests on are in the new sources [N1–N10].

## 1. The question

ManjoDB will start with one or two people and a polyglot codebase:

- a Rust engine and the `manjo` binary;
- TypeScript packages;
- language-neutral specs and conformance fixtures;
- docs, agent skills, examples, benchmarks, and brand assets.

How should all of this live in one repository so that work is fast now? And how is it shaped so that, if ManjoDB succeeds, pieces can move to their own repositories without a rewrite or a lost history?

## 2. What comparable projects do

| Project | Layout | Lesson for ManjoDB |
| --- | --- | --- |
| **Drizzle ORM** | One pnpm + Turborepo monorepo holding `drizzle-orm`, `drizzle-kit` (the migration CLI), validator bridges (`drizzle-zod`, `drizzle-valibot`, …), and `drizzle-seed` [M1] | A TypeScript library family that versions together lives comfortably in one repo |
| **Prisma** | TypeScript in `prisma/prisma`; the Rust engines in a *separate* repo, `prisma/prisma-engines`, shipped into the TS repo as binaries or WebAssembly [M2] | Splitting the Rust core from the TS surface early costs an artifact-version handshake on every change. Prisma 7 moved query execution into TypeScript and dropped the Rust query-engine binary by default [M2]. Do not split tightly coupled layers. |
| **DuckDB** | Core engine repo, plus **every official client in its own repo** (Python, Node, Go, Java, R, Rust, Swift, Wasm, …) [M3]. The Python client was split out of the core monorepo in 2025 so it could iterate and release independently [M3]. | Clients move out when their release cadence and maintainers diverge from the core. That is a growth event, not a day-one design. |
| **MongoDB** | Each driver in its own repo, plus a shared **specifications** repository: cross-driver behavior specs and machine-readable test files that every driver runs [M4] | This is exactly ManjoDB's `spec/` + conformance design (plan §14.3). It becomes its own repo once several independent clients consume it. |
| **GraphQL** | The specification (`graphql-spec`) is a separate repo from the reference implementation (`graphql-js`) [M5] | A language spec earns its own repo and governance once other implementations exist |

**Pattern.** Every project above keeps the **core engine together**. Splits follow **independent release cadence, independent maintainers, or independent consumers**. Prisma's early core/surface split is the cautionary case.

## 3. Recommendation: one repo now, with seams cut in advance

### 3.1 Phase 1 layout (`manjodb/manjodb`)

```text
manjodb/
├─ nx.json                    # Nx: targetDefaults, cache inputs, plugins, release config
├─ Cargo.toml                 # virtual workspace; [workspace.dependencies]. Cargo stays the source of truth for Rust
├─ Cargo.lock
├─ rust-toolchain.toml
├─ package.json               # private root: Nx and tooling devDependencies
├─ pnpm-workspace.yaml        # packages/*, docs, examples/*; pnpm catalogs
├─ pnpm-lock.yaml
├─ crates/                    # ── SEAM A: engine (never split); a project.json beside each Cargo.toml ──
│  ├─ manjo-core/             # IDs, values, encodings
│  ├─ manjo-mql/              # lexer, parser, binder, IR, diagnostics, signatures
│  ├─ manjo-ref/              # in-memory reference evaluator (test oracle)
│  ├─ manjo-graph/            # graph layer over the KV substrate; catalog
│  ├─ manjo-engine/           # planner, executor, transactions, receipts
│  ├─ manjo-server/           # protocol v1
│  ├─ manjo/                  # the `manjo` binary: CLI, shell, serve, mcp
│  └─ xtask/                  # repo automation in Rust (codegen, release checks)
├─ packages/                  # ── SEAM B: TypeScript surface ──
│  ├─ client/                 # @manjodb/client
│  └─ schema/                 # @manjodb/schema
├─ spec/                      # ── SEAM C: language-neutral contracts ──
│  ├─ mql/                    # mql.ebnf, profiles
│  ├─ protocol/               # OpenAPI + normative prose
│  ├─ schema-document/        # JSON Schema
│  ├─ errors.json  capabilities.json  signature.schema.json
│  ├─ corpus/                 # task → MQL → expected rows
│  └─ conformance/            # wire fixtures, fault scenarios
├─ skills/                    # ── SEAM D: agent skills (Agent Skills format) ──
├─ docs/                      # ── SEAM E: documentation site source ──
├─ examples/                  # dependency-impact/, data-lineage/
├─ bench/                     # harness + PostgreSQL baselines
├─ rfcs/
├─ research/                  # notes like this one
├─ brand/                     # logo SVGs, brand sheet, usage rules
├─ PRODUCT.md
├─ ManjoDB-Grand-Plan.md      # later: docs/architecture/
└─ .github/                   # workflows (`nx affected`), CODEOWNERS
```

**Why this split of directories.** Each top-level directory marked **SEAM** is a *future repository candidate*. Everything inside a seam may change together freely. Anything that crosses a seam must go through a published contract.

### 3.2 Seam rules (what makes a later split cheap)

1. **No cross-seam source imports.**
   - TypeScript never imports from `crates/`.
   - Rust never reads `packages/`.
   - Nx enforces this with project tags and module-boundary rules (§3.3); Cargo path dependencies stay inside `crates/`, and Cargo itself cannot depend on TypeScript.
2. **Cross-seam dependencies go through artifacts, exactly as they would after a split.**
   - The TS client's conformance tests run against a **built `manjo` binary**, never against Rust internals.
   - Spec consumers read generated files from `spec/`, never hand-copied constants.
3. **`spec/` is versioned on its own** (`spec/VERSION`, with a changelog). Every client declares which spec version it implements. This is the MongoDB model [M4], ready to move out as is.
4. **Each seam carries its own README, CHANGELOG, and package metadata, and gets its own release tag:**

   | Seam | Tag format |
   | --- | --- |
   | Engine | `manjo-v0.1.0` |
   | npm packages | `@manjodb/client@0.1.0` |
   | Spec | `spec-v1.0.0` |
   | Skills | `skills-v0.1.0` |

   A seam that already releases independently can be moved without inventing a new process.
5. **Commit scopes name the seam**, for example `feat(mql): …`, `fix(client): …`, `docs(spec): …`. After an extraction, history stays readable, and release tooling (`nx release`, and release-plz if it is used for crates; §3.3) can generate notes per seam.
6. **CI runs only what a change affects.** `nx affected` runs the projects touched by a change and everything downstream of them, with one required "all green" aggregate check. A docs typo does not run the crash suite. Heavy suites (crash, power-loss, conformance against the fault proxy, benchmarks) run on a schedule.
7. **CODEOWNERS names an owner per seam**, even if it is the same person today. This is what plan §27's "no official subsystem without an owner" looks like in practice.
8. **No seam reaches into `research/`, `rfcs/`, or `brand/` at build time.** Those directories are reference material, not inputs.

### 3.3 Nx workspace design

**What Nx provides here** (from Nx's documentation, checked 2026-11-15):

- A project is a directory with a `project.json`, or a `package.json` that is part of the package manager's workspaces. Tasks come from `package.json` scripts, from `project.json` targets, or from plugins that read tool configuration. Shared defaults live in `targetDefaults` in `nx.json`, and the precedence is plugin-inferred, then `targetDefaults`, then the project's own file [N1, N2].
- Task results are cached, and `nx affected` computes which projects a change can influence from the project graph [N1, N2].
- **Module boundaries.** The `@nx/enforce-module-boundaries` ESLint rule checks JS/TS imports against `depConstraints` written over project tags. A separate Conformance plugin can enforce project boundaries across languages by reading the Nx project graph; I did not verify its availability or licensing [N3].
- **Releases.** `nx release` has three phases (version, changelog, publish), supports independent versioning per project, and can derive bumps from conventional commits [N4].
- **Rust.** There is no Rust support in Nx core. The path is `@monodon/rust`, a **community plugin** that Nx's own how-to documents (§3.4 covers the risk) [N5, N6].

**Projects and tags.** One tag family names the seam; another names the kind of project.

| Projects | Project file | Tags |
| --- | --- | --- |
| `crates/*` (the `manjo` binary also gets `type:app`) | `project.json` beside each `Cargo.toml` | `seam:engine`, `type:crate` |
| `packages/client`, `packages/schema` | `package.json` (and a `project.json` only if needed) | `seam:typescript`, `type:lib` |
| `spec` | `project.json` (targets: `generate`, `validate`) | `seam:spec`, `type:spec` |
| `skills` | `project.json` | `seam:skills` |
| `docs` | `package.json` | `seam:docs`, `type:app` |
| `examples/*`, `bench` | as needed | `scope:examples`, `scope:bench` (unconstrained consumers; they are integration tests of the engine) |

**Boundary constraints** (illustrative, in the format Nx documents [N3]; verify against the Nx version in use):

```json
[
  { "sourceTag": "seam:engine",     "onlyDependOnLibsWithTags": ["seam:engine"] },
  { "sourceTag": "seam:typescript", "onlyDependOnLibsWithTags": ["seam:typescript", "seam:spec"] },
  { "sourceTag": "seam:docs",       "onlyDependOnLibsWithTags": ["seam:docs", "seam:typescript", "seam:spec"] },
  { "sourceTag": "seam:skills",     "onlyDependOnLibsWithTags": ["seam:skills", "seam:spec"] },
  { "sourceTag": "seam:spec",       "onlyDependOnLibsWithTags": ["seam:spec"] }
]
```

**What enforces what.** The ESLint rule covers TypeScript imports only. Rust and cross-language edges are checked from the project graph: either the Conformance plugin, or a short script in `xtask` (or Node) that reads the exported graph and fails CI on a forbidden edge. Add whichever one works before the first engine code lands, so the rule exists before there is anything to violate it.

**Artifact dependencies are task edges, not source edges.** The TypeScript client's conformance target depends on *building* the `manjo` binary (`client:conformance` has `dependsOn: ["manjo:build"]`). Task dependencies are allowed across seams; imports and Cargo path dependencies are not (§3.2 rule 2). Every such edge is declared in the consumer's project file, so `nx graph` shows exactly where one seam leans on another.

**Rust integration.**

- **Cargo stays the source of truth.** `Cargo.toml`, `Cargo.lock`, and `rust-toolchain.toml` are authoritative. Nx orchestrates and caches; it does not replace Cargo.
- Crates become Nx projects through a `project.json` beside each `Cargo.toml`. The plugin's generators create them, and its executors map to `cargo build`, `cargo test`, `cargo clippy`, and `cargo run`. A plain `nx:run-commands` target also works without the plugin [N5, N6].
- Per the Nx guide, path dependencies in the root `Cargo.toml` provide the edges that `nx affected` uses [N5].
- **Cache correctness.** Give each target its own `target-dir` (otherwise targets overwrite each other's artifacts and cached outputs stop matching), and list `Cargo.toml`, `Cargo.lock`, and `rust-toolchain.toml` as cache inputs, or a Rust version bump can replay stale artifacts [N5].
- **Node bindings.** The plugin's library generator has a `--napi` option for Node-API builds [N6]. That helps the embedded Node.js experiment in `research/developer-adoption-strategy.md` (A4).
- CI machines need a Rust toolchain installed separately [N5].

**Releases.**

- **npm packages:** `nx release`, independently per package, from conventional commits [N4].
- **Rust crates: unresolved.** Nx lists a guide for releasing Rust crates, but my fetch of the address a search returned was a 404, and a search snippet described that recipe as old and tied to legacy versioning [N7]. The plugin's changelog mentions a release-version generator [N6]. Settle it with an **M0 spike**: try `nx release` for crates; if it is not clean, use release-plz [M7] for crates and `nx release` for npm, both driven by the same conventional commits.
- Tag formats stay as in §3.2 rule 4.

**CI.** Pull requests run `nx affected -t lint test build`. A scheduled job runs the heavy suites. Use the local cache and the CI provider's cache first. Nx Cloud remote caching is optional: it has a free tier, but the credit and contributor limits differ across the third-party pages I found, and I could not confirm whether the remote cache can be self-hosted. Read Nx's own pricing page before depending on it [N8].

**Targets.** Every project defines `lint`, `test`, and `build`, with `conformance` (client, schema), `generate` and `validate` (spec), and `docs` (docs) where they apply. Root commands: `nx run-many -t lint test build`, `nx affected -t …`, and `nx graph`.

### 3.4 Tooling summary, and the trade-offs of choosing Nx

| Concern | Choice | Notes |
| --- | --- | --- |
| Workspace and task runner | **Nx**, decided 2026-11-15 | 23.1.0 was the latest stable release found (2026-07-13) [N9]. Pin the version |
| Rust build | Cargo virtual workspace with `[workspace.dependencies]` | The source of truth |
| TS build | pnpm workspaces with catalogs (one version per dependency) | Nx reads the workspaces |
| Rust in Nx | `@monodon/rust` (community plugin) | Version 3.0.0, 2026-06-01; requires Nx 22 or newer [N6]. Fallback: plain `nx:run-commands` targets |
| Module boundaries | `@nx/enforce-module-boundaries` plus a project-graph check | §3.3 |
| npm releases | `nx release` | |
| Rust releases | **Open:** `nx release` or release-plz | Decided by the M0 spike |
| Large files | None; brand SVGs are small | Git LFS for `brand/raster/` only if raster assets appear |
| Build system | Not Bazel | Never at this scale |

**Benefits and costs.**

| Benefit | Cost or risk | Mitigation |
| --- | --- | --- |
| One command surface, one project graph, and cached, affected-only tasks across Rust and TypeScript | Rust support is a **community plugin**. As read on 2026-11-15 the repository was MIT-licensed with about 55 stars, 19 open issues, and one principal maintainer [N6] | Cargo stays the source of truth; targets can be plain `run-commands`; pin the plugin; budget time for its upgrades; contribute fixes upstream |
| Boundary rules turn the seam design into something CI enforces | The ESLint rule covers only JS/TS; Rust edges need the graph check (§3.3) | Add the graph check before the first engine code |
| `nx release` for npm; generators for new crates and packages | Rust crate releases are unresolved (§3.3) | M0 spike |
| `nx affected` keeps CI short as the repository grows | Per-target `target-dir` values mean build, test, and clippy each compile dependencies separately under Nx (my inference from [N5]), so Nx runs can be slower and larger than plain Cargo ones | Use `cargo` directly for the inner development loop; use Nx for CI and cross-project tasks; measure CI time in M0 |
| A familiar tool for TypeScript developers | Nx majors move fast (22.x and 23.x in 2026) and each needs `nx migrate` work [N9]; more config files than a `justfile` (`nx.json` plus a `project.json` per project) | Upgrade on a schedule, not on release day; lean on plugin inference and `targetDefaults` to keep project files small |
| Free local caching | Nx Cloud terms are unclear (§3.3) | Local and CI-provider caches first |

**Avoid:**

- **Git submodules for internal code.** They add coordination friction without the benefits of either approach.
- **Polyrepo from day one.** It turns every protocol change into a multi-repo, multi-PR dance; Prisma's split illustrates the cost.
- **Mirroring internal packages to separate read-only repos** before anyone needs them.
- **Letting Nx replace Cargo.** If a Rust task only works through the plugin, it will break when the plugin does.

## 4. Splitting playbook (for when the business succeeds)

### 4.1 Triggers

Split a seam only when **at least two** of these hold, and record the decision as an RFC:

1. **Release cadence diverges.** The seam ships on a different rhythm, and coupled releases block one side.
2. **A different maintainer group** owns the seam and needs its own permissions, triage, and review norms.
3. **The consumer set differs.** Outside implementers or contributors use only this seam, for example spec readers or SDK authors in other languages.
4. **CI cost or noise.** The seam's CI is slow or flaky in ways unrelated to the rest, even with `nx affected` and caching.
5. **The toolchain diverges.** The seam needs build tooling or runtimes the core does not (mobile SDK toolchains, a docs CMS).
6. **Issue-tracker confusion.** Users routinely file issues in the wrong place, or labels can no longer separate concerns.

Licensing is **not** a trigger: everything is open source (`PRODUCT.md`). If that ever changes, any closed component must start in its own private repo on day one, never as a directory that is later "removed".

### 4.2 Likely order, and what never splits

| Order | Unit | Target repo | Expected trigger |
| --- | --- | --- | --- |
| Born separate | Each **non-TypeScript SDK** (Python, Go, JVM, .NET, …) | `manjodb/manjodb-python`, `manjodb/manjodb-go`, … | Different toolchain, maintainer, and cadence from day one. This is the DuckDB and MongoDB pattern [M3, M4]. They consume `spec/` conformance by version. |
| 1 | `docs/` site | `manjodb/website` | Non-engineering contributors; deploy cadence; CMS or toolchain |
| 2 | `spec/` | `manjodb/spec` | Two or more independent implementations consume it [M4, M5] |
| 3 | Studio (when it starts, v0.2+) | `manjodb/studio` | UI toolchain and cadence; it is purely a protocol client |
| 4 | `skills/` | `manjodb/skills` | Agent-skill directories and marketplaces index repositories; skills release with docs, not with the engine |
| Late | `packages/client` | `manjodb/manjodb-js` | Only after protocol v1 freezes (1.0). Until then the reference client co-evolves with the server and must stay in the core repo. |
| **Never** | `crates/*` | stays in `manjodb/manjodb` | The engine layers change together. Splitting them repeats Prisma's coupling cost [M2]. |
| **Never** | `examples/`, `bench/` | stay in core | They are integration tests of the engine |

### 4.3 How to extract a seam with its history

Run the extraction on a fresh clone:

```bash
git clone https://github.com/manjodb/manjodb manjodb-spec && cd manjodb-spec
```

```bash
git filter-repo --subdirectory-filter spec
```

`git filter-repo` is the tool GitHub's documentation recommends for splitting a subfolder into a new repository while preserving its history. It is faster and safer than `filter-branch` [M9].

Then:

1. **Push** to the new repo. Re-create the seam's tags; they already exist with seam-specific names, per §3.2 rule 4.
2. **In the core repo**, replace the directory with a pinned dependency: a published package, a release artifact, or a versioned download in `xtask`. Delete the directory in the same PR, and leave a short `MOVED.md` pointer.
3. **Move the seam's open issues** with GitHub issue transfer. Update CODEOWNERS and the docs links, remove the seam's projects and its tag constraint from the Nx workspace, and move its release configuration to the new repository. The new repository can be its own Nx workspace or a plain project; the seam rules mean it builds from published artifacts either way.
4. **Keep the conformance run** in core CI against the pinned version (a task that downloads the released artifact, in place of a `dependsOn` edge on a local build). A split must never silently stop the cross-check.

## 5. Naming (proposed; must be checked before use)

- **GitHub organization:** `manjodb`.
- **Repositories:** core `manjodb/manjodb`; later `spec`, `website`, `studio`, `skills`, `manjodb-<language>`.
- **Packages:** npm `@manjodb/*`, crates `manjo-*`, PyPI `manjodb`. These match plan §18.8; availability is not verified.

## 6. What to do now

1. Turn this folder into the repo root (`git init` is done); add the Phase 1 skeleton directories with READMEs. `brand/`, `research/`, and `PRODUCT.md` already sit where the layout puts them.
2. **Add Nx to the existing pnpm workspace.** The Nx CLI can initialize an existing repository (`npx nx@latest init`; check the current Nx docs for the exact command and options). Install `@monodon/rust` (needs Nx 22 or newer), pin both versions, and add a `project.json` beside each crate.
3. **Add the tags and the boundary constraints** from §3.3, plus the project-graph check for Rust edges, before the first engine code.
4. Define the standard `lint`, `test`, and `build` targets, and the cache inputs for Rust (§3.3). Root commands are `nx run-many` and `nx affected`; there is no `justfile`.
5. **M0 spikes** (two days at most, each reported in an RFC-0000 appendix): (a) release a throwaway crate with `nx release` and with release-plz; (b) measure CI time for `build`, `test`, and `clippy` under Nx's per-target `target-dir` against plain Cargo, on a placeholder crate.
6. Add CODEOWNERS and the `nx affected` CI workflow from the first commit, while it is cheap.
7. Record this structure as **RFC-0000 (repository layout)**, including the tags, constraints, and the spike results, so later splits follow the triggers instead of mood.

## Sources

- **[M1]** Drizzle ORM repository: a pnpm + Turborepo monorepo with `drizzle-orm`, `drizzle-kit`, validator packages, and `drizzle-seed`. <https://github.com/drizzle-team/drizzle-orm>
- **[M2]** Prisma documentation, *Engines*: engines in `prisma/prisma-engines`; Prisma ORM 7 runs without Rust engines by default. <https://www.prisma.io/docs/orm/more/under-the-hood/engines>
- **[M3]** DuckDB documentation, *Repositories*: core repo and separate official client repositories, including `duckdb-python`. <https://duckdb.org/docs/current/dev/repositories>
- **[M4]** MongoDB, *Specifications* repository: cross-driver specs and shared test files. <https://github.com/mongodb/specifications>
- **[M5]** GraphQL specification repository, separate from the reference implementation. <https://github.com/graphql/graphql-spec>
- **[M6]** moonrepo, *moon*: a Rust-based polyglot task runner and monorepo tool supporting JS/TS, Rust, and others. The alternative considered; no longer planned after the Nx decision. <https://moonrepo.dev/moon>
- **[M7]** release-plz: release PRs, git-cliff changelogs, crates.io publishing, Cargo workspace support. <https://github.com/release-plz/release-plz>
- **[M8]** Changesets: versioning and changelogs for multi-package JS repositories. An alternative to `nx release` for npm; not planned. <https://github.com/changesets/changesets>
- **[M9]** GitHub Docs, *Splitting a subfolder out into a new repository* (git filter-repo). <https://docs.github.com/en/get-started/using-git/splitting-a-subfolder-out-into-a-new-repository>
- **[N1]** Nx, *Inferred tasks* (projects from `project.json` or workspace `package.json`; plugin, `targetDefaults`, and project precedence; affected). <https://nx.dev/docs/concepts/inferred-tasks>
- **[N2]** Nx, *nx.json reference*. <https://nx.dev/docs/reference/nx-json>
- **[N3]** Nx, *Enforce module boundaries* (ESLint rule, tags, `depConstraints`; the Conformance plugin for other languages). <https://nx.dev/docs/features/enforce-module-boundaries>
- **[N4]** Nx, *Manage releases* (`nx release`: version, changelog, publish; independent versioning; conventional commits). <https://nx.dev/docs/features/manage-releases>
- **[N5]** Nx, *Add a Rust application to an Nx workspace* (community plugin; `project.json` beside `Cargo.toml`; path-dependency edges; per-target `target-dir`; cache inputs; toolchain on CI). <https://nx.dev/docs/kb/add-rust-to-nx-workspace>
- **[N6]** `@monodon/rust` repository, README, and changelog (MIT; 3.0.0 dated 2026-06-01; requires Nx 22; generators `binary` and `library` with `--napi`; executors build, lint, napi, run, test; 55 stars and 19 open issues when read). <https://github.com/cammisuli/monodon/tree/main/packages/rust>
- **[N7]** Nx, *Using Nx Release with Rust*. A search result listed it at <https://nx.dev/docs/guides/nx-release/publish-rust-crates>, but fetching that address returned a 404; a search snippet called the page old and tied to legacy versioning. Treat Rust crate releases as unverified.
- **[N8]** Nx, *Pricing* (Nx Cloud free tier and limits; third-party pages disagree on the numbers). <https://nx.dev/pricing>
- **[N9]** Nx 23.1.0 release notes, 2026-07-13, via newreleases.io; 22.7.0 dated 2026-04-24. <https://newreleases.io/project/npm/nx/release/23.1.0>
- **[N10]** Nx, *Exploring polyglot monorepos with Nx, TanStack and Rust* (blog). <https://nx.dev/blog/polyglot-nx-monorepo-rust-tanstack>

**Limitations.**

- The comparable-project facts come from those projects' own docs and repositories, checked 2026-10-03.
- The Nx facts come from Nx's documentation and the plugin's repository, read on 2026-11-15. **I did not build an Nx workspace to test them**, so the Rust graph edges, the cache behaviour, and the release flow are as documented, not as observed.
- The thresholds in §4.1 (two of six triggers) are proposed project policy, not industry standards.
