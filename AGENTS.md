# Central Personal Skill Library

This repository is the canonical shared library of reusable Agent Skills. It is a
capability repository, not a place for project memory, credentials, or private context.

## Every session

1. Read `manifest.json` for the canonical registry.
2. Read `skills/INDEX.md` for human-friendly routing.
3. Select only the smallest set of skills that matches the task.
4. Read each selected `SKILL.md` completely before acting. Resolve its relative files
   from that skill's directory.
5. Follow the current project's instructions and the user's request when they are more
   specific. This library supplies workflows; it does not override project authority.

Host-neutral Skill discovery does not guarantee automatic loading of sidecars. If a Skill
references functions from `kernel.py` and they are not already available, read or execute the
sidecar explicitly as described in `docs/PORTABILITY.md`.

Do not load every `SKILL.md` by default. Progressive loading keeps the Agent context
small and reduces accidental instruction conflicts.

## Quick routing

- Stanford SCG SSH setup and Slurm CPU/GPU jobs: `compute-scg`
- SSH connection reuse and Slurm jobs on any cluster: `remote-compute-ssh`

- Connect and visualize concepts across Markdown, documents, or code: `graphify`

- Synced Apple Voice Memos transcription and daily reports: `intake-skill`

- Scientific mechanisms and article illustrations with controlled style: `baoyu-article-illustrator`
- One scientific plot or plot QA: `skills/figure-style/SKILL.md`
- One multi-panel scientific figure: `figure-composer`, then `figure-style`
- Make research writing of any type follow one question and one answer, by polishing the
  author's draft or rewriting it: `paper-narrative` (its optional figure review routes to
  the figure skills)
- Scientific literature search or synthesis: `literature-review`
- Reader-first technical analysis of one or a few scientific papers:
  `research-paper-analysis-writing`
- Diagnose stalled or partially complete AI-assisted engineering work:
  `ai-programming-mindset`
- Design or review reusable Skill instructions: `skill-writing-principles`
- Recurring artistic covers from repository elements and a personal library: `image-dream`
- Visual explanation with a diagram, code-shape sketch, or focused HTML artifact: `show-me`
- Internal memos, external analytical articles, or article distribution posts:
  `writing-workflows`
- Structured product, service, feature, or open-problem ideation: `innovation-assistant`
- Provider-selectable local image generation, editing, or upscaling: `image-generation`
- Export local AI coding sessions to a private Markdown archive: `ai-session-export`
- Search an existing private Markdown archive of prior AI sessions:
  `ai-session-search-archive`
- Online media download, transcription, source identification, metadata, library deduplication,
  or bilingual subtitles: `online-media`
- Presentation decks, keynotes, teaching slides, speaker notes, or Reveal scaffolds:
  `presentation`

`skills/INDEX.md` remains the complete routing table.

## Sharing with projects

Projects should refer to this repository instead of copying Skill content. Use
`templates/AGENTS.skill-library.md` in project-level Agent instructions. Claude Code can
import that project's `AGENTS.md` from `CLAUDE.md` with `@AGENTS.md`.

Symlinks created for Agent-native discovery are local projections only. Generate them
with `scripts/link_skills.py`; never commit those links into this repository.

## Changing the registry

For every addition, update, rename, or removal:

1. Work on a review branch.
2. Keep the canonical implementation under `skills/<name>/` with a required `SKILL.md`.
3. Update `manifest.json`, `skills/INDEX.md`, relevant profiles, and `CHANGELOG.md`.
4. Record the canonical source and license. If provenance is unknown, mark it unresolved;
   do not invent a URL.
5. Keep reusable behavior here and private paths, aliases, data, and secrets in a local
   project overlay.
6. Run:

   ```bash
   python3 scripts/check_registry.py
   python3 scripts/check_public_content.py
   git diff --check
   ```

7. Require explicit human functional and privacy review before merge. CI is evidence,
   not approval. Do not enable auto-merge.

## Safety

- Treat imported skills as executable instructions and review scripts before use.
- Do not commit credentials, unpublished sensitive data, personal identifiers, internal
  endpoints, or machine-specific paths.
- Do not silently duplicate a Skill maintained in another repository; register its
  canonical source or add a small local adapter with attribution.
- Do not overwrite existing Agent skill directories when installing links.
