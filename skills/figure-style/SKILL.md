---
name: figure-style
description: Create, compose, revise, or review scientific figures, including multi-panel layouts, Nature formatting, consistent palettes, and figure legends.
license: Apache-2.0
---

# Scientific Figures

Deliver a scientifically faithful, legible figure and an accurate legend in the
requesting project's output location. This skill covers individual plots and
multi-panel figures; it replaces `figure-composer`.

## Establish the task

Use the question, source data or analysis outputs, intended audience, final size,
and requested file formats to choose the work:

- **Create or revise:** build a plot, preserving analytical meaning during a
  presentation edit. Reuse established project settings unless asked to change them.
- **Compose:** plan and assemble related panels; read
  [composition.md](references/composition.md) before choosing their layout.
- **Review:** inspect the source, legend, and final export; fix evidenced defects
  within the requested scope. An image alone cannot establish numerical fidelity.

For new publication figures without an established project style, use the bundled
Nature preset. For Nature submission work, read
[nature-guidance.md](references/nature-guidance.md) and verify the target journal,
article type, and main/Extended Data requirements. Current journal/editor
instructions take precedence. Record deliberate project overrides.

## Preserve scientific meaning

- Verify plotted values, labels, filters, thresholds, and claims against source
  results. Report a limitation when the evidence does not support the requested claim.
- Keep excluded observations out of included-data summaries; identify them if
  shown. Distinguish missing values from zero.
- Identify the unit of replication and exact sample sizes. Choose statistical
  summaries and uncertainty appropriate to the sampling design, including pairing
  and nesting. Add inference only when supported by the analysis.
- Select meaningful baselines and transformations; label contrasts and direction.
  Preserve comparable scales and category order across related panels.
- Keep repeated numerical claims consistent across figures, legends, and text.

## Set visual defaults once

Read [colors.md](references/colors.md) when assigning categories or continuous
scales. Keep one project mapping from entity to color; reuse it in schematics and
data panels. Use explicit keys or labels and an additional encoding when needed.

[house_style.yaml](house_style.yaml) separates official Nature constraints from
local defaults. For Matplotlib, inspect and explicitly import
[nature_style.py](nature_style.py); use `load_style`, `apply_style`, `figsize_mm`,
`panel_label`, and `save_figure`. It requires Matplotlib and PyYAML. Pass project
then figure overrides as explicit YAML paths; the most specific layer wins.
The helper checks font availability rather than silently substituting a font.

The older [kernel.py](kernel.py) remains available for generic styles and plot
helpers. Inspect signatures before use. For Nature work, apply the Nature preset
after generic helpers so their defaults cannot overwrite it. Other plotting
systems can implement the same specification directly.

For chart choice or a redesign, read only the relevant sections of
[design-guidance.md](references/design-guidance.md). Its numerical layout budgets
are suggestions; the requested endpoint and journal guidance take priority.

## Write and verify the legend

For a new or substantively changed publication figure, read
[legends.md](references/legends.md), write a companion legend, and check it against
every panel and the source analysis. For a small cosmetic edit, review the
existing legend and update only affected descriptions.

Design examples must point to real published Nature figure panels whose original
artwork has been inspected. Give the paper, figure/panel, source link, and the
specific design choice it illustrates. Synthetic test plots are not teaching
examples. This package currently includes no verified published-panel examples.
The adaptation sources and their limits are in [sources.md](references/sources.md).

## Export and inspect

Keep data graphics, text, and panel labels editable in the final vector output.
Build related panels in one vector canvas when possible; independently rendered
panels require a composition tool that preserves vectors. A PDF containing a
flattened PNG is a raster preview. Retain the editable plotting source as well.

Render the saved export and inspect both each panel and the composite at intended
size: clipping, overlap, readable marks, contrast, shared scales, color identity,
and correct legend/leader binding. Inspect PDF/SVG output as well as the PNG
preview. Geometric checks help locate defects but do not replace viewing.

Fix affected panels and recheck them and the composite. Stop when material
defects are resolved; report remaining limitations explicitly. If independent
review is useful and available, request findings supported by locations and
evidence, allowing zero findings. Delegation is optional.

Deliver the requested exports, plotting source/regeneration command, legend, and
effective style/color mapping in the consuming project. State what was checked
and which visual or scientific checks remain unavailable. Automated style checks
do not validate the analysis or guarantee journal acceptance. Creating a figure
does not authorize publishing it or starting an analysis-report workflow.
