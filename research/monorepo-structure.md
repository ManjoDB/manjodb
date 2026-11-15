# Research note: repository structure, now and after growth

**Date:** 2026-10-03. **Status:** recommendation for M0 (plan §25). **Relates to:** `ManjoDB-Grand-Plan.md` §5.3–5.4, §14, §18.8, §27, §29; `PRODUCT.md` (everything open source, confirmed 2026-10-03).

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
├─ Cargo.toml                 # virtual workspace; [workspace.dependencies]
├─ Cargo.lock
├─ rust-toolchain.toml
├─ package.json               # private root; scripts only
├─ pnpm-workspace.yaml        # packages/*, docs, examples/*; pnpm catalogs
├─ pnpm-lock.yaml
├─ justfile                   # the one task entry point for humans, CI, and agents
├─ crates/                    # ── SEAM A: engine (never split) ──
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
└─ .github/                   # workflows (path-filtered), CODEOWNERS
```

**Why this split of directories.** Each top-level directory marked **SEAM** is a *future repository candidate*. Everything inside a seam may change together freely. Anything that crosses a seam must go through a published contract.

### 3.2 Seam rules (what makes a later split cheap)

1. **No cross-seam source imports.**
   - TypeScript never imports from `crates/`.
   - Rust never reads `packages/`.
   - Lint rules enforce this: dependency-cruiser or ESLint import boundaries for TS; Cargo path dependencies only inside `crates/`.
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
5. **Commit scopes name the seam**, for example `feat(mql): …`, `fix(client): …`, `docs(spec): …`. After an extraction, history stays readable, and changelog tools (release-plz, Changesets) can generate notes per seam.
6. **CI is path-filtered per seam**, with one required "all green" aggregate check. A docs typo does not run the crash suite.
7. **CODEOWNERS names an owner per seam**, even if it is the same person today. This is what plan §27's "no official subsystem without an owner" looks like in practice.
8. **No seam reaches into `research/`, `rfcs/`, or `brand/` at build time.** Those directories are reference material, not inputs.

### 3.3 Tooling: minimal now, with named upgrade points

| Concern | Now | Upgrade when | Upgrade to |
| --- | --- | --- | --- |
| Rust build | Cargo virtual workspace with `[workspace.dependencies]` | — | — |
| TS build | pnpm workspaces + catalogs (one version per dependency) | — | — |
| Task entry | `justfile` (or `cargo xtask` for logic) | Cross-language caching matters: CI > ~15 min, or local rebuilds hurt | **moon**, which is Rust-aware and polyglot [M6]. Turborepo is JS-centric and would need `package.json` wrappers for Rust tasks. |
| Rust releases | release-plz: release PRs, changelogs, crates.io publishing from conventional commits [M7] | — | — |
| npm releases | Changesets (per-package versions and changelogs) [M8] | — | — |
| Large files | None; brand SVGs are small | Raster brand or press assets appear | Git LFS for `brand/raster/` only |
| Build system | Not Bazel | Never at this scale | — |

**Avoid:**

- **Git submodules for internal code.** They add coordination friction without the benefits of either approach.
- **Polyrepo from day one.** It turns every protocol change into a multi-repo, multi-PR dance; Prisma's split illustrates the cost.
- **Mirroring internal packages to separate read-only repos** before anyone needs them.

## 4. Splitting playbook (for when the business succeeds)

### 4.1 Triggers

Split a seam only when **at least two** of these hold, and record the decision as an RFC:

1. **Release cadence diverges.** The seam ships on a different rhythm, and coupled releases block one side.
2. **A different maintainer group** owns the seam and needs its own permissions, triage, and review norms.
3. **The consumer set differs.** Outside implementers or contributors use only this seam, for example spec readers or SDK authors in other languages.
4. **CI cost or noise.** The seam's CI is slow or flaky in ways unrelated to the rest, even after path filtering.
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
3. **Move the seam's open issues** with GitHub issue transfer. Update CODEOWNERS, the CI path filters, and the docs links.
4. **Keep the conformance run** in core CI against the pinned version. A split must never silently stop the cross-check.

## 5. Naming (proposed; must be checked before use)

- **GitHub organization:** `manjodb`.
- **Repositories:** core `manjodb/manjodb`; later `spec`, `website`, `studio`, `skills`, `manjodb-<language>`.
- **Packages:** npm `@manjodb/*`, crates `manjo-*`, PyPI `manjodb`. These match plan §18.8; availability is not verified.

## 6. What to do now

1. Turn this folder into the repo root: `git init`, then add the Phase 1 skeleton directories with READMEs. `brand/`, `research/`, and `PRODUCT.md` already sit where the layout puts them.
2. Add `justfile` targets: `just check` (format + lint + test on every seam), `just conformance`, `just docs`.
3. Add CODEOWNERS and path-filtered CI from the first commit, while it is cheap.
4. Record this structure as **RFC-0000 (repository layout)** so later splits follow the triggers instead of mood.

## Sources

- **[M1]** Drizzle ORM repository: a pnpm + Turborepo monorepo with `drizzle-orm`, `drizzle-kit`, validator packages, and `drizzle-seed`. <https://github.com/drizzle-team/drizzle-orm>
- **[M2]** Prisma documentation, *Engines*: engines in `prisma/prisma-engines`; Prisma ORM 7 runs without Rust engines by default. <https://www.prisma.io/docs/orm/more/under-the-hood/engines>
- **[M3]** DuckDB documentation, *Repositories*: core repo and separate official client repositories, including `duckdb-python`. <https://duckdb.org/docs/current/dev/repositories>
- **[M4]** MongoDB, *Specifications* repository: cross-driver specs and shared test files. <https://github.com/mongodb/specifications>
- **[M5]** GraphQL specification repository, separate from the reference implementation. <https://github.com/graphql/graphql-spec>
- **[M6]** moonrepo, *moon*: a Rust-based polyglot task runner and monorepo tool supporting JS/TS, Rust, and others. <https://moonrepo.dev/moon>
- **[M7]** release-plz: release PRs, git-cliff changelogs, crates.io publishing, Cargo workspace support. <https://github.com/release-plz/release-plz>
- **[M8]** Changesets: versioning and changelogs for multi-package JS repositories. <https://github.com/changesets/changesets>
- **[M9]** GitHub Docs, *Splitting a subfolder out into a new repository* (git filter-repo). <https://docs.github.com/en/get-started/using-git/splitting-a-subfolder-out-into-a-new-repository>

**Limitations.**

- The comparable-project facts come from those projects' own docs and repositories, checked 2026-10-03.
- The thresholds in §3.3 and §4.1 (CI over 15 minutes; two of six triggers) are proposed project policy, not industry standards.
