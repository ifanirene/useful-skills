"""Read-only checks for wiki coverage, provenance and links, configured by living-wiki.toml."""

from __future__ import annotations

import argparse
from collections import deque
from fnmatch import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))  # Sibling modules, from any working directory.
import wikiconf  # noqa: E402


def without_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def frontmatter(text: str) -> dict:
    match = re.match(r"---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    pairs = re.findall(r"(?m)^([\w-]+):(.*)$", match.group(1)) if match else []
    return {key: value.strip().strip("\"'") for key, value in pairs}


def audit(cfg: dict) -> dict:
    root, conf = cfg["root"], cfg["wiki"]
    wiki = conf["dir"]
    errors, warnings = [], []
    if conf["manifest"].is_file():
        manifest = json.loads(conf["manifest"].read_text())
    else:
        manifest = {"files": []}
        errors.append(f"Source manifest is absent: {os.path.relpath(conf['manifest'], root)}")
    entries = manifest["files"]
    registered = {x["path"] for x in entries}
    if len(registered) != len(entries):
        errors.append("Duplicate source paths in manifest")
    current = set()
    for folder in conf["raw_roots"]:
        if not folder.is_dir():
            warnings.append(f"Raw root does not exist: {os.path.relpath(folder, root)}")
        current |= {p.relative_to(root).as_posix() for p in folder.rglob("*") if p.is_file() and not any(x.startswith(".") for x in p.relative_to(folder).parts)}
    current = {x for x in current if not any(fnmatch(x, pattern) for pattern in conf["ignore"])}
    for name in sorted(current - registered):
        errors.append(f"Unregistered resource: {name}")
    for row in entries:
        source = root / row["path"]
        if not source.exists():
            errors.append(f"Missing source: {row['path']}")
        elif hashlib.sha256(source.read_bytes()).hexdigest() != row["sha256"]:
            errors.append(f"Source changed; reread before accepting hash: {row['path']}")
        if not row.get("note"):
            errors.append(f"Source lacks note: {row['path']}")
        elif not (wiki / row["note"]).is_file():
            errors.append(f"Missing source note: {row['note']}")
        else:
            meta = frontmatter((wiki / row["note"]).read_text())
            if row.get("source_id") not in (meta.get("source_id"), meta.get("id")):
                warnings.append(f"Source note frontmatter lacks source_id/id {row.get('source_id')}: {row['note']}")
        if row.get("status") != "ingested":
            warnings.append(f"Reading/integration status {row.get('status')}: {row['path']}")
        if row.get("status") == "ingested" and not row.get("coverage"):
            errors.append(f"Ingested source lacks coverage record: {row['path']}")
    pages = {x.resolve() for x in wiki.rglob("*.md") if not any(x.is_relative_to(d) for d in conf["skip_dirs"])}
    edges = {x: set() for x in pages}
    zotero_file = cfg["zotero"]["export_dir"] / "zotero-items.json"
    keys = {x["key"] for x in json.loads(zotero_file.read_text())["items"]} if zotero_file.exists() else set()
    for page in sorted(pages):
        text = without_code(page.read_text())
        for key in re.findall(r"zotero://select/library/items/([A-Z0-9]+)", text):
            if key not in keys:
                errors.append(f"Zotero key absent from verified export: {key} in {page.relative_to(wiki)}")
        for match in re.finditer(r"!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)", text):
            target = match.group(1).strip("<>")
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            path = (page.parent / unquote(parts.path)).resolve()
            if not path.exists():
                errors.append(f"Broken link: {page.relative_to(wiki)} -> {target}")
            if path in pages:
                edges[page].add(path)
    start = conf["index"].resolve()
    visited, queue = set(), deque([start])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        queue.extend(edges.get(node, set()) - visited)
    for page in sorted(pages - visited):
        warnings.append(f"Unreachable from index: {page.relative_to(wiki)}")
    image_count = 0
    if cfg["images"]["enabled"]:
        from wiki_images import audit_images
        image_result = audit_images(cfg)
        image_count = image_result["registered_images"]
        errors.extend(image_result["errors"])
        warnings.extend(image_result["warnings"])
    return {"registered_images": image_count, "registered_files": len(entries), "resource_files": len(current),
            "unique_source_hashes": len({x['sha256'] for x in entries}), "wiki_pages": len(pages),
            "verified_zotero_items": len(keys), "errors": errors, "warnings": warnings,
            "scope": "Mechanical checks only; scientific interpretation requires source review."}


def stubs(root: Path, names: list[str]) -> list[dict]:
    rows = []
    for name in names:
        path = root / name
        if not path.is_file():
            raise SystemExit(f"Not a file: {name}")
        data = path.read_bytes()
        rows.append({"path": Path(os.path.relpath(path, root)).as_posix(), "sha256": hashlib.sha256(data).hexdigest(),
                     "bytes": len(data), "status": "pending"})
    return rows


def with_baseline(result: dict, path: Path, root: Path) -> dict:
    if not path.is_file():
        raise SystemExit(f"Baseline not found: {path}; create it with --write-baseline")
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or not isinstance(data.get("known_errors"), list):
        raise SystemExit(f"Baseline must be a JSON object with a known_errors list: {path}")
    known, errors = set(data["known_errors"]), result.pop("errors")
    return {**result, "baseline": os.path.relpath(path, root), "known_errors": [x for x in errors if x in known],
            "new_errors": [x for x in errors if x not in known]}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory)")
    parser.add_argument("--config", type=Path, help="Configuration file (default: ROOT/living-wiki.toml)")
    parser.add_argument("--report", type=Path, help="Optional output JSON; source and wiki content remain read-only")
    parser.add_argument("--baseline", type=Path, metavar="FILE", help="Accepted known errors; overrides [audit] baseline")
    parser.add_argument("--write-baseline", type=Path, metavar="FILE", help="Record the current errors as accepted known errors")
    parser.add_argument("--stub", nargs="+", metavar="PATH", help="Print manifest stubs for repo-relative files and exit")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.stub:
        print(json.dumps(stubs(root, args.stub), indent=2, ensure_ascii=False))
        return
    cfg = wikiconf.load(root, args.config)
    result = audit(cfg)
    if args.write_baseline:
        args.write_baseline.parent.mkdir(parents=True, exist_ok=True)
        args.write_baseline.write_text(json.dumps({"known_errors": sorted(set(result["errors"]))}, indent=2, ensure_ascii=False) + "\n")
    baseline = args.write_baseline or args.baseline or cfg["audit"]["baseline"]
    if baseline:
        result = with_baseline(result, baseline, root)
    report = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report)
    print(report, end="")
    raise SystemExit(bool(result["new_errors"] if baseline else result["errors"]))


if __name__ == "__main__":
    main()
