# Local Review Packet: Show Me

- Date prepared: 2026-09-03
- Branch: `codex/central-personal-skill-library`
- Upstream repository: `https://github.com/humanlayer/skills`
- Source document: `plugins/show-me/skills/show-me/SKILL.md`
- Pinned source commit: `3c2629142c5d437428269b1b722b08c0b87f574d`
- License: MIT; upstream license copied to `skills/show-me/LICENSE`
- State: local checks passed; human review pending

## Source and adaptation review

The upstream artifact is one instruction-only Agent Skill with no scripts, assets, private
configuration, or external runtime dependency. Its examples cover pseudocode, call trees,
component trees, file trees, Mermaid, structural diffs, code blocks, and focused HTML.

The local adaptation preserves those visual forms and examples. It adds the license field
required by this registry, explicit use boundaries and acceptance checks, and replaces the
macOS- and Claude-specific `Bash(open ...)` instruction with a host-neutral preview or
file-link rule.

## Privacy and safety review

The imported content contains synthetic example paths and identifiers only. It includes no
credentials, personal paths, private endpoints, user data, executable scripts, or network
actions. The HTML route remains governed by the consuming project's authority and is only used
when a simpler visual is insufficient.

## Local verification

| Check | Result |
| --- | --- |
| Source commit and upstream file | Verified |
| Upstream license | Verified: MIT |
| Registry consistency | Passed: 15 Skills and 14 profiles agree |
| Public-content scan | Passed: 72 text files checked; manual human review remains required |
| Isolated discovery profile | Passed: Codex and Claude links resolve to the canonical Skill |
| `git diff --check` | Passed |

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge until local checks pass and both human dispositions are explicitly approved.
