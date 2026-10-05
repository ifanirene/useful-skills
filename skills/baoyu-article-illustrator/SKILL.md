---
name: baoyu-article-illustrator
description: Generate scientific and article illustrations with consistent type, rendering style, palette, and reference images. Use for biological mechanisms, experimental workflows, and teaching explainers; use figure-style for quantitative plots.
license: MIT
---

# Baoyu Article Illustrator

## Source and loading

This is a small adapter for Jim Liu's MIT-licensed Baoyu Article Illustrator. The upstream
implementation and all supporting references remain in the pinned `../../projects/baoyu_skills`
submodule. Only this skill is projected into agent discovery.

1. Resolve this file to its real location before following relative paths.
2. Read `../../projects/baoyu_skills/skills/baoyu-article-illustrator/SKILL.md` completely.
3. Resolve all upstream relative references from that upstream skill directory, including
   `references/workflow.md`, the selected style, prompt construction, and configuration.
4. If absent, initialize from the library root with
   `git submodule update --init projects/baoyu_skills`.
5. Follow the current host's actual tool schemas and instructions. Upstream example tool
   names and arguments are illustrative, not a replacement for runtime documentation.

Upstream path correction: the `references/style-presets.md` link inside
`references/usage.md` is relative to the upstream skill root, not to the usage file.
Resolve it as `<upstream-skill>/references/style-presets.md`.

## Scientific illustration

For scientific content, recommend the upstream `scientific` style unless the user specifies
another style. Read `references/styles/scientific.md` in the upstream skill directory.
Select the image type from the intended explanation: flowchart for experimental steps,
comparison for conditions, or infographic for a mechanism.

- Establish the entities, anatomical compartments, relationships, and intended claim from
  user-provided source material before generating.
- Preserve species, cell identities, molecular names, directionality, and intervention details.
- Distinguish established mechanisms from hypotheses; causal arrows must match the evidence.
- Keep palette, line treatment, label conventions, and reference images consistent across a series.
- Never invent measurements, microscopy, statistical support, or experimental outcomes.
- Route quantitative plots to `figure-style` and figure assembly to `figure-composer`.
  Generated illustration is a conceptual schematic, not experimental evidence.

## Configuration and execution

Use upstream project or user `EXTEND.md` preferences. Keep real preferences, reference images,
source text, prompts, and generated output in the requesting project's private storage or an
ignored local overlay, never in this public adapter or the upstream submodule.

Use the current host's native image generation when available under its own skill and tool
contract. Do not install other Baoyu skills or run upstream provider scripts automatically.
Inspect any required helper before executing it. Installation and structural validation must
not trigger live image API calls.

Carry existing user authorization forward under the current host's instructions. Ask only
for missing information that materially affects the image. Save complete prompts before
generation, as required upstream, and retain the selected style and reference associations.

## Outputs and acceptance

Return the illustration files, saved prompts, and upstream outline in the requesting project.
Visually inspect every delivered illustration for label spelling, legibility, anatomy,
relationship direction, unsupported claims, and style consistency. Report unresolved defects;
passing registry checks does not validate biological accuracy or image quality.

For installation, verify the pinned commit and entrypoint, supporting reference files,
registry checks, and discovery links. Human functional and privacy review remains required
before merging the registry change.
