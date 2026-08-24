# Architecture

## Goal

This repository gives every Agent one stable place to discover and share reusable personal
capabilities. It adapts the routing pattern from `grapeot/context-infrastructure`: a small
root instruction file points to indexes, and detailed content is loaded only when needed.

It deliberately does not copy that project's memory, identity, heartbeat, or personal-rule
layers. Those concerns are useful in a full context system but create privacy and instruction
leakage risks in a portable Skill library.

## Layers

```text
Project Agent instructions
        │ reference
        ▼
AGENTS.md ──► manifest.json ──► skills/INDEX.md
                    │                   │
                    └──────────┬────────┘
                               ▼
                      skills/<name>/SKILL.md
                               │
                               ▼
                    scripts, references, assets
```

### Root router

`AGENTS.md` tells any visiting Agent how to discover, load, and maintain Skills. It remains
short enough to be included from projects without consuming the context needed for the task.
`CLAUDE.md` imports the same router so Claude Code does not require a second policy copy.

### Canonical registry

`manifest.json` is the source of truth for identity and governance. Each Skill record has:

- one canonical name, path, entrypoint, category, and description;
- one canonical URL and a separate provenance record;
- packaging compatibility, status, license, and tracked files;
- an explicit note when earlier provenance is incomplete.

README and `skills/INDEX.md` are human-readable projections. CI checks that they do not drift
from the manifest.

### Canonical Skill sources

All Skill content maintained in this repository lives under `skills/<name>/`. A Skill has a
required `SKILL.md` and may include `scripts/`, `references/`, `assets/`, tests, or sidecars.
The directory name and frontmatter `name` must agree.

A capability with a substantial independent codebase and release cycle should remain in its
own repository. This registry should point to that canonical source or contain a small,
clearly attributed adapter instead of silently forking it.

Pinned standalone tools may be checked out as Git submodules under `projects/`. Each such
project is exposed through one adapter under `skills/`; the upstream project's own root Skill
is not separately projected into Agent discovery.

### Profiles and projections

`profiles/*.txt` select small task-oriented sets for Agent-native discovery. The link script
projects those selections into local Agent directories. These links are never canonical and
are never committed.

Projects can instead use reference-only mode by including the supplied block in their Agent
instructions. This avoids catalog bloat and loads a Skill only when needed.

## Public and private boundary

This GitHub repository is public. It may contain reusable workflows, public examples, and
properly licensed helper code. It must not contain credentials, real personal or research
records, machine-specific paths, private endpoints, unpublished sensitive data, customer or
employee identifiers, or project-only assumptions.

Private configuration belongs in the consuming project's ignored files or another local
overlay. A reusable Skill may document the overlay contract and placeholders, but not the
real values.

This repository reserves the ignored `.local/<skill-name>/` tree for machine-only overlays.
See `docs/LOCAL_OVERLAYS.md`. Public checks skip that tree because it is not registry content;
reviewers must still ensure no overlay values leak into tracked files or task output.

## Change flow

1. Prepare a focused change on a review branch.
2. Update the canonical Skill and every affected registry projection.
3. Run structural and privacy checks.
4. Record the change and any migration effect.
5. Obtain explicit human functional and privacy approval.
6. Merge only after approval; passing CI alone is not approval.

Removal follows the same flow. Delete profiles, links, indexes, and aliases that point to the
removed Skill, and preserve the reason in `CHANGELOG.md` and review history.
