# Explicit color defaults

Use the same entity→color map throughout a project, including its schematics.
Preserve an existing, readable mapping on a targeted edit. Pick the encoding by
the variable's meaning before choosing hues.

| Data role | Default | Conditions |
| --- | --- | --- |
| Two categories | blue `#0072B2`, orange `#E69F00` | Arbitrary category assignment; keep it fixed. |
| Further categories | teal `#009E73`, purple `#CC79A7`, vermillion `#D55E00`, sky blue `#56B4E9`, black `#000000` | Check adjacent pairs at actual mark size; add labels/shapes or facets when crowded. |
| Focal observations vs context | blue `#0072B2`, gray `#B8B8B8` | Gray means context, not automatically nonsignificant/excluded. Define it. |
| Ordered unsigned quantity | `cividis` | `viridis` or a perceptually suitable single-hue scale may better fit a project. |
| Effect around a reference | `RdBu_r` | Blue negative, red positive; center on the scientific null, usually 0 for log fold change. A ratio's null is 1. |
| Missing measurement | gray `#D9D9D9`, explicit `NA` where feasible | Missing is distinct from zero/the diverging midpoint. |
| Labels/background | black/white | Use swatches with black key text. |

The categorical colors are from the palette illustrated in Nature's
[panel guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/).
Yellow `#F0E442` is available but omitted from the default cycle because fine
yellow marks on white can be difficult to see. These are local selections from
an accessible example palette, not a mandated journal identity.

For continuous data, follow the
[sequential/diverging distinction](https://matplotlib.org/stable/users/explain/colors/colormaps.html).
Comparable panels need the same normalization and numeric limits. With a diverging
map, explicitly set the center (`TwoSlopeNorm` or equivalent); choosing a colormap
name does not center data automatically. Preserve or explain saturated values and
any robust clipping. Periodic variables need a cyclic map instead.

## Project configuration

```yaml
colors:
  entities:
    Control: '#0072B2'
    Treatment: '#E69F00'
  sequential: cividis
  diverging: RdBu_r
  diverging_center: 0
```

Load this once and use `entity_colors(["Control", "Treatment"], style=style)`.
With an explicit mapping, missing labels are errors: a reordered dataframe must
not silently change colors. With no mapping, the helper assigns the configured
cycle in the supplied order; save that initial mapping for later figures. The
helper rejects more categories than available colors rather than recycling hues.

## Composition and accessibility

Carry color identities from the approach schematic into the data. Use one accent
for a highlighted result when that fits the question; multiple comparisons may
need multiple categorical hues. Avoid fixed meanings such as red=disease across
unrelated projects. Different metrics can use distinct scales, each clearly keyed.

Check actual marks under color-vision simulation and in grayscale when relevant.
Categorical hues and opposite diverging tails may merge in grayscale: use shape,
line style, sign labels, or separate panels to retain the required distinction.
Palette choice alone does not guarantee accessibility, especially with small,
transparent, overlapping, or pale marks. For dozens of programs/clusters, prefer
grouping, facets, or direct labels to an unresolvable long color key.
