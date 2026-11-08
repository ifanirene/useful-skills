---
name: assemble-figure-in-illustrator
description: Assemble scientific panels or revise part of an existing Adobe Illustrator figure using native JSX or computer interaction, with manageable objects, selective rasterization and editable annotations. Calls figure-style for plotting and visual style.
license: NOASSERTION
---

# Assemble figures in Illustrator

Deliver an editable native AI composition whose local panels and whole-page layout
both work at the final physical size. Use this for Illustrator assembly or local
replacement, not for artistic illustration or a standalone plot alone.

## Use the existing plotting skill

Read [figure-style](../figure-style/SKILL.md), resolving this link from the canonical
skill directory. Use its scientific checks, style configuration and plot helpers;
load its composition reference when planning a layout. Do not modify or copy that
skill. If the dependency is missing, locate its registered installation and report
what remains unavailable rather than silently inventing an equivalent.

For this assembly workflow, selective rasterization is an intentional exception to
figure-style's general preference for editable vector data graphics: dense marks
may be pixels, while text, axes and annotations remain editable. Preserve plotting
sources so the raster content can be regenerated. The user's task and project
settings determine that boundary.

## Establish the composition

Find the actual AI document, current unsaved edits, source plots, plotting scripts
and analytical outputs. A screenshot identifies appearance or location; it is not
a quantitative source unless the user explicitly requests embedding that image.
Work in a native copy unless in-place editing is requested; preserve unsaved work.
For a new figure, create a native document at the intended physical dimensions.

Inspect the full figure and inventory affected native objects before moving them.
Record panel slots, source mapping, required labels, stacking and unaffected areas
in the consuming project. Bounds alone do not establish panel membership: invisible
or clipped objects can extend far beyond the panel. Check covered old artwork too.

Set final panel size before redrawing. Judge visual weight, legend size and reading
order as well as alignment. If fitting a slot makes labels too small, revise the
plot or layout. Do not repeatedly shrink an exported panel to solve crowding.
Use project font sizes measured after placement. Do not treat one project's sizes
as a universal Nature rule; publication-specific checks belong to figure-style.

## Redraw an existing figure with new data

When the user supplies an existing figure and asks to redraw it with new data,
treat the original as the visual specification. The new figure must remain highly
similar unless the user requests a redesign. A data update alone does not authorize
restyling or replacing the original with a generic publication preset.

Inspect the original artwork before plotting. Reuse its editable source or plotting
code when available. Match panel arrangement, canvas and plot proportions, spacing,
colors and entity mappings, fonts and sizes, line widths, markers, axes and ticks,
legend placement, and annotation style. Preserve axis ranges and category order
when compatible with the new data and the original ordering rule.

Update data-dependent marks, values, labels, statistics, and annotations from the
new results. Make only necessary visual adjustments for new ranges or categories;
do not clip, distort, or alter data to imitate the old result. Explain any necessary
departure from the original appearance.

Before delivery, compare the rendered old and new figures side by side at the same
display size. Fix unintended style and layout differences. Completion requires
both accurate new data and high visual similarity; a valid or attractive plot alone
is not enough. If the original cannot be inspected, obtain it or state that visual
similarity remains unverified.

## Prepare manageable artwork

Read [plot-import.md](references/plot-import.md) when generating or replacing plots.
Rasterize dense heatmap bodies, gradient strips and point clouds where individual
marks need no manual editing. Retain vector axes, text, statistics and trajectory
lines. Keep sparse marks vector when that improves editing.

Reuse native panels once. Avoid assembling multiple cropped copies of a whole-page
PDF. Use named panel groups with only useful subgroups or layers. Keep meaningful
image or plot crops; remove only proven redundant wrappers. Zero masks is not the
objective. Lower mask counts do not prove lower object counts or visual fidelity.

## Operate Illustrator

Read [illustrator-operations.md](references/illustrator-operations.md) before JSX
or computer interaction. Prefer JSX for repeatable geometry, object inventories,
naming and exports; use the UI for visual inspection and unsupported actions.
Discover available tools and read their usage instructions. Do not assume a plugin,
script runner, menu command or API is present. Inkscape is optional, not a required
round trip. If Illustrator is unavailable, prepare assets and state that native
assembly and verification are incomplete.

## Acceptance and delivery

Check the saved native output, not only a working SVG or an old screenshot:

- Source coordinates, groups, values and statistical calls are preserved during a
  presentation edit. Rasterization did not introduce filtering or smoothing.
- The affected panel has the intended size, fonts, stroke widths, readable legend
  and statistics. No labels are clipped, substituted or unintentionally outlined.
- Dense regions are manageable; record object, clipping-group, raster and text
  counts with the counting method. Inspect nesting and actual selection behavior.
- Images have sufficient effective resolution after placement. Necessary masks
  remain; no repeated full-page artwork or exposed obsolete content remains.
- Native panel groups can be selected and moved independently. Check text editing
  in a working copy, and compare unaffected regions against the source.
- Inspect a fresh saved-file export both at reading size and in affected details.
  Review the complete layout after every material local size or placement change.

Deliver the AI, a fresh preview, changed panel exports, regeneration sources and a
short project receipt with input/output identities, final dimensions, raster/vector
choices, typography, checks and unresolved limits. Reuse existing project provenance
conventions. Do not claim analytical validation or journal compliance from geometry
or structure checks. Keep private artwork, paths and panel coordinates in the project.

For source provenance or reuse of external utilities, read
[sources.md](references/sources.md).
