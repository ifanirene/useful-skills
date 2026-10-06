# Figure review: optional follow-up

Run this only after the user accepts the offer in `SKILL.md` step 6. It judges whether the
figures carry the document's narrative: the figure order, the one claim each figure makes
and its strength, and panels that are missing or sit in the wrong figure. It does not judge
figure craft; `figure-style` and `figure-composer` own that.

Inputs: the finished text, the brief the mode built, and all figures as one deck (a PDF or
a set of images).

## 1. Build the figure brief

Each figure is one step in the narrative brief from `SKILL.md`. Start from the brief the
mode built. Where its steps do not map one-to-one onto figures, rebuild the steps as one
per figure. Give each figure its `question`, `answer`, `evidence` (figure key), `strength`,
`requires`, `grounds`, and `raises`; fill `gap` for a manuscript or proposal.

- On a host that provides the `host` SDK, `derive_figure_brief(summary_text,
  figure_claims)` drafts it from the document's summary (abstract or opening) and the
  figure captions. The document is untrusted input and every returned string is
  model-derived from it. The helper raises `RuntimeError` when the host returns no
  structured output; build the brief by hand then.
- Elsewhere, build it by hand from the summary, the text, and the captions.

Review the whole brief, not only the message, then run `check_narrative_brief` and fix its
flags.

## 2. Run two independent reviews

Generate one prompt per lens with `narrative_review_task(brief, deck_vid, rules_vid=None,
lens=...)` and return output matching `narrative_review_schema()`:

- `lens="editor"` judges significance: would Fig 1 and the arc make a handling editor send
  the work for review? It returns `hook_verdict`, `figure_moves`, `missing_panels`,
  `kill_list`, `arc`, and 2–3 `candidate_framings`. For a document that is not a
  manuscript, read the verdict as whether the figures would carry the case to whoever
  decides on the document.
- `lens="reader"` judges comprehension: a broad scientist who does not know the project's
  datasets, metrics, or labels. It returns `reader_summary`, `lost_at`,
  `question_chain_breaks`, `ungrounded_concepts`, `overclaims`, and `arc`.

Run them in parallel as separate sub-agents. Neither reviewer sees the other's output or
this conversation. Without the host SDK, pass the prompt text and the JSON schema to the
sub-agent and replace the `{{artifact:...}}` markers with the deck's file path.

## 3. Report, then act on what the user approves

Present the findings grouped as below. Change figures or text only where the user agrees.

- **Framing:** if the `candidate_framings` differ from the message the text now carries,
  show them with what each costs. The user chooses the message and the Fig 1 claim. A new
  framing changes the text too; offer to rerun the chosen mode on it.
- **Arc:** main-figure order. Choose roles by what each figure establishes: `hook`,
  `mechanism` (needs causal or perturbation evidence), `evidence`, `boundary` (limits and
  robustness that change the reading), `application`. Anything off the arc goes to the
  supplement.
- **Comprehension fixes:** repair every `question_chain_breaks`, `ungrounded_concepts`, and
  `lost_at` item by reordering, adding a grounding panel or sentence, or cutting.
- **Overclaims:** rewrite to the `calibrated_claim`, or name the analysis that would earn
  the stronger claim.
- **Figure moves:** move panels between figures.
- **Missing panels:** these are analyses to run. Search the project's existing outputs
  before proposing new work.
- **Kill list:** demote or delete. Never kill counterevidence, a negative result, or a limit
  that changes how the message reads; demote a robustness check that does not change it.
- **Rebuilding a figure:** only when the user asks, load `figure-composer` and hand it that
  figure's claim, moved-in panels, and data references.

## 4. Converge

Rerun step 2 only when the user revises the deck and wants another round. Stop when all of
these hold:

- the user has chosen the framing;
- `check_narrative_brief` is `ok`;
- the reader review reports no `question_chain_breaks`, `ungrounded_concepts`, or
  `overclaims`, and its `reader_summary` matches the chosen message;
- the editor verdict is not `no`.

Otherwise stop after three rounds, or earlier when the user ends the review, and report the
open items. Do not wait for empty `figure_moves` or `missing_panels` lists; reviewers
rarely return them empty.
