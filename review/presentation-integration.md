# Local Review Packet: Presentation Integration

- Date prepared: 2026-08-16
- Branch: `codex/central-personal-skill-library`
- Upstream: `https://github.com/grapeot/presentation_skill`
- Pinned commit: `f9881ad99400994134b5cff989093e30bc9f2d79`
- State: local checks passed; CI and human review pending

## Scope

- Pin the upstream repository at `projects/presentation_skill` as a Git submodule.
- Add one Agent-Skills adapter at `skills/presentation/SKILL.md`.
- Register one `presentation` entry in the manifest, human index, README, provenance record,
  changelog, and isolated discovery profile.
- Project that one root into the Codex and Claude user-level discovery directories.
- Add an ignored `.local/presentation/` overlay for private aliases, paths, credentials,
  generated decks, and runtime artifacts.

## Routing decision

The upstream project is a standalone presentation package with its own CLI, tests, license,
root router, and progressive-disclosure workflows. It remains the canonical implementation.
The central adapter is the only `SKILL.md` exposed to discovery. It requires an Agent to read
the upstream `AGENTS.md`, any future `WORKSPACE.md`, and `skills/skill_presentation.md`, then
load only the supporting workflow required by the deck task.

No `WORKSPACE.md` exists at the pinned commit. The four supporting upstream Markdown
workflows are not linked into Codex or Claude discovery.

## Source and safety review

- The core CLI scaffolds decks, prepares local image assets, and exports compatible image
  decks to PDF. Its default tests are offline.
- The copied image-deck scaffold contains optional OpenAI and Gemini renderers that read a
  deck-local `.env` and can issue parallel live image requests. Installation and validation
  did not run those tools.
- The adapter prefers the installing workspace's configured image-generation capability,
  keeps live rendering task-scoped, starts with draft batches, and forbids silent mode
  downgrade.
- Preview binds to localhost by default; LAN exposure requires an explicit request.
- Native `.pptx` editing remains outside this Skill and routes to a PPTX-capable workflow.

## Privacy boundary

- No live image generation, generated deck, preview server, private asset, or credential was
  used during integration.
- The upstream privacy scan found only documented fake `op://your-vault/...` placeholders in
  `.env.example`; no personal home path or token pattern was found.
- The ignored local overlay contains placeholders only. Its values are excluded from public
  files and discovery links.

## Local verification

| Check | Result |
| --- | --- |
| Upstream default offline suite | Passed: 40 tests |
| Upstream CLI help | Passed |
| Skill Creator validation | Passed |
| `python3 scripts/check_registry.py` | Passed: 7 Skills, 6 profiles |
| `python3 scripts/check_public_content.py` | Passed: 39 text files; semantic review still required |
| `git diff --check` | Passed |
| Submodule pin | Passed: manifest, Git link, URL, commit, and entrypoint agree |
| Codex discovery | Passed: one `presentation` root; zero upstream projections |
| Claude discovery | Passed: one `presentation` root; zero upstream projections |
| Local overlay ignore rules | Passed for README, env, and aliases placeholders |

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge or publish until both reviews are explicitly approved and CI passes.
