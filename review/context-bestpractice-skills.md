# Local Review Packet: Context Best-Practice Skills

- Date prepared: 2026-08-23
- Branch: `codex/central-personal-skill-library`
- Upstream repository: `https://github.com/grapeot/context-infrastructure`
- Pinned source commit: `3f62b8b57f04d6a248770298b797ad38208db2d5`
- State: local checks passed; human review pending

## Sources

- `rules/skills/bestpractice_ai_programming_mindset.md`
- `rules/skills/bestpractice_skill_writing.md`

Both are instruction-only Markdown documents with no executable code or Agent-Skills
frontmatter.

## Routing review

The upstream chain is `AGENTS.md` → `rules/WORKSPACE.md` and `rules/skills/INDEX.md` → the two
documents under `rules/skills/`.

This workspace uses `CLAUDE.md` → `AGENTS.md` → `manifest.json` and `skills/INDEX.md` →
`skills/<name>/SKILL.md`, with profiles projecting canonical Skill directories into the Codex
and Claude user-level discovery roots. The documents were therefore adapted as
`ai-programming-mindset` and `skill-writing-principles` at the canonical `skills/` layer. An
unused local `rules/skills/` copy was not created.

## Adaptation boundary

### AI programming mindset

- Preserved the feedback-loop diagnosis, observable success criteria, outcome certainty,
  reasoning/execution distinction, and accountable human judgment.
- Reframed filesystem state and model intuition as conditional design choices rather than
  universal rules.
- Removed the fixed eight-subagent recommendation and made delegation conditional on current
  authorization and independent work.
- Required diagnostic detail to remain useful while secrets and private data are redacted.

### Skill writing principles

- Preserved outcome certainty, acceptance criteria, resource and boundary contracts, enabling
  guidance, high information density, evidence-based pitfalls, and progressive disclosure.
- Distinguished content design from the built-in host `skill-creator`, which remains
  responsible for packaging, frontmatter, metadata, and mechanical validation.
- Removed upstream-specific index paths and examples as requirements.

## Privacy and provenance

Private paths, fixtures, credentials, internal thresholds, examples, and schemas route to
ignored `.local/<skill-name>/` overlays or consuming-project ignored files. No private values
were added.

The upstream README declares MIT, but the repository has no standalone license file. This
limitation is recorded in the manifest and provenance documentation.

## Local verification

| Check | Result |
| --- | --- |
| Skill Creator validation | Passed for both Skills |
| Registry consistency | Passed: 14 Skills and 13 profiles agree |
| Public-content scan | Passed: 68 registry text files checked; manual review still required |
| Codex discovery | Passed: both canonical roots linked |
| Claude discovery | Passed: both canonical roots linked |
| `git diff --check` | Passed |

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge until local checks pass and both human dispositions are explicitly approved.
