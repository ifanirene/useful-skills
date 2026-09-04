---
name: research-paper-analysis-writing
description: Research and write a reader-first technical analysis of one or a small set of scientific papers, separating paper claims, external evidence, and analyst judgment while locating the work in its technical or product ecosystem. Do not use for broad systematic reviews or one-sentence summaries.
license: MIT
---

# Research Paper Analysis Writing

## Objective

Turn one paper, or a tightly related small set, into an analysis for technically informed
readers who have not read the source. Lead with what changed and why it matters, then explain
the mechanism, strength of evidence, limits, and place in the wider technology stack.

This Skill adapts the public
[`workflow_research_paper_survey_writing.md`](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/workflow_research_paper_survey_writing.md)
workflow from `grapeot/context-infrastructure`, pinned in `manifest.json`. The upstream
filename says “survey,” but its stated scope excludes broad academic surveys.

## Resolve context safely

1. Use papers, audience, language, publication format, and output location supplied for the
   current request.
2. Put private search aliases, credentials, embargoed notes, and machine paths under
   `../../.local/research-paper-analysis-writing/` relative to the real location of this
   `SKILL.md`. Read only the fields needed for the task and never copy their values into
   public files or responses.
3. Use available literature and web research tools; do not assume Tavily, Claude Code, or a
   particular provider. For substantial literature retrieval or citation verification, also
   load the registered `literature-review` Skill.
4. Do not upload unpublished papers or private notes to an external service without explicit
   authorization.

## Build the evidence base

### Extract the paper's skeleton

Read enough of the original paper to record:

- its central claim in one sentence;
- the intuitive mechanism before equations or implementation detail;
- experiments, datasets, scales, and baselines that support the claim;
- limitations stated by the authors and important untested conditions.

Treat the paper as the primary source for what the authors claim, not as independent proof
that the claim generalizes.

### Add external evidence and context

Search for peer review, replications, critiques, follow-up work, relevant baselines, competing
open-source or commercial approaches, and credible product integration. Prefer primary
sources and distinguish community attention from validation. Keep source links with each
finding.

Organize the evidence ledger into three explicit layers:

1. **Paper claim:** what the authors report and the conditions tested.
2. **External evidence:** independent verification, criticism, reviews, and surrounding facts.
3. **Analysis:** the writer's inference, confidence, and conditions that could reverse it.

Never blend these layers into an unqualified factual statement.

### Locate the work in its ecosystem

Answer five questions with concrete constraints and comparisons:

1. Which bottleneck does the work address?
2. What alternatives existed, and what did each cost in accuracy, compute, time, hardware,
   money, data, or workflow complexity?
3. Does it create a capability that was previously unavailable, or mainly reduce the cost of
   an existing capability?
4. Where does it act in the stack: model, runtime/inference, infrastructure, data pipeline,
   product experience, or organizational workflow?
5. If the result holds, which adjacent systems, products, or workflows change?

Say “not yet known” when the evidence cannot support an answer.

## Write in reader order

Use the user's requested language and format. For a technical article, prefer this sequence:

1. **Core finding:** within the first three paragraphs, state what changed, the concrete
   consequence, who is affected, and the most important uncertainty. Do not begin with a long
   literature history or method walkthrough.
2. **Prior state:** explain how the problem was handled before and the cost of those routes.
3. **Mechanism:** give an intuitive mental model first; add formal or implementation detail
   only after the reader has that anchor.
4. **Evidence and boundary:** show what was tested, what was not, author limitations, and
   external validation or criticism.
5. **Ecosystem position and judgment:** answer the five ecosystem questions, state confidence,
   and name the evidence that would change the conclusion.

Use specific numbers only with their baseline and experimental conditions. Avoid vague
phrases such as “large improvement” or “significant cost reduction” without a comparison.

## Acceptance checks

- After five paragraphs, a reader can explain what changed, why it matters, and what remains
  unverified.
- A sampled paragraph is clearly attributable to paper claim, external evidence, or analysis.
- The bottleneck, prior alternatives, stack layer, and downstream impact are all addressed.
- Method detail follows significance and context, not the paper's reviewer-oriented order.
- Claims, quotations, and current facts have verifiable source links near the relevant text.
- Community reaction is labeled as signal rather than proof.
- Private paths, credentials, unpublished material, and research notes remain outside the
  public Skill registry.
