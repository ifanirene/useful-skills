---
name: paper-narrative
description: "Make research writing easy to follow: one question, a one-sentence answer, and steps that each answer the reader's next question, use only explained concepts, and claim no more than the evidence. Any document type. `polish` edits structure and clarity in the author's voice; `rewrite` reorganizes for delivery. Not for style-only line editing or literature synthesis."
license: Apache-2.0
---

# paper-narrative

## Objective

Make research writing easy to follow and hard to misread, whatever the document: a result
write-up, a report, a progress report, a manuscript, or a grant section. The goal is the
same for every type. After the opening, the reader knows the question and the answer. Each
later step answers the question the previous step raised, uses no concept the text has not
yet explained, and claims no more than its evidence supports. The document type sets only
the required structure and length.

In scope: structure and clarity, including order, headings, paragraphing, the opening,
first-use definitions, links between steps, and claim strength. Out of scope: line editing
purely for style, and literature synthesis.

## Choose the mode

| Mode | Use when | May change | Keeps | Delivers |
|---|---|---|---|---|
| `polish` | the author has a draft and wants it clearer in their own voice | section and paragraph order, headings, paragraph splits and merges, the opening (main point first), bridge sentences between steps, first-use definitions, verbs stronger than the evidence, cuts of material that supports no step | the author's sentences, wording, terms, and tone wherever clarity allows | the edited text in the input's format, plus a change list |
| `rewrite` | delivering the result matters more than the author's voice, or the input is raw material (results, tables, figures, an outline) | framing, order, and prose | every result, number, evidence source, and limit | new text in the input's format, plus the narrative brief |

Both modes apply the same core: the narrative brief, its checks, the hard constraints, and
the cold read. `polish` applies them with a light hand.

When the user names no mode, use `polish` for an author's draft and `rewrite` for raw
material. Ask only when the request fits both and the choice would change the result, for
example a full draft with "make this better".

Default reader: the reader the document names or implies. Otherwise, an informed reader
outside this work, who knows the field and the goal but not this work's methods, metrics,
labels, or file names. Ask about the reader only if a different reader would change the
brief.

## 1. Build the narrative brief

Write the brief as a short table or JSON (`narrative_brief_schema()` in
[kernel.py](kernel.py)):

- `reader` and `prerequisites`: who reads, and the concepts they already bring.
- `question`: the central question in the reader's terms, including what is at stake in
  the answer.
- `gap` (optional; useful for a manuscript or proposal): "It remains unclear whether, why,
  or under what conditions ___." Not "no one has used this method".
- `message` and `message_strength`: the most specific one-sentence answer the evidence
  supports.
- `steps`, in reading order, each with: `question` the reader holds at that point;
  `answer`; `evidence` (file path, table, figure, or the passage of the input that reports
  it); `strength`; `requires` (concepts it leans on); `grounds` (concepts it explains);
  `raises` (the question it leaves for the next step). Mark context-only steps
  `load_bearing: false`.
- `limits`: qualifications that change how the message should be read.
- `next`: the next decision or analysis.

Strength labels: `shows` (direct test with a control or perturbation), `suggests`,
`consistent_with`, `unresolved`. Association, prediction, and sensitivity are not `shows`
for a causal or mechanistic claim.

Also list a kill list: material that supports no step, such as repeated summaries,
superseded results or commands, process chronology that does not change the reading,
cosmetic iterations, and detail no step needs.

**In `polish`**, derive the brief from the draft as written: its question, its message, and
its steps in their current order. A compact brief is enough; fill `requires` and `grounds`
only for terms the reader might not know. Keep the brief internal unless it exposes a
decision for the author, such as no clear message, two competing messages, or a claim the
evidence does not support. Report those with the change list.

**In `rewrite`**, derive the brief from the work itself (drafts, analysis logs, saved
tables, figures), not from memory of the conversation, and choose the step order that best
answers the reader's questions. When more than one message is defensible, draft 2–3
candidate question–message pairs that imply different stories, say what each costs, and
let the user choose.

## 2. Check the brief before editing or writing

Run `check_narrative_brief(brief)` from [kernel.py](kernel.py); it is pure Python. Without
Python, apply the same checks by hand. Fix every flag or state why it stands:

- `ungrounded`: a concept used before it is explained → explain it in an earlier step,
  add it to `prerequisites`, or cut it.
- `unlinked_steps`: a step that does not say what question it leaves → add `raises`, or
  merge or cut the next step.
- `no_evidence`: a step with no named file, table, figure, or input passage.
- `overclaims`: the message is stronger than a load-bearing step.

Then judge what the checker cannot: does each step's `question` follow from the previous
`raises`, and does each `strength` label fit its evidence?

## 3. Edit or write

### Polish

Make the smallest edit that fixes each problem the brief exposed:

- Put the question and the answer in the opening. Lead each section and paragraph with its
  point.
- Reorder sections or paragraphs so each step answers the question the previous one
  raised. Where the link is missing, add one bridge sentence.
- Define a term at its first use, or move the first use after the definition.
- Replace a verb that is stronger than its step's `strength`.
- Add, rename, split, or merge headings and paragraphs when that makes the structure
  visible.
- Cut kill-list items.

Leave a clear sentence as it is. Do not change wording, terminology, tone, tense, person,
citation style, or formatting conventions for taste.

Record every change in a change list placed after the text:

| # | Where | Change | Why |
|---|---|---|---|
| 1 | Results, paragraph 1 | moved the answer to the first sentence | main point first |

Group repeated small edits into one row. Under "Questions for the author", list decisions
you cannot make, such as a claim that needs evidence you cannot see. For a word-processor
file, also apply the edits as tracked changes when the host's tools can write them.

### Rewrite

Use this shape, and adapt it to the document's required structure:

```markdown
# <the message, stated as a finding>

**Question.** <one or two sentences, in the reader's terms>
**Answer.** <the message with its key number, at its strength>

## <step answer, stated as a finding>
<Why this question follows → only the method detail needed to judge the result →
result with number and source → what it means: the technical reading, then the
reading for the domain question.>

## Limits and open questions
## Next
## Sources
```

When the document has a required structure, such as IMRaD sections, a funder's headings, or
a template, keep that structure and apply the shape inside each section. Match the length
the user or venue sets; for a quick write-up, aim for 300–800 words with at most one figure
or table per step. Lead each section with its point. Explain a term where it is first
needed. Describe a pattern in ordinary words instead of coining a label. Translate internal
IDs, column names, and script names into what they mean, or move them to `Sources`.

For the end-of-analysis report of a computational analysis that needs scripted numeric
guards, use `analysis-report-writing` when it is available and build its section order
from this brief.

## 4. Cold read

Give the edited or rewritten text, not the brief, to an isolated reviewer that has not
seen the conversation: "In one sentence, what question does this answer, and what is the
answer? Where did you first get lost? Which term did you not understand?" Revise if its
answer differs from the brief's `message`. Run it by default in `rewrite`, and in `polish`
when the edits changed the opening or the order. Skip it when the user asks for speed. If
no isolated reviewer is available, say the cold read was not done; do not certify the text
yourself.

## 5. Deliver in the input's format

Return the text in the format it arrived in: Markdown as Markdown, a word-processor file as
the same file type with the same heading levels, lists, and tables, LaTeX as LaTeX, and
text pasted in chat as a reply in chat.

When the user asks for interactive HTML, also produce one self-contained `.html` file:

- all CSS and JavaScript inline, and images embedded as data URIs; no external fonts,
  scripts, stylesheets, or network requests, so it opens offline;
- the same text as the plain deliverable, without further rewording;
- a table of contents linked to section anchors, and collapsible sections
  (`<details>`/`<summary>` work without JavaScript);
- in `polish`, the change list as its own section.

## 6. Offer a figure review

After either mode finishes, if the input included figures or a figure deck, ask the user
whether they want a figure review. It judges whether the figure order follows the
narrative, whether each figure makes one claim at the right strength, and which panels are
missing or sit in the wrong figure. Do not run it without a yes; a request for it in the
user's original message counts as a yes. On a yes, read
[references/figure-review.md](references/figure-review.md). Hand a figure to
`figure-composer` only when the user asks for that figure to be rebuilt.

## Hard constraints

- Never invent or alter a result, number, citation, analysis, or decision.
- In `rewrite`, every number names its source: a saved file, table, figure, or the input
  passage that reports it. In `polish`, leave numbers unchanged and flag any whose source
  seems wrong.
- Never strengthen a claim to improve the story. Never cut counterevidence, a negative
  result, or a limit that changes how the message reads; place it where it limits the
  claim.
- Fill an evidence gap with a named next step, not with language.
- When framings compete, the user chooses.
- In `polish`, make no silent edits: every change appears in the change list.

## Acceptance checks

- The opening states the question and the answer. For an edit of one section, the
  section's opening does.
- `check_narrative_brief` returns `ok`, or each remaining flag is explained.
- Every claim verb matches its step's `strength`.
- `rewrite`: every number names its source.
- `polish`: every change appears in the change list; unlisted passages keep the author's
  wording; no number changed.
- The output uses the input's format. Requested HTML is one file that opens without network
  access and contains all the text.
- The cold read's one-sentence summary matches the message, or the output says the cold
  read was not done.
- If the input included figures, the user was asked about a figure review, and the review
  ran only on a yes. If it ran, it stopped under the rule in
  [references/figure-review.md](references/figure-review.md).
