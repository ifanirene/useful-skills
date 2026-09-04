---
name: innovation-assistant
description: Generate structured innovation candidates for products, services, features, or open problems using SIT or Think Bigger, with named precedents, derivation chains, scoring, and human checkpoints. Do not use for paradigm-level reframing, scientific discovery, or choosing among fixed options.
license: MIT
---

# Innovation Assistant

## Objective

Use the pinned pure-Markdown project at `../../projects/innovation_assistant_skill` to run
structured innovation. This adapter is the only root Skill exposed to Agent discovery; do not
separately link the upstream pipelines, axioms, or experiment files.

## Required context

1. Resolve this `SKILL.md` to its real location before following relative paths.
2. Locate `../../projects/innovation_assistant_skill` from the real Skill directory.
3. Read the upstream `AGENTS.md`, any `WORKSPACE.md` it may add later, and
   `skills/innovation_assistant.md` completely before running or changing the project.
4. Follow the upstream root's progressive loading: read `axioms/axioms.md`, then only the SIT
   or Think Bigger pipeline selected for the request.
5. If the project directory is absent, initialize the pinned checkout from the central
   library root with
   `git submodule update --init projects/innovation_assistant_skill`.

## Routing boundary

- Route an existing product, service, feature, or interface to SIT.
- Route an open problem without a committed solution shape to Think Bigger.
- Use Think Bigger as the outer loop and SIT as a tactic generator when both apply.
- Ask the user when the classification is genuinely ambiguous. If neither method fits, say
  so and recommend first-principles analysis instead of forcing a pipeline.

Keep the upstream human checkpoints intact: the user chooses the problem, states their wants,
makes taste calls on the shortlist, and owns real-world validation. When the user cannot be
asked, record substitutions in the upstream assumption table and mark affected conclusions
provisional.

## Evidence and execution boundary

- Use web search for named precedents and cite evidence near each tactic or factual claim.
- Preserve complete derivation chains and the pipeline's numeric validators.
- Do not present retrospective classification statistics as forward success probabilities.
- Label simulations as rehearsals; they do not replace feedback from real people.
- The pinned project contains no runtime code or install step. Do not add dependencies merely
  to load the Markdown workflows.

## Local overlay and outputs

Resolve private configuration from `../../.local/innovation-assistant/`, relative to the real
Skill directory. The central repository ignores the entire `.local/` tree.

- `aliases.json`: private product, organization, audience, or project aliases.
- `env`: optional names of credential variables for approved evidence sources; never
  auto-source it.
- `runtime/`: private inputs, working maps, reports, and validation artifacts.
- `README.md`: private operator notes.

Write reports to the requesting project when it provides an output location. Otherwise use
the local runtime overlay. Never copy private problem statements, customer information,
credentials, machine paths, or overlay values into this public adapter, registry, review
packet, or upstream submodule.

## Acceptance checks

- Exactly one `innovation-assistant` root appears in each configured Agent discovery
  directory; no upstream pipeline or axiom is projected separately.
- The pinned commit and root entrypoint match `manifest.json`.
- The routing decision and selected pipeline fit the problem type.
- Every final candidate preserves the upstream audit trail, evidence, scoring, and human
  checkpoint requirements.
- Public files contain no private overlay values or user problem artifacts.
