---
name: figure-style
description: Create or review scientific plots for data fidelity, legibility, and publication-ready output.
license: Apache-2.0
---

# Scientific Figure Style

Produce a scientifically faithful, legible plot in the requested format and
style. For a small revision, inspect its source variant and change the requested
presentation; preserve the analytical meaning unless the user requests otherwise.

## Correctness

- Verify plotted values, categorical labels, thresholds, and claim titles against
  the source. Qualify a claim that the plotted evidence does not support.
- Excluded observations stay out of included-data summaries; if displayed, mark
  and explain their status. Distinguish missing measurements from zero.
- Identify the unit of replication and sample size for summaries. Make protocol
  or sampling differences visible when they affect comparisons.
- Choose scales, baselines, statistics, and uncertainty intervals appropriate to
  the data and inference. Do not truncate an axis just to fill space or use filled
  bars on a log value axis. Label actual reference values and their meaning.
- Define every series and visual encoding. Reuse entity colors consistently;
  supplement color where needed for accessibility. Center a diverging scale on
  the meaningful reference, not an arbitrary midpoint.
- Match labels and leader endpoints to the observations they name. Keep repeated
  quantitative claims consistent across panels, captions, and accompanying text.

## Conditional guidance

For chart choice or redesign, consult the relevant sections of
[design-guidance.md](references/design-guidance.md): §1 data checks, §2 labels,
§3 axes, §4 color, §5 typography, §6 chart families, and §7 layout. Those section
numbers also support existing `figure-composer` references. Treat numerical layout
budgets and aesthetic choices as defaults; task requirements take precedence.
A passing panel need not be redesigned to satisfy unrelated style preferences.

Use `figure-composer` when the deliverable requires composing multiple panels and
`paper-narrative` when revising the story across a paper's figures. A standalone
plot does not require either workflow.

## Helpers and output

For Matplotlib work using the bundled defaults, inspect and explicitly import
[kernel.py](kernel.py), then call `apply_figure_style` with the project's font,
frame, and sizes. Preserve established styling for a targeted edit. Other plotting
systems may implement the same requirements directly. Do not assume automatic
helper loading or host-specific artifact tools.

The sidecar includes `focal_palette`, `bar_with_points`, `strip_with_median`,
`end_of_line_labels`, `panel_letter`, `set_frame`, and `panel_crops`. Inspect the
relevant signature before use, especially crop coordinates and export settings.

## §9.2 Rendered-output review

Render the final export and inspect it at intended display size for clipping,
overlap, contrast, readable marks, and legend/leader correspondence. Use geometric
checks for suspected collisions; they do not replace visual inspection. For a
multi-panel export, inspect both individual panels and the composite. Fix defects
and recheck affected areas, then stop when the requested artifact passes.

Keep editable output where the requested format permits it and link the result.
State any unavailable visual validation; formatting checks do not establish
scientific validity.
