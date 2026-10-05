# Explain with STE: review packet

## Scope and provenance

Original instruction-only skill for concept explanations and technical drafting or revision.
Selected language guidance is paraphrased from official ASD sources linked in the skill.
No full standard, dictionary, private examples, external implementation, or scripts are bundled.
The original skill has no assigned redistribution license (`NOASSERTION`).

## Functional review cases

These are author-reviewed examples, not independent agent execution results or verified STE text.
Each draft needs full vocabulary review before a compliance claim.

### Explain a concept

Prompt: “Explain a cache to an adult who is new to computers.”

Draft:

> A cache stores copies of data that a computer may need again.
> The computer can read these copies instead of requesting the same data from its original source.
> This can reduce the time needed to get the data.
>
> For example, a browser can store a copy of an image from a website.
> It can use that copy when you open the page again.
> The stored copy can become out of date if the original image changes.

Review: defines the technical term, explains the process and its purpose, and gives an example and a limit.
Technical-term eligibility and general vocabulary remain unchecked.

### Preserve uncertainty during a revision

Source: “The intervention might reduce marker X; however, these results do not establish that it prevents disease.”

Draft:

> The intervention may reduce marker X.
> These results do not show that the intervention prevents disease.

Review: preserves the tentative claim and the limit on inference.
It does not change an effect on a marker into disease prevention.

### Put a condition before an action

Source: “Save the file only after the status reads READY, then close the editor.”

Draft:

> 1. If the status is READY, save the file.
> 2. Close the editor.

Review: preserves the required condition and action order, with one action per step.
READY is an exact status identifier, not a general vocabulary replacement.

### Review a compliance request without the reference

Prompt: “Certify that this paragraph complies with ASD-STE100. No dictionary is available.”

Expected behavior: produce or review a useful STE-style draft, identify missing vocabulary and rules checks,
and avoid a certification claim. A glossary or a sentence-length check does not close that gap.

## Validation and promotion

Run the skill frontmatter validator, registry validator, public-content scan, and `git diff --check`.
Preview the isolated `explain-ste100` discovery profile without changing host directories.
These checks verify packaging and common privacy patterns; they do not establish STE compliance or agent behavior.

Author checks passed: skill frontmatter validation, UI metadata checks, registry validation
(19 skills, 18 profiles), public-content scan, whitespace check, and discovery-profile preview.
The ten example sentences passed a simple sentence-length screen. This is not the standard's full word-count review.
The frontmatter validator needed PyYAML; it ran with a temporary dependency directory outside the repository.
Host discovery links were previewed but not installed.

Before merge, obtain explicit human functional and privacy review as required by repository policy.
