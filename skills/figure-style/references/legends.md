# Figure legends

Write a short title followed by panel descriptions in reading order. A legend
should let the reader interpret the figure without the main text. Match existing
legends from the same manuscript when available: title punctuation, panel syntax,
terminology and level of detail. Use them as style references, not as evidence for
the new figure's claims.

Under the dated Nature main-figure guidance, keep the complete legend below 250
words; verify the limit for the actual journal and figure type. See
[nature-guidance.md](nature-guidance.md). A working word target is not a journal rule.

## Choose what the reader needs

Include applicable information grounded in the source results:

- System, comparison, measured variable and units. Keep transformations,
  normalization and selection rules when they change what the reader can infer.
- Definitions of lines, colors, symbols, summaries and uncertainty. Group panels
  with a shared readout and define shared details once. If the same color changes
  meaning between panel groups, define it separately for each group.
- Sample sizes and their units where needed to interpret the evidence or meet
  journal requirements. Distinguish independent biological units from cells,
  technical repeats and nested observations; define independent repeats for
  representative images. Verify counts in the fact sheet even when the author
  omits them from a descriptive legend. Do not automatically repeat printed
  counts or add total cell numbers to every embedding.
- Test, sidedness, pairing and multiplicity adjustment when inferential results
  are displayed. Define statistical symbols; retain exact values in source data.
- Scale bars, attribution and source-data availability where applicable. Spell
  out nonstandard abbreviations on first use.

When inference is shown, state the independent unit and the sample size supporting
it; cell counts do not substitute for animal or donor counts. Explain the handling
of nesting or pairing where it affects interpretation.

Separate interpretive definitions from implementation details. A denominator or
control-exclusion rule may belong in the legend; fitting settings, seeds, software
versions, exact smoothing bandwidths and support filters usually belong in Methods
unless the reader needs them to interpret that panel. Keep paths, commands and
environment records in project provenance. A report caption may need more detail
than a manuscript legend.

Keep the title within the evidence and the body focused on what is shown. Use a
brief qualification where a specific misreading is likely. Do not automatically
append sentences announcing absent tests, absent confidence intervals or general
limitations when no such inference is suggested. Broader implications and limits
belong in Results, Discussion or Methods as appropriate. Removing boilerplate
must not turn an association into a causal or lineage claim.

## Draft, then verify

1. Extract a fact sheet: panel mapping, readouts, units, sample and replication
   definitions, normalization, controls, selection and displayed statistics.
2. Draft the title and panel groups in the manuscript's style. For each method
   detail, decide whether it changes interpretation or only enables reproduction.
3. Read the figure and legend together. Check each claim against the correct
   source panel/group and each key against the saved figure. A matching number
   somewhere in a manifest is insufficient; a top labeled tick is not necessarily
   an axis limit.
4. Check the actual final word count. Remove repeated labels, redundant counts
   and generic closing caveats before compressing essential readout definitions.
   Resolve unknowns as author queries; never invent n, tests or interpretations.

If external review is requested, give the reviewer the figure, verified facts,
relevant manuscript examples and the author's scope. When the author requests
advice before drafting and revision afterward, preserve that sequence. Ask for
specific edits or omissions, not expansion of every checklist item. Check the
reviewed text against the sources and the author's preferences before adoption;
model review is not scientific validation. External review is optional otherwise.

## Template

Use the manuscript's numbering and punctuation:

```text
Figure N. Brief title covering the whole figure.
a, [System, readout and essential visual key].
b–d, [Shared comparison and interpretation-changing definitions].
[Applicable replication, statistics, scale bars or attribution].
```

Resolve placeholders before delivery. Teaching examples must use real published
figures whose artwork and legends have been inspected at their source; keep
unpublished project examples outside this reusable skill.
