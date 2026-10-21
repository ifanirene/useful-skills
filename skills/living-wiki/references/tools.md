# Configuration and tools

Read when adopting a wiki, configuring a repository, or running the audit, Zotero or image tools.

## `living-wiki.toml`

Put it at the repository root; copy `templates/living-wiki.toml`. A missing file means all
defaults. Unknown keys, wrong types and invalid values stop every tool with a
`living-wiki config error`. Paths marked R are repo-relative; W are wiki-relative.

| Key | Default | Meaning |
|---|---|---|
| `wiki.dir` (R) | `wiki` | Wiki folder |
| `wiki.index` (W) | `index.md` | Entry page for reachability |
| `wiki.manifest` (W) | `source-manifest.json` | Source register |
| `wiki.raw_roots` (R) | `["resources"]` | Curated folders whose every non-hidden file must be registered; `[]` when sources live elsewhere |
| `wiki.ignore` (R) | `[]` | fnmatch globs excluded from the raw-root scan (`*` also matches `/`) |
| `wiki.skip_dirs` (W) | `["evidence"]` | Regenerable folders excluded from page checks |
| `audit.baseline` (R) | `""` | JSON of accepted known errors |
| `zotero.mode` | `none` | `local-api` reads the Zotero desktop local API; needs `root_collection` |
| `zotero.api_base`, `root_collection`, `export_dir` (W), `exclude_item_types`, `exclude_doi_prefixes` | see template | Export scope; excluded items stay wiki sources |
| `images.enabled` | `false` | Turns on the image register and gallery |
| `images.manifest` (W), `scan_roots` (R), `gallery` (W), `gallery_dir` (W), `library_page` (W), `criteria_page` (W), `thumbnail_dir` (R), `thumbnail_size`, `max_references` | see template | Image register, scan scope and gallery rendering; keep thumbnails outside the scan roots |

## Commands

Resolve the scripts from this skill's real directory and run them with Python 3.11 or newer.
`--root` defaults to the current directory and `--config` to `<root>/living-wiki.toml`.

```bash
python3 scripts/wiki_audit.py --root <repo>                         # read-only; exit 1 on errors
python3 scripts/wiki_audit.py --root <repo> --report <file.json>    # also save the JSON report
python3 scripts/wiki_audit.py --root <repo> --write-baseline <file> # accept the current errors as known
python3 scripts/wiki_audit.py --root <repo> --stub <path> [<path> ...]  # sha256/bytes stubs for manifest rows
python3 scripts/wiki_zotero.py --root <repo>                        # refresh the read-only bibliography views
python3 scripts/wiki_images.py scan --root <repo>                   # check the image register
python3 scripts/wiki_images.py render --root <repo>                 # regenerate gallery pages and thumbnails
```

**Audit.** The audit checks:

- duplicate and unregistered files;
- missing or changed sources;
- missing notes and coverage;
- note IDs against the manifest (a warning);
- Zotero keys against the last export;
- relative links outside code fences;
- reachability from the index (a warning);
- the image register, when enabled.

It does not check URLs, anchors, placement, synthesis or claim support; review those yourself.
With a baseline active, the report separates `known_errors` from `new_errors` and fails only on
new ones. Write a baseline only for errors that cannot be fixed now, and list them in
`NOTES.md`. Never baseline an error to hide it.

**Zotero.** The refresh overwrites the generated files in `export_dir` and never writes to the
library. A registered source that is missing produces a warning and is skipped. If Zotero is
closed, the refresh stops before writing. Add or merge library items with the library tools
first, check for duplicates, then refresh.

**Images.** `render` deletes stale generated gallery pages. Inspect the rendered gallery,
because the checks cannot judge visual quality.

Optional dependencies: PyMuPDF for PDF DOI scanning, and Pillow when images are enabled.
