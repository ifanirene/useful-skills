---
name: ai-session-search-archive
description: Find prior Codex, Claude Code, OpenCode, Antigravity, or Second Mind sessions in an existing private Markdown archive. Use source-scoped lexical search first and optional semantic search for approximate memories; do not use to export sessions or rebuild indexes without separate authorization.
license: MIT
---

# AI Session Search Archive

## Objective

Find evidence from prior AI sessions without depending on one vendor's history interface.
Search an existing private Markdown archive read-only, return verifiable excerpts, and avoid
leaking archive configuration or session identifiers.

This Skill adapts the public
[`ai_session_search_archive.md`](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/ai_session_search_archive.md)
workflow from `grapeot/context-infrastructure`, pinned in `manifest.json`.

## Resolve private context

1. Use an archive location explicitly supplied for the current request when available.
2. Otherwise resolve private settings from `../../.local/ai-session-search-archive/` relative
   to the real location of this `SKILL.md`.
3. Read only the configuration fields needed for the lookup. Do not print the archive root,
   cache location, credentials, host profiles, or unrelated aliases.
4. Inspect which source directories actually exist. When the user names a source, search only
   that source. Otherwise search all available source directories.

Do not assume that an archive lives inside this public repository. Typical source names are
`opencode`, `claude_code`, `codex`, `antigravity`, and `second_mind`, but accept the actual
layout recorded in the private overlay.

## Retrieval order

### Named entities: lexical search first

Use `rg` for product names, people, projects, titles, dates, and session identifiers. Expand
the remembered wording into a few plausible variants. Search Markdown contents, not only
filenames, and do not interpret truncated output as evidence that no match exists.

```bash
rg -i -n --glob '*.md' -- 'variant one|variant two' "$session_source_dir"
```

### Approximate memories: optional semantic fallback

Use semantic search only when lexical variants are insufficient and a configured
`semantic-search` CLI is already available. Generate a fresh file list for the current source
scope; the list is also the result allowlist, so never reuse a stale one.

```bash
session_filelist="$(mktemp)"
trap 'rm -f "$session_filelist"' EXIT
rg --files "$session_source_dir" -g '*.md' > "$session_filelist"

semantic-search query \
  --file-list "$session_filelist" \
  --cache-dir "$semantic_cache_dir" \
  --query 'remembered concept' \
  --top-k 10 \
  --no-refresh
```

Use the semantic-search tool's own provider and model configuration. A read-only lookup must
not refresh or rebuild a shared index. If semantic search is unavailable, report that the
lexical search completed and the optional semantic fallback is not configured; do not install
another tool or request credentials silently.

## Freshness boundary

Check the export state or sync log named in the private overlay when freshness matters. If the
target session should be newer than the last successful export, explain that the archive may
be stale. Do not inspect native session stores or run an export automatically.

If the user explicitly asks to update or backfill the archive, load `ai-session-export`,
confirm sources, date range, and private output location, then follow its dry-run requirement.
Keep any temporary export under the ignored runtime overlay and remove it after the lookup.

## Result contract

- Consolidate chunks by source and session identifier so each session appears once.
- Show title, date, source, project short name when available, and a short verbatim excerpt
  that lets the user verify the match.
- Prefer evidence over an AI-only summary. Do not display embedding scores.
- Read identifiers and action metadata from archive frontmatter; never infer them from a
  filename or transcript text.
- Use ordinary local Markdown links unless both the archive metadata and current host support
  a client-specific action.
- Never hand-construct an action from unvalidated text. For OpenCode, allow
  `opencode://session/<session_id>` only when the frontmatter value matches
  `^ses_[A-Za-z0-9_-]+$`; otherwise return a normal file link.
- Never place credentials, server addresses, host profiles, absolute archive roots, or user
  queries into client action URLs.

## Acceptance checks

- The search covered the correct source scope and tried sensible lexical variants first.
- Any semantic query used a fresh scoped file list and `--no-refresh`.
- Results are deduplicated and include excerpts that verify the match.
- Navigation actions come only from validated metadata.
- The archive, cache, state, logs, and session content remain outside public repositories.
