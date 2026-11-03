# Multi-panel composition

Use for one coherent figure, starting from a question/claim plus source outputs,
or an existing figure to revise. A visual reconstruction supplies geometry and
labels, not verified data or evidence. Locate the original sources before
changing a quantitative claim.

## Plan

Write a small panel map in the project: panel letter, question, message, data
source, plot type, intended dimensions, shared scales/order/colors, and legend
facts. Match the strength of the figure claim to its evidence.

Give the principal comparison enough space. Put panels in a reading order that
introduces necessary concepts before their use. Choose the grid, panel count,
and presence of a schematic for this figure; the workflow does not prescribe a
12-column grid, a hero panel, or a minimum number of panels.

Borrow these design ideas from the Engreitz composition notes (attribution and
limits in [sources.md](sources.md)):

- An approach schematic can end in a small illustration of the actual readout,
  helping readers connect experiment and plot. Label a predicted outcome as a
  hypothesis; it must not be mistaken for observed data.
- Declare conditions with a key and reuse their colors in later panels.
- Align related heatmaps/tables by the same row order. A deliberate reordering
  needs a visible explanation.
- Share axes/colorbars when variables and normalization match. Keep enough local
  labels for readers to identify the comparison.
- Label the actual contrast, denominator, and sign. Read the direction back
  against a known observation before export.

These are design options, not measurements of the cited paper or automatic
requirements. The referenced paper PDF has not been bundled or independently
verified. No example artwork is bundled. Add a design example only after
inspecting a real published Nature figure, with a source link and panel-specific
observations; a plausible generated plot is insufficient.

## Build an editable composite

Prefer a single Matplotlib `Figure` with `GridSpec`, or an equivalent vector
canvas. Plotting functions should accept an axes object and shared style/mapping.
Use `width_ratios`/`height_ratios` to fit evidence rather than forcing equal slots.
Let layout engines arrange content within the fixed canvas; verify the export.

For independently generated panels, retain their PDF/SVG originals and use a
vector-capable composition application. Check their final placed scale, fonts,
and labels. Raster tiling is useful for a preview, but wrapping that bitmap in
PDF does not produce editable data graphics. The retired composer's PNG tiler
and host-specific SDK helpers are not part of this workflow.

Separate panel work only when it benefits the task and the host supports it.
Give each worker the same panel map, style file, category mapping, normalization,
source paths, and output dimensions. A single process is sufficient for a simple
figure. Inspect any sidecar explicitly; assume no automatic kernel loading.

## Review and change propagation

Inspect each saved panel and the full composite, including PDF/SVG output. Check
panel letters, alignment, shared furniture, legend binding, mark visibility,
font size at final scale, and label collisions. Spot-check values and directions
against source analysis. If using a reviewer, request located evidence and fixes;
zero findings is a valid outcome. Finding counts are not a quality target.

Distinguish figure-level layout defects from panel-local defects. Revise affected
panels, then inspect the composite again. Recheck the legend's sample sizes,
statistics, color descriptions, and answer whenever upstream results change;
recheck accompanying text if its claim is affected. A cosmetic change need not
trigger a scientific rewrite. Stop when material defects are resolved or report
the specific unresolved limitation.
