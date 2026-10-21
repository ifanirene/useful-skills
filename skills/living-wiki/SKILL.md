---
name: living-wiki
description: Build and maintain an LLM-maintained project wiki in any repository. It gives each durable question one current answer, grounded in registered sources with hashes and reading coverage, and keeps investigator decisions separate from agent suggestions. Use to bootstrap a wiki from selected resources, adopt an existing wiki, ingest or revise a source, update answers after analysis, literature or writing work, promote pursued Ouroboros ideas, or audit wiki health.
license: NOASSERTION
---

# Living wiki

Keep a project's current understanding where people and agents can find it, trust its sources
and build on it. Automation reads it too: `ouroboros` treats each wiki folder and its registered
sources as the whole readable world of a project. The wiki is useful when a newcomer can find
the current answer to a project question in two or three steps, see what supports it, and tell
which parts the investigator decided.

## Layers

| Layer | Home | Rule |
|---|---|---|
| Raw sources | anywhere in the repo, registered in `<wiki>/source-manifest.json` | Never rewrite. Capture a changed online source as a new dated file. |
| Source notes | `<wiki>/sources/`, one stable `SRC-*` ID each | What that source says, with exact locators, evidence role and limits. |
| Current answers | topic pages under the wiki's branches | One canonical home per question. Revise in place when evidence changes. |
| Decisions and questions | `decisions.md`, `questions.md` | Investigator choices with attribution; open questions with status. |
| Operations | wiki `AGENTS.md`, `NOTES.md` runbook, append-only `log.md` | Rules, rerun guidance, meaningful changes. |
| Bibliography | Zotero when configured; regenerated views in `references/` | Formal publications live in the library, not in hand-written lists. |

## Invariants

- **Preserve originals.** Read the full relevant content of a source before registering it,
  including the figures and tables its interpretation needs, and state what was not read.
  Register a file in the manifest only after reading and integration, with its hash and coverage.
- **Give each question one home.** A new source or result revises the existing answer and its
  conclusions together. A source-note link alone is not synthesis. Create a page only for a
  distinct question that deserves maintenance, and link it from its immediate parent.
- **Keep evidence roles distinct.** Resource-reported findings, primary evidence actually
  checked, investigator-reported preliminary data, hypotheses, planned experiments and agent
  interpretations are different things. Matching metadata is not verification. Keep the model,
  stage, compartment, intervention, endpoint and denominator wherever interpretation depends on them.
- **Separate suggestions from decisions.** A suggestion becomes a decision only when the
  investigator accepts it. Silence is not acceptance. Record decisions in the
  [decision format](references/formats.md#decision-records) with a `Decided by` line.
- **Do not duplicate analysis records.** Where an analysis-documentation system already owns
  results (for example `project-memory`'s per-branch `NOTES.md` and `ANALYSIS_INDEX.md`), link to
  it for numbers and provenance. The wiki holds what the results mean across sources. Personal
  judgment belongs to the attributed decision memory, not to the wiki.
- **Match maintenance to the change.** A typo needs no log entry. A changed answer needs its
  sources, its decision or question entries and one log entry.
- **Write in English** unless the repository's instructions set another language.

## Choose the task

- **Bootstrap a wiki** in a repository without one: [bootstrap.md](references/bootstrap.md).
- **Adopt an existing wiki** without restructuring it: add `living-wiki.toml` that reproduces
  its layout ([tools.md](references/tools.md)), point the repository `AGENTS.md` to this skill,
  write an audit baseline for known errors, and log the adoption.
- **Ingest or revise a source**, or **update answers after analysis, literature or writing
  work**: [maintain.md](references/maintain.md).
- **Promote a pursued Ouroboros idea**: add it to `questions.md` as a proposed question that
  carries the idea ID and links the brief. Pursuing an idea is not a decision about the science.
- **Audit**: run the audit and review placement and claim support yourself
  ([tools.md](references/tools.md)).

Templates live in `templates/`. Copy them; never link them from a wiki.

## Completion

Before ending substantive work in a repository with a wiki:

1. The affected current answers say what changed, with provenance.
2. Decisions and questions are updated where the work produced them.
3. New sources are registered with coverage.
4. The immediate index links any new page.
5. One log entry names the change.
6. The audit shows no new errors.

Report unresolved problems as they are. Never alter originals, the bibliography, personal
memory or drafts just to pass an audit. A mechanical audit establishes neither completeness nor
scientific correctness.
