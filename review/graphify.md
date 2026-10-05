# Graphify installation review

## Scope and source

Install the official `graphifyy==0.9.77` Python tool and register one shared skill.
Source: https://github.com/Graphify-Labs/graphify . Package metadata and bundled
Apache-2.0, MIT, and NOTICE files were inspected. The source workflow delegates semantic
extraction to the host agent or a configured backend. The adapter respects the consuming
workspace and actual host tools, and does not install mandatory graph-first hooks.

## Decision

Investigator requested Graphify installation on 2026-10-05. The agent selected an isolated
uv package runtime plus a shared package adapter to avoid vendoring upstream code.
Cost: the runtime must remain installed for the skill to load. No branch switch, commit,
publication, hook, watcher, or private-data corpus scan is included.

## Verification

Verified on 2026-10-05:

- Official package import and CLI help passed; executables resolve through the existing PATH.
- Six discovery locations resolve to the shared skill: Agents, Codex, Claude Code, Gemini,
  OpenCode, and Antigravity. Codex, Claude, and OpenCode packaged workflows each have eight
  readable progressive reference files, including extraction-spec.md.
- Registry consistency passed: 21 skills, 20 profiles. Public-content scan passed:
  100 text files. Whitespace checks passed.
- A disposable synthetic corpus detected one Python file and two Markdown files.
  Code-only extraction built three nodes and three edges; a query returned the expected
  function call with source line attribution. This code-only run explicitly skipped prose
  extraction, so it does not validate Markdown semantic quality.
- No private research files were scanned. Live HTML interaction remains unverified.

## Promotion

Local installation is authorized. Named human functional and privacy approval remains
required before publishing or merging the registry changes.
