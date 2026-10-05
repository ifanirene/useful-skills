---
name: literature-review
description: Find and verify scientific papers, compare methods, or synthesize evidence for a literature question.
license: Apache-2.0
metadata:
  third_party:
    - kind: service
      name: Crossref
      info_url: https://www.crossref.org/documentation/retrieve-metadata/
      privacy_url: https://www.crossref.org/operations-and-sustainability/privacy/
    - kind: service
      name: OpenAlex
      terms_url: https://openalex.org/OpenAlex_termsofservice.pdf
      privacy_url: https://openalex.org/OpenAlex_privacy_policy.pdf
---

# Literature Review

Answer the requested literature question with retrieved evidence. Match scope to
purpose: a specific-paper lookup may need one citation; a comparison needs a
tradeoff; a review needs synthesis. Ask only when ambiguity changes the search.

## Evidence

Retrieve the primary source before citing it. Verify authors, year, identifier,
and the passage supporting the claim; resolving a DOI verifies identity, not
claim support. Keep bibliographic metadata with the evidence. If full text is
unavailable, state the resulting limit and use only what the accessible source
supports. Never fill missing identifiers or author names from memory.

Choose available scholarly search tools for the field. Expand references or
cited-by links when a seminal source, contradictory result, or coverage gap
needs checking. Let the question and remaining evidence gaps determine search
breadth; there is no fixed paper count or citation-expansion quota. Check
corrections, retractions, and replication where they could change the conclusion.

Distinguish direct measurements from proxies, association from causation,
preprints from peer-reviewed work, and absence of evidence from evidence of no
effect. Evaluate the question's premise; a nearby paper is not evidence for an
unsupported claim. Preserve organism, population, intervention, and outcome scope.

## Deliverable

Lead with the answer and organize synthesis around questions or findings.
Compare agreement, contradictions, methodological differences, and remaining
uncertainty. Use connected prose for an argument and a table or list when the
requested comparison or bibliography benefits from it. Follow the user's length,
format, and citation requirements.

Default citations are linked author-year references using verified DOIs or stable
primary-source URLs. URL-encode parentheses in DOI links when needed. For a full
review or a requested reusable deliverable, save a Markdown artifact and link it;
a short lookup or comparison need not create a file. The response must still
contain the substantive answer. Report material access or verification gaps.

Finish when the requested claims are supported or explicitly unresolved and the
requested artifact is usable. Broaden the search only to resolve a material gap.

## Optional helpers

When available search tools are insufficient or DOI checks need batching,
inspect and explicitly import [kernel.py](kernel.py). It provides
`crossref_lookup`, `search_openalex`, `expand_citations`, and `verify_dois`.
Check the helper's current credentials and API requirements before use; callers
send queries to the external services declared in the metadata. Do not assume
an automatically loaded kernel or a particular connector name.

`style_pass` is an optional deterministic prose lint. Inspect its suggestions;
user-required formats and substantive limitations take precedence over stylistic
flags. It is not a citation or scientific-validity check.
