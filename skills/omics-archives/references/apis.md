# Public API routes

Documentation checked 2026-11-10. URLs below are starting points, not frozen
schemas. Inspect the live documentation and response before building a query or
parser. Encode query parameters with an HTTP client or curl `--data-urlencode`.
Never assemble download URLs from guessed file paths when the archive supplies links.

## GEO

- [Programmatic access](https://www.ncbi.nlm.nih.gov/geo/info/geo_paccess.html)
- [E-utilities documentation and usage policy](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- Base: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

Search `esearch.fcgi` with `db=gds`, an encoded `term`, and `retmode=json`.
To restrict to Series, combine the biological query with `gse[ETYP]`.
Page using `retstart` and `retmax` and compare with `esearchresult.count`.
Fetch `esummary.fcgi` with `db=gds`, the returned Entrez IDs and `retmode=json`.
Entrez IDs are not GSE accessions; retain both and check the summary's accession.
Use the linked GEO record and its SOFT/MINiML metadata for sample-level design.
Follow supplied supplementary-file and SRA links for processed and sequencing data.

Public lookup example:

```sh
curl --fail --max-time 30 --get \
  'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi' \
  --data-urlencode 'db=gds' \
  --data-urlencode 'term=GSE10072[ACCN] AND gse[ETYP]' \
  --data-urlencode 'retmode=json'
```

NCBI service use is subject to its [disclaimer and copyright notice](https://www.ncbi.nlm.nih.gov/About/disclaimer.html).

## ArrayExpress / BioStudies

- [ArrayExpress collection](https://www.ebi.ac.uk/biostudies/arrayexpress/)
- [BioStudies API help](https://www.ebi.ac.uk/biostudies/RH3R/help)
- Base: `https://www.ebi.ac.uk/biostudies/api/v1/`

Search `search` with `collection=arrayexpress`, `query`, `page`, and `pageSize`.
Check the response's actual pagination and total fields before iterating.
Fetch `studies/{accession}`; `E-MTAB-5061` is a public example.
The study contains nested sections, attributes, files, and links. Traverse these
structures rather than assuming a flat record. Locate the SDRF sample annotation
table and IDF protocol information. One SDRF row may represent an assay or channel,
so count biological samples using their identifiers and experimental design.
The search endpoint returns summaries; fetch the study before judging eligibility.

## MetaboLights

- [API documentation](https://www.ebi.ac.uk/metabolights/ws/api/spec.html)
- [Live API schema](https://www.ebi.ac.uk/metabolights/ws/api/spec.json)
- [Files and downloads](https://ebi-metabolights.github.io/guides/Files/)
- [Official client](https://github.com/EBI-Metabolights/mtblspy)
- Base: `https://www.ebi.ac.uk/metabolights/ws/`

Fetch `studies/{accession}`; `MTBLS1` is a public example. Inspect the returned
`mtblsStudy` and `isaInvestigation` structures rather than treating the response
as a flat sample table. Consult the live API documentation for public listing,
file inventory, and search operations. Listing accessions is not a full-text study
search; never interpret an accession list as verified biological matches.

Use study-linked ISA-Tab investigation, sample, and assay files to map experimental
factors and samples to raw/derived spectral files. Inspect metabolite assignment
files separately from raw spectra. Metadata files can be retrieved through
`studies/{studyid}/{filename}` using a filename obtained from the study inventory.
Search raw-data subdirectories as well as top-level metadata when building a file
manifest. Return incomplete inventory status if nested contents were not inspected.

## MGnify

- [Current REST API documentation](https://docs.mgnify.org/src/docs/api.html)
- Base: `https://www.ebi.ac.uk/metagenomics/api/v2/`
- [OpenAPI schema](https://www.ebi.ac.uk/metagenomics/api/v2/openapi.json)

Use v2 for current data. The official documentation says v1 was deprecated in
June 2026 and serves frozen data excluding V6 analyses. A successful v1 response
does not establish current search coverage.

List `studies` with `page_size` (up to 100). Read current search/filter and page
parameters from OpenAPI; v1 JSON:API syntax must not be assumed for v2. V2 list
responses use `count` and `items`. Fetch `studies/{accession}` and its documented
relationships; `MGYS00010397` is a documentation example. Retrieve analyses and
their detail records for download links and pipeline versions. Distinguish MGYS
studies, samples, sequencing runs, and MGYA analyses; their counts differ.

## PRIDE

- [Live OpenAPI schema](https://www.ebi.ac.uk/pride/ws/archive/v3/v3/api-docs)
- Base: `https://www.ebi.ac.uk/pride/ws/archive/v3/`

Search `search/projects` with `keyword`, optional `filter`, zero-based `page`,
and `pageSize`. The current schema describes an array response; inspect response
headers for totals rather than assuming an older HAL `_embedded` envelope.
Verify filter names and semantics against current documentation and returned
records; keyword matching alone may not enforce the intended conjunction.

Fetch `projects/{accession}`; `PXD000001` is a public example. List
`projects/{accession}/files` with pagination; the `/files/count` route supplies
an inventory count. Inspect raw spectra, result files, and experimental metadata.
For protein-to-project lookup, consult `/proteins/{accession}` and
`/proteins/search` in the live schema. The `/pride-ap/search/proteins` route
is an affinity-proteomics index and should not be described as all PRIDE protein
evidence. Absence there does not prove that a protein is absent from a dataset.
