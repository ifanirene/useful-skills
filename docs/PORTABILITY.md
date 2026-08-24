# Skill Portability

## Portable core

Every Skill uses a directory with a required `SKILL.md` containing `name` and `description`
frontmatter. Any Agent that can read project instructions and Markdown can use this core by
following the central registry route.

Native discovery directories differ by Agent. That is why this repository keeps one canonical
Skill source and treats user-directory links as local projections.

The built-in link targets follow the current official documentation: Codex uses
`~/.agents/skills/`, while Claude Code uses `~/.claude/skills/`. Other Agents use the generic
`--target` option rather than an unverified hard-coded path.

## Python sidecars

The four initial Skills include `kernel.py`. Their original host loaded these helpers into a
live Python kernel when the Skill was activated. That behavior is not part of the portable
`SKILL.md` contract and must not be assumed on another Agent.

When a selected Skill refers to a helper such as `apply_figure_style()`:

1. inspect that Skill's `kernel.py` before execution;
2. import it explicitly from its absolute file path or reuse the needed function in the
   project's own code;
3. run the Skill's verification steps after execution;
4. never assume helpers from one Skill are already present in another session.

Agents that provide a persistent Python kernel may load the sidecar there. Agents with only a
shell can invoke a small Python entrypoint or write a project script that imports the sidecar.
The scientific workflow and QA rules in `SKILL.md` apply regardless of how helpers are loaded.

## Agent-specific extensions

Keep shared instructions in `SKILL.md`. Put optional host metadata in sidecar configuration
files supported by that Agent. Do not add host-specific frontmatter to the portable core unless
all intended consumers safely ignore it.

When a workflow truly depends on one Agent's unique execution model, create a small adapter and
state the dependency in `manifest.json` instead of making the shared Skill silently fail.
