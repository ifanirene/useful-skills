# Sources and adaptation boundaries

## Existing library

The original `figure-style` and now-retired `figure-composer` were recorded as
Anthropic imports with Apache-2.0 frontmatter. Their exact upstream URLs were
not preserved; that historical uncertainty remains. Git retains the retired
implementation. This update keeps the generic plotting helpers and rewrites
composition as a portable workflow.

## Nature

The requirements reference public Nature pages checked 2026-10-26:

- https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/
- https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/
- https://www.nature.com/nature/for-authors/initial-submission

These are attributed factual summaries, not a license to redistribute Nature's
artwork. No publisher illustration is included. Recheck live instructions when
submission decisions depend on them.

## Engreitz Lab design and legend ideas

Reference project: [EngreitzLab/EngreitzLabAgents at bd501c4](https://github.com/EngreitzLab/EngreitzLabAgents/tree/bd501c4ec697a67fe94c6e7f6ed33ad5e8ae733f).
Inspected files at that pin:

- `style/house_style.yaml`: a shared style configuration, separating numeric
  settings from advisory design notes and allowing project/figure specificity.
- `style/figure_composition.md`: schematic/readout handoff, consistent condition
  colors, aligned comparisons, shared plot furniture, and explicit direction.
- `skills/analysis-report/legend_examples.md`: three teaching cases (paired
  peak-calling comparison, correlation, and multi-panel methods comparison), each
  followed by an explanation of its writing choices.
- `skills/analysis-report/lander_voice.md`: clear peer-scientist prose and precise
  quantitative statements; report-specific narrative rules were not imported.

No repository-wide upstream license was found at this pin. Accordingly, this
package includes newly authored prose, configuration, and helper code; it does
not vendor those files or
their numerical/example text, lab preferences, unpublished datasets, or figures.
The source's referenced figure PDF was not inspected, and its panel-level
observations are not represented here as independently verified observations.
Direct redistribution of upstream text/code/artwork needs a separate rights review.

Our YAML changes the old 247 mm height to the current Nature main-figure 170 mm,
distinguishes ordinary 5–7 pt text from 8 pt panel labels, adds explicit color
defaults, and uses a fixed export canvas. The helper is independent of the
Engreitz runtime. No teaching figures or worked numerical legends are included.
Published-panel examples require inspection of original Nature artwork before
inclusion. Test fixtures exercise software behavior only and are not presented
as design examples.
