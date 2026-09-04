# Local Review Packet: Writing Workflows Integration

- Date prepared: 2026-08-23
- Branch: `codex/central-personal-skill-library`
- Upstream: `https://github.com/grapeot/writing-skill`
- Pinned commit: `9f2f6974a143de92c52dc5be1bfd931018a09f39`
- State: local checks passed; CI and human review pending

## Scope

- Pin the upstream repository at `projects/writing_skill` as a Git submodule.
- Install its package and development dependencies in an ignored project-local `.venv`.
- Add one language-aware Agent-Skills adapter at `skills/writing-workflows/SKILL.md`.
- Register one `writing-workflows` entry in the manifest, human index, README, provenance
  record, changelog, and isolated discovery profile.
- Project that one root into the Codex and Claude user-level discovery directories.
- Keep private drafts, voice material, aliases, reviewer credentials, publishing routes, and
  outputs under the ignored `.local/writing-workflows/` overlay.

## Routing decision

The upstream repository has one Chinese canonical router, focused internal/external/Twitter
workflows, English mirrors of the focused files, an MIT-licensed deterministic Chinese prose
lint CLI, and offline tests. It remains the canonical implementation. The central English
adapter routes by audience, artifact, and output language and is the only root exposed to
discovery.

No `WORKSPACE.md` exists at the pinned commit. Upstream focused workflows, language mirrors,
references, package modules, and lint documentation are not separately linked into Codex or
Claude discovery.

## Source, privacy, and portability review

- The lint package uses only the Python standard library, reads one supplied Markdown file,
  and writes reports to stdout. It makes no network calls and does not mutate the input.
- Chinese is canonical upstream; English mirrors exist only for focused files. The central
  adapter reads the canonical root first and then selects the matching language file.
- One English external workflow still names the pre-package module path
  `rules.skills.external_prose_lint_cli`; the installed adapter overrides it with the current
  `writing_skill.external_prose_lint_cli` module.
- External live gates assume an independent second-model context and sometimes name the
  upstream-specific `agy` command. The adapter requires an actually isolated available
  reviewer or reports the gate unavailable instead of silently simulating it.
- No private draft, correspondence, voice sample, client or publication identifier,
  credential, or real reviewer transcript was read or added during installation.

## Local verification

| Check | Result |
| --- | --- |
| Upstream offline suite | Passed: 18 tests |
| Upstream CLI help | Passed |
| Skill Creator validation | Passed |
| `python3 scripts/check_registry.py` | Passed: 14 Skills, 13 profiles |
| `python3 scripts/check_public_content.py` | Passed: 67 text files; semantic review still required |
| `git diff --check` | Passed |
| Submodule pin | Passed: manifest, Git link, URL, commit, license, and entrypoint agree |
| Codex discovery | Passed: one `writing-workflows` root; zero focused projections |
| Claude discovery | Passed: one `writing-workflows` root; zero focused projections |
| Local overlay ignore rules | Passed for README, env, aliases, references, and runtime |

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge or publish until both reviews are explicitly approved and CI passes.
