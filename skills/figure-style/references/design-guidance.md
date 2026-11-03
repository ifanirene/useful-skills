# Figure Design Guidance

Read only sections relevant to the current chart or edit. Original section
numbers remain for older project references. The skill entrypoint defines
correctness requirements; numeric layout limits and stylistic prescriptions below
are defaults, not universal acceptance gates. Follow the requested venue and
project style. In particular, preserve a meaningful baseline and do not cut an
axis or force a percentage of occupied space merely to satisfy a layout target.
For Nature work, use the current [Nature guidance](nature-guidance.md),
[color defaults](colors.md), and [composition workflow](composition.md).

## §1 Data fidelity & self-consistency

**1.1 Excluded rows.** A row marked excluded or flagged in the source data is
either omitted entirely or drawn with a visually distinct open/hatched marker
and named in the key. It **never** enters a summary statistic plotted alongside
the included rows.

**1.2 Comparable conditions only.** Arms measured under non-comparable
conditions (different N, epoch budget, initialization, protocol) are not plotted
as visual peers. Separate them with a facet break or a marker on the label, and
state the difference once in the caption.

**1.3 Self-consistency.** Every key, threshold, and title inside the figure must
be satisfied by every plotted row. Before saving, walk each categorical outcome
label back to the rule that defines it; if a row's value contradicts its label
or the title, the figure is wrong, not the data.

**1.4 Claim-titles must be true.** A sentence-title (§5.1) is tested against
every category on the axis before rendering. If any contradicts it, qualify the
title ("on 3 of 4 pairs") or downgrade it to a description.

**1.5 State n and what was held fixed.** Every panel that draws a summary mark
states `n` and the unit of replication, and every small-multiple that holds a
variable fixed states the fixed value — in the panel or, when §2 budget is
tight, in the caption.

**1.6 Reference structure is reference.** A tree, ordering, or topology drawn as
*context* (a scale bar, a category strip) uses an established reference, not
one inferred from the plotted data. Infer the structure only when the structure
*is* the result.

**1.7 One number per claim.** A quantitative claim (runtime, accuracy, count)
has exactly one canonical value across every panel, caption, and the abstract.
Define what it measures and use that value everywhere.

---

## §2 Label economy — floor and ceiling

The figure shows the pattern; the **caption** carries the context. Design for a
general scientific reader, not the author.

**2.1 Identification.** Make every distinct series, symbol, and comparator
identifiable from figure plus legend. Put essential visual keys in the figure
when feasible. Comparator labels name the method/condition instead of an
ambiguous version label. Explain unfamiliar terms in the companion legend.

**2.2 Ceiling.** Per panel: title + axis labels + tick labels + series identity
(labeled once per row of small multiples) + at most 2–3 result annotations.
Count the strings; >6 beyond axes/ticks means you're over. The ceiling counts
*narrative* annotations (callouts, value labels, brackets) — identity labels are
floor, not budget.

**2.3 Move to the caption:** n=, what's-held-fixed, abbreviation expansions,
non-comparable footnotes, exclusion rationale, methodological caveats.

**2.4 Titles and headers.** Put a manuscript figure's full title in its legend.
Use short condition/comparison headers inside panels where useful. For reports
and slides, a supported finding can serve as an on-plot title. For a row of
small multiples, consider a shared header rather than repeated titles.

**2.5 Value-on-mark only for the headline number** — the one a reader would
quote. Everything else is read off the axis.

**2.6 When in doubt, delete the label and re-read.** If the message survives, it
stays deleted.

---

## §3 Axes, scales, small multiples

**3.1 Axis padding.** Axis limits clear the data by ≥ one marker radius on every
side; markers and text never touch a spine. `ax.margins(0.04)` after plotting,
or extend the limit past any annotation.

**3.2 Baselines and axis breaks.** Preserve a meaningful baseline, especially
when bar length encodes magnitude. Use a restricted range or clearly marked break
only when the measurement and comparison justify it, not to meet an occupancy
target. Never draw a reference line, threshold, or annotation inside a broken-axis
gap; the gap has no coordinate.

**3.3 Log axes get human-readable ticks** — `10²`, `10³`, or `1k / 10k / 100k`,
not raw exponents. **Never** draw filled bars on a log-scaled value axis (bar
length encodes ratio to an arbitrary floor); use points + median tick instead.

**3.4 Shared axes across small multiples.** A row or column of small multiples
shows tick labels once (leftmost / bottommost panel); interior panels keep ticks
but drop labels. When the panels share a y-axis and differ only by x-variable,
render them as abutting subplots (`wspace≤0.06`) with one row-header title.

**3.5 Use space deliberately.** Fit slots to their evidence, labels, and natural
aspect ratios. Adjust the grid when there is wasted space; retain whitespace
that supports legibility or meaningful shared baselines. There is no occupancy
percentage requirement.

**3.6 Direction of goodness.** When higher- or lower-is-better is not obvious
from the axis label, place a small upright cue ("higher = better") in the
margin — once per row of panels, never per panel, and never only in the caption.
A directional glyph embedded in rotated text rotates with it; set the cue
upright.

**3.7 Physical width.** Build at the target physical width and check the saved
page dimensions. Raster DPI governs sampling, not vector canvas width. Allocate
space for any new schematic without making existing text/marks unreadable.

---

## §4 Color

**4.1 Threading.** Bind entity colors once and reuse them for lines, fills,
markers, and annotation strips across figures. Default to black text with
swatches or keylines for Nature work. Explicit keys supplement color identity.

**4.2 Limit hues.** Use as few distinct hues as the data require. When the
figure compares a focal series against others, make the focal series visually
dominant (saturated, heavier weight) and render comparators with lower visual
weight (desaturated, lighter, or thinner). Keep the focal entity's assigned hue;
avoid reusing it for an unrelated meaning in the same figure. The focal series must
remain identifiable even when its mark is zero-width or coincident with others —
via outline, marker, or a light tinted band.

**4.3 Hierarchical categories.** When categories nest (groups within groups),
the outer level picks the hue family and the inner level samples within it.

**4.4 Continuous and diverging.** Use a perceptually suitable sequential map
for ordered magnitude, a diverging map around a meaningful reference, and a
cyclic map for periodic quantities. The null is 0 for a log ratio and 1 for a
ratio. A data median is a center only when deviation from that median is the
stated question. Normalize comparable panels identically.

**4.5 CVD safety.** Never rely on a red/green contrast for a binary or opposing
distinction. Check actual marks under relevant color-vision simulations. Use
additional encodings where necessary. A perturbation condition is a data series;
its color need not imply an alarm or disease.

**4.6 Two palettes, two legends.** When a figure uses two categorical color
systems, each legend sits adjacent to the first panel where its palette applies.

---

## §5 Typography

**5.1 Headers.** A necessary panel header identifies the condition/comparison
in plain language, regular weight, left-aligned. A manuscript figure title
belongs in the legend; finding titles on plots are appropriate for some reports.

**5.2 Role-mapped size ladder.** A figure uses **at most three** font sizes,
mapped to *role* not space: titles/axis-labels/series-identity at the base size;
legend/annotation text one step down; tick labels one step further. Panel
letters are the only exception (bold, larger). If a label doesn't fit at its
role's size, fix the layout or shorten the text — don't reach for an
intermediate size. The generic `apply_figure_style(sizes=(8,7,6))` is not the
Nature preset; use `nature_style.py` with 5–7 pt ordinary text and 8 pt letters.

**5.3 Nomenclature.** Species, gene, and variable names that scientific
convention italicizes are italicized. Abbreviated codes inherit the rule; expand
once on first appearance.

**5.4 Magnitude suffixes.** Large counts use `k / M / B` (`4.2B`, `120 kb`),
not comma-grouped full numerals.

**5.5 Numeric annotations.** On-mark numbers use at most 2 significant figures —
unless 2-sf rounding would make two distinct rows print the same value, in which
case show the digit that separates them. Text on a filled mark reaches ≥4.5:1
contrast; if it doesn't, place the text outside the mark.

**5.6 No internal codes.** Axis labels use plain-language names; codebase
abbreviations appear only in parentheses after the readable name or in the
caption. Comparator series are labeled with what they *are*, not a role word.

**5.7 Panel letters.** Bold, top-left, outside the axes box. Case follows the
target venue's convention; `panel_letter(ax, 'a', case=...)` handles either.

---

## §6 Chart-family guidance (by data shape)

**6.1 Categorical × numeric.** Show the distribution, not just the summary.
Chart choice follows n: jittered strip with a median tick for small n; box or
violin for large n; bar + overlaid raw points or bar + interval when the mean is
the message. The `errorbar='ci95'` helper uses a t-based interval for the mean; check its
assumptions and the independent replication unit before using it. Raw points
and summary uncertainty can both be useful: one shows observations, the other
precision of an estimate. Define both in the legend. A
category absent from a group is marked (`n.d.`, `—`, or a hatched ghost) at its
slot; an empty slot can be confused with zero. Identify a zero-valued bar with
a dot or label at zero; a positive-height stub would change its quantitative meaning.

**6.2 Single-observation categories.** A filled dot with a thin neutral stem to
the semantic zero (lollipop). Value labels sit beside the dot.

**6.3 Continuous series.** Mean-per-x as a line with markers; individual runs as
thin translucent lines or points behind it. Label each series with direct text
at the right end of its line in preference to a legend box. Summary glyphs
(per-bin mean/median) use a shape that cannot be mistaken for a raw observation,
identical across series, drawn below the raw points in z-order.

**6.4 Distributions on shared support.** When two distributions overlap heavily,
stack them as small panels with a shared x-axis or use a ridgeline. Overlay only
when the separation is visually clear.

**6.5 Matrices.** Add cell values only when exact numbers matter and remain
legible. Define normalization, limits, reference, and any saturation. Mark
missing values distinctly from zero. Linked panels use a common row order.

**6.6 Embeddings.** Dimensionality-reduction scatters (UMAP, t-SNE, PCA) drop
ticks and tick labels; a small corner arrow pair names the axes. Clusters are
labeled by thin leader lines to text in surrounding whitespace.

**6.7 Paired prediction vs. observation.** Stack the two as adjacent tracks with
identical x and color; let the alignment carry the comparison. Target regions
are translucent spans registered in the legend.

**6.8 Insets.** Connect a detail inset to its source region visibly — a bounding
box with connector lines, or a translucent wedge.

**6.9 Label relevant observations.** On a scatter of named observations, label
points needed for the question; extremes need no automatic annotation. After
rendering, verify every leader endpoint terminates within one marker radius of
the row it names.

---

## §7 Layout & narrative

**7.1 Show what is measured before the result.** A reader should grasp what's
being compared before seeing the comparison — via a plain-language title, a
labeled schematic, or panel ordering. Any schematic uses the same words and
glyphs as the data panels' labels.

**7.2 One figure, one message.** A multi-panel figure has a single sentence it
is trying to make true. Every panel either states it, supports it, or bounds it;
panels that do none of these belong in supplement.

**7.3 Legends live in whitespace.** Frameless, placed inside the figure's
natural whitespace, or replaced by direct labeling. Legend entries are
swatch-first, left-aligned, and resolve every visually distinct glyph on the
panel.

**7.4 Row-band headers for nested faceting.** When small multiples are grouped,
each group gets one spanning header, not repeated per-panel titles.

**7.5 The figure arc.** For a paper: Figure 1 renders the paper's one-sentence
pitch as data — scope, not architecture. Subsequent figures cover mechanism,
evidence, robustness, application. A panel is judged against the paper's pitch,
not just its own figure's claim; content moves between figures if that's where
the story needs it. (`paper-narrative` runs this review.)

**7.6 Don't re-decorate a passing panel.** Between revision rounds, a panel that
already passes is not made more visually complex to fix nothing. Adding marks or
labels to a clean panel is a regression.

---
