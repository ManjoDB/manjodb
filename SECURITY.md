# Security policy

## Status

ManjoDB is at the design stage. **No software has been released**, so there are no supported versions and no known vulnerabilities in shipped code. This policy applies from now, so that it is in place before the first release.

## Reporting a vulnerability

**Please do not open a public issue, pull request, or discussion for a security problem.**

Email **shanidze.geo2004@gmail.com** with:

- what you found and where (file, document, or component);
- how to reproduce it, or why you believe it is a problem;
- the impact you expect;
- how you would like to be credited, or whether you prefer to stay anonymous.

If you are not sure whether something is a security issue, send it anyway.

## What to expect

These are targets, not guarantees. ManjoDB is maintained by a very small team.

- **Acknowledgement** within 7 days.
- **An assessment** and a plan within 30 days of acknowledgement.
- **Coordinated disclosure.** We will agree a disclosure date with you. We aim to publish a fix and an advisory within 90 days of your report, sooner for serious issues.
- **Credit** in the advisory, unless you ask not to be named.

We will not take legal action against people who report in good faith, who avoid harming other people's data or services, and who give us reasonable time to fix the problem.

## Scope

**Today:** the contents of this repository, which are documents and brand files. Examples of useful reports are leaked credentials, an unsafe instruction in the documentation, or a flaw in a design that would become a vulnerability if built as written (for example in the authorization or backup design in the plan).

**After the first release:** the engine, the `manjo` CLI and server, the TypeScript client and schema packages, the MCP adapter, and the release artifacts and their build pipeline.

**Out of scope:** third-party services and packages that ManjoDB depends on (report those to their maintainers), and social engineering of maintainers.

## AI agents and tools

The plan treats AI agents as untrusted clients. If you find a way for generated or injected input to bypass validation, authorization, or the audit path, that is a security issue. Please report it as one.

## Supported versions

| Version | Supported |
| --- | --- |
| No release yet | Not applicable |

This table will list the supported versions once there are releases.
