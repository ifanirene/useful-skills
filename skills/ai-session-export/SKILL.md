---
name: ai-session-export
description: Export local AI coding sessions from OpenCode, Claude Code, Codex, Google Antigravity, and Second Mind into a private Markdown archive using the pinned upstream tool.
license: MIT
---

# AI Session Export

## Objective

Use the pinned standalone project at `../../projects/ai_session_export` to turn local AI
coding-session stores into a consistent Markdown archive. This adapter is the only root Skill
that should be exposed to Agent discovery; do not link the upstream project's `skill.md`
separately.

## Use when

- Exporting or incrementally syncing AI coding sessions to Markdown.
- Backfilling sessions from a chosen date or one supported source.
- Validating an export configuration with a dry run.
- Extending the upstream project with another source adapter.

## Required context

1. Resolve relative paths from this Skill directory and locate
   `../../projects/ai_session_export`.
2. Read the upstream project's `AGENTS.md`, any `WORKSPACE.md` it may add later, and its
   lowercase `skill.md` completely before changing or running the tool.
3. Run commands from the upstream project root.
4. If the project directory is absent, initialize the pinned submodule from the central
   library root with `git submodule update --init projects/ai_session_export`.

## Privacy and safety boundary

- Session transcripts, project paths, prompts, and responses are private data. Keep exports
  outside this public Skill library and outside other public repositories.
- Selecting this Skill does not authorize an export. Confirm the requested sources, date
  range, and private output location before a write-producing run.
- Start with `--dry-run` when checking a new configuration.
- Source databases and transcript files are read-only inputs. The tool writes only its
  configured Markdown archive and incremental state file.
- Do not enable live end-to-end tests unless the user explicitly wants local transcript data
  exercised. The normal test suite uses synthetic fixtures.

## Common commands

```bash
# Inspect available options without exporting.
python export_sessions.py --help

# Count recent Codex sessions without writing files or state.
python export_sessions.py --source codex --since-date 2026-08-01 --dry-run

# Export to an explicitly private directory after the user approves the scope.
python export_sessions.py --source codex --base-dir /path/to/private/session-archive

# Validate the pinned project with synthetic fixtures only.
python -m pytest tests/ -v
```

The upstream tool also supports OpenCode, Claude Code, Antigravity, and Second Mind. Use its
`skill.md` for the full command surface and output contract.

## Acceptance checks

- The selected source and date range match the user's request.
- A dry run completes before the first real export for a new configuration.
- Real exports and state are outside public repositories.
- Output files follow the upstream YAML-frontmatter and alternating User/Assistant contract.
- Upstream non-live tests pass after code changes.

