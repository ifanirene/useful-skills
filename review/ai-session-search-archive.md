# Local Review Packet: AI Session Search Archive

- Date prepared: 2026-08-23
- Branch: `codex/central-personal-skill-library`
- Upstream file: `https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/ai_session_search_archive.md`
- Inspected commit: `3f62b8b57f04d6a248770298b797ad38208db2d5`
- State: local checks passed; CI and human review pending

## Source discovery trace

The upstream repository has no `CLAUDE.md`. Its manual discovery chain is:

```text
AGENTS.md
  -> rules/WORKSPACE.md
  -> rules/skills/INDEX.md
  -> rules/skills/ai_session_search_archive.md
```

The target file is an instruction-only Markdown workflow without Agent Skills frontmatter,
scripts, or tests. It searches a private multi-source Markdown archive with lexical search
first, optional semantic fallback, exporter freshness checks, deduplicated evidence, and
validated navigation actions.

## Local discovery trace

This library's portable chain is:

```text
CLAUDE.md -> AGENTS.md -> manifest.json / skills/INDEX.md
                            -> skills/ai-session-search-archive/SKILL.md
                            -> profiles/session-search.txt
                            -> user-level Codex and Claude links
```

The upstream `rules/skills/` directory was not copied or linked. Doing so would import
unrelated identity, memory, axioms, and many other workflows. One attributed, host-neutral
Skill is installed at the canonical local layer instead.

## Privacy and authorization boundary

- No real archive, native session store, export state, sync log, cache, transcript, project
  path, session identifier, provider credential, or user query was read during installation.
- Private archive and semantic-search settings belong under the ignored
  `.local/ai-session-search-archive/` overlay.
- Archive lookup is read-only. The Skill does not export sessions, inspect native stores,
  refresh embeddings, install semantic search, or request credentials silently.
- `semantic-search` is not currently installed. Lexical search remains available; approximate
  semantic lookup reports the missing optional dependency.
- Export or backfill requires a separate request and the existing `ai-session-export` dry-run
  and scope-confirmation rules.

## Provenance boundary

The local Skill is an adaptation, not a verbatim directory install. The upstream README
declares MIT, but the inspected repository contains no standalone license file. The source
file URL, inspected commit, provider, and packaging limitation are recorded in
`manifest.json` and `docs/PROVENANCE.md`.

## Local verification

| Check | Result |
| --- | --- |
| Source routing trace | Passed: root router, workspace route, index entry, and target file agree |
| Source executable review | Not applicable: target file contains no code or scripts |
| Skill Creator validation | Passed |
| `python3 scripts/check_registry.py` | Passed: 8 Skills, 7 profiles |
| `python3 scripts/check_public_content.py` | Passed: 43 text files before this packet; semantic review still required |
| `git diff --check` | Passed |
| Codex discovery | Passed: one local root; zero upstream projections |
| Claude discovery | Passed: one local root; zero upstream projections |
| Local overlay ignore rules | Passed for README, config, and env placeholders |

## Required review

| Reviewer | Role | Disposition | Time |
| --- | --- | --- | --- |
| `@ifanirene` | Functional owner | Pending | — |
| `@ifanirene` | Privacy owner | Pending | — |

Do not merge or publish until both reviews are explicitly approved and CI passes.
