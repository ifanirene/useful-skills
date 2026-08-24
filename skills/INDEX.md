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

### [`paper-narrative`](paper-narrative/SKILL.md)

Use when judging or rebuilding the story told by all figures in a manuscript. It runs
before `figure-composer` when the task covers a complete paper.

## Developer productivity

### [`ai-session-export`](ai-session-export/SKILL.md)

Use for dry-running, exporting, or incrementally syncing local AI coding sessions into a
private Markdown archive. The Skill routes execution to a pinned standalone upstream project.

## Media processing

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
- Private AI session archive: `ai-session-export`
- Online media workflow: `online-media`
- Presentation deck: `presentation`
