"""Load living-wiki.toml: merge defaults, resolve paths and validate types.

Repository-relative keys resolve against the repository root; wiki-relative keys
resolve against [wiki] dir. Empty optional paths become None.
"""

from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    raise SystemExit("living-wiki requires Python 3.11 or newer (tomllib)") from None

DEFAULTS = {
    "wiki": {"dir": "wiki", "index": "index.md", "manifest": "source-manifest.json",
             "raw_roots": ["resources"], "ignore": [], "skip_dirs": ["evidence"]},
    "audit": {"baseline": ""},
    "zotero": {"mode": "none", "api_base": "http://127.0.0.1:23119/api/users/0", "root_collection": "",
               "export_dir": "references", "exclude_item_types": [], "exclude_doi_prefixes": []},
    "images": {"enabled": False, "manifest": "image-manifest.json", "scan_roots": [],
               "gallery": "sources/images.md", "gallery_dir": "sources/image-gallery",
               "library_page": "", "criteria_page": "", "thumbnail_dir": "output/wiki-gallery/thumbnails",
               "thumbnail_size": [300, 220], "max_references": 2},
}
REPO_PATHS = {"wiki.dir", "wiki.raw_roots", "audit.baseline", "images.scan_roots", "images.thumbnail_dir"}
WIKI_PATHS = {"wiki.index", "wiki.manifest", "wiki.skip_dirs", "zotero.export_dir", "images.manifest",
              "images.gallery", "images.gallery_dir", "images.library_page", "images.criteria_page"}
OPTIONAL = {"audit.baseline", "images.library_page", "images.criteria_page"}
MODES = ("none", "local-api")


def fail(source: Path | str, message: str) -> None:
    raise SystemExit(f"living-wiki config error ({source}): {message}")


def check(source: Path | str, name: str, value, default) -> None:
    if isinstance(default, list):
        kind = type(default[0]) if default else str
        ok = isinstance(value, list) and all(type(x) is kind for x in value)
        expected = "a list of integers" if kind is int else "a list of strings"
    else:
        ok = type(value) is type(default)
        expected = {bool: "true or false", int: "an integer", str: "a string"}[type(default)]
    if not ok:
        fail(source, f"{name} must be {expected}, got {value!r}")


def load(root: Path, config: Path | None = None) -> dict:
    root = root.resolve()
    path = config or root / "living-wiki.toml"
    user: dict = {}
    if path.is_file():
        try:
            user = tomllib.loads(path.read_text())
        except tomllib.TOMLDecodeError as error:
            fail(path, f"invalid TOML: {error}")
    elif config:
        fail(path, "file not found")
    source = path if path.is_file() else "defaults"
    for section, values in user.items():
        if section not in DEFAULTS:
            fail(source, f"unknown section [{section}]; expected one of {', '.join(DEFAULTS)}")
        if not isinstance(values, dict):
            fail(source, f"[{section}] must be a table")
        for key in values:
            if key not in DEFAULTS[section]:
                fail(source, f"unknown key {section}.{key}; expected one of {', '.join(DEFAULTS[section])}")
    cfg: dict = {"root": root, "config": path if path.is_file() else None}
    for section, defaults in DEFAULTS.items():
        cfg[section] = {}
        for key, default in defaults.items():
            value = user.get(section, {}).get(key, default)
            check(source, f"{section}.{key}", value, default)
            cfg[section][key] = value
    if cfg["zotero"]["mode"] not in MODES:
        fail(source, f"zotero.mode must be one of {', '.join(MODES)}, got {cfg['zotero']['mode']!r}")
    size = cfg["images"]["thumbnail_size"]
    if len(size) != 2 or min(size) < 1:
        fail(source, f"images.thumbnail_size must be [width, height] in pixels, got {size!r}")
    if cfg["images"]["max_references"] < 0:
        fail(source, "images.max_references must not be negative")
    wiki = root / cfg["wiki"]["dir"]
    for names, base in ((REPO_PATHS, root), (WIKI_PATHS, wiki)):
        for name in names:
            section, key = name.split(".")
            value = cfg[section][key]
            if isinstance(value, list):
                cfg[section][key] = [base / x for x in value]
            else:
                cfg[section][key] = None if name in OPTIONAL and not value else base / value
    # Unset image scan roots default to the raw roots plus the wiki itself.
    cfg["images"]["scan_roots"] = cfg["images"]["scan_roots"] or [*cfg["wiki"]["raw_roots"], wiki]
    cfg["images"]["thumbnail_size"] = tuple(size)
    return cfg
