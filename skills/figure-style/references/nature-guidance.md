# Nature formatting: requirements and local choices

Checked 2026-10-26. This preset targets **Nature main figures**. Recheck the named
journal and display type before submission; Nature Portfolio is not one uniform
submission format. Editor instructions override this dated summary.

## Official sources

- [Building and exporting panels](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/):
  89 or 183 mm widths, 170 mm maximum height, 5–7 pt ordinary type, editable
  artwork, and an example accessible palette.
- [Artwork specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/):
  Arial/Helvetica, 8 pt bold upright lowercase panel letters, embedded fonts,
  accessible colors, labelled axes, and editable scale bars. PDF Type 42 is
  explicitly recommended for Matplotlib.
- [Initial submission](https://www.nature.com/nature/for-authors/initial-submission):
  legends below 250 words, independently understandable figures, exact sample
  sizes and defined replicates/error bars. Its approximate 90/180 mm widths are
  rounded; use the dedicated panel guide's 89/183 mm in this preset.

The 247 mm full-page depth in older guidance and the upstream lab YAML is not the
170 mm figure-height allocation in the current panel guide.

## Practical implementation

Construct at final physical size; inspect the **saved file's** page dimensions.
Cropping or later resizing changes physical text/mark sizes. Use an uncropped
canvas for exact-size exports and fix clipping through layout.

Use black text on white by default, with explicit swatches/keys for series.
Keep text, axes, scale bars, and labels as vectors in a PDF/SVG source. Raster
microscopy can sit inside a vector figure, with a separate editable scale bar.
Nature's image page states 300 dpi minimum for photography and recommends 450 dpi
for highest online-proof quality; the export section also asks for 450 dpi. Our
450 dpi raster default covers that target. Upsampling does not restore detail.

The panel guide requests editable main-figure vectors and lists PDF among the
preferred formats. Our PNG is a review/report preview. Extended Data instructions
use different formats and size/resolution rules: check them separately rather
than applying the main-figure preset unchanged.

## Local choices

`house_style.yaml` holds local defaults: 7 pt labels, 6 pt ticks/key text, 0.5 pt
axes/ticks, 1 pt data lines, an open frame, and explicit colors. The stroke widths,
palette ordering, and open frame are design choices, not universal Nature rules.
Small panel headers may identify conditions; the full figure title belongs in
the companion legend by default. Reports/slides may need different sizes/titles.

For project overrides, create `figures/style.yaml`, optionally followed by a
figure-specific YAML. Pass paths explicitly to `load_style(overrides=[...])`.
Use the same `defaults`/`colors` structure; an example is in
[colors.md](colors.md). Keep source requirements intact and document any
intentional departure; an override does not establish compliance.

## Example use

Import `nature_style.py` from its resolved skill directory, not a discovery-root
working-directory assumption. In a project script with that directory explicitly
added to `sys.path`:

```python
import matplotlib.pyplot as plt
from nature_style import load_style, apply_style, figsize_mm, save_figure

style = load_style(overrides=["figures/style.yaml"])
apply_style(style)
fig, ax = plt.subplots(figsize=figsize_mm(89, 65))
# Draw the analysis result and labels here.
save_figure(fig, "figures/fig1", style=style)
```

Inspect the resolved font files, vector text, final size, smallest labels, and
embedded raster resolution. The exporter checks ordinary text size, supported
font families, and canvas bounds in the live figure. It cannot establish panel
meaning, detect every overlap, or prove PDF font embedding; inspect the saved PDF.
