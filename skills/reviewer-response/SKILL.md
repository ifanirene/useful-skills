---
name: reviewer-response
description: Revise scientific responses to reviewers by connecting each concern to completed corrective work, verified evidence, and a defensible conclusion. Use for substantive revision letters and their figure legends; not for generic manuscript copyediting.
license: NOASSERTION
---

# Reviewer response

Help the reviewer decide whether the revision addresses the concern. Write a
positive, direct account of what the authors did and what the evidence supports.
Confidence must come from the work, not from stronger adjectives.

## Establish the answer before polishing it

Open the investigator-specified file before choosing the baseline. When learning
from a coauthor's edits, read tracked insertions, deletions and anchored comments
in that file. A later derivative or plain-text view can omit the example. Keep
authored changes, comments and investigator replies distinct. Use the supplied
template's reviewer numbering and local question–answer structure.

Read the exact reviewer comment, matching response, relevant figures and latest
analysis records. Preserve accepted choices and the purpose of author-added
passages. Treat queries and placeholders as items to verify, not finished claims.
Separate the underlying concern from a suggested remedy: an alternative can
answer the concern if its suitability is explained.

For each substantive concern, make a compact internal map:

| Concern | Completed action | Verified result and figure | Supported conclusion |
|---|---|---|---|
| What could undermine the result? | What directly tests or corrects it? | What changed or persisted? | What can the reviewer now accept? |

Before declaring evidence missing, inspect the relevant saved results and code.
Useful evidence is often already present but absent from the draft. Add it when
it answers the concern. Perform feasible, authorized checks when needed. If the
evidence still falls short, identify the specific unresolved question and the
next test; never write a proposed analysis or unverified manuscript edit as completed work.

Ask only core questions that materially change the answer, such as which claim
the investigator intends to defend. Resolve file identities and methods from
the available records rather than asking the investigator to rediscover them.

## Select analyses for the formal reply

When moving from a report to a reply, recommend the key analyses and explain
what each contributes. Discuss choices that change the scientific emphasis or
claim with the investigator; routine wording cuts need no separate approval.
Keep evidence that answers a distinct concern or changes the conclusion. Leave
redundant checks, repeated methods and secondary numerical inventories in the
report, Methods or legends. Select less content while keeping the answer explicit.

## Build the argument around the revision

Answer factual and definitional questions where they are asked. Include a short
reason when it explains an important choice. Answer every sub-question; use
cross-references for supporting detail, not to send the reviewer searching for
the answer. Match length to the question rather than imposing a sentence count.

For substantive concerns, lead with the direct answer and main corrective action.
State what was retained, what changed, why, and whether the work is complete.
Name both sides of a comparison before using labels such as “revised fit”. Connect:

**Concern → completed action → result → scientific meaning.**

Use this as a reasoning sequence, not mandatory headings. Each paragraph
should answer the next question the reviewer would reasonably ask. For example:
Does the revised method address the input problem? Does the result persist under
another formulation? Does it reproduce experimentally? Which biological claim
therefore remains supported?

When the method changes, explain whether the manuscript's key findings survive.
Use verified overlap and named examples when useful, and state material changes
or exceptions. Preserve this conclusion when cutting a long methods paragraph
or statistical inventory; agreement metrics alone do not supply its meaning.

When a limitation changes the inference, state it once with the relevant result
and supported conclusion. Do not add generic sentences about what each check
cannot prove. Keep evidence distinctions in the reasoning without turning them
into repeated disclaimers in the reply.

Compare the full tested set when the claim concerns the screen as a whole. Then
use selected examples to explain biological meaning. Label selected subsets and
their selection rule. Keep effect magnitude, statistical evidence, calibration,
and reproducibility distinct; agreement between methods using the same data is
not independent experimental validation.

## Keep the detail needed to judge the answer

Keep the minimum method detail needed to interpret the answer: the endpoint,
comparison group, changed adjustment, unit of replication, selection rule and
correction family when they matter. Move the full procedure to Methods or a
legend rather than repeating it in the reply.
Name an analysis clearly enough that the investigator can identify its source:
“linear-regression coefficients from the CRT analysis” is more useful than
“a companion model.” Do not trade method identity for brevity. Explain an
essential transformation by naming the operation and reference. If that detail
is only a technical detour, move it to the legend or Methods instead of leaving
an unexplained phrase in the reply.

Cut internal paths, software chronology, superseded attempts, repetitive
qualifications, and secondary numbers from the response. Keep their provenance
in a separate source record. State what the result means, not just its metric.

## Make figures carry the evidence

Map every included figure and panel to a claim in the response. Cite it where
that claim is made. When a figure directly answers a requested check, explain
what it shows and what follows; a bare citation can be insufficient. If an
important new claim has no visible support, add the relevant panel when
authorized or identify the missing panel specifically.

Legends should explain the observations, model or comparison, colors, selection,
statistical definitions, and any transformation or display restriction needed
to interpret the plot. Do not repeat counts and statistics already legible in
the panel unless needed to remove ambiguity. Distinguish an effect comparison
from a significance comparison. Check plot, prose, and legend against the same
saved data.

## Optional Argon 4 rewrite, polish, or consult

Argon 4 is optional. Use `polish` for wording, `rewrite` for argument structure,
or `consult` for requested advice. Prepare a bounded packet of the verified
source draft, relevant evidence, figures and claim limits. For advice based on
coauthor edits, include their actual changes and comments. Request the actual
edit or advice needed.

Use the configured Vertex AI route with `gemini-4-argon` and verify returned
identity; do not silently substitute models. Reuse authorization within its
scope. Check output against sources and keep a brief packet/model/result receipt.
Treat truncation as partial. If unavailable, continue locally and state that the
pass was not performed. The primary agent owns final accuracy.

## Deliver and check

Return the requested format. For this investigator, default to a clean Word copy
with black editable text; retain meaningful plot colors. Create tracked changes
only when explicitly requested. Preserve the live input and unrelated sections.
Provide a short change note and inspect the rendered document and figures.

Check the response directly against the concern–evidence map. Do not add a cold
read unless requested. If the optional Argon step was used, briefly identify its
editing contribution and the source checks performed; do not describe it as
independent scientific validation.

The response is ready when a reviewer can identify what was done, see the
evidence, understand its biological meaning, and judge the remaining claim
without reconstructing the analysis history.
