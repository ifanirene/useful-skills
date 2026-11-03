# Figure legends

Write a short title for the whole figure, followed by panel descriptions in
reading order and the information needed to interpret them. A manuscript legend
should remain understandable with its figure alone. Under the dated Nature
main-figure guidance, keep the complete legend below 250 words; verify a different
venue's limit. The official source is in [nature-guidance.md](nature-guidance.md).

## Legend contract

Include only applicable items, grounded in the source results:

- What each panel depicts: system, comparison, measured variable, transformation,
  normalization, selection, and units that change interpretation.
- Mean/median or other summary, error bars/bands, box/whisker definitions,
  reference lines, symbols, and any essential visual key.
- Exact group sample sizes and what they count. Distinguish independent biological
  units, technical repeats, and nested observations. For a representative image,
  identify the independent repeats supporting it and the scale bar.
- Test, sidedness, pairing, and multiplicity adjustment where inferential results
  are displayed. Define star thresholds if stars are used; preserve exact values
  in source data. Statistical annotations are optional when there is no valid test.
- Dataset attribution/citation and source-data availability where needed; spell
  out nonstandard abbreviations on first use.

Separate the independent-unit count from the number of points. If 500 cells
come from five mice, say both; do not imply 500 independent mice. Explain how
the analysis handles the hierarchy if inference is shown.

Use a title whose claim is supported by the figure. Keep the body descriptive;
place broader biological interpretation in Results/Discussion. Reserve detailed
protocols for Methods and local paths, regeneration commands, and environment
fingerprints for project provenance. Internal analysis reports can have longer
interpretation and provenance blocks when requested. The Engreitz report's
collapsible HTML format is not required for a manuscript legend.

## Draft, then verify

1. Extract a fact sheet from the source analysis: units, n, summaries, transforms,
   filters, tests/corrections, repeated measurements, keys, and sources.
2. Draft title → panels → shared statistical/replication information, referring to
   panel letters exactly as printed. Describe shared details once when unambiguous.
3. Read figure + legend without the main text. Check every quantitative statement
   against a named result/table, and every description against the final export.
4. Check the word limit and missing facts. Preserve unknowns as explicit draft
   queries; never invent a sample size, test, accession, or interpretation.

Matching a numerical value somewhere in a manifest is not enough: verify that it
belongs to the correct panel, group, endpoint, and analysis. An automated word
count or structure check cannot validate these associations.

## Template

```text
Figure N | Brief title covering the whole figure.
a, [What is depicted, including essential context and readout].
b, [Comparison/relationship; keys or reference lines if needed].
[Exact n and replicate definition, summary/error representation, applicable
tests, sidedness/correction, and scale bars]. [Source attribution if applicable].
```

The brackets are authoring placeholders; resolve them before calling a legend
final. Add a worked legend example only with its real published figure and
verified source; generated numerical claims are not teaching material.
