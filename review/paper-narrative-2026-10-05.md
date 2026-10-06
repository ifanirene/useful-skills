# paper-narrative: reader-first update — review packet

## Decision record

### Revision 2 (supersedes the mode split in revision 1)

- **Context:** revision 1 split the skill into `report`, `notes`, and `paper` modes by
  document type, and coupled the `notes` mode to an external note-keeping skill.
- **Investigator's choice (owner, 2026-10-05, chat, relayed to the implementing agent):**
  - exactly two modes for any kind of writing, because the communication goal is the same
    for every document type: `polish` (focused structure and clarity edits that keep the
    author's style and voice, with visible edits) and `rewrite` (full narrative brief;
    reorganize and rewrite for delivery, with voice secondary);
  - remove the `notes` mode and every coupling to the owner's note-keeping workflow; the
    owner's own use is one example of how the skill is used, not skill content; add no
    other user-specific workflow references;
  - figure review becomes a follow-up offer after either mode when the input has figures;
    never run it automatically; hand figures to `figure-composer` only on request;
  - output format follows the input; self-contained interactive HTML on request.
- **Agent judgment calls (not separately endorsed):** default to `polish` for an author's
  draft and `rewrite` for raw material when no mode is named; an explicit request for a
  figure review in the original message counts as accepting the offer; the reference file
  is renamed `references/figure-review.md` and the helpers `derive_figure_brief` /
  `figure_brief_schema` (no callers outside the skill); `gap` is no longer required in the
  figure brief; the cold read runs by default in `rewrite` and in `polish` only when the
  opening or order changed.
- **Supersedes:** revision 1's `report`, `notes`, and `paper` modes, the `NOTES.md`
  handoff, and the automatic figure-deck review.

### Revision 1

- **Context:** the imported skill reviewed only a paper's figure deck, through one
  handling-editor persona, from a pitch-centred brief ("grandest supportable claim").
- **Investigator's choice (owner, 2026-10-05, chat):** improve `paper-narrative`; its main
  uses will be (1) quick, easy-to-follow reports with a clear message for the owner and
  collaborators and (2) documenting project analysis in `NOTES.md`.
- **Agent recommendation, accepted by implementation (not separately endorsed):** keep the
  name `paper-narrative`, because `figure-composer`, `figure-style`, and `project-memory`
  route to it by name; add `report` and `notes` modes around one shared narrative brief;
  keep paper mode in a reference file.
- **Alternatives considered:** a new separate skill (rejected: would compete with this one
  and with `analysis-report-writing` for the same prompts); renaming (deferred: breaks
  three references, one in another repository).
- **Accepted cost:** the name now understates the scope; the frontmatter description
  carries discovery.
- **Supersedes:** the pitch/vision brief, the single editor review, `boldest_defensible_fig1`,
  and the "empty lists" convergence rule.

## What changed

- Two modes for any research writing: `polish` (edits to order, headings, paragraphing,
  the opening, bridges, first-use definitions, claim verbs, and cuts, in the author's
  voice, with a change list) and `rewrite` (full brief, new order and prose).
- One narrative brief for both: reader and prerequisites, central question, optional gap
  sentence, one-sentence message with strength, ordered steps carrying `question`,
  `answer`, `evidence`, `strength`, `requires`, `grounds`, `raises`, and a kill list.
- `check_narrative_brief` (pure Python, no host SDK): missing fields, unlinked steps,
  concepts used before grounding, steps without evidence, and a message stated more
  strongly than a load-bearing step.
- Cold-read acceptance check; hard constraints against inventing results, inflating
  claims, cutting counterevidence, or silent edits in `polish`.
- Output in the input's format; on request, one self-contained HTML file with a table of
  contents and collapsible sections.
- Figure review as an optional follow-up: derived brief asks for the most specific
  supported answer; two independent review lenses (editor, broad reader); candidate
  framings chosen by the user; `boundary` arc role; changes only where the user agrees;
  convergence capped at three rounds; `rules_vid` optional.

## Sources of ideas (paraphrased, not copied)

- Concept grounding (`requires` / `grounds`, prerequisites): `mattpocock/skills`
  `writing-beats` and `writing-shape` (MIT).
- Broad-reader model, observation-before-interpretation, claim calibration, no casual
  coinage: `Boom5426/Nature-Paper-Skills` `manuscript-optimizer` and
  `write-scientific-manuscript` (MIT).
- Question chain and gap sentence: `Yuan1z0825/nature-skills` shared Introduction and
  Results guidance (Apache-2.0).

## Validation

- Synthetic smoke test of `check_narrative_brief`: a clean brief passes; a brief with an
  ungrounded concept, an unlinked step, a missing evidence source, and a message stronger
  than a load-bearing step reports each issue; a context-only step is exempt from the
  overclaim check; concept matching ignores case and spacing. Schemas serialize to JSON;
  `narrative_review_task` builds both lenses and omits design rules when `rules_vid` is
  absent.
- Not yet done: an end-to-end `polish` or `rewrite` run on a real document, or a figure
  review on a real deck; host `llm` paths (`derive_figure_brief`) were not executed. Owner
  functional review is required before merge.
