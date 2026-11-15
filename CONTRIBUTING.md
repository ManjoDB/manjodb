# Contributing to ManjoDB

Thank you for your interest. ManjoDB is at the **design stage**: the repository holds an architecture plan, research notes, and brand files, and no code has been released. That shapes what is most useful right now.

By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md). For security problems, do not open an issue; follow [SECURITY.md](SECURITY.md).

## What helps most today

- **Challenge the plan.** Read [`ManjoDB-Grand-Plan.md`](ManjoDB-Grand-Plan.md) and tell us where it is wrong, unclear, or too ambitious. The plan states its assumptions as hypotheses, and a good counterexample is a real contribution.
- **Correct the research.** The notes in [`research/`](research/) cite sources and mark what was not verified. Corrections, better sources, and missing competitors are welcome.
- **Test the query language on paper.** MQL is a candidate, not a settled design. If you write the example queries for your own use case and find they do not work, that is valuable evidence.
- **Share a real workload.** Dependency impact, data lineage, permission explanation, and similar relationship questions drive the design. A description of yours (without private data) helps decide what comes first.
- **Take part in the usability study** when it starts (plan, Appendix C).

## How to propose a change

1. **Open an issue first** for anything beyond a typo or a clear factual correction. Describe the problem before the solution.
2. **Keep pull requests small and focused**, one idea each, with a short explanation of why.
3. **Larger design changes go through an RFC**, as the plan describes (§29). The `rfcs/` directory does not exist yet. Until it does, discuss the proposal in an issue.

## Standards for documents

The documents follow rules that a contribution must keep:

- **Evidence rules.** Do not state a benchmark, a customer result, an adoption number, or an implementation status that does not exist. A claim about another system needs a source. A claim about ManjoDB is a *requirement* or a *hypothesis*, never a result.
- **Say what you did not verify.** Mark vendor claims, snippet-level facts, and anything unchecked as such.
- **One canonical answer.** Each design question has a home section in the plan. Link to it instead of restating it, and update every section a change affects, including examples.
- **Plain, precise language.** Avoid absolute words such as "fast", "safe", "scalable", or "production-ready" unless they are defined or measured.
- **Keep examples consistent with the current MQL grammar** (plan §8 and Appendix A).

## Commit messages

Use short, imperative subjects. When the monorepo exists, we expect conventional commits with the seam as the scope, for example `docs(spec): …` or `fix(mql): …` (see [`research/monorepo-structure.md`](research/monorepo-structure.md)).

## Licensing of contributions

ManjoDB is licensed under the [Apache License 2.0](LICENSE). Under Section 5 of that license, unless you state otherwise, any contribution you intentionally submit is licensed under the same terms. Do not submit anything you do not have the right to contribute.

**Sign-off.** We may adopt the Developer Certificate of Origin (a `Signed-off-by:` line on each commit). That decision is open (plan §29), and **sign-off is not required yet**. If it is adopted, it will be announced here before it applies.

## Code contributions

There is no code or build system yet. The planned stack is a Rust engine and an Nx monorepo (plan §5). Code contributions will open when the repository scaffold exists (milestone M0, plan §25), and this file will then describe how to build, test, and run the checks.

## Getting help

Open an issue with your question. If it involves a private matter, such as a conduct concern, use the contact in the [Code of Conduct](CODE_OF_CONDUCT.md).
