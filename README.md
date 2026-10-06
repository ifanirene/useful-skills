# Central Personal Skill Library

This is my shared personal Skill repository for Codex, Claude Code, Cursor, OpenCode, and
other Agents that can read Markdown workflows.

The repository borrows the root-routing pattern from
[`grapeot/context-infrastructure`](https://github.com/grapeot/context-infrastructure), but
contains only reusable capabilities. Personal memory, credentials, machine paths, and private
project context stay outside the public registry.

## Start here

- Agent router: [`AGENTS.md`](AGENTS.md)
- Human-readable Skill index: [`skills/INDEX.md`](skills/INDEX.md)
- Canonical machine-readable registry: [`manifest.json`](manifest.json)
- Project integration: [`docs/PROJECT_INTEGRATION.md`](docs/PROJECT_INTEGRATION.md)
- Architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- Local overlay contract: [`docs/LOCAL_OVERLAYS.md`](docs/LOCAL_OVERLAYS.md)
- Sidecar portability: [`docs/PORTABILITY.md`](docs/PORTABILITY.md)

## Skills

| Skill | Purpose |
| --- | --- |
| [`compute-scg`](skills/compute-scg/SKILL.md) | SCG SSH onboarding, Slurm CPU/GPU jobs, resource discovery and project environments |
| [`intake-skill`](skills/intake-skill/SKILL.md) | Synced Apple Voice Memos transcription and daily reports |
| [`baoyu-article-illustrator`](skills/baoyu-article-illustrator/SKILL.md) | Scientific and article illustrations with controlled style, palette, and references |
| [`figure-style`](skills/figure-style/SKILL.md) | Scientific plots with source fidelity and rendered-output checks |
| [`figure-composer`](skills/figure-composer/SKILL.md) | Multi-panel scientific figure planning, composition, and review |
| [`paper-narrative`](skills/paper-narrative/SKILL.md) | Question-first narrative for any research writing: `polish` the author's draft or `rewrite` it for delivery |
| [`literature-review`](skills/literature-review/SKILL.md) | Verified paper lookup, method comparison, and evidence synthesis |
| [`research-paper-analysis-writing`](skills/research-paper-analysis-writing/SKILL.md) | Reader-first technical paper analysis with evidence layers and ecosystem positioning |
| [`ai-programming-mindset`](skills/ai-programming-mindset/SKILL.md) | Diagnose feedback, verification, and orchestration gaps in AI-assisted engineering |
| [`skill-writing-principles`](skills/skill-writing-principles/SKILL.md) | Design outcome-driven, bounded, and testable Agent Skill instructions |
| [`image-dream`](skills/image-dream/SKILL.md) | Recurring artistic covers from repository elements and a personal or ChatGPT image library |
| [`graphify`](skills/graphify/SKILL.md) | Connect concepts across Markdown, documents, and code; query and visualize knowledge graphs |
| [`visual-explainer`](skills/visual-explainer/SKILL.md) | Interactive HTML explanations with diagrams, controls, process steppers, and requested slide decks |
| [`show-me`](skills/show-me/SKILL.md) | Explain structure, flow, and change with concise visual forms |
| [`explain-ste100`](skills/explain-ste100/SKILL.md) | Concept explanations and technical English with ASD-STE100 principles and explicit compliance limits |
| [`writing-workflows`](skills/writing-workflows/SKILL.md) | Internal memos, external analytical articles, and article distribution posts |
| [`innovation-assistant`](skills/innovation-assistant/SKILL.md) | Structured SIT or Think Bigger ideation with auditable derivation chains |
| [`image-generation`](skills/image-generation/SKILL.md) | Generate, edit, or upscale local images through Gemini or OpenAI provider APIs |
| [`ai-session-export`](skills/ai-session-export/SKILL.md) | Export local AI coding sessions to a private Markdown archive |
| [`ai-session-search-archive`](skills/ai-session-search-archive/SKILL.md) | Find prior AI sessions in an existing private Markdown archive |
| [`online-media`](skills/online-media/SKILL.md) | Route permitted media download, transcription, source identification, metadata, deduplication, and bilingual subtitle workflows |
| [`presentation`](skills/presentation/SKILL.md) | Create image-rendered or Reveal.js decks with speaker notes, preview, and validation |

`manifest.json` is the source of truth for Skill identity, path, category, source, pinned
upstream commit, and status. This table and `skills/INDEX.md` are human-readable projections.

## Use from any project

The lightest integration is a reference from the project's `AGENTS.md`. Copy the block in
[`templates/AGENTS.skill-library.md`](templates/AGENTS.skill-library.md) and replace the
placeholder with the checkout path on that machine. Claude Code projects can import the same
policy from `CLAUDE.md`:

```markdown
@AGENTS.md
```

For Agent-native discovery, preview and apply a small profile:

```bash
python3 scripts/link_skills.py --profile research --agent all
python3 scripts/link_skills.py --profile research --agent all --apply
```

The online-media integration deliberately exposes one root Skill only:

```bash
python3 scripts/link_skills.py --profile online-media --agent all
python3 scripts/link_skills.py --profile online-media --agent all --apply
```

Presentation authoring follows the same one-root pattern:

```bash
python3 scripts/link_skills.py --profile presentation --agent all
python3 scripts/link_skills.py --profile presentation --agent all --apply
```

Structured innovation also exposes only its upstream root router:

```bash
python3 scripts/link_skills.py --profile innovation-assistant --agent all
python3 scripts/link_skills.py --profile innovation-assistant --agent all --apply
```

Provider-selectable local image generation follows the same one-root pattern:

```bash
python3 scripts/link_skills.py --profile image-generation --agent all
python3 scripts/link_skills.py --profile image-generation --agent all --apply
```

General internal and external writing also uses one root router:

```bash
python3 scripts/link_skills.py --profile writing-workflows --agent all
python3 scripts/link_skills.py --profile writing-workflows --agent all --apply
```

The linker creates per-Skill symbolic links and refuses to replace real directories or links
to other sources.

## Standalone upstream projects

Substantial tools remain in their own repositories and are pinned under `projects/` as Git
submodules. A small adapter under `skills/` is the only discoverable root. This keeps one
canonical upstream codebase while preventing every focused internal workflow from crowding
the Agent Skill catalog.

Initialize pinned projects after cloning:

```bash
git submodule update --init --recursive
```

## Private local configuration

Use `.local/<skill-name>/` for private aliases, machine paths, credentials, and runtime
artifacts. The entire `.local/` tree is ignored and excluded from public-content validation.
Never copy its values into public Skills, documentation, review packets, or command output.

## Repository layout

```text
useful-skills/
├── AGENTS.md                 # Canonical Agent router
├── CLAUDE.md                 # Claude Code import of the router
├── manifest.json             # Canonical registry
├── skills/                   # One discoverable root per registered Skill
│   ├── INDEX.md
│   └── <skill>/SKILL.md
├── projects/                 # Pinned standalone upstream projects
├── profiles/                 # Small discovery selections
├── templates/                # Project integration templates
├── docs/                     # Architecture and governance
├── scripts/                  # Linking and validation tools
├── .local/                   # Ignored private overlays
└── .github/workflows/        # Registry consistency checks
```

## Change a Skill

1. Work on a review branch.
2. Update the canonical Skill or pinned upstream project.
3. Synchronize `manifest.json`, `skills/INDEX.md`, relevant profiles, `README.md`, and
   `CHANGELOG.md`.
4. Run:

   ```bash
   python3 scripts/check_registry.py
   python3 scripts/check_public_content.py
   git diff --check
   ```

5. Obtain explicit functional and privacy approval before merging.

Do not commit credentials, private data, machine-specific paths, customer information,
unpublished research data, or material that cannot be redistributed.
