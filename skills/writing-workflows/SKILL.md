---
name: writing-workflows
description: Draft or revise internal memos, decision briefs, external analytical articles, or distribution posts using audience-specific writing workflows. Use scientific writing Skills instead for manuscripts, paper analysis, literature synthesis, or grant prose.
license: MIT
---

# Writing Workflows

## Objective

Use the pinned standalone project at `../../projects/writing_skill` for audience-aware internal
and external writing. This adapter is the only root Skill exposed to Agent discovery; do not
separately link the upstream Chinese router, focused workflows, English mirrors, references,
or lint CLI documentation.

## Required context

1. Resolve this `SKILL.md` to its real location before following relative paths.
2. Locate `../../projects/writing_skill` from the real Skill directory.
3. Read the upstream `AGENTS.md`, any `WORKSPACE.md` it may add later, and the canonical
   `skills/writing_workflows.md` completely before drafting or changing the package.
4. Select only the focused workflow and references required for the task.
5. Run CLI commands from the upstream project root using its `.venv`.
6. If the checkout or environment is absent, initialize and install from the central library
   root:

   ```bash
   git submodule update --init projects/writing_skill
   uv venv projects/writing_skill/.venv
   uv pip install --python projects/writing_skill/.venv/bin/python -e 'projects/writing_skill[dev]'
   ```

## Audience and artifact routing

- Readers who share project context: internal workflow.
- Readers without shared context: external workflow.
- A distribution post derived from a finished external article: Twitter-post sub-workflow.
- Ambiguous audience: ask who the reader is and whether they already know the project.

Use the scientific writing Skills for manuscripts, paper-centered technical analysis,
literature reviews, methods sections, or grant prose. This Skill turns already verified
material into an audience-appropriate artifact; it does not replace evidence gathering.

## Language routing

Chinese under `skills/` is upstream-canonical. For English output, read the matching focused
file under `skills_en/`; there is no separate English root router. If an English mirror and
its Chinese canonical file disagree, follow the Chinese rule while expressing the result in
English and record the mismatch for upstream maintenance.

For this user's work, default to English unless the request specifies another language.

## Portable execution boundary

- The current package CLI is:

  ```bash
  .venv/bin/python -m writing_skill.external_prose_lint_cli path/to/draft.md
  ```

  Do not use the stale `rules.skills.external_prose_lint_cli` path that remains in one English
  mirror.
- The lint CLI is Chinese-primary. Treat its Chinese lexicon and character-count rules as
  completion gates only for Chinese prose. For English prose, use only relevant shared
  mechanical signals and do not report a Chinese-lint pass as proof of English quality.
- External-writing cold reads and voice comparisons require an independent context that has
  not seen the writing contract. Use an available isolated reviewer only when the workflow
  can preserve that boundary. If it cannot, state that the gate is unavailable and do not
  claim the fully gated workflow completed.
- Do not assume the upstream-specific `agy` command exists. Use an equivalent available
  isolated-review mechanism or report the missing capability.

## Local overlay and outputs

Resolve private configuration from `../../.local/writing-workflows/`, relative to the real
Skill directory. The central repository ignores the entire `.local/` tree.

- `aliases.json`: private project, audience, publication, domain, or output aliases.
- `env`: optional credential-variable names for an approved independent reviewer or
  publishing system; never auto-source it.
- `references/`: private voice samples, client guidance, terminology, and publishing rules.
- `runtime/`: drafts, contracts, lint output, review artifacts, and final deliverables.
- `README.md`: private operator notes.

Write deliverables to the requesting project when it provides an output location. Otherwise
use the ignored runtime overlay. Never copy private drafts, client names, correspondence,
voice samples, credentials, domains, or publishing configuration into tracked registry files
or the upstream submodule.

## Acceptance checks

- Exactly one `writing-workflows` root appears in each configured Agent discovery directory;
  no focused or language-specific upstream workflow is separately projected.
- The pinned commit, submodule URL, license, and upstream root match `manifest.json`.
- The audience, artifact type, and output language are explicit before drafting.
- The package's offline tests pass, and any lint result is interpreted within its
  Chinese-primary scope.
- Public files contain no private drafts, voice material, aliases, credentials, paths, or
  publishing data.
