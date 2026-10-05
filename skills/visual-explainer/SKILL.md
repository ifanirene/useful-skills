---
name: visual-explainer
description: Explain technical concepts, mechanisms, systems, and comparisons with interactive HTML diagrams, parameter controls, process steppers, or requested slide decks.
license: MIT
---

# Visual Explainer

Use the pinned [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer)
workflow to make complex ideas clear with figures and useful interaction.
This adapter exposes one skill; upstream scripts, references, and templates remain in their canonical project.

## Load the upstream workflow

Resolve paths from the real location of this file, including when installed through a symlink.
Read `../../projects/visual_explainer/plugins/visual-explainer/SKILL.md` completely before working.
Resolve its relative references, templates, commands, and scripts from
`../../projects/visual_explainer/plugins/visual-explainer/`, not from this adapter.
Read the upstream style guide before creating HTML and other references only when relevant.
If the pinned checkout is missing, report the missing dependency; do not improvise a different implementation.

## Apply project and host context

- The user's request and consuming project's instructions govern scope, content, paths, and approval.
  Do not turn an unrelated short answer or table into an unsolicited HTML artifact.
- Use the requested output path, or a suitable writable directory in the consuming project.
  Use the host's file preview or browser tools to show the result. In Codex, use `open_in_codex` when available.
- Produce a complete HTML file with working controls. Choose interaction that teaches a relation:
  change a parameter, step through a mechanism, compare states, or inspect relevant detail.
- Base factual figures on supplied or verified sources. Preserve uncertainty, conditions,
  and the distinction between observation and inference even where upstream discourages hedges.
  Clearly label illustrative simulations and their assumptions.
- Upstream's approximate STE guidance does not establish ASD-STE100 compliance.
  If the user requests controlled technical English, pair with `explain-ste100` when available.
- Use only tools actually available in the host. Optional Pi, MCP, PPTX, image, and video tools
  are not installed by this adapter. Inspect upstream scripts before running them.
- Check the rendered result and controls at useful desktop and mobile sizes.
  If live browser checks are unavailable, state which checks remain unverified.

Keep private drafts, local output defaults, and unpublished examples in the consuming project
or the ignored `../../.local/visual-explainer/` overlay, resolved from this file's real location.

## Attribution

Upstream is MIT licensed, copyright 2025 Nico Bailon; see
`../../projects/visual_explainer/LICENSE`. The pinned commit and source are recorded in `manifest.json`.
This adapter does not copy the upstream implementation or change it.
