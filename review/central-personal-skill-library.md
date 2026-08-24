# Local Review Packet: Central Personal Skill Library

- Date prepared: 2026-08-07
- Branch: `codex/central-personal-skill-library`
- Reference: `https://github.com/grapeot/context-infrastructure`
- State: local checks passed; CI and human review pending

## Scope

- Move the four existing Skill directories under `skills/`.
- Add a root Agent router, canonical registry, task profiles, and project reference template.
- Add safe local link generation for Agent-native discovery.
- Add registry consistency, public-content validation, and CI.

## Design boundary

The reference repository's routing organization is reused. Its personal memory, identity,
scheduled observation, and workspace-context layers are intentionally excluded. This public
repository accepts reusable workflows and public examples only; private configuration stays
in consuming projects or ignored local overlays.

## Migration impact

Existing paths such as `figure-style/SKILL.md` move to `skills/figure-style/SKILL.md`.
Consumers using copied folders are unaffected until their next install. Consumers with links
to the old root paths must relink using `scripts/link_skills.py`.

## Known open item

Precise upstream URLs for the four pre-existing Anthropic-imported Skills were not recorded in
the old manifest. They remain explicitly unresolved in `manifest.json` and
`docs/PROVENANCE.md`.

## Local verification

| Check | Result |
| --- | --- |
| `python3 scripts/check_registry.py` | Passed: 4 Skills and 3 profiles agree |
| `python3 scripts/check_public_content.py` | Passed: 28 text files scanned; manual semantic review still required |
| Link preview and apply against a temporary target | Passed: 3 expected Skill links resolved |
| Native-target preview | Safe refusal: existing Claude Code directories were not overwritten |
| `git diff --check` | Passed |

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge until the checks pass and both dispositions are explicitly approved.
