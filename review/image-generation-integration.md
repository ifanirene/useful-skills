# Local Review Packet: Image Generation Integration

- Date prepared: 2026-08-23
- Branch: `codex/central-personal-skill-library`
- Upstream: `https://github.com/grapeot/image-generation-skill`
- Pinned commit: `5c1b2593a628a4f9c78883df90dd00feada256a4`
- State: local checks passed; CI and human review pending

## Scope

- Pin the upstream repository at `projects/image_generation_skill` as a Git submodule.
- Install its Python package and development dependencies in its ignored `.venv`.
- Add one Agent-Skills adapter at `skills/image-generation/SKILL.md`.
- Register one `image-generation` entry in the manifest, human index, README, provenance
  record, changelog, and isolated discovery profile.
- Project that one root into the Codex and Claude user-level discovery directories.
- Keep credentials, aliases, source images, outputs, and runtime artifacts under the ignored
  `.local/image-generation/` overlay.

## Routing decision

The upstream repository is a standalone Python package with a stable CLI, one root skill,
offline tests, and explicit Gemini and OpenAI provider integrations. It remains the canonical
implementation. The central adapter distinguishes its provider-selectable local file workflow
from ordinary host-native image generation and is the only root exposed to discovery.

No `WORKSPACE.md` exists at the pinned commit. The upstream root Markdown file, package
modules, script wrapper, docs, and tests are not separately linked into Codex or Claude
discovery.

## Source, privacy, and safety review

- Provider SDK imports are lazy. Network calls occur only inside explicit generation or
  upscale functions; the default test suite is offline.
- The package can read API keys from environment variables or optional generic 1Password
  references. Real values remain in the ignored central overlay and are never printed or
  committed.
- The package writes only requested image outputs and temporary format-conversion files. It
  uses macOS `sips` for JPEG conversion and removes only its own temporary files after a
  successful conversion.
- No live image request, credential lookup, source-image read, or generated output occurred
  during installation.

## License finding

The inspected commit has no license file and `pyproject.toml` contains no license declaration.
The adapter and registry therefore use `NOASSERTION`. Human review must resolve or explicitly
accept this limitation before publication or merge.

## Local verification

| Check | Result |
| --- | --- |
| Upstream offline suite | Passed: 23 tests |
| Upstream CLI help | Passed |
| Skill Creator validation | Passed |
| `python3 scripts/check_registry.py` | Passed: 11 Skills, 10 profiles |
| `python3 scripts/check_public_content.py` | Passed: 59 text files; semantic review still required |
| `git diff --check` | Passed |
| Submodule pin | Passed: manifest, Git link, URL, commit, and entrypoint agree |
| Codex discovery | Passed: one `image-generation` root; zero upstream projections |
| Claude discovery | Passed: one `image-generation` root; zero upstream projections |
| Local overlay ignore rules | Passed for README, env, aliases, runtime, and `.env` projection |

## Test-scope observation

The first pytest invocation was launched from the central library root, so pytest used the
central configuration and collected tests from neighboring submodules. Their missing optional
dependencies caused collection errors. Rerunning from the image-generation project root used
its own `pyproject.toml`, collected only its 23 offline tests, and passed. This was a working-
directory error, not an upstream test failure.

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge or publish until the license finding is resolved or accepted, both reviews are
explicitly approved, and CI passes.
