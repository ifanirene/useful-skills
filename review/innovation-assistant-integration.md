# Local Review Packet: Innovation Assistant Integration

- Date prepared: 2026-08-23
- Branch: `codex/central-personal-skill-library`
- Upstream: `https://github.com/grapeot/innovation-assistant-skill`
- Pinned commit: `e062b37e67dcd48a79202780802788a675685269`
- State: local checks passed; CI and human review pending

## Scope

- Pin the upstream repository at `projects/innovation_assistant_skill` as a Git submodule.
- Add one Agent-Skills adapter at `skills/innovation-assistant/SKILL.md`.
- Register one `innovation-assistant` entry in the manifest, human index, README, provenance
  record, changelog, and isolated discovery profile.
- Project that one root into the Codex and Claude user-level discovery directories.
- Add an ignored `.local/innovation-assistant/` overlay for private aliases, paths,
  credentials, problem inputs, and generated reports.

## Routing decision

The upstream project is a pure-Markdown package with one root router, two focused pipelines,
an axiom layer, experiment evidence, its own Agent instructions, and a standalone MIT license.
It remains the canonical implementation. The central adapter is the only `SKILL.md` exposed
to discovery and loads only the pipeline selected by the upstream router.

No `WORKSPACE.md` exists at the pinned commit. The SIT pipeline, Think Bigger pipeline,
axioms, and experiment files are not linked into Codex or Claude discovery.

## Source, privacy, and safety review

- The upstream project contains no executable scripts, package runtime, build step, or
  credential integration. Installation did not run an innovation workflow or web search.
- The adapter preserves the upstream human checkpoints, explicit out-of-scope route,
  evidence requirement, derivation chains, and ban on treating retrospective statistics as
  forward success probabilities.
- No private problem statement, product alias, organization name, customer data, machine
  path, credential, precedent-search result, or generated report was added to tracked files.
- The ignored local overlay contains placeholders only. Its values are excluded from public
  files and discovery links.

## Local verification

| Check | Result |
| --- | --- |
| Upstream executable review | Passed: pure Markdown; no runtime code |
| Skill Creator validation | Passed |
| `python3 scripts/check_registry.py` | Passed: 9 Skills, 8 profiles |
| `python3 scripts/check_public_content.py` | Passed: 48 text files; semantic review still required |
| `git diff --check` | Passed |
| Submodule pin | Passed: manifest, Git link, URL, commit, and entrypoint agree |
| Codex discovery | Passed: one `innovation-assistant` root; zero upstream projections |
| Claude discovery | Passed: one `innovation-assistant` root; zero upstream projections |
| Local overlay ignore rules | Passed for README, env, and aliases placeholders |

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge or publish until both reviews are explicitly approved and CI passes.
