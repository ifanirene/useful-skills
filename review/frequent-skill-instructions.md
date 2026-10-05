# Frequent-skill instruction revision

Local review of `literature-review` and `figure-style`, informed by OpenAI's
[Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).
The change narrows discovery, makes detailed guidance conditional, and defines
completion by the requested artifact and relevant checks.

## Behavior changes

- Literature searches follow the question and unresolved evidence gaps. Removed
  the suggested minimum paper count, mandatory citation expansion, automatic
  artifact for every multi-paper answer, and mandatory stylistic lint pass.
- Preserved retrieved-source grounding, citation metadata, contradictory evidence,
  correction/retraction checks where material, and explicit access limitations.
  Citation identity is distinguished from support for a claim.
- Figure correctness and rendered inspection stay in the entrypoint. Numbered
  chart/style guidance moves to `references/design-guidance.md` for conditional
  reading. Preserved the §9.2 reference used by `figure-composer`.
- Removed the axis-occupancy trigger for cutting axes. The t-interval helper's
  assumptions must be checked rather than claiming validity from small n alone.
- Helpers now require explicit inspection/import when used; no automatic kernel
  loading or host-specific artifact function is assumed.

## Registry and provenance

Canonical sources, licenses, and unresolved historical upstream provenance are
unchanged. Updated the two manifest descriptions, figure reference inventory,
README, skill index, and changelog. Profile membership, skill identity, discovery
links, and helper implementations are unchanged. No additional skills are exposed.

Only portable instructions and public references enter this diff. Local usage
statistics, original-file backups, machine paths, and private task details remain
outside the public registry. Existing unrelated working changes are retained.

## Validation and review

The five-skill local optimization batch passed skill frontmatter validation;
this registry contains two of those skills. An independent agent reviewed realistic
lookup, synthesis, figure-edit, critique, memory, and instruction-edit scenarios.
The review caught an axis-rule contradiction and a missing §9.2 reference; both
were corrected. The final review has no outstanding material findings.

Registry consistency, public-content scanning, local links, source preservation,
and whitespace are checked at application. These checks do not benchmark model
performance. No external literature APIs, helper computations, scheduled jobs,
or production artifact generation are part of this instruction-only validation.

Human functional and privacy approval remain pending for merge. Agent review
and passing checks do not replace those approvals. No merge or publication is
included in this local revision.
