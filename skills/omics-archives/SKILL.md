---
name: omics-archives
description: Find public omics datasets and inspect study metadata, sample annotations, and downloadable files in GEO, ArrayExpress/BioStudies, MetaboLights, MGnify, and PRIDE. Use for dataset discovery and reuse assessment, rather than literature-only searches or downstream analysis.
license: NOASSERTION
---

# Omics Archives

Find datasets that can answer the user's biological question, then verify their
experimental design and available files. This is an independent, instruction-only
skill: it works through public archive APIs with an HTTP-capable host and requires
no Claude Science installation, MCP server, or third-party Python package.

## Choose the archive

| Data sought | Archive | Typical accession |
| --- | --- | --- |
| Gene expression, functional genomics, epigenomics | GEO | GSE / GSM |
| Functional genomics with sample annotations | ArrayExpress in BioStudies | E-MTAB / E-GEOD |
| Metabolomics, including mass spectrometry and NMR | MetaboLights | MTBLS |
| Microbiome and metagenomics studies and analyses | MGnify | MGYS / MGYA |
| Proteomics, protein/peptide identifications and spectra | PRIDE | PXD |

Use a supplied accession directly. Otherwise identify the organism, tissue or
system, comparison, assay, and whether raw data or a processed matrix is needed.
Use the information already supplied; clarify only omissions that would change
which datasets qualify. Search across archives only when the question needs it.

Read [API routes and archive caveats](references/apis.md) for the selected archive.
Prefer an available archive connector for operations its current tools support;
inspect its schema before calling it. Otherwise use public HTTP GET requests via
the host's web tool, curl, or Python standard library. Report which route was used.
Installing this skill does not register a connector or expose new host tools.

## Search and verify

1. Translate the question into archive-specific search terms. Record the query,
   filters, date, endpoint, and any result limit. Start with a small page to verify
   the response schema before expanding retrieval.
2. Fetch the study record for plausible matches. Check organism, tissue, assay,
   treatment, controls, time points, and linked publications against the question.
   Search hits and paper abstracts alone do not establish eligibility.
3. Inspect sample annotations and file inventories when assessing reuse. Separate
   biological replicates from technical replicates, runs, and assay rows. Preserve
   missing values as unknown; a study-level sample count is not a per-group count.
4. Follow pagination for the requested scope, deduplicate by archive accession,
   and compare retrieved counts with API totals when supplied. Label capped,
   interrupted, or partially inspected retrievals explicitly. Link records mirrored
   across archives using accession cross-references; similar titles alone do not
   prove duplication.
5. Separate raw reads or spectra, processed matrices, annotation tables, and
   analysis outputs. Return archive-provided file links and sizes/checksums when
   available. Download files when requested; estimate large transfers from the
   inventory first and use the user's storage constraints. Retain original names
   and checksums in the consuming project's download manifest.

Use bounded requests with timeouts. Respect provider rate limits and Retry-After;
retry transient failures with backoff, stopping after three retries and reporting
the incomplete scope. NCBI allows three E-utilities requests per second without a
key. Keep credentials in the host's private configuration if needed. Public
metadata discovery should not require copying Science credentials or runtime files.
An HTTP failure, inaccessible record, or unsupported filter is not a negative result.

## Judge whether the data fit

Explain why a candidate can answer the question and what might prevent reuse:
missing controls, confounded batches, incompatible tissue, unmatched time points,
unclear replication, unavailable raw files, or missing sample-to-file mappings.
Distinguish a keyword mention from a measured feature. A protein identification
does not establish differential abundance; metabolite annotation does not by
itself establish confident chemical identification or absolute concentration.
MGnify pipeline versions and experiment types affect which outputs are comparable.

## Return the useful result

For a single accession, answer the requested metadata or file question directly.
For a shortlist, use a compact table with accession and source link, biological
system, assay, relevant comparison, verified sample information, file availability,
and the reason for inclusion or exclusion. Mark unknown fields explicitly.

State search coverage and any retrieval limit. Cite the archive records supporting
the selection. End with the biological or technical implication: which comparison
is feasible, what is missing, or what should be inspected before analysis. Keep
downloaded records, private queries, and analysis outputs in the consuming project.

## Source and scope

Original workflow authored for this library, informed by the public archive
documentation linked in [the API reference](references/apis.md). The name and
five-archive scope reflect Claude Science's Omics Archives connector. No connector
code, tool schemas, credentials, or runtime is copied. Its redistribution license
has not been established. This skill is not an exact replacement for the original
17-tool MCP server; it supplies portable dataset-retrieval guidance. No license is
assigned to this original package yet (`NOASSERTION`).
