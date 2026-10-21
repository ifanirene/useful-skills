# Formats

Read when writing a page, a decision, a question or a log entry.

## Pages

- Frontmatter on every page: `type` (one of `index`, `topic`, `source`, `decision-register`,
  `questions`, `log`, `runbook`, `contract`) and `updated: YYYY-MM-DD`. Source notes also carry
  `source_id: SRC-<UPPER-SLUG>`, which never changes after first use.
- Use descriptive filenames and relative Markdown links, with spaces percent-encoded. Anchor to
  headings for exact locators. Cite original page, figure or section locators in source notes.
- Add a verified library key, DOI or PMID when one is available.

## Decision records

Append one record per decision in `decisions.md`, newest last:

```markdown
## <What was decided> — YYYY-MM-DD

- **Context:** <what prompted it>
- **Alternatives:** <the options considered>
- **Decision:** <the choice, quoting the investigator verbatim when possible>
- **Decided by:** investigator (direct, <conversation | meeting | comment>, <date>) | investigator via <person> (attributed) | agent default pending review
- **Reason and accepted cost:** <why, and what was given up>
- **Scope:** <what it governs, and what it does not>
- **Supersedes:** <link to an earlier record, or none>
- **Agent recommendations not accepted:** <keep them visible, labelled>
- **Current answer:** <link to the page that now carries the consequence>
```

A recommendation awaiting the investigator goes under a `## Pending recommendations` heading
with its status. It is not a decision.

## Questions

```markdown
## Q<n> · <the question>

- **Status:** open | answered (<link>) | dropped (<reason>)
- **Why it matters:** <the decision it blocks or informs>
- **Working interpretation (agent):** <current best reading, labelled as the agent's>
- **What would resolve it:** <evidence, analysis or choice>
- **Origin:** <source, meeting or Ouroboros idea O-YYYYMMDD-n pursued on <date>, with the brief link>
```

Close a resolved question by linking the decision or answer that resolved it. Do not delete it.

## Log

Append-only, newest last, one heading format:

```markdown
## YYYY-MM-DD · <intake | synthesis | decision | structure | adoption> · <short title>

- Changed: <pages>
- Why: <the source, result or decision>
- Unresolved: <what remains, or none>
```

## Evidence roles

Use these words in answers and notes: **resource-reported** (stated by a supplied source),
**primary checked** (verified against the primary paper or data), **investigator-reported**
(preliminary, unpublished), **hypothesis**, **planned**, **agent interpretation**.
