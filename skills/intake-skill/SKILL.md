---
name: intake-skill
description: Install, verify, operate, and debug the Apple Voice Memos intake pipeline, with local MLX transcription and Codex daily reports.
license: MIT
---

# Intake Skill

Use the pinned `grapeot/intake-skill` project at `../../projects/intake_skill`.
This adapter is the only discoverable root; do not separately expose upstream workflows.

## Load and route

1. Resolve this file's real location before resolving relative paths.
2. Read the consuming project's AGENTS.md and any WORKSPACE routing first.
3. Read the upstream `AGENTS.md` and `skills/skill_intake.md` completely before operation.
   Resolve their relative references from the upstream project root.
4. If absent, initialize the pinned checkout from the library root with
   `git submodule update --init projects/intake_skill`.
5. Use the upstream `.venv/bin/python`; do not install packages globally.

## Local overlay

Keep private configuration and all generated artifacts in `../../.local/intake-skill/`
relative to this adapter, or an explicitly chosen private consuming-project directory.
The library ignores this overlay. Use `aliases.json` for private routes, `env` for optional
configuration, `runtime/` for data, logs and temporary artifacts, and `README.md` for
operator notes. Never auto-source an env file or copy overlay values into public files.

Set `INTAKE_DATA_DIR` to the overlay's runtime data directory on every invocation.
The local `run.py` launcher provides this setting. If the installed Codex CLI rejects
upstream `--full-auto`, a local compatibility shim may translate it to the supported
`--sandbox workspace-write` flag after checking `codex exec --help`; never bypass
approvals or sandboxing. Keep that host-specific shim in the overlay. The default upstream data location
is inside its checkout; do not use that default for personal recordings.
For synthetic validation, pass explicit overlay `--source` and `--data-dir` paths.
Keep package/model caches and validation logs in ignored local storage as well.

## Boundaries

- Apple Notes and Voice Memos may already provide usable transcripts. Do not claim this
  model is more accurate without a matched comparison. This upstream pipeline retranscribes
  audio; importing Apple transcripts or Notes recordings requires a separate adaptation.

- Process already-synced Apple Voice Memos only. No microphone recording, speaker
  recognition, diarization, or inferred participant identity.
- First run offline tests, then validate real MLX ASR and Codex postprocessing on synthetic
  audio before processing private recordings. Mock success is not real-ASR validation.
- Explain the first model download or warm-up before running it.
- Codex postprocessing uses the configured Codex service; local ASR does not imply that
  transcript summarization stays offline. Verify the non-private Codex check first.
- Installing the registry adapter does not authorize processing existing personal recordings.
- Nightly automation remains optional and requires explicit user authorization. The upstream
  cron builder does not propagate the overlay data setting. Prepare and verify a local
  schedule that uses the overlay launcher before enabling it; never install the default
  upstream cron line blindly. Keep schedule backups and logs in the overlay.
- Keep dashboard binding on localhost. Inspect its runtime paths and scheduling behavior
  before enabling controls; upstream schedule controls use the default cron builder.

## Acceptance

The manifest pin matches the upstream checkout and license; the index and single-skill
profile agree; exactly one adapter is exposed per host discovery chain. Registry and
privacy checks and upstream offline tests pass. Report real-ASR or Codex setup failures
separately from successful registry installation. A fully operational pipeline additionally
requires a nonempty `speaker,content` CSV and inspected daily Markdown, HTML, and meeting
artifacts from synthetic audio. Human functional/privacy review is required before merge.
