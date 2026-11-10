# Omics Archives addition — 2026-11-10

## Request and implementation

The owner requested a standalone Omics Archives capability in useful-skills.
The addition is an independent instruction-only skill using public archive APIs,
with an optional route through existing host connectors. It has no dependency on
Claude Science and does not install an MCP server or reproduce its 17 tools.
No global host configuration is changed by this addition.

The original connector has no established redistribution license. Its code,
schemas, runtime, and configuration are excluded. The new workflow is authored
locally from the primary sources linked in `skills/omics-archives/references/apis.md`.
The original package license remains unassigned (`NOASSERTION`).

## Scope and verification

- Registered `omics-archives` as experimental, with research/all/dedicated profiles,
  README, index, changelog, and provenance synchronized.
- Live HTTP GETs returned 200 with JSON for a BioStudies experiment
  (`E-MTAB-5061`), GEO accession search (`GSE10072`), MetaboLights study
  (`MTBLS1`), MGnify study listing, and PRIDE project (`PXD000001`).
- BioStudies search with `collection=arrayexpress`, `query=hypoxia`, and
  `pageSize=1` returned a study hit, page fields, and `totalHits`.
- MGnify v2 listing returned `count` and `items`. Official current documentation
  identifies v1 as deprecated and frozen; the reference explicitly uses v2.
- Live PRIDE OpenAPI confirms v3 search, project, file, and protein routes.
  Live MetaboLights API schema is available at `/ws/api/spec.json`.
- Registry validation, public-content scan, whitespace checks, and the host
  skill validator passed. The validator was run in an existing Python environment
  with PyYAML after the default Python lacked that dependency.

These checks establish packaging consistency and basic public endpoint access.
They do not establish exhaustive retrieval, correct sample mapping for every
archive, all protein-search semantics, or full behavioral equivalence with the
Claude Science connector. The skill instructs future runs to validate live
schemas, pagination, and biological eligibility for the actual query.

## Privacy and review state

New files contain public accessions, public documentation links, and generic
workflows. No private datasets, machine paths, credentials, original connector
source, or saved queries are included. Existing living-wiki changes were present
before this task and were left intact.

Prepared on `codex/add-omics-archives-20261110`. The owner subsequently requested
a commit and GitHub publication of this addition. Only the Omics Archives files
and registry changes are included in that commit; existing living-wiki edits
remain uncommitted. No host installation or merge is included. Human functional
and privacy approval for merge remains pending under the promotion policy.
