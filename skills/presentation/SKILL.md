---
name: presentation
description: Create or revise presentation slide decks, keynotes, teaching decks, speaker notes, and previewable deck scaffolds. Default to image-rendered slides; use Reveal.js when exact text, editable HTML, code, real data, links, or interaction must remain in the DOM. Do not use for direct PPTX editing.
license: MIT
---

# Presentation

## Objective

Use the pinned standalone project at `../../projects/presentation_skill` to plan, scaffold,
render, preview, and validate presentation decks. Expose this adapter as the only root Skill;
do not separately link the upstream Markdown files under `skills/`.

## Required context

1. Resolve this `SKILL.md` to its real location before following relative paths.
2. Locate `../../projects/presentation_skill` from the real Skill directory.
3. Read the upstream `AGENTS.md`, any `WORKSPACE.md` it may add later, and
   `skills/skill_presentation.md` completely before creating or changing a deck.
4. Let the upstream root load only the supporting workflow needed for the request.
5. Run helper commands from the upstream project root and use its `.venv` when available.
6. If the project directory is absent, initialize the pinned checkout from the central
   library root with `git submodule update --init projects/presentation_skill`.

## Mode boundary

- Default new decks to image mode for cohesive full-slide visual composition.
- Select Reveal mode when exact or editable copy, code, real data, links, fragments, or
  interaction must remain in HTML. Do not silently change modes when rendering fails.
- Route direct `.pptx` creation or editing to a PPTX-capable Skill. This project produces
  image or Reveal decks, not native PowerPoint files.
- Keep the agent responsible for the argument, slide claims, visual direction, factual
  fidelity, speaker notes, and final review. Treat the Python helpers as scaffold and
  validation tools, not as an AI planner.

## Local overlay and outputs

Resolve private configuration from `../../.local/presentation/` relative to the real Skill
directory. The central repository ignores the entire `.local/` tree.

- `env`: optional credential-variable names and machine-specific tool settings.
- `aliases.json`: private brand, audience, asset, provider, and output aliases.
- `runtime/`: generated decks, images, PDFs, previews, logs, and validation artifacts.
- `README.md`: private operator notes.

Write deliverables to the requesting project when it supplies an output directory. Otherwise,
use the local runtime overlay. Never write generated decks or real configuration into the
public adapter or upstream submodule. Do not source `env` automatically, print credentials,
or copy private paths into public files.

## Execution safety

- Prefer the installing workspace's configured image-generation capability. Use the
  scaffolded OpenAI or Gemini wrappers only when the task requires live rendering and the
  user has configured that provider.
- Keep default validation offline. Do not make image API calls while installing, updating,
  or testing this Skill.
- Start live rendering with a draft-sized scoped batch before a costly final render.
- Bind the preview server to localhost. Do not expose it to the LAN unless the user asks.
- Preserve exact logos, screenshots, QR codes, charts, tables, numbers, and links as real
  assets or DOM content; do not ask an image model to invent them.

## Acceptance checks

- Exactly one `presentation` root appears in each configured Agent discovery directory.
- The pinned upstream commit and root entrypoint match `manifest.json`.
- The selected mode matches the content and editability requirements.
- The deck contains a plan, speaker notes, a working local preview, and a validation note.
- Public files contain no overlay values, generated decks, credentials, or private paths.
- Upstream offline tests and central registry checks pass after integration or code changes.
