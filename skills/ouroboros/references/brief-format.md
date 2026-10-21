# Brief format

Read when writing or reviewing a brief. `ouroboros.py finish` rejects a brief that breaks the
structure below. Use the idea IDs from the packet in slot order.

```markdown
# Ouroboros — <date> (<mode>): <the lead idea in a few words>

Read from <wiki> at <short sha>, <wiki> at <short sha> · <n> changed files since the last brief ·
Lenses: <ID name>, <ID name>, wildcard <ID name>.
<One line naming any unpushed wiki changes the run could not see; omit when there are none.>

## Lead · [O-YYYYMMDD-1] <title that states the idea>

<About 600–900 words of argued prose. No bullet lists.>

**Trigger:** [<page>](<wiki>:<path>#<section>) · [<page>](...)
**Cheapest check:** <one or two sentences: data, literature or pilot, and what result would count against>
**Evidence:** verified [1][2] · source-reported [3] · speculation: <which step>
**Verdict:**

## Short · [O-YYYYMMDD-2] <title that states the idea>

<About 150 words.>

**Trigger:** ...
**Cheapest check:** ...
**Evidence:** ...
**Verdict:**

## Wildcard · [O-YYYYMMDD-3] <title that states the idea>

<About 150 words. Name the far analogy and the structural feature it shares.>

**Trigger:** ...
**Cheapest check:** ...
**Evidence:** ...
**Verdict:**

## Maintenance

- <wiki>: <audit finding or unintegrated material, and what to do>
- Promote <ID> into <wiki> (pursued on <date>).

## Discarded

- <candidate in one line> — <reason>

## References

1. <Authors> (<year>). <Title>. <Journal>. PMID <n> / DOI <doi>.
```

Rules:

- A slot with no surviving idea is written `## Short · none survived` or
  `## Wildcard · none survived`, with no fields.
- Leave every `**Verdict:**` empty. Only the investigator fills it: `pursue — <why>` or
  `drop — <why>`. A blank verdict means not now.
- Links to wiki pages use the `<wiki>:<path>` form. They point into the investigator's
  repositories, not into the run cache.
- Evidence labels follow [pipeline.md](pipeline.md#3-verify-one-fresh-subagent). Do not cite a claim labelled speculation.
- Write in English, in the investigator's register: name the concrete observation before its
  label, prefer one claim per sentence, and never borrow a sentence from a source or exemplar.
