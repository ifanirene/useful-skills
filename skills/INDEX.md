# Skill Index

Read this page to route a task; then read only the selected `SKILL.md`. The canonical
machine-readable record is [`../manifest.json`](../manifest.json).

## Scientific research

### [`literature-review`](literature-review/SKILL.md)

Use for a specific-paper lookup, method comparison, or evidence synthesis. Match search
breadth and output length to the question; verify both citation identity and claim support.

## Scientific visualization

### [`figure-style`](figure-style/SKILL.md)

Use for a scientific plot or figure review. Keep source fidelity and rendered-output checks
in scope; consult detailed design guidance only for the chart or edit at hand.

### [`figure-composer`](figure-composer/SKILL.md)

Use for one multi-panel scientific figure. It routes panel work through `figure-style` and
adds figure-level planning, composition, and adversarial review.

### [`baoyu-article-illustrator`](baoyu-article-illustrator/SKILL.md)

Use for scientific mechanisms, experimental workflows, and article illustrations with
consistent style, palette, and reference images. Includes a dedicated scientific style.
Generated schematics require factual and visual review; route quantitative plots to figure-style.

## Scientific writing

### [`research-paper-analysis-writing`](research-paper-analysis-writing/SKILL.md)

Use for turning one paper, or a tightly related small set, into a reader-first technical
analysis. It separates paper claims, external evidence, and analyst judgment, then locates the
work in its technical or product ecosystem. Use `literature-review` instead for broad surveys.

### [`paper-narrative`](paper-narrative/SKILL.md)

Use to make any research writing (a result write-up, report, progress report, manuscript,
or grant section) read as one question, one answer, and a chain of steps a reader can
follow. `polish` edits structure and clarity in the author's voice; `rewrite` reorganizes
for delivery. When the input has figures, it offers a figure review that can hand figures
to `figure-composer`. Use `research-paper-analysis-writing` for other people's papers.

## Agent engineering and skill authoring

### [`ai-programming-mindset`](ai-programming-mindset/SKILL.md)

Use when AI-assisted engineering stalls at plausible partial completion because the success
criteria, observation channel, verification loop, or division between reasoning and execution
is unclear. It is not a general coding-style guide.

### [`skill-writing-principles`](skill-writing-principles/SKILL.md)

Use to design or review the content of portable Agent Skills for outcome certainty, clear
boundaries, testable acceptance criteria, and progressive disclosure. Pair it with the current
host's creation tooling for packaging and mechanical validation.

## Knowledge integration

### [`graphify`](graphify/SKILL.md)

Use to build or explore concept graphs across related Markdown files, documents, and code.
Loads the official installed Python package's host workflow and references. Preserve source
provenance and distinguish explicit relationships from semantic inferences.

## Visual communication

### [`visual-explainer`](visual-explainer/SKILL.md)

Use for interactive HTML concept explanations, mechanisms, parameter controls, process
steppers, and requested slide decks. The adapter loads pinned upstream references and
templates and preserves factual uncertainty. Use `show-me` for smaller inline diagrams.

### [`show-me`](show-me/SKILL.md)

Use when a concise diagram, code-shape sketch, diff, or focused HTML artifact would make
structure, flow, change, or tradeoffs materially easier to understand than prose.

### [`image-dream`](image-dream/SKILL.md)

Use to build an artistic cover series from a repository element and a personal reference
library, including ChatGPT Library. Supports style exploration, private run history, and
host-managed scheduling. Use baoyu-article-illustrator for explanatory article illustrations.

## General writing

### [`explain-ste100`](explain-ste100/SKILL.md)

Use for concept explanations or technical drafts and revisions when the user requests
ASD-STE100 or STE-style language. Preserve technical meaning and distinguish a draft
from text reviewed against the complete standard and dictionary.

### [`writing-workflows`](writing-workflows/SKILL.md)

Use for internal memos and decision briefs when readers share project context, external
analytical articles when readers do not, or distribution posts derived from a finished
article. Use the scientific writing Skills for manuscripts, paper analysis, or literature
synthesis.

## Innovation methods

### [`innovation-assistant`](innovation-assistant/SKILL.md)

Use for systematic idea generation on an existing product, service, or interface, or on an
open problem. The root adapter routes to SIT or Think Bigger and keeps derivation chains,
named precedents, scoring, and human judgment checkpoints explicit.

## Developer productivity

### [`ai-session-export`](ai-session-export/SKILL.md)

Use for dry-running, exporting, or incrementally syncing local AI coding sessions into a
private Markdown archive. The Skill routes execution to a pinned standalone upstream project.

### [`ai-session-search-archive`](ai-session-search-archive/SKILL.md)

Use for finding prior Codex, Claude Code, OpenCode, Antigravity, or Second Mind sessions in an
existing private Markdown archive. It searches named entities lexically before using an
optional semantic fallback.

## Media processing

### [`intake-skill`](intake-skill/SKILL.md)

Use for synced Apple Voice Memos, local MLX transcription, and Codex daily reports.
Private data stays in the local overlay; nightly automation is opt-in.

### [`image-generation`](image-generation/SKILL.md)

Use for local image generation, prompt-based editing, or upscaling when the workflow needs
explicit Gemini or OpenAI model selection, a stable CLI, and files written to the requesting
project. Use the host image generator for ordinary in-app generation without those controls.

### [`online-media`](online-media/SKILL.md)

Use for permitted media download and transcription, medley source identification, candidate
source search, metadata repair, local music deduplication review, or bilingual subtitle work.
The Skill exposes one root adapter and routes focused workflows through a pinned upstream
project.

## Presentation authoring

### [`presentation`](presentation/SKILL.md)

Use for image-rendered or Reveal.js slide decks, keynotes, teaching decks, speaker notes, or
previewable presentation scaffolds. Route native PowerPoint editing to a PPTX-capable Skill.

## Remote computing

### [`remote-compute-ssh`](remote-compute-ssh/SKILL.md)

Use for SSH access to SCG, Sherlock, or another Slurm cluster from a local agent: reuse one
authenticated connection, transfer files, and submit or monitor jobs. Ships a standalone
helper that needs only Bash and OpenSSH. Use `compute-scg` for SCG-specific sizing and templates.

### [`compute-scg`](compute-scg/SKILL.md)

Use for Stanford SCG onboarding and Slurm CPU/GPU work. Includes a portable SSH
helper, live account/resource discovery, dated templates and project-environment
guidance. Lab account and personal path values stay in private overlays.

## Common combinations

- Standalone plot: `figure-style`
- Multi-panel figure: `figure-composer` + `figure-style`
- Clearer research draft in the author's voice: `paper-narrative` (`polish`)
- Research write-up restructured for the reader: `paper-narrative` (`rewrite`)
- Manuscript figure revision: `paper-narrative` (figure review) → `figure-composer` →
  `figure-style`
- Literature-grounded scientific claim: `literature-review`, then the relevant writing or
  visualization skill
- Reader-first paper analysis: `research-paper-analysis-writing` + `literature-review`
- Stalled AI-assisted implementation: `ai-programming-mindset`
- Skill content design or review: `skill-writing-principles`
- Visual explanation: `show-me`
- Concept explanation in STE: `explain-ste100`
- Internal memo or external analytical article: `writing-workflows`
- Structured innovation: `innovation-assistant`
- Private AI session archive: `ai-session-export`
- Find a prior archived AI session: `ai-session-search-archive`
- Provider-selectable local image generation or upscaling: `image-generation`
- Online media workflow: `online-media`
- Presentation deck: `presentation`
