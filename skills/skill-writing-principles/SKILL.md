---
name: skill-writing-principles
description: Design or review reusable agent skill instructions for outcome certainty, clear boundaries, testable acceptance criteria, high information density, and progressive disclosure. Use the host skill-creation tooling separately for packaging and validation.
license: MIT
---

# Skill Writing Principles

## Objective

Write reusable agent instructions that improve the probability of a correct outcome without
turning a reasoning agent into a brittle natural-language script. This Skill governs content
design and review; use the current host's skill-creation tooling for directory layout,
frontmatter rules, metadata, and mechanical validation.

This Skill adapts the public
[`bestpractice_skill_writing.md`](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_skill_writing.md)
guidance from `grapeot/context-infrastructure`, pinned in `manifest.json`.

## Define the reusable contract

A useful Skill makes four elements unambiguous:

- **Objective:** the result it enables and the requests that should select it.
- **Acceptance criteria:** observable conditions another agent can use to decide whether the
  task is complete.
- **Resources and boundaries:** allowed tools and context, required inputs, authorization
  limits, failure behavior, and explicit non-goals.
- **Output contract:** artifact type, format, schema, destination rules, or handoff state.

Put certainty in the outcome. Prescribe a sequence only when ordering protects a dependency,
permission boundary, safety invariant, or genuinely fragile operation. Otherwise state useful
decision criteria and let the agent choose the route.

## Keep instructions enabling and dense

- Retain guidance that changes a decision or prevents a demonstrated failure.
- Separate hard constraints from recommendations.
- Give concrete examples when they clarify a schema or acceptance test; do not add examples
  merely to make the document look complete.
- Record traps only when they come from real failures, rework, or repeated misunderstanding.
  Do not invent speculative pitfalls for a new Skill.
- Preserve diagnostic detail such as exception type or response status when it helps recovery,
  but redact secrets, personal data, and private endpoints.
- Remove background material that can be discovered elsewhere and does not change execution.

Use progressive disclosure: keep routing, shared invariants, and essential acceptance checks
in `SKILL.md`; place substantial provider-, format-, or mode-specific detail in focused
references that are read only when needed. Do not create extra files or routing layers when a
short self-contained Skill is enough.

## Review boundaries and discovery

Before adding a new root, inspect the current registry for overlapping capabilities. Prefer a
focused update or a clearly differentiated name over two skills that compete for the same
prompt. Make the frontmatter description discriminating enough for selection without listing
every possible use case.

Keep private paths, credentials, customer examples, internal schemas, aliases, and unpublished
context under `../../.local/skill-writing-principles/`, resolved from the real location of this
`SKILL.md`, or in a consuming project's ignored overlay. Public examples must be synthetic or
explicitly public.

## Acceptance checks

- A new agent can identify the objective, boundaries, inputs, outputs, and completion state.
- Acceptance criteria are testable or name the required human audit explicitly.
- Process requirements exist only where deviation creates a concrete failure or risk.
- Hard constraints and optional methods are visibly distinct.
- The description selects the intended requests without becoming a catch-all.
- Every section materially improves task success; redundant background is removed.
- Supporting resources are linked with clear read conditions and are not loaded by default.
- Known pitfalls are evidence-based rather than speculative.
- Registry/index projections and host-specific validation are handled by the relevant creation
  and registry workflows.
- Private context remains outside the public Skill package.
