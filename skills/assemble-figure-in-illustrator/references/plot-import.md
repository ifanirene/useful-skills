# Plot preparation for native editing

## Choose what remains editable

Use the original plotting script and data to generate a local panel at the final
slot dimensions. Choose representation by edit needs, not the file extension:

| Content | Starting choice |
| --- | --- |
| Dense UMAP or other cell cloud | Raster marks; vector labels and trajectory lines |
| Large heatmap or finely sampled gradient strip | Raster body; vector ticks, labels and legend |
| Small heatmap or sparse dot plot | Vector when individual marks remain useful |
| Curves, error bars and statistical annotations | Vector |
| Micrograph | Raster image with a meaningful crop |

In Matplotlib, apply rasterization to the intended artist (for example a mesh or
scatter collection), not the entire axes or page. Keep text as text for supported
vector exports. A mixed PDF/SVG must be tested on import: its extension does not
prove that Illustrator preserved text, images or hierarchy.

Rasterization changes representation, not scientific sampling. Preserve points,
ordering, color normalization, alpha and interpolation. Do not replace the plot
with a subsample, smoothed density or newly interpolated heatmap unless requested.
A native gradient can be an alternative only when it reproduces the original
mapping; a visually similar gradient is not enough for a quantitative colorbar.

Set raster resolution from final placed dimensions. Effective DPI equals pixel
width divided by placed width in inches (and independently for height). Enlarging
an image lowers effective DPI. Use the target output requirement or a recorded
project choice; do not declare one DPI correct for every kind of image. Check
small points, antialiasing, transparent edges and color against the source.

## Prevent import debris

Prefer one local panel export over a crop of an entire multi-panel PDF. Use explicit
SVG image width and height. Verify zero-sized or scale-zero images against the native
source: they can be lost covers, not disposable objects. Test the chosen export in
Illustrator before importing many panels.

A plot viewport may legitimately clip out-of-range marks. Remove its clipping only
when all relevant content is contained, or after a true crop with equivalent output.
Do not globally disable clipping or release every mask to reduce a count.

After import, inspect editable text, embedded/linked image state, bounds, object
counts and visual appearance. Package required linked assets or embed them according
to the handoff. Avoid image tracing: converting pixels back into many paths defeats
the reason for rasterization. Re-render a dense panel at source instead of repeatedly
flattening an already converted composite.

## Typography and layout

Keep project typography settings with the figure. Record important-label minimum,
subtitle size, font family and final physical size before assembly. Check actual
placed text, including mixed-size spans; source-script settings alone are insufficient.
If a project specifies 6 pt important labels and 7 pt subtitles, enforce those values
at final size. These are example project settings, not universal publication rules.
Preserve symbols and italics; do not outline text merely to hide a missing font.
