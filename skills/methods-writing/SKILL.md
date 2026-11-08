---
name: methods-writing
description: Write or revise Methods, Method details, Experimental model and subject details, and related reporting sections for scientific papers, especially Nature-style life-science papers. Use when turning protocols, notes, figure plans, or old drafts into publication-ready methods prose; when checking a Methods draft for missing reproducibility details; or when filling in reagent, model, sequencing, software, and statistics information from primary sources.
license: NOASSERTION
---

# Methods Writing

## Overview

Write Methods text as publication-ready prose, not as a lab protocol. Preserve scientific accuracy, make the work reproducible, and surface missing information explicitly instead of smoothing over gaps.

Default to the scientific reader's perspective. Methods sections are external-facing scientific explanations, not internal analysis logs. Explain the goal and logic when introducing a specialized assay or analysis. State shared context once; routine downstream steps do not each need a new purpose sentence. Use enough detail for scientific understanding and reproducibility, but do not import repo-local bookkeeping, file names, temporary run identifiers, or other internal-facing notes unless they are genuinely necessary for an external reader.

Do not use editorial framing such as "manuscript", "manuscript-facing", "paper-facing", "reader-facing", or similar labels in generated Methods prose or code annotations unless the user explicitly asks for that framing. Prefer direct scientific wording that simply states the retained workflow and outputs.

When a branch, comparison, or exploratory step is no longer part of the retained workflow, do not narrate its removal in the final prose or code comments unless that omission is itself scientifically necessary to understand the method. Present the retained workflow cleanly instead of explaining what was excluded.

Use the target paper’s existing Methods as the first style reference when available; copy its level of detail and terminology, not unverified claims or outdated settings. Load `references/style-patterns.md` at the start of the task. Its register, reagent density and formatting are project defaults, not universal journal requirements. Load `references/compliance-core.md` before finalizing the draft or when auditing an existing Methods section for missing reporting items. Load `references/computational-methods.md` whenever the Methods section includes sequencing processing, image quantification, single-cell analysis, perturbation assignment, trajectory analysis, gene-program discovery, or statistical modeling.

Use companion skills only when they clearly help:
- Use `doc` or `docx-to-markdown` when critical source material is in `.docx`.
- Use `scientific-writing` when the task expands beyond Methods into broader paper drafting.
- Use web or vendor documentation only to recover concrete missing details such as catalog numbers, kit identities, software versions, or official nomenclature.

When the user also wants publication-supporting code, treat the script as part of the scientific communication package. The same external-facing standard applies to both the Methods text and the released script.

## Workflow

### 1. Gather the highest-priority sources

Read the target paper draft and the most authoritative source materials first.

Use this precedence order unless the user says otherwise:
1. User corrections and experiment-specific protocols
2. Project tables, legends, and curated notes
3. For computational analyses: final result objects together with the matching execution logs, configuration, generating code and environment records
4. Existing paper drafts
5. Previously published example Methods sections from the same group or project style
6. Official vendor, JAX, 10x, software, or repository documentation for missing factual details

This is a reading order, not a guarantee that one file type is always correct. Prefer the protocol and the user’s correction over older draft text. For computational facts, verify that each source belongs to the retained run: result objects establish stored values, dimensions and metadata; matching code and configuration define transformations and model settings; execution logs and recorded environments help establish what ran. Objects can omit parameters, scripts can change after execution, and lockfiles can describe a different environment. Reconcile discrepancies or report them; do not infer an absent setting or historical version from a current installation. Do not preserve a polished sentence if it encodes the wrong experiment.

If a Results draft exists for the same figure, panel, or analysis, read the relevant Results subsection before finalizing the Methods, especially for computational analyses and publication-supporting scripts. Use the Results to clarify the analytic goal, the primary versus secondary readouts, the comparison structure, and which outputs need emphasis. Do not import interpretive claims from Results into Methods; use the Results only to improve rationale, ordering, and emphasis.

### 2. Map the subsection structure before drafting

Make the Methods follow the order of the paper, not the order of a bench protocol.

Across the relevant subsections, make the following information available. Define shared material and study-wide context once; repeat it only when it changes:
- What was done
- In what material or model
- At what developmental stage, time point, or condition
- With what sample definition and experimental unit
- How the data were collected, processed, and analyzed

Keep every main figure panel and each quantitative supplemental panel anchored to a Methods home. If a figure has no corresponding Methods subsection, add one or flag the gap.

### 3. Draft in paper prose

Write full paragraphs for paper text. Use bullets only for your own working notes, missing-information reports, or questions to the user.

Follow these style rules:
- Use short, descriptive subsection headers.
- Prefer material-and-action openings for wet-lab paragraphs when they orient the reader; do not force the same opening into every paragraph.
- Introduce a specialized computational analysis with its purpose when needed; do not repeat the purpose before each routine downstream step.
- Convert stepwise protocol language into concise narrative prose.
- Keep related wet-lab steps together and related computational steps together.
- Use exact values for ages, doses, times, temperatures, filter thresholds, and read depths when known. Explain the functional role of a custom or non-obvious filter, score or selection rule when it affects interpretation. State a cutoff rationale only when supported; never invent a justification because a numerical threshold is present.
- Follow the project default of vendor and catalog information at first mention for named reagents, antibodies, kits, mouse lines and stains, including commodity reagents; report instrument model and manufacturer. Follow a different author or journal format when specified. Missing identifiers remain queries, not guesses. See `references/style-patterns.md` for placement and density.
- Include primer sequences inline in the text when they are part of a named PCR or dial-out strategy.
- Include software names, versions, references, and key non-default parameters in the same subsection as the assay they support. Quote non-default argument values verbatim when they are at the reproducibility boundary.
- Prefer the nature of the inputs over repo-specific file names. For example, write "ranked gene loadings for each program" rather than a local CSV path unless the exact deposited file is itself part of the scientific record.
- When citing custom code or pipelines, prefer the public repository or code-availability destination over an internal commit hash unless version pinning is scientifically important and publicly resolvable.
- If you mention a custom score, filter, or ranking metric, define it in reader-facing terms at first mention — including which direction of the score means what biologically.
- Keep a small number of high-value quantities that orient the reader (for example, number of genes used for enrichment, number of genes passed to an annotation model, major significance thresholds), but omit low-value run bookkeeping that matters only for repeating the analysis inside the same repo.
- Preserve the local writing voice: direct, specific, and compact rather than chatty or protocol-like.

Do not let the Methods read like instructions to another scientist in the imperative mood. Describe what was done in past tense.

### 3a. Draft computational methods with full analytic traceability

For computational subsections, make it possible for a reader to reconstruct the analysis path from raw or intermediate data to the reported result.

Balance traceability with audience relevance. External readers need to understand the analytic goal and logic of the method in addition to how it was run. Do not let internal implementation details bury the conceptual reason the analysis exists.

Across the relevant computational subsections, state the following when applicable, using a precise cross-reference for shared definitions:
- what data or matrices entered the analysis
- what software, package, or pipeline version was used
- what reference genome, annotation, feature reference, or custom resource was used
- what QC filters, thresholds, and exclusion rules were applied
- what transformation, normalization, integration, model fitting, or test was run
- what outputs or labels were produced and how they were used downstream

Verify computational parameters with the matched run sources described in Section 1. Use stored parameters when present, and check generating code, configuration, logs and environment records for settings absent from the object. A final table does not by itself establish how it was generated.

Do not collapse major steps into vague summaries such as "data were processed using standard pipelines." Name the actual commands, packages, and key parameters when they matter for reproducibility.

At the same time, do not let the section turn into an internal notebook. Prefer descriptions such as "program loading matrix", "cell-type enrichment table", or "Perturb-seq regulator effects" over local file names. Include counts and thresholds that shape interpretation, but drop repo-local output paths, checkpoint names, and batch bookkeeping unless they are essential to understand the method.

For computational subsections, keep one paragraph focused on one analysis stage:
- primary processing
- QC and filtering
- annotation or assignment
- downstream modeling or hypothesis testing

When the subsection involves single-cell or Perturb-seq analysis, follow the concrete reporting patterns in `references/computational-methods.md`.

### 3b. Clean up and annotate scripts for publication support

When the user asks for a script to accompany the paper, convert exploratory analysis code into a clear, inspectable script that a reader can run interactively and understand section by section.

Treat publication scripts as explanatory analysis documents, not just execution wrappers.

Follow these rules:
- Match the sequence of major analysis blocks to the Methods text when there is tension between the final paper narrative and the order used in older exploratory scripts.
- Prefer a flat, top-to-bottom interactive script over a monolithic pipeline; do not add `main()`, CLI parsers, or helper functions unless the user asks for them or the released script family already uses them.
- Use explicit section headers and dense comments before each major block so a reader understands what the block does, why it is there, and what object or output it produces.
- Name files, objects, and saved outputs by their contents — developmental stage, condition, biological group, or processed state — not by batch IDs, MOI labels, internal nicknames, or unexplained acronyms. Prefer names like `filtered_perturbseq_ec_seurat_with_state_labels.rds` or `Mouse_E13.5_heart_endothelial.h5ad` over cryptic shorthand. Keep raw file IDs as secondary provenance fields only.
- Remove internal-facing wording such as "reader-facing", "legacy quick fix", "temporary rerun", or repo-private shorthand. Replace it with concrete scientific descriptions.
- Print session information at the beginning of the script. If a stable environment snapshot is known, record that exact snapshot in comments and in the emitted log, then also print live `sessionInfo()` from the current run.
- Save outputs in the documentation or release area requested by the user when the script is meant to ship with the paper, rather than burying them in transient results locations by default.
- Keep release scripts consistent with the Methods text, including ortholog handling, normalization order, QC thresholds, integration logic, and final annotation terminology.
- If a threshold, label map, or species-specific filter is uncertain in the source scripts, surface that uncertainty clearly in comments and make the active choice easy to inspect.
- If a user flags a line or filename as confusing, assume the name needs to be rewritten in plainer language rather than defended as project shorthand.

Before finalizing a publication-supporting script, check that it answers these questions directly in the code comments:
- What data enter this step?
- Why is this step needed for the reported result?
- What transformation, filter, score, or label is being applied?
- What object or file should exist after the step finishes?
- Could a new lab member understand the top input/output block without already knowing project-specific abbreviations?
- Are the editable filenames descriptive enough that a reader could guess the correct replacement file?

### 4. Check reproducibility and reporting completeness

Before finalizing, verify that the section covers the core reporting items in `references/compliance-core.md`.

At minimum, confirm:
- Animal models, genotypes, source information, ages, sex handling, and approvals
- Sample sizes, pooling, replication, exclusion rules, randomization, and blinding when relevant
- Critical reagents with source identifiers
- Instrument model, manufacturer, key settings, and gating order where relevant
- Library preparation chemistry, sequencing platform, read structure, and target or achieved depth
- Processing pipeline, reference genome or annotation version, software versions, and assignment logic
- Statistical tests, covariates, correction procedures, and what `n` represents

Audit completeness across the Methods, figure legends, source-data tables and required reporting forms; do not repeat every item in every subsection. Keep sample sizes locatable. Define pooling, the analysis unit, independent replicates, pairing and nesting in the Methods prose where an assay or test introduces them. Exact per-panel counts and P values can be placed in inspected legends or source-data tables; do not assume an uninspected location contains them. A sequencing lane or a hemisphere is not automatically an independent animal. For descriptive analyses, define the aggregation and denominator without inventing inferential units. Mark an item not applicable only when the journal or checklist expects that disclosure.

### 5. Handle missing information carefully

Recover missing factual details from primary sources when the answer is stable and attributable. Prefer official sources such as:
- Vendor product pages or instruction PDFs
- JAX or MGI for mouse lines
- 10x Genomics documentation for kit chemistry and sequencing setup
- GEO, SRA, or portal records for public datasets
- Official software documentation or release pages for versioned pipelines

When a detail cannot be determined confidently:
- Ask the user only if the gap would materially change the scientific meaning
- Otherwise keep the prose conservative and report the unresolved item explicitly
- Distinguish confirmed facts from candidate source matches and inference. A current product page or software manual can identify a product or default; it does not prove which reagent, lot, version or setting was used in the experiment.

Never invent approvals, catalog numbers, doses, software versions, or sample sizes.

## Output Expectations

When producing a revised Methods section:
- Return publication-ready paragraphs
- Keep section order aligned with the paper
- Keep terminology consistent across subsections
- End with a short, explicit list of unresolved items when any remain

When reviewing an existing Methods section:
- Prioritize missing reproducibility details, factual inconsistencies, and figure-to-method coverage gaps
- Report the highest-risk omissions first

## Resources

- `references/style-patterns.md`
  Use for tone, subsection shape, and paragraph-level writing patterns modeled on the project example.
- `references/compliance-core.md`
  Use for the general reporting rules distilled from the compliance checklist sections 0-2.
- `references/computational-methods.md`
  Use for specific instructions on writing sequencing-processing, single-cell, Perturb-seq, trajectory, gene-program, and statistics subsections.
