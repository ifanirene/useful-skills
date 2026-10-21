# Configuration and scheduling

Read when setting up a journal, adding a wiki, or changing the schedule.

## Journal

One private journal serves all of the investigator's wikis. Create it with
`python3 scripts/ouroboros.py init --journal <dir>`. The command makes a git repository, because
the verdict history is part of the record.

```text
<journal>/
  config.toml      wikis, judgment files, voice exemplars, schedule (template: templates/config.toml)
  briefs/          delivered briefs, named <date>-<mode>.md; the investigator writes verdicts here
  verdicts.md      investigator verdicts harvested from briefs, one attributed entry each
  ledger.jsonl     every idea proposed, with its slot, brief, status and verdict
  state.json       last snapshot commit per wiki, last deep run, recent lens use
  runs/<key>/      packet, stage outputs, brief draft and run.json for each run
  cache/           registered-only wiki snapshots (git-ignored)
```

The journal never holds wiki content beyond the cache. Do not commit it into a skill library.
Keep it private: briefs quote unpublished work.

## Wikis

Each `[[wiki]]` names a GitHub repository and its wiki folder. A run sees the pushed `main`
(or configured branch), not the local working tree. The snapshot contains only the wiki
folder and the files its source manifest registers. A file that is not registered is invisible
to the run, so register a source before expecting it to matter. Add `local` to report unpushed
wiki changes and to run the `living-wiki` audit on the local checkout.

Private repositories authenticate through `gh` when it is installed. A wiki that cannot be
fetched, or whose wiki folder is not on the branch, is reported as blocked; the run continues
with the others.

## Judgment and voice

`judgment.files` lists distilled judgment files, for example an attributed decision memory's
principles and reflections. They are read-only inputs. Ouroboros never edits them.

`voice.exemplars` lists the investigator's own writing as `<wiki>:<registered path>`, for
example a set of aims or a research statement. Exemplars calibrate register; never copy their
sentences.

If an attributed decision memory collects decision evidence, register the journal's
`verdicts.md` with it as a decision source, with the investigator's authorization. Do not
register briefs: their idea text is agent proposal, and only the verdict lines are decisions.

## Schedule

`prepare --mode auto` decides each occurrence:

- **deep** on `deep_weekday`, at most once in six days;
- **nightly** when any registered wiki content changed since the last brief;
- **skip** otherwise. A skip writes nothing except newly harvested verdicts.

A host scheduler runs one daily task. A local scheduler that sees the journal and the judgment
files is preferable while those files live only on the investigator's machine. A self-contained
task prompt:

```text
Run the Ouroboros think tank for the journal at <journal>. Read the ouroboros skill's SKILL.md
first and follow it exactly with mode auto. If prepare reports skip, stop without output.
If a run is blocked, notify only when the blocker is new.
```

A cloud scheduler can run the same task once the journal and the judgment files are reachable
from it, for example in a private repository. The wiki side already reads through GitHub.
Before activating a schedule, run one brief by hand and confirm that it validates. Report
whether the schedule is active and when it runs next.
