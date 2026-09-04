# Skill Index

Read this page to route a task; then read only the selected `SKILL.md`. The canonical
machine-readable record is [`../manifest.json`](../manifest.json).

## Scientific research

### [`literature-review`](literature-review/SKILL.md)

Use for finding a specific paper, verifying citations, comparing scientific methods, or
writing a source-grounded literature synthesis.

## Scientific visualization

### [`figure-style`](figure-style/SKILL.md)

Use for one standalone plot or for checking data fidelity, chart choice, labels, color,
layout, and publication legibility.

### [`figure-composer`](figure-composer/SKILL.md)

Use for one multi-panel scientific figure. It routes panel work through `figure-style` and
adds figure-level planning, composition, and adversarial review.

## Scientific writing

### [`research-paper-analysis-writing`](research-paper-analysis-writing/SKILL.md)

Use for turning one paper, or a tightly related small set, into a reader-first technical
analysis. It separates paper claims, external evidence, and analyst judgment, then locates the
work in its technical or product ecosystem. Use `literature-review` instead for broad surveys.

### [`paper-narrative`](paper-narrative/SKILL.md)

Use when judging or rebuilding the story told by all figures in a manuscript. It runs
before `figure-composer` when the task covers a complete paper.

## Agent engineering and skill authoring

### [`ai-programming-mindset`](ai-programming-mindset/SKILL.md)

Use when AI-assisted engineering stalls at plausible partial completion because the success
criteria, observation channel, verification loop, or division between reasoning and execution
is unclear. It is not a general coding-style guide.

### [`skill-writing-principles`](skill-writing-principles/SKILL.md)

Use to design or review the content of portable Agent Skills for outcome certainty, clear
boundaries, testable acceptance criteria, and progressive disclosure. Pair it with the current
host's creation tooling for packaging and mechanical validation.

## Visual communication

### [`show-me`](show-me/SKILL.md)

Use when a concise diagram, code-shape sketch, diff, or focused HTML artifact would make
structure, flow, change, or tradeoffs materially easier to understand than prose.

## General writing

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

## Common combinations

- Standalone plot: `figure-style`
- Multi-panel figure: `figure-composer` + `figure-style`
- Manuscript figure revision: `paper-narrative` → `figure-composer` → `figure-style`
- Literature-grounded scientific claim: `literature-review`, then the relevant writing or
  visualization skill
- Reader-first paper analysis: `research-paper-analysis-writing` + `literature-review`
- Stalled AI-assisted implementation: `ai-programming-mindset`
- Skill content design or review: `skill-writing-principles`
- Visual explanation: `show-me`
- Internal memo or external analytical article: `writing-workflows`
- Structured innovation: `innovation-assistant`
- Private AI session archive: `ai-session-export`
- Find a prior archived AI session: `ai-session-search-archive`
- Provider-selectable local image generation or upscaling: `image-generation`
- Online media workflow: `online-media`
- Presentation deck: `presentation`
