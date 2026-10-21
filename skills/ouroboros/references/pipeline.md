# Run pipeline

Read before producing a brief. Save every stage output in the run directory. Subagents run
in fresh contexts and receive only the inputs listed; pass file paths rather than summaries, so
each one reads the material itself. A stage ends on its completion criterion, not on effort spent.

## 1. Fragments (main agent)

Inputs: `packet.md`, the changed files it lists with their log entries, each wiki's questions
and decisions files, and the orphan sample. Read the changed pages in full. Open other pages only
to locate a fragment.

Write `fragments.md` with 8–15 numbered fragments. Each is one or two sentences in the wiki's own
terms, with an exact link (`<wiki>:<path>#<section>`) and one type:

- **open**: an unresolved question, a stuck step, or a tension between results;
- **result**: a recent finding or progress that could matter beyond its own page;
- **assumption**: something the current plan relies on without having tested it;
- **orphan**: an older note that no current answer uses.

Nightly runs draw mostly on recent changes. Deep runs draw mostly on the oldest open questions
and on the orphan sample. Do not interpret yet.

Done when there are at least three open fragments and two assumptions (or the packet shows
there are none), and every fragment links to a snapshot path.

## 2. Dream (one subagent per dreamer listed in the packet, in parallel)

Give each dreamer `fragments.md`, its lenses from the packet (the last dreamer also gets the
wildcard), the snapshot paths, the past-ideas list, the judgment file paths, and this brief:

> You are dreaming about a research program, not planning it. Use your lenses as forced moves on
> specific fragments: collide two fragments from different projects, map a fragment onto a lens,
> or invert an assumption. Prefer moves the investigator would not make during an ordinary
> working day. Skip standard next steps, generic advice and project management. Draw on your own
> knowledge of the literature freely, but write every outside fact you rely on as a separate
> checkable claim. Do not search yet.
>
> Write five candidates (the last dreamer adds one wildcard candidate). For each give: a title
> that states the idea; the fragments used; the move (lens ID or inversion); the idea in 3–5
> sentences; the outside claims, one sentence each, naming the organism, tissue or context each
> applies to; the cheapest check that could separate the idea from its main alternative using
> existing data, the literature or a small pilot; and why it is not obvious from inside the project.
>
> Then read the judgment files. Choose the two principles most relevant to your candidates. Add one
> candidate that a principle provokes — a question it raises that your first pass missed. Mark any
> candidate that conflicts with a principle; keep it and name the tension. Principles generate
> questions here; they do not filter.

Save as `dream-<n>.md`. Done when every candidate has every field, outside claims are separate
sentences, and lens IDs are recorded.

## 3. Verify (one fresh subagent)

Give it the dreamer files, the snapshot paths and the past-ideas list, with this brief:

> Check every outside claim with the literature tools available (for example PubMed, OpenAlex,
> bioRxiv, Zotero) and read the abstract or text you cite. Label each claim: **verified** — a
> located paper states it in the stated context; **source-reported** — a wiki source note or a
> review states it but you did not check the primary paper; **speculation** — no support found, or
> the claim is itself an inference; **contradicted** — evidence against it. Give authors, year,
> journal and a PMID or DOI, plus a quote or locator of at most 25 words. Where the paper's
> context (organism, tissue, stage, assay) differs from the claim, say so; that difference often
> decides whether a connection holds.
>
> Then check novelty. Search the snapshots for each candidate's core idea and compare it with the
> past ideas. Flag **already in wiki** or **previously proposed** (with its ID), and say whether
> evidence has appeared since.

Save as `verification.md`. Done when every claim has a label, every verified or source-reported
claim has an identifier, and every candidate has a novelty flag.

## 4. Critic (one fresh subagent)

Give it the dreamer files, `verification.md`, the judgment files, the past-ideas list and the
snapshot paths, with this brief:

> Remove candidates whose key premise is contradicted, that repeat a past idea without new
> evidence, that a wiki already contains, or that amount to generic advice. Score each remaining
> candidate 0–2 on four questions: Would this investigator not already have thought of it? Is the
> mechanism coherent given the verified facts? Is there a cheap check that discriminates? Would it
> change a decision or priority if true? Select a **Lead** (highest total, with at least one
> verified outside fact or a strong link between two wikis), a **Short** idea (the next best, from
> a different fragment or project), and a **Wildcard** (the best surviving far-analogy candidate;
> its plausibility bar is lower, but its facts must still carry labels). Do not force a common
> theme. List at least three discarded candidates with a one-line reason each.

It ends its file with:

```text
SELECTION
lead: <candidate>
short: <candidate or none>
wildcard: <candidate or none>
```

Save as `critic.md`. Done when every candidate has either a removal reason or four scores, and
the selection block is present.

## 5. Write (main agent)

Read the voice exemplars, then write `brief.md` following [brief-format.md](brief-format.md).
Write the Lead as an argument a scientist can follow in five minutes:

1. Start from the observation as the wiki states it, with its link.
2. Show why the current reading leaves something unexplained.
3. Bring in the connection and the evidence for it.
4. Say what it would change and which result would kill it.
5. End with the cheapest check.

Keep every fact at its label's strength and mark speculation within the sentence. Cite only
verified or source-reported claims, numbered in order of first use.

## 6. Cold read (one fresh subagent)

Give it only the brief, with permission to open the snapshot paths and references it cites:

> Read as the investigator would at breakfast. Check that: every outside fact has a citation or
> an explicit label; no sentence is stronger than its evidence; every idea traces to a cited
> wiki path; the Lead is an argument rather than a list, and a scientist outside the project can
> follow it; no idea is a standard next step or generic advice; idea IDs and empty verdict lines
> are intact. End with exactly one line: `VERDICT: SHIP` or `VERDICT: BLOCK — <reasons>`.

Save as `cold-read.md`. On BLOCK, revise once and run a new cold read. If the second read also
blocks, finish the run as `failed` with its reasons and keep the draft in the run directory.
