---
name: graphify
description: Connect concepts across Markdown files, documents, and code; build, query, and visualize knowledge graphs with explicit and inferred relationships.
license: Apache-2.0
---

# Graphify

Use [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) to build
and explore concept graphs across a bounded folder of Markdown, documents, or code.
This package adapter loads the upstream workflow from the installed `graphifyy`
Python tool instead of copying its implementation or reference files.

## Load the installed workflow

The verified package version is `graphifyy==0.9.77`. Check `graphify --help` first.
Locate the interpreter in the existing uv tool environment:

```sh
graphify_tool_root="$(uv --no-cache tool dir)"
graphify_python="$graphify_tool_root/graphifyy/bin/python"
"$graphify_python" -c 'from pathlib import Path; import graphify; print(Path(graphify.__file__).parent)'
```

Read the packaged workflow completely before a graph operation. Select
`skill-codex.md` for Codex, `skill-opencode.md` for OpenCode, and `skill.md`
for Claude Code or another host. These files live in the printed package directory.
Resolve each `references/*.md` against `skills/codex/references/`,
`skills/opencode/references/`, or `skills/claude/references/` in that same package.
Other hosts may use the Claude workflow with their actual available tools.
Keep all subsequent Python operations in the resolved tool interpreter.
If the runtime or a reference is missing, report the missing dependency.

## Apply workspace and host authority

- The user's request and consuming workspace govern scan scope, output locations,
  documentation, Git operations, and permissions. Resolve the requested corpus before
  scanning; do not expand to unrelated data or generated outputs.
- This adapter activates for requested graph work. Installing it does not make graphs
  mandatory for every codebase question or add hooks, watchers, or project rules.
- Map upstream subagent instructions to the tools and concurrency limits actually
  available. Do not change host settings just to match an upstream example.
- Use the host agent for document semantic extraction when appropriate; headless
  semantic extraction needs a configured backend. Do not claim code-only extraction
  has analyzed concepts in Markdown prose.
- Preserve EXTRACTED, INFERRED, and AMBIGUOUS relationship labels and source locations.
  An inferred link is a hypothesis, not verified evidence or biological causation.
- Keep credentials and private runtime configuration outside the public skill registry.
  Honor the session's authorization before transferring content to another service.
- Keep generated graphs with the consuming project or its private overlay. Follow its
  manifest and documentation rules when graph construction changes scientific meaning.

## Completion

Check graph JSON, source references, and the written report. Inspect the rendered
HTML and useful controls when visualization is requested. Report extraction coverage,
missing sources, graph integrity issues, and any visual checks that remain unverified.
Installation verification alone does not establish semantic extraction quality.

## Provenance

The official package is `graphifyy`; the executable is `graphify`.
Upstream version 0.9.77 is Apache-2.0 licensed and includes `LICENSE`,
`LICENSE-MIT`, and `NOTICE`. The upstream runtime and sidecars remain unchanged.
