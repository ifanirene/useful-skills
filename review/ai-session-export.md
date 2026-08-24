# Local Review Packet: AI Session Export

- Date prepared: 2026-08-07
- Branch: `codex/central-personal-skill-library`
- Upstream: `https://github.com/grapeot/ai_session_export`
- Pinned commit: `e52754dfe11b7da74b64ec9cf8035c82beb94e56`
- State: local checks passed; human review pending

## Scope

- Add the upstream tool as a pinned submodule at `projects/ai_session_export`.
- Add one `skills/ai-session-export/SKILL.md` adapter and one single-Skill discovery profile.
- Register the adapter in the manifest, root router, local index, README, provenance, and
  changelog.
- Keep generated transcripts and state outside the public Skill library.

## Source review

The pinned project is a Python 3.11+ local exporter. Its runtime uses only the standard
library, makes no network or shell calls, opens the OpenCode database read-only, reads the
other transcript stores as files, and writes Markdown plus incremental state only to the
configured archive root. Its live tests are opt-in and were not run.

The upstream README declares MIT, but the pinned commit contains no standalone license file.
That provenance limitation is recorded in `manifest.json`, `docs/PROVENANCE.md`, and the
changelog.

## Discovery boundary

Only the central `ai-session-export` adapter is linked into Agent-native discovery. The
upstream project's lowercase `skill.md` remains inside the submodule and is read on demand by
the adapter; it is not exposed as a second root Skill.

## Local verification

| Check | Result |
| --- | --- |
| Upstream non-live tests | Passed: 27; skipped: 3 opt-in live tests |
| Registry validation | Passed: 5 Skills and 4 profiles agree |
| Public-content scan | Passed: 32 registry text files checked; manual review still required |
| One-Skill native discovery link | Passed: one `ai-session-export` link created for Codex |
| `git diff --check` | Passed |

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge until the checks pass and both dispositions are explicitly approved.
