# Assemble figures in Illustrator: design discussion

Status: discussion only; no new skill or registry entry has been created.
The investigator requested a separate skill that calls the unchanged figure-style.
Previous uncommitted Illustrator additions to figure-style were withdrawn.

## Scope and proposed approach

- Assemble and revise scientific figures in native Illustrator documents.
- Invoke figure-style for scientific plotting and appearance; do not modify it.
- Plan final panel dimensions before generating and importing local replacements.
- Reuse native panels once; avoid repeated cropped copies of the entire PDF.
- Rasterize dense heatmap bodies, gradient strips and UMAP clouds at source.
  Keep labels, axes, ticks, statistics and trajectory lines editable as vectors.
  Retain data and code for regeneration. Rasterization loses per-point editing;
  it does not require downsampling, smoothing or changing plotted values.
- Keep small heatmaps and sparse plots vector when useful. Base the decision on
  edit needs, native object counts and responsiveness.
- Keep meaningful crops; remove only verified redundant clipping wrappers.
- Use named panel groups and a few useful layers. Do not create a layer per mark.
- Use JSX for repeatable geometry, naming, inventory and export; use computer
  interaction for visual review and unsupported actions. Inkscape is optional.
- Validate saved AI structure and a fresh whole-page export. Fewer clipping masks
  do not prove fewer objects, readable type or visual fidelity.

## Investigator preferences and unresolved choices

Important labels should be at least 6 pt; subtitles around 7 pt, measured after
final placement. These are provisional project choices. Discuss Nature page
sizes and typography later; do not claim journal compliance from these values.
Choose raster resolution at the final placed size and inspect effective DPI.
Agree on the editable/raster boundary and panel hierarchy before creating the skill.
Files should be changed directly, with no patch-file delivery.

## References inspected

- https://github.com/creold/illustrator-scripts — JSX utilities; repository declares
  MIT. Candidate reference for basic operations. No code imported or executed.
  Review specific files, attribution and behavior before reuse.
- https://matplotlib.org/stable/gallery/misc/rasterization_demo.html — official
  examples of per-artist rasterization in vector exports, including pcolormesh.

No new functional skill test has been performed. This document records design
choices for discussion, not an installed or completed capability.
