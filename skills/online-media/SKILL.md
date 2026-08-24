---
name: online-media
description: Route permitted online-media workflows for downloading and transcribing media, identifying medley source songs, finding candidate sources, repairing metadata, reviewing local music duplicates, or producing bilingual SRT subtitles. Do not use to bypass access controls or publish private media artifacts.
license: MIT
---

# Online Media

## Objective

Use the pinned standalone project at `../../projects/online_media_skill` for deterministic
media artifacts and agent-led evidence judgments. This adapter is the only root Skill exposed
to Agent discovery; do not separately link any Markdown files from the upstream `skills/`
directory.

## Required context

1. Resolve this `SKILL.md` to its real location before following relative paths.
2. Locate `../../projects/online_media_skill` from the real Skill directory.
3. Read the upstream `AGENTS.md`, any `WORKSPACE.md` it may add later, and
   `skills/online_media.md` completely before running or changing the project.
4. Let the upstream root route the request to exactly the focused workflow needed for the
   task; do not load every focused workflow by default.
5. Run commands from the upstream project root and use its `.venv` when available.
6. If the project directory is absent, initialize the pinned checkout from the central
   library root with `git submodule update --init projects/online_media_skill`.

## Use when

- Downloading permitted online audio or video and preserving metadata sidecars.
- Running configured ASR and producing reusable transcript artifacts.
- Identifying songs in medleys from lyric evidence.
- Finding and verifying candidate media sources.
- Planning or reviewing local music metadata repair and duplicate cleanup.
- Correcting, translating, rendering, or validating bilingual subtitles.

## CLI and agent boundary

Use the CLI for deterministic transformations and artifact production: download, metadata,
ASR, parsing, query packs, inventories, plans, subtitle rendering, and structural validation.
Keep search strategy, source credibility, song identity, translation quality, confidence,
and final synthesis in the agent layer with explicit evidence.

## Local overlay

Private configuration belongs under `../../.local/online-media/`, resolved from the real
Skill directory. The central repository ignores the entire `.local/` tree.

- `env`: optional environment assignments for credentials and machine-specific tool paths.
- `aliases.json`: private media-library, playlist, and source aliases.
- `runtime/`: downloaded media, transcripts, sidecars, search payloads, and review artifacts.
- `README.md`: private operator notes.

Never copy overlay values into the public adapter, registry, review packet, command output, or
upstream submodule. Do not source `env` automatically; inspect only the variable names needed
for the requested workflow and ask before using credentials for a live operation.

## Safety boundary

- Work only with media the user is allowed to access and process. Do not bypass DRM, paywalls,
  authentication controls, or platform restrictions.
- Default tests are offline. Live downloads, ASR, and search require explicit task scope and
  the upstream opt-in environment variables.
- Start metadata repair, conversion, deduplication, and library changes with a dry run or plan.
  Do not overwrite, move, trash, or import media until the user approves the reviewed plan.
- Keep real media, platform `.info.json`, signed URLs, cookies, transcripts, library paths,
  search payloads, and result files out of public repositories.
- Treat aggregate search answers as hints. High-confidence identity claims require returned
  evidence that supports both the content anchor and claimed source.

## Acceptance checks

- Exactly one `online-media` root appears in the Agent discovery catalog.
- The pinned upstream commit and root router match `manifest.json`.
- The selected focused workflow matches the user request.
- Public files contain no private overlay values or runtime artifacts.
- Mutation-producing workflows have a reviewed plan and explicit approval.
- Upstream offline tests and privacy scan pass after integration or code changes.
