---
name: ai-programming-mindset
description: Diagnose and structure AI-assisted engineering work when an agent stalls at partial completion, success criteria are subjective, feedback is missing, or reasoning and orchestration roles are unclear. Not a general coding-style guide.
license: MIT
---

# AI Programming Mindset

## Objective

Make AI-assisted engineering converge on a verifiable result instead of stopping at a
plausible implementation. The central idea is that partial completion usually reflects a
broken feedback loop: the agent cannot observe the real outcome, or “good” was never defined
well enough to guide iteration.

This Skill adapts the public
[`bestpractice_ai_programming_mindset.md`](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_ai_programming_mindset.md)
guidance from `grapeot/context-infrastructure`, pinned in `manifest.json`.

## Establish the feedback loop

Before choosing an implementation, make four things concrete:

- **Outcome:** what state must be true when the work is complete.
- **Evidence:** tests, logs, screenshots, measurements, fixtures, or user-visible behavior that
  can distinguish success from a plausible-looking failure.
- **Observation channel:** how the agent will see that evidence after every meaningful change.
- **Stopping condition:** which checks must pass and which unresolved risks require human
  judgment.

Prefer measurable conditions and representative examples over adjectives such as “clean,”
“robust,” or “production-ready.” A test is useful only when it exercises the behavior that
matters; passing a narrow unit test is not evidence that the full workflow works.

## Separate responsibilities

- Use reasoning for problem framing, trade-offs, architecture, and hypotheses.
- Use agentic execution for tools, state changes, observation, and iteration against the
  external world.
- Use deterministic code for stable invariants, schemas, accounting, and transformations.
- Use model judgment for semantic interpretation or fuzzy trade-offs when explicit rules would
  be brittle, but surround that judgment with observable inputs and reviewable outputs.
- Keep problem definition, value judgments, risk acceptance, and final quality approval with
  the accountable human.

Reasoning is not a substitute for observing a changed system. Re-read current state after
mutations rather than assuming the plan still matches reality.

## Work toward outcome certainty

Give the agent freedom over implementation details unless a sequence or method protects a real
invariant. Favor a thin end-to-end slice that can be run and inspected, then iterate from
evidence:

1. create the smallest result that exercises the real path;
2. run it through the relevant observation channel;
3. compare the evidence with the success criteria;
4. change the diagnosis or implementation based on the mismatch;
5. repeat until the stopping condition is met.

Use files as durable, auditable state when that makes progress reproducible, but do not force
filesystem state onto systems with a better canonical store. Preserve raw diagnostic detail
needed for debugging while redacting credentials, personal data, and private endpoints.

When context becomes too large, narrow scope or split independent reading and verification
work only when the current host and user instructions authorize delegation. Do not prescribe a
fixed number of agents or parallelize work that shares mutable state.

## Private context

Machine paths, private fixtures, credentials, internal endpoints, and organization-specific
acceptance thresholds belong under `../../.local/ai-programming-mindset/`, resolved from the
real location of this `SKILL.md`, or in the consuming project's ignored files. Never copy
their values into the public Skill or registry.

## Acceptance checks

- Completion is stated as observable system behavior, not only code changes.
- The agent can access the evidence needed to evaluate that behavior.
- Tests and inspections cover the real integration path in proportion to risk.
- Reasoning, deterministic logic, model judgment, and human approval have explicit roles.
- Iteration responds to observed failures rather than repeating the same plan.
- Persistent state is auditable and uses the system's canonical store.
- Private configuration and diagnostic secrets remain outside public content.

