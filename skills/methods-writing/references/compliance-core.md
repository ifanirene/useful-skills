# Methods Compliance Core

Use this file as a condensed final-pass checklist for Methods drafting. It is distilled from the general rules and sections 0-2 of the local Nature-style compliance checklist.

## 1. Global rules

Across the Methods and their linked reporting locations, confirm the following when applicable. Shared study context need not recur in each subsection:
- what was done
- in what material or model
- at what age, stage, or condition
- with what sample definition or experimental unit
- how the result was analyzed

Also check:
- every main figure and every quantitative supplement panel has a matching Methods home
- datasets follow the paper’s logic, subject to the target journal’s section structure
- exact numbers are used when available
- repeated measurements are identified as technical or biological repeats
- software names, versions, and key parameters are tracked
- non-relevant reporting items are explicitly marked as not relevant when needed

## 2. Study-wide reporting items

### Ethics and oversight

Report:
- animal protocol approval body and institution
- species used in each experiment
- sex usage or why sex was not analyzed separately
- age or developmental stage for each experiment
- whether human or field-collected samples were used, if relevant

### Study design

Report:
- how sample sizes were chosen when known
- exclusion rules or that no exclusions occurred beyond predefined QC filters
- what was biologically replicated
- whether randomization was used
- where blinding was used and where it was not

### Statistics

For each inferential analysis, define the analysis unit, independent replicate structure, pooling, pairing and nesting in the Methods prose itself. Do not equate lanes, cells or two hemispheres with independent animals. Exact per-comparison counts and P values may be placed in inspected legends or source-data tables with clear links; do not assume those locations contain missing details. Check:
- exact `n` and what it counts
- statistical test and the hypothesis or contrast it addresses
- one-sided or two-sided status when relevant
- multiple-testing correction and the family of hypotheses it covers, where applicable
- summary statistic format
- exact `P` values where practical
- effect sizes, coefficients, or model terms when relevant

For descriptive analyses, define the population, aggregation and denominator. Do not invent tests or add standard statistical defaults that were not used. A shared statistical statement must not conceal analysis-specific exceptions.

### Software, code, and data

Record:
- data availability destinations or accession placeholders
- code repository or placeholder
- software used for data collection
- software used for analysis and figure generation
- versions for major packages and pipelines
- where custom code will be deposited

## 3. Reagents, models, and biological materials

### Animal models

Report:
- full strain names and source or stock number
- genotypes used for each experiment
- husbandry or housing details if journal style expects them
- timed pregnancy definitions or developmental staging method
- neonatal handling details when relevant to injections, hypoxia, or tissue collection

### Viral tools and perturbation reagents

Report:
- vector or capsid identity
- cassette design logic
- guide library composition and controls
- pool construction or validation QC
- production, purification, titer, and dose
- route, volume, timing, and interval to harvest

### Antibodies and stains

Report:
- target
- clone when applicable
- vendor
- catalog number
- RRID when available and easy to recover
- dilution or working concentration

### Cell lines and external datasets

When used, report source, accession, sample type and role. State that none were used only when the journal or reporting form requires that disclosure.

## 4. Missing-information policy

If a required item is missing:
- recover it from a primary source when possible
- otherwise leave the prose conservative
- end with a short unresolved-items list instead of guessing
