# Research note — the `as` keyword in MQL

**Date:** 2026-10-02. **Status:** **Option B adopted for the M1 prototype on 2026-10-03** (plan §8.15). It can be reversed by the evaluation in §6 below. No syntax option has been user-tested. **Relates to:** `ManjoDB-Grand-Plan.md` §8.1, §8.2, §8.8, §8.9, Appendix A, Appendix C.

## 1. The observation

Revision 4 of the plan has 13 MQL example blocks: 84 lines, with **71 occurrences of `as`**.

| Use | Count | Example |
| --- | --- | --- |
| Introducing a binding (`find`, `follow`, `add`, `node`/`edge`, `connect`) | 43 | `find Service as dependency`, `through DEPENDS_ON as link from Service as consumer` |
| Renaming an output column in `show` | 28 | `consumer._id as service_id` |

The reference-workload queries are the worst case: about 8 `as` per 6–9 line query. The D1 incident query, for example:

```mql
find Service as dependency
where dependency.key = $service_key
follow dependency through DEPENDS_ON as link from Service as consumer
follow consumer through OWNS from Team as owner
show consumer._id as service_id, consumer.name as service, owner.name as owner, link._id as evidence_id
take 50
```

## 2. Diagnosis

### 2.1 `as` has two meanings, so the plan's own rule is false

§8.1 states that "each word has one meaning". In fact `as` means two different things:

1. **Declaring a binding.** "This matched node or edge is called `dependency`." The name refers to a graph object, is visible to later clauses, and can be compared by `_id`.
2. **Naming an output column.** "Call this projected value `service_id` in the result." The name exists only in the response and cannot be referenced by any clause.

Both meanings sit in the same query and often on the same line. In the `show` line above, `owner.name as owner` uses the binding `owner` and also creates an output column named `owner`.

### 2.2 Most `show` renames are forced, not chosen

v0.1 makes the output key the bare property name, and makes duplicate keys an error (§8.8). Almost every multi-hop query projects several `_id`s and several `name`s, so the author *must* rename. In the D1 query, all four renames exist only to avoid key collisions. They are a consequence of the default naming rule, not of anything the user wanted to express.

### 2.3 Every binding needs a marker word

The grammar puts the type first and the name last (`Service as dependency`), so the name always needs an introducer. A `follow` with a named edge needs two introducers (`through DEPENDS_ON as link from Service as consumer`). The clause then interleaves type, name, type, name, which is hard to scan: the names sit in different horizontal positions on every line.

### 2.4 `as` already means something else to the primary audience

The first target users write TypeScript (plan §1.3). In TypeScript, `value as Type` is a **type assertion** [A1]: value first, type second, the opposite order to MQL's `Type as name`. Kotlin and Swift also use `as` for casts. Python uses it for renaming (`import numpy as np`), and SQL for aliasing (`FROM users AS u`, `SELECT x AS y`) [A2]. SQL's order matches MQL, so SQL users are unaffected, but a TypeScript developer can plausibly read `find User as person` as "treat User as a person". This is a hypothesis to test, not a finding.

## 3. How other languages name things

| Language | Declare a binding / variable | Name an output column | Notes |
| --- | --- | --- | --- |
| SQL (standard, PostgreSQL) | `FROM users AS u` (`AS` optional) | `expr AS name` (`AS` optional in the standard) | PostgreSQL requires `AS` when the output name is a keyword, and recommends always writing it, because omitting it is syntactically ambiguous [A2]. SQLFluff's AL02 rule enforces explicit `AS` for columns by default [A3]. |
| Cypher / GQL | `(p:Person)` (name, colon, label); `IS` is the GQL-style alternative label syntax [A4] | `RETURN expr AS name` | Binding is name-first; output is name-last. The two meanings use different syntax. |
| TypeQL | `$p isa person` | `select $p` (variables only) | Name-first, with a dedicated typing word [A5] |
| EdgeQL (Gel) | `with u := Issue.owner` | Computed shape field `title_upper := …` | Name-first with `:=` for both meanings [A6] |
| KQL (Kusto) | `let x = …` | `project StartLocation = BeginLocation` | Name-first `=` [A7] |
| PRQL | `let x = …` | `select {name = expr}` / `derive name = expr` | Name-first `=` [A8] |
| Malloy | `source: airports is table(…)` | `group_by: age_in_dog_years is age * 7` | Name-first `is` for every definition [A9] |
| TypeScript / Rust / Kotlin / Python | `const x: T`, `let x: T`, `x: T` | — | Name-first colon for "name has type" [A1] |

Two patterns emerge:

- **Modern languages put the name first** when declaring something. Cypher/GQL, TypeQL, EdgeQL, KQL, PRQL, and Malloy all do this, and so do most programming languages. SQL's `FROM t AS u` is the main exception.
- **Languages that keep `AS` use it for output naming,** where SQL convention is nearly universal (SQL, Cypher, GQL, SPARQL). Cypher/GQL is the closest analogue to MQL, and it uses *different* syntax for the two meanings: `:` to bind, `AS` to name output.

## 4. Options

Each option below is shown on the D1 query from §1, which currently has 8 `as`.

### Option A — keep the current syntax (8 `as`)

| Pros | Cons |
| --- | --- |
| Reads aloud as an English sentence. Matches SQL `FROM t AS u`. No punctuation. | One word with two meanings. Forced renames. Names scattered across each line. Reversed order compared with TypeScript `as`. |

### Option A′ — keep `as` for bindings; fix default output names (4 `as`)

```mql
find Service as dependency
where dependency.key = $service_key
follow dependency through DEPENDS_ON as link from Service as consumer
follow consumer through OWNS from Team as owner
show consumer._id, consumer.name, owner.name, link._id
take 50
```

New default output key: `<binding>_<property>`. Metadata drops its underscore. The D1 columns become `consumer_id`, `consumer_name`, `owner_name`, `link_id`.

The keys are unique by construction, because binding names are unique and each property appears once per binding. The rare clash, such as a user property literally named `id` on a binding that also projects `_id`, is a binding error that suggests `as`. Every key is a valid identifier in every SDK language, which helps code generation.

| Pros | Cons |
| --- | --- |
| Removes every forced rename. A small, low-risk change. | `as` still has two meanings. The binding-side issues remain. |

### Option B — name-first bindings with `:`; `as` only renames output; plus A′ naming (**0 `as`**, recommended)

```mql
find dependency: Service
where dependency.key = $service_key
follow dependency through link: DEPENDS_ON from consumer: Service
follow consumer through OWNS from owner: Team
show consumer._id, consumer.name, owner.name, link._id
take 50
```

- **One meaning per construct.** `name: Type` declares a binding, `expr as name` names an output, and `as` becomes optional, used only when a custom column name is wanted.
- **Names align at fixed positions.** The token right after `find`, `through`, `to`, and `from` is always a binding name or an anonymous type, which helps scanning and completion.
- **Direction reads between names.** `follow source through READS from job1: Job` puts both endpoint names next to the direction word ("job1 READS source"). Whether this reduces direction errors is a hypothesis for the study.
- **Familiar declaration form.** `name: Type` is the declaration syntax of TypeScript, Rust, Kotlin, Swift, and Python type hints, and it matches Cypher/GQL's `(p:Person)` binding order [A1, A4]. That is a plausible advantage for humans and LLMs alike, and it must be measured, not assumed.
- **Anonymous edges stay simple.** `through OWNS` is anonymous; `through link: DEPENDS_ON` is named. A later profile could allow anonymous endpoints (`from Team`) without new syntax.

**Writes.** One `by` form replaces the separate "by ID" and "by key" forms:

```mql
write
  node consumer: Service by key = $consumer_key
  node dependency: Service by key = $dependency_key
  connect consumer through link: DEPENDS_ON to dependency
  set link.environment = $env, link.source = "deploy-manifest", link.observed_at_ms = $now
  show link._id
end
```

`node alice: User by _id = $alice_id` binds by ID. Because `_id` is unique by definition, the grammar loses an alternative.

| Pros | Cons |
| --- | --- |
| Removes every forced or structural `as`. Fixes the two-meaning defect. Familiar declaration form. Shorter lines. | Adds one punctuation mark to a word-oriented language. Reads less like an English sentence aloud. Possible pull toward full Cypher syntax (`(p:Person)`) from Cypher-trained users and models; the validator catches this with a targeted hint. Screen-reader announcement of `:` depends on punctuation verbosity settings and must be tested. |

### Option C — name-first everywhere, including output (`name = expr`; 0 `as`)

```mql
show service_id = consumer._id, service = consumer.name, owner = owner.name
```

This follows KQL and PRQL [A7, A8].

| Pros | Cons |
| --- | --- |
| Output names line up at the left. | `=` would mean comparison in `where`/`require`, assignment in `set`, and naming in `show`. `owner = owner.name` reads like a predicate. It abandons the near-universal `AS` for output, so it is not recommended. |

### Option D — implicit binding names derived from the type

`find Service` would bind `service` automatically.

**Rejected.**

- Real queries repeat types (D1 has two `Service` bindings), so names are still required.
- Adding a second binding of the same type would silently force the first one to be renamed.
- It hides the binding identity that the plan treats as essential (§8.1, principle 2).

### Option E — juxtaposition with no marker (`find Service dependency`)

**Rejected.**

- PostgreSQL documents the ambiguity that implicit output aliases create [A2].
- A dropped comma or keyword silently becomes a new name, which is the class of bug that SQL linters exist to prevent [A3].

## 5. Recommendation

**Adopt Option B (colon declarations + `as` only for output + `<binding>_<property>` default keys) as the M1 prototype syntax.** Keep Option A′ as the fallback if the study rejects the colon.

Reasons:

1. It fixes a real specification defect: one keyword with two meanings, contradicting §8.1.
2. It removes the root cause of most `as` usage, which is collision-forced renames.
3. It aligns MQL with how Cypher/GQL already separate binding from output naming.
4. It leaves MQL's distinctive structure untouched: one clause per hop, a named source, words for direction.

The changes are surface-level. The binder, IR, and semantics do not change. The cost of changing course after M1 is therefore small, provided the change is made before `mql.v1` is frozen.

## 6. What must be tested

Add these to the plan's usability study (Appendix C2) and LLM evaluation (§18.7) as a **within-subject variant comparison** between Option A (current) and Option B, with counterbalanced order:

| Question | Measure |
| --- | --- |
| Does `name: Type` change direction errors on `to`/`from` tasks? | Direction-error rate (critical metric) |
| Do participants confuse binding names with output names? | Errors on tasks 3, 5, and 8 of C3; think-aloud explanations of each name |
| Do TypeScript developers misread `Type as name`? | Comprehension probe: "what does `find User as person` do?" |
| Do default keys (`consumer_name`) surprise people? | Prediction of result column names |
| Do Cypher users write `(p:User)` under Option B? | Frequency of Cypher-shaped attempts; whether the targeted diagnostic fixes them |
| Is reading aloud or screen-reader use harmed? | Screen-reader sessions at default punctuation settings |
| LLM authoring | First-attempt and post-validator correctness under each option, several vendors |

**Decision rule.** Adopt B for `mql.v0_1` unless it is worse on direction or binding-comprehension errors. A preference for one option does not count.

## 7. Grammar delta (Option B relative to plan Appendix A1)

```ebnf
Find     = "find", Binding ;
Binding  = Alias, ":", TypeName ;
Follow   = "follow", Alias, "through", (Binding | TypeName),
           ("to" | "from"), Binding ;
Add      = "add", Binding ;
Bind     = ("node" | "edge"), Binding, "by", PropertyName, "=", Value ;  (* PropertyName is _id or a declared unique property *)
Connect  = "connect", Alias, "through", Binding, "to", Alias ;
Field    = Property, ["as", Identifier] ;     (* default key: <alias>_<property>; metadata drops its leading underscore *)
```

- The lexer gains the `:` token.
- `as` remains reserved, but appears only in `Field`.
- The keyword count stays at 32.

## 8. Plan sections affected if adopted

- §8.1 (vocabulary and "one meaning" rule), §8.2, §8.3, §8.6, §8.8 (default keys and result example), §8.9 (write steps and `by _id`), §8.11 diagnostics, §14.2 / §14.5 (signature column names).
- §16.3 sync example, §18.4 MCP (generated MQL), Appendix A (grammar, fixture queries, diagnostics), Appendix C3 tasks, Appendix D queries, Appendix E examples, Appendix F code samples, and `spec/corpus/`.

## Sources

- **[A1]** TypeScript Handbook, *Everyday Types — Type Assertions* (`expr as Type`) and type annotations (`name: Type`). <https://www.typescriptlang.org/docs/handbook/2/everyday-types.html>
- **[A2]** PostgreSQL documentation, *SELECT*: optional `AS` for output names, keyword conflicts, and the recommendation to always write `AS`. <https://www.postgresql.org/docs/current/sql-select.html>
- **[A3]** SQLFluff, *Rules Reference*, AL02 "Implicit/explicit aliasing of columns" (explicit `AS` by default). <https://docs.sqlfluff.com/en/3.1.0/rules.html>
- **[A4]** Neo4j, *Cypher Manual — Label expression predicates* (colon form and `IS` form; GQL conformance). <https://neo4j.com/docs/cypher-manual/25/expressions/predicates/label-expression-predicates/>
- **[A5]** TypeDB, *TypeQL Reference — Match stage* (`$x isa user`). <https://typedb.com/docs/typeql-reference/pipelines/match/>
- **[A6]** Gel (EdgeDB), *With block* (`alias := expression`) and computed shape fields. <https://docs.geldata.com/reference/reference/edgeql/with>
- **[A7]** Microsoft, *Kusto `project` operator* (`ColumnName = Expression`). <https://learn.microsoft.com/en-us/kusto/query/project-operator>
- **[A8]** PRQL Language Book, *select* (`select {name = expr}`). <https://prql-lang.org/book/reference/stdlib/transforms/select.html>
- **[A9]** Malloy documentation, *Fields* (`dimension: full_name is …`). <https://docs.malloydata.dev/documentation/language/fields>

**Limitations.** This is a design comparison, not an empirical result. No source above measures the readability of `as` versus `:` for graph queries. The counts in §1 come from the plan's own examples, not from real user queries.
