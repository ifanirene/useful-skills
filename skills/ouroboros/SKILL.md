---
name: ouroboros
description: Produce a lateral-thinking research brief from an investigator's registered project wikis. It fragments recent progress and open problems, collides them with scientific lenses and inversions, verifies outside claims, filters with fresh-context critics, and records the investigator's verdicts. Use to set up the think tank, run a brief now or on a schedule, or record verdicts on ideas.
license: NOASSERTION
---

# Ouroboros

Turn what the wikis already know into ideas the investigator would not reach during an ordinary
working day. Examples: a method from one project that settles a question in another; an untried
angle on a stuck problem; a gene's known role in another organ that explains an observation here.
A brief succeeds when the investigator finds at least one idea worth a verdict. Volume does not
count.

## Boundaries

- **Read only registered wiki content.** That means each configured wiki folder plus the files
  its source manifest registers, as fetched into the run cache, along with the configured
  judgment files and this skill. Never open other project files. If something matters but is
  not registered, say so in the brief's maintenance list.
- **Never edit a wiki, a judgment file or a source.** Write only inside the journal. Ideas reach
  a wiki only after the investigator marks them `pursue`; `living-wiki` then promotes them as
  proposed questions that carry the idea ID.
- **Check outside facts separately from generating ideas.** Dreamers use recall. A fresh
  verifier labels each outside claim `verified`, `source-reported`, `speculation` or
  `contradicted`, with a PMID or DOI. The brief never states a claim more strongly than its label.
- **Do not repeat yourself.** No idea from the ledger returns without new evidence, whether it
  was marked or not.
- **Language:** briefs are written in English. Inputs may be in any language.

## Set up

Read [configuration.md](references/configuration.md). Create the journal with `init`. Fill
`config.toml` with the wikis, the judgment files, the voice exemplars and the schedule. Run one
brief by hand. Activate a host schedule only when the investigator has asked for one. Setup is
complete when a manual brief passes `finish`, and the schedule's state is reported.

## Run a brief

Resolve `scripts/ouroboros.py` from this skill's real directory. Use a Python 3.11+ interpreter.

1. **Prepare.** `python3 scripts/ouroboros.py prepare --journal <journal> --mode auto`. Use
   `manual` when asked for a brief now, and `nightly` or `deep` to force a mode.
   - `skip`: stop silently.
   - `exists`: inspect that run; do not start a second one.
   - `blocked`: notify only if `notify` is true.
   - `reserved`: read `packet.md` in the run directory.

   The packet lists the snapshots, the changes since the last brief, the lenses, the judgment
   files, the voice exemplars, the past ideas, the pursued ideas awaiting promotion, the audit
   findings and the idea IDs to use.
2. **Fragment, dream, verify, criticize, write and cold-read** as in
   [pipeline.md](references/pipeline.md). Draw dreaming moves from
   [lenses.md](references/lenses.md). Write the brief to
   [brief-format.md](references/brief-format.md).
3. **Finish.** `python3 scripts/ouroboros.py finish --journal <journal> --key <key> --status
   complete --brief <run dir>/brief.md --note "<one line>"`. The script validates the brief,
   files it under `briefs/`, extends the ledger, records the snapshot commits and commits the
   journal. On a validation error, fix the brief and finish again. Use `failed` or `blocked`
   with a reason when the run cannot produce a brief. Never retry a failed run automatically. A
   retry the investigator requests gets a new key through `--key`.
4. **Deliver.** Notify the investigator with the lead's title and the brief's path, if a
   notification tool is available. Otherwise return them. Stay silent on skips.

## Verdicts

The investigator writes after an idea's `**Verdict:**` label:

- `pursue — <why>`: take it up. It appears under maintenance until a wiki page mentions its ID.
- `drop — <why>`: not useful. The reason teaches later runs.
- Blank: not now. Nothing happens.

When the investigator gives a verdict in conversation, write their words verbatim under that
idea in the brief. Then run `python3 scripts/ouroboros.py harvest --journal <journal>`. Never
fill a verdict yourself.

## Outputs and completion

A completed run leaves `packet.md`, `fragments.md`, the dreamer files, `verification.md`,
`critic.md`, `cold-read.md` and `run.json` in its run directory, plus one validated brief in
`briefs/` that ended with `VERDICT: SHIP`. Every idea in the brief must:

- trace to a cited wiki path;
- name its cheapest discriminating check;
- label its evidence.

The ledger and `state.json` must match the brief.
