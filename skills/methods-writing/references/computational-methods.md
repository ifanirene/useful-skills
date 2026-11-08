# Computational Methods Instructions

Use this file when drafting or reviewing computational Methods sections. It is tuned for life-science papers with single-cell, Perturb-seq, image quantification, and downstream modeling.

## Core rule

Write computational methods as a sequence of analysis stages, each with named inputs, software, parameters, and outputs. The reader should be able to tell what entered the analysis, what was filtered or transformed, what model or algorithm was run, and what object was passed to the next step.

For manuscript Methods, also make the goal and logic of the analysis legible to an external reader. A computational subsection should explain why the analysis was introduced in the paper and what scientific interpretation it supports, not just enumerate the implementation.

## Recommended subsection order

For most omics analyses, use this order unless the paper structure clearly needs another arrangement:
1. Primary processing
2. Quality control and exclusions
3. Integration, clustering, and annotation
4. Perturbation or feature assignment
5. Derived scores, trajectories, or programs
6. Differential or association testing
7. Specialized downstream analyses

Avoid mixing all of these into one oversized paragraph.

## What every computational subsection should include

Make the following available across the relevant analysis stages when applicable; reference a shared definition rather than repeating it in every subsection:
- input object: FASTQ, BCL, BAM, count matrix, feature-barcode matrix, image stack, segmentation masks, or pseudobulk table
- software and version
- reference genome, annotation, whitelist, feature reference, or other custom resource
- key command, function, or pipeline step
- non-default parameters and thresholds
- unit of analysis: cell, nucleus, section, embryo, mouse, hemisphere, perturbation group, or pseudobulk sample
- output passed forward: filtered matrix, cluster labels, guide assignments, fate scores, program usage matrix, model coefficients, or DE table

Prefer reader-facing descriptions of inputs and outputs over repo-local filenames or transient run labels. Name the deposited pipeline or public code repository when useful, but avoid internal bookkeeping unless it is scientifically necessary.

If code or custom scripts were used, state where they are deposited or that they will be made available.

## Writing templates by analysis stage

### 1. Primary processing

State:
- how raw data were demultiplexed
- how reads were aligned or counted
- which chemistry or assay mode was assumed
- what reference genome and annotation were used
- what custom files were supplied

Typical content:
- `cellranger mkfastq`, `cellranger count`, `bcl2fastq`, `STARsolo`, `kallisto|bustools`, `bwa mem`, `minimap2`
- reference genome build and annotation release
- feature barcode or guide capture reference
- sequencing read structure when relevant to the pipeline choice

Example pattern:
"BCL files were converted to FASTQ with ... Transcriptome reads were aligned to ... using ... Guide-capture reads were quantified with ... using a custom feature reference describing ..."

### 2. Quality control and exclusions

State:
- what cells, nuclei, images, sections, or perturbations were filtered
- exact thresholds
- whether thresholds differed by cell class, assay, or batch
- how doublets, ambient contamination, low-complexity libraries, or low-quality images were handled

Typical metrics:
- genes per cell
- UMIs per cell
- mitochondrial fraction
- intronic fraction
- doublet score
- barcode-rank or knee criteria
- guide UMIs per cell
- library complexity or read depth

Do not say only "low-quality cells were removed." State exact thresholds and what they filter. Explain the basis for a non-obvious or interpretation-changing cutoff when the source supports it; do not invent a rationale for a recorded empirical choice.

### 3. Integration, clustering, and annotation

State:
- normalization method
- variable-feature selection
- dimensionality reduction
- integration or batch-correction method
- clustering method and key settings
- annotation approach and marker logic

Typical content:
- `NormalizeData`, `SCTransform`, `FindVariableFeatures`
- PCA, UMAP
- Harmony, Seurat integration, BBKNN, scVI
- clustering resolution and dimensions used
- label transfer or marker-based annotation

If annotations were based on an external reference, name the reference dataset and version.

### 4. Perturbation or feature assignment

For Perturb-seq, hashing, dial-out, or barcode assignment, state:
- which matrix or read set was used for assignment
- how singlets, multiplets, negatives, and uncertain cells were defined
- thresholds for guide detection
- MOI or multi-guide handling
- whether assignments came from Cell Ranger, DemuxEM, custom code, or another method
- whether downsampling, ambient correction, or calibration was applied

If assignment decisions affected downstream inclusion, say exactly which cells were retained. Distinguish an individual-guide threshold from a summed-gene threshold, and inclusive from strict inequalities. Define target-specific control exclusions, dominance rules and whether other target assignments remain allowed when those choices shape the comparison. Do not assume groups are mutually exclusive in a multi-guide assay.

### 5. Differential testing and association models

State:
- what comparison was made
- the unit of testing
- the model or test used
- covariates and batch terms
- low-expression filtering
- multiple-testing correction
- significance threshold

Typical examples:
- pseudobulk edgeR or DESeq2
- cell-level regression
- `propeller.ttest`
- SCEPTRE
- Spearman correlation
- elastic net or multinomial models

Do not report only the package name. State the hypothesis, contrast and direction. Define the independent replicate and any pooling, pairing or nesting. Keep the correction family explicit when showing only a subset of tested features. Do not substitute cell counts or sequencing lanes for independent animals without evidence.

### 6. Trajectory, state-score, or fate analyses

State:
- method used to infer pseudotime or transitions
- how root or terminal states were defined
- how scores were calculated
- which cells were included
- whether smoothing or binning was applied
- the space used for fitting versus visualization, when different
- whether roots and endpoints were supplied or inferred, and how weights and scales were normalized
- whether pseudotime is scaled globally or separately for each route; expression ordering alone does not establish chronological time or lineage conversion

For state scores, specify whether they were module scores, UCell scores, rank-based scores, or another metric, and reference or list the genes used. For smoothed profiles or density maps, define the denominator, weighting, aggregation across batches, smoothing scale and any support masking needed to reconstruct the displayed readout. Separate descriptive spatial density differences from inferential tests of state fractions or lineage weights.

### 7. Gene-program analyses

For cNMF, NMF, topic models, or latent programs, state:
- input matrix and cell subset
- gene filtering and normalization
- range of `k` values tested
- how the final `k` was selected
- how program stability was assessed
- how usage scores were normalized, including the order of row/column operations and any conversion to count-like responses
- how programs were combined into families and whether family memberships overlap, when relevant
- how programs were annotated
- how perturbation effects on usage were tested

When a subsection describes any downstream interpretation or labeling step, explain the interpretive logic, not only the mechanics. Readers should understand whether the labels or summaries were assigned manually, evidence-first, literature-guided, enrichment-assisted, classifier-based, or model-assisted, and what safeguards were used to keep them interpretable and reproducible.

If a custom score, filter, or ranking metric is used, define it in plain language at first mention rather than naming it only as code or jargon.

Retain a few high-value counts and thresholds that anchor interpretation, such as how many features, genes, images, regions, samples, or observations entered a downstream summary step and the main enrichment or significance cutoffs. Omit repo-internal file names, batch chunk counts, output paths, and checkpoint names unless the paper truly depends on them.

### 8. Image quantification and spatial analysis

If the analysis is imaging-based, state:
- how images were registered, segmented, or projected
- software and version
- what was quantified and at what unit
- blinding, if used
- inclusion or exclusion of fields or sections
- how summary measurements were aggregated

For spatial transcriptomics, also state panel design logic, segmentation approach, endothelial-cell identification criteria, and pseudobulk or section-level aggregation strategy.

## Single-cell and Perturb-seq specifics to check

For this class of paper, explicitly check for:
- number of biological replicates or pooled animals per batch
- library kit and chemistry version
- sequencing platform and read structure
- exact QC thresholds
- doublet handling method
- guide detection threshold
- guide assignment logic
- positive and negative control behavior
- knockdown estimation method
- batch-concordance or replicate-consistency assessment
- whether analyses were cell-level or perturbation-group level

## Style rules for computational prose

- Keep the prose compact, but do not hide parameters.
- Lead with purpose before implementation details when the subsection introduces a specialized downstream analysis.
- Name functions or commands when they are the real reproducibility boundary.
- Quote function arguments and option strings verbatim when they are non-default and critical: `the family argument was set to "multinomial"`, `with s = "lambda.min"`, `n.sv = 1`.
- Prefer one coherent paragraph per analysis stage.
- Avoid switching back and forth between biological interpretation and computational procedure in the same paragraph.
- Use past tense and manuscript prose, not notebook commentary.
- For a workflow-manager pipeline, name the framework and recorded version; report a DSL version when applicable. Describe its role directly without requiring a first-person or chronological sentence formula.
- Cite public repositories or code-availability locations in reader-facing prose; reserve commit IDs or local run identifiers for places where exact versioning is required and publicly recoverable.

## Method selection and comparisons

Describe the retained workflow by default. Include an alternative-method comparison
when it is a reported result or necessary to justify a consequential selection,
not merely because several tools were tried. State the selection criterion and
supported evidence; exact benchmark results belong here only when relevant to the
reported comparison. A concise tested rank range and stability criterion can define
a retained factorization without narrating each discarded run. Keep troubleshooting
history in project records. If a comparison is retained, identify its data, unit,
metric and selection rule without implying the benchmark proves every downstream
analysis valid.

## Citing literature to justify computational choices

When an analytical choice is motivated by community guidance or methodological literature (e.g., pseudobulk DE testing, ambient RNA correction, downsampling thresholds), cite the relevant publication inline with a brief phrase: "exercising caution as recommended by existing literature.[REF]" Do not simply list the package without context. This applies to:
- pseudobulk frameworks over cell-level tests
- doublet-detection approach selection
- correction of systematic biases in gRNA or barcode assignment

## Missing-information policy for computational sections

If a computational detail is missing, cross-check sources matched to the retained run:
- final objects and tables for stored values, dimensions, retained entities and recorded settings
- generating code and pipeline configuration for transformations, formulas, thresholds and arguments
- execution logs and recorded environments for runtime settings and package versions
- deposited code releases, workflow metadata and figure-generation code for the link from analysis to displayed result
- official documentation for stable nomenclature or a candidate default, not proof that the experiment used it

No file type guarantees complete provenance. An object can omit settings, a script
can have changed since execution, and a lockfile may not describe the executed
environment. Confirm the run association. Resolve conflicts or list the discrepancy;
do not silently substitute today’s package version or infer an unstored parameter.

If you still cannot determine a critical item, end with an unresolved-items note such as:
- software version unknown
- genome build not stated
- exact clustering resolution not recoverable
- multiple-testing correction not specified
- guide-assignment threshold not documented
