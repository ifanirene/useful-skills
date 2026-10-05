# Intake Skill integration review

## Source and scope

- Source: https://github.com/grapeot/intake-skill
- Pin: `830956d107cc0e9fc4849809827d8841b8426837`
- License: MIT, verified in the pinned LICENSE.
- Checkout: `projects/intake_skill`; upstream source remains unchanged.
- One public adapter: `skills/intake-skill/SKILL.md`.
- Discovery: dedicated profile containing only `intake-skill`, projected to Codex and Claude.
- Uses the existing review branch; preserves pre-existing staged and unstaged work.
- No WORKSPACE routing file found in this library or the imported project.

## Privacy and runtime boundary

Private aliases, machine settings, outputs and local launcher are under the ignored
`.local/intake-skill/` overlay. No credentials were copied. No personal recordings
were processed. Upstream defaults write data within its checkout; the local launcher
sets the overlay data destination. Upstream cron drops this setting, so automatic
scheduling must use an explicitly reviewed overlay-aware command.

## Verification

- Upstream offline suite: 28 passed. The localhost server test required sandbox escalation.
- MLX dependency import passed with GPU access outside the sandbox.
- Registry: 18 skills, 17 profiles. Public-content scan: 90 text files.
- `git diff --check` passes; both discovery links resolve to the sole adapter.
- ffmpeg installed; synthetic speech generation and sync passed.
- The installed Codex CLI rejects upstream `--full-auto` (exit 2). A private shim
  translates it to `--sandbox workspace-write`; the non-private Codex check passed.
- Initial Xet weight transfer stalled; standard HTTP fallback completed successfully.
- Real Qwen ASR passed on synthetic speech, producing a nonempty CSV with exactly
  `speaker,content` columns. The expected spoken sample sentence was recovered.
- Codex generated daily Markdown, matching self-contained HTML, and a no-meeting note.
  Inspected file contents correctly identify synthetic audio and invent no action items.
- The privacy scanner previously excluded overlay text but still flagged overlay symlinks.
  Aligned the symlink pass with the documented `.local/` exclusion; verified that a
  symlink outside the overlay remains rejected.
- Upstream checkout remains clean. Runtime compatibility changes are local only.
- No nightly schedule was installed; no affirmative scheduling choice was received.
- Apple-versus-Qwen accuracy comparison awaits a selected recording and Apple transcript.

## Product fit

The model is an upstream dependency, not a demonstrated accuracy improvement over
Apple transcription. Existing Apple transcripts may avoid redundant processing.
This version ingests Voice Memos audio, not Apple Notes or exported Apple transcripts.

## Human review

Functional reviewer: pending. Privacy reviewer: pending.
Local installation is authorized. No merge or publication is performed.
