---
name: image-generation
description: Generate, edit, or upscale local image files through the pinned Gemini and OpenAI CLI when explicit provider, model, size, quality, or multi-input controls are needed. Use the host image generator for ordinary in-app generation without those local CLI requirements.
license: NOASSERTION
---

# Image Generation

## Objective

Use the pinned standalone project at `../../projects/image_generation_skill` for local,
provider-selectable image generation, prompt-based editing, and upscaling. This adapter is the
only root Skill exposed to Agent discovery; do not separately link the upstream root document,
package modules, or CLI wrapper.

## Required context

1. Resolve this `SKILL.md` to its real location before following relative paths.
2. Locate `../../projects/image_generation_skill` from the real Skill directory.
3. Read the upstream `AGENTS.md`, any `WORKSPACE.md` it may add later, and
   `skills/skill_image_generation.md` completely before invoking or changing the package.
4. Run commands from the upstream project root and use its `.venv`.
5. If the checkout or environment is absent, initialize and install from the central library
   root:

   ```bash
   git submodule update --init projects/image_generation_skill
   uv venv projects/image_generation_skill/.venv
   uv pip install --python projects/image_generation_skill/.venv/bin/python -e 'projects/image_generation_skill[dev]'
   ```

## Routing boundary

- Use this Skill when the user needs a local output file plus explicit Gemini or OpenAI model,
  size, aspect-ratio, quality, editing, multi-input, or upscaling controls.
- Use the host's native image-generation capability for ordinary in-app generation or editing
  when provider-specific CLI behavior is unnecessary.
- Do not use this Skill for stock-image search, design review, asset catalog management, or
  publication of generated files.

## Local overlay and configuration

Private configuration belongs under `../../.local/image-generation/`, resolved from the real
Skill directory. The local upstream `.env` is an ignored projection of that overlay; the
credential values remain outside tracked public content.

- `env`: private API keys, generic 1Password references, and optional model overrides.
- `aliases.json`: private provider, model, input, output, or project aliases.
- `runtime/`: private source images, generated images, logs, and validation artifacts.
- `README.md`: private operator notes.

Inspect only the variables needed for the requested provider. Never print credential values,
place them in prompts, or copy them into the public adapter, upstream submodule, registry,
review packet, shell summaries, or generated metadata.

## Execution safety

- Installation and default validation are offline. A live provider call may incur cost and
  transmit the prompt and any input images; make it only when the user asks for actual image
  generation, editing, or upscaling and the selected provider is configured.
- Write outputs to the requesting project's explicit destination. If none is supplied, use
  the ignored local runtime overlay. Never write generated images into tracked registry files
  or the upstream submodule.
- Treat input images as private unless the user says otherwise. Do not reuse them in examples,
  tests, or public documentation.
- Use the upstream documented timeout and concurrency guidance for slow or batched calls, but
  keep the batch scoped to the user's requested outputs and verify every expected file.
- Preview generated results when the task requires visual quality assessment; successful CLI
  exit alone does not establish image correctness.

## Acceptance checks

- Exactly one `image-generation` root appears in each configured Agent discovery directory;
  no upstream project file is separately projected.
- The pinned commit, submodule URL, and upstream entrypoint match `manifest.json`.
- The upstream offline suite passes and `scripts/generate-image --help` renders.
- No live provider request occurs during installation or validation.
- Public files contain no private credentials, aliases, paths, source images, or generated
  artifacts.
