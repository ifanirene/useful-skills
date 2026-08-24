# Local Review Packet: Online Media Integration

- Date prepared: 2026-08-08
- Branch: `codex/central-personal-skill-library`
- Upstream: `https://github.com/grapeot/online-media-skill`
- Pinned commit: `794ff6c5545da5cbdfcc0b0ff785379fb983380e`
- State: local checks passed; CI and human review pending

## Scope

- Pin the upstream repository at `projects/online_media_skill` as a Git submodule.
- Add one valid Agent-Skills adapter at `skills/online-media/SKILL.md`.
- Register one `online-media` entry in the manifest, human index, README, provenance record,
  changelog, and isolated discovery profile.
- Project that one root into the Codex and Claude user-level discovery directories.
- Add an ignored `.local/online-media/` overlay for private aliases, paths, credentials, and
  runtime artifacts.

## Routing decision

The upstream project is a substantial CLI and workflow repository with its own release cycle,
tests, license, root router, and focused Markdown workflows. It remains the canonical source.
The central adapter is the only `SKILL.md` exposed to discovery. It requires an Agent to read
the upstream `AGENTS.md`, any future `WORKSPACE.md`, and `skills/online_media.md`, then load
only the focused workflow matching the task.

No `WORKSPACE.md` exists at the pinned upstream commit. No focused upstream workflow is linked
into Codex or Claude discovery.

## Privacy and safety boundary

- No live downloads, ASR, search, media-library reads, metadata mutation, deduplication, file
  moves, or subtitle processing were run.
- No private aliases, machine paths, media files, transcripts, search payloads, or credentials
  were added to tracked files.
- The local overlay contains placeholders only and is ignored by Git and public-content scans.
- The adapter forbids bypassing access controls and requires reviewed plans plus explicit
  approval before mutation-producing media workflows.

## Local verification

| Check | Result |
| --- | --- |
| Upstream default offline suite | Passed: 55 tests |
| Upstream documented privacy scan | Passed: zero matches |
| `python3 scripts/check_registry.py` | Passed: 6 Skills, 5 profiles |
| `python3 scripts/check_public_content.py` | Passed: 35 text files; semantic review still required |
| Registry script compilation | Passed |
| `git diff --check` | Passed |
| Submodule pin | Passed: manifest, Git link, URL, and entrypoint agree |
| Codex discovery | Passed: one `online-media` root; zero focused projections |
| Claude discovery | Passed: one `online-media` root; zero focused projections |
| Local overlay ignore rules | Passed for README, env, and aliases files |

## Environment observation

An already-active Miniforge environment initially captured `uv pip install`, leaving the new
project `.venv` without `pytest`. Reinstalling with an explicit
`uv pip install --python .venv/bin/python -e '.[dev]'` targeted the correct interpreter; the
offline suite then passed. This was an environment-selection issue, not an upstream test
failure.

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge or publish until both reviews are explicitly approved and CI passes.
