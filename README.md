# Useful Scientific Research Skills

These are Anthropic-authored, portable SKILL.md-format skills (folder + YAML-frontmatter
Markdown + optional sidecar script). This is the same open convention used by
Claude Code, Codex CLI, Cursor, and other coding agents, so no format conversion
is needed.

## Install into Claude Code

- Personal (all projects): copy each skill folder into `~/.claude/skills/<skill-name>/`
- Project-scoped (shared via git): copy into `.claude/skills/<skill-name>/`

Claude Code watches these directories for changes; edits typically apply within
the current session. Creating a brand-new top-level `skills/` directory that
didn't exist at session start requires a restart. Verify with `/skills`.

## Install into Codex CLI

- Global: copy each skill folder into `~/.codex/skills/<skill-name>/`
- Project: copy into `.codex/skills/<skill-name>/`

Codex loads skills at startup and matches them to your prompt via the
`description` field in SKILL.md frontmatter. On some Codex builds skills are
still gated behind a feature flag (`codex --enable skills`) -- check your
version if the skill doesn't show up in `/skills`.

## Important: the `kernel.py` sidecar

Each skill folder includes a `kernel.py` alongside `SKILL.md`. On the platform
these were exported from, `kernel.py` is auto-loaded into the live Python
kernel the moment the skill is loaded -- its functions (e.g.
`apply_figure_style()`) become directly callable with no import statement.

Claude Code and Codex do NOT have that auto-injection mechanism. They will
read `SKILL.md` as instructions but won't automatically execute `kernel.py`
into a persistent kernel. To get equivalent behavior there, either:

1. Add a line near the top of `SKILL.md` telling the agent to run
   `python -c "from kernel import *; ..."` (or `exec(open('kernel.py').read())`)
   in its own code-execution tool before using any helper function, or
2. Have the agent read `kernel.py` and inline the relevant helper function
   definitions directly when it writes plotting code.

The Markdown guidance in each SKILL.md (data fidelity checks, label rules,
chart-choice logic, etc.) applies as-is regardless of language/tool -- only the
"auto-loaded helper functions" convenience needs this manual bridge.

## Skills included

- `figure-style/`      - single-plot publication-grade correctness rules + helpers
- `figure-composer/`   - multi-panel figure composition workflow
- `paper-narrative/`   - whole-paper figure arc / narrative review workflow

## Adding a skill

1. Add a directory named after the skill.
2. Include a `SKILL.md` with YAML frontmatter containing at least `name` and
   `description`.
3. Add any sidecar scripts or templates in the same directory.
4. Record the skill's origin and tracked files in `manifest.json`.
5. Add the skill to the list above.

Do not commit generated files, credentials, private data, or licensed material
that cannot be redistributed.
