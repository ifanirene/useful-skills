# Methods style patterns

Use the target paper’s existing Methods to set terminology, paragraph shape and
level of detail. These are project defaults for compact life-science prose;
author and target-journal instructions take precedence. Existing prose is style
evidence, not proof that its experimental claims or parameters are correct.

## Voice and structure

Write in past tense with short descriptive subsection headers and coherent
paragraphs. Wet-lab prose often starts with the sample and action; computational
prose can start with the analytic goal when that goal is not already clear.
Both passive voice and first-person “we” are acceptable. Choose the clearer
sentence rather than prescribing one grammatical opening for every paragraph.

Keep material, manipulation, collection and readout in their scientific order.
For computational work, connect input, key transformation, output and downstream
use. State shared context once and keep one paragraph focused on one stage.
Do not impose one paper’s heading order on a journal with another structure.

## Select the level of detail

Retain information needed to understand and reproduce the reported work:
material and model identity, stage or timing, dose and route, critical conditions,
reagent identity, measurement definition, software and key settings. Explain a
custom score or non-obvious choice in plain terms, including what its direction
means. Keep implementation detail from burying the reason the analysis was done.

Use exact recorded values. A threshold’s value and the rule it implements are
required when they determine inclusion or interpretation; a numerical cutoff
does not license inventing a biological justification. Explain rationale when
known and useful. Keep unrecorded reasons in the unresolved-items report.

Describe only the retained workflow unless a method comparison is itself reported
or needed to understand selection of the final method. Do not add the history of
discarded branches or routine troubleshooting to otherwise complete prose.

## Reagent and sequence defaults

This project favors vendor and catalog information at first mention for all
named reagents, including media, serum and other commodity reagents. Preserve
that default unless the author or journal chooses another format. This is a
project preference, not a universal reporting requirement. Critical biological
materials and reagents must remain identifiable regardless of presentation.

- Report antibody target, clone when relevant, vendor, catalog number and dilution.
  Combine antibodies into a dedicated sentence or place each next to its use,
  whichever is clearer. Do not require one field order or one long list.
- Include lot numbers for rare or custom-conjugated reagents when recorded and
  relevant; never recover an experiment’s lot from a current vendor listing.
- Give instrument model and manufacturer rather than demanding a catalog number.
- Keep full primer sequences inline by default for named PCR or dial-out strategies,
  with clear primer labels; use a sequence table if the author or journal specifies
  that format. Do not lose the sequence or its link to the relevant assay.
- Define custom buffers by their recorded composition and pH at first use, or
  reference a complete accessible recipe. Do not guess missing concentrations.

## Sentence and quantitative mechanics

Use chronological connectors where they clarify dependent steps. Add purpose
clauses for non-obvious roles; do not append a rationale to every wash or cutoff.
“To …” is often a concise way to introduce an analysis goal. Participial openings,
“We next …” and inline enumerations are options, not required formulas.

Report incubation series as compact durations or narrative sentences according
to clarity; preserve every condition that changes the procedure. Use “Briefly”
only for an actual summary of a cited protocol, not to bypass critical detail.
Use full stops, commas or semicolons according to the relation between clauses.

Keep numbers, ranges and units consistent. Useful formats include “300g for
5 min at 4°C”, a clear R1/R2 read structure, and injection titer, dose and rate
with their units. These formats do not supply values missing from the sources.

Quote exact function arguments or command options when they define the
reproducibility boundary; otherwise describe the operation in scientific prose.
Use the target journal’s citation and unit conventions rather than enforcing
one superscript spacing rule or typography across all venues.

## Final prose check

Read the section without the working notes. A reader should understand the
material, analysis logic, readout and evidence needed to reproduce it. Remove
repeated context, internal paths, temporary run labels and editorial framing.
Check essential details against the matched source record. Keep unresolved
facts in a short separate author-query list, not placeholder-filled final prose.
