"""Refresh a read-only, source-linked Zotero view for the wiki, configured by living-wiki.toml."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))  # Sibling modules, from any working directory.
import wikiconf  # noqa: E402

SCANNED = {".pdf", ".md", ".tex", ".html"}


def normalized_doi(value: str) -> str:
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value.strip(), flags=re.I)
    value = value.rstrip(".,;:]}>")
    while value.endswith(")") and value.count(")") > value.count("("):
        value = value[:-1]
    return value.lower()


def get_json(base: str, route: str) -> list:
    with urlopen(base + route, timeout=30) as response:
        return json.load(response)


def paged(base: str, route: str) -> list:
    rows = []
    for start in range(0, 100000, 100):
        batch = get_json(base, f"{route}?format=json&limit=100&start={start}")
        rows.extend(batch)
        if len(batch) < 100:
            return rows
    raise RuntimeError("Pagination did not terminate; no export written")


def doi_occurrences(cfg: dict, manifest: dict) -> tuple[dict, list[str]]:
    """Return DOI candidates with their source locations, and warnings for skipped sources."""
    occurrences: dict[str, list[dict]] = {}
    warnings: list[str] = []
    excluded = tuple(x.lower() for x in cfg["zotero"]["exclude_doi_prefixes"])
    for entry in manifest["files"]:
        path = cfg["root"] / entry["path"]
        if path.suffix.lower() not in SCANNED:
            continue
        if not path.is_file():
            warnings.append(f"Missing source skipped in DOI scan: {entry['path']}")
            continue
        if path.suffix.lower() == ".pdf":
            import fitz  # PyMuPDF is needed only when a PDF must be read.

            with fitz.open(path) as doc:
                pages = entry.get("pdf_pages", range(1, len(doc) + 1))
                chunks = [(f"PDF page {i}", doc[i - 1].get_text()) for i in pages]
        else:
            chunks = [("document", path.read_text())]
        for locator, text in chunks:
            text = html.unescape(text).replace("\\/", "/")
            for match in re.finditer(r"10\.\d{4,9}/[^\s<>\"'\\\[\]{}]+", text, re.I):
                doi = normalized_doi(match.group())
                if doi.startswith(excluded):
                    continue  # Configured non-bibliographic identifiers, such as project records.
                record = {"path": entry["path"], "source_id": entry.get("source_id") or entry["path"], "locator": locator}
                if record not in occurrences.setdefault(doi, []):
                    occurrences[doi].append(record)
    return occurrences, warnings


def clean_title(value: str) -> str:
    return re.sub(r"<[^>]+>", "", html.unescape(value)).replace("\n", " ").replace("|", "\\|")


def refresh(cfg: dict) -> dict:
    root, conf = cfg["root"], cfg["zotero"]
    base, collection = conf["api_base"].rstrip("/"), conf["root_collection"]
    manifest = json.loads(cfg["wiki"]["manifest"].read_text())
    excluded_types = set(conf["exclude_item_types"])
    all_items = [item for item in paged(base, "/items/top") if item["data"].get("itemType") not in excluded_types]
    collections = paged(base, "/collections")
    collection_keys = {collection}
    for _ in range(len(collections) + 1):
        previous = len(collection_keys)
        collection_keys.update(c["key"] for c in collections if c["data"].get("parentCollection") in collection_keys)
        if len(collection_keys) == previous:
            break
    in_collection = [x for x in all_items if set(x["data"].get("collections", [])) & collection_keys]
    if not in_collection:
        raise RuntimeError("Root collection is empty or unavailable; previous export preserved")
    by_doi: dict[str, list[dict]] = {}
    for item in all_items:
        doi = normalized_doi(item["data"].get("DOI", ""))
        if doi:
            by_doi.setdefault(doi, []).append(item)
    candidates, warnings = doi_occurrences(cfg, manifest)
    matches = []
    for doi, locations in sorted(candidates.items()):
        items = by_doi.get(doi, [])
        matches.append({"doi_candidate": doi, "occurrences": locations,
                        "status": "matched" if len(items) == 1 else "ambiguous" if items else "unresolved",
                        "zotero_keys": [x["key"] for x in items]})
    selected = {x["key"]: x for x in in_collection}
    for match in matches:
        if match["status"] == "matched":
            item = by_doi[match["doi_candidate"]][0]
            selected[item["key"]] = item
    items = sorted(selected.values(), key=lambda x: clean_title(x["data"].get("title", "")).lower())
    bibtex = []
    for offset in range(0, len(items), 50):
        keys = ",".join(x["key"] for x in items[offset:offset + 50])
        query = urlencode({"itemKey": keys, "format": "bibtex", "limit": 100})
        with urlopen(base + "/items?" + query, timeout=30) as response:
            bibtex.append(response.read().decode())
    combined_bibtex = "\n".join(bibtex)
    bib_count = len(re.findall(r"(?m)^@\w+\{", combined_bibtex))
    if bib_count != len(items):
        raise RuntimeError(f"BibTeX export mismatch: {bib_count} entries for {len(items)} items")
    checked = datetime.now(timezone.utc).isoformat()
    snapshot = {"checked": checked, "api": "Zotero Desktop local API", "library": base.rsplit("/api/", 1)[-1],
                "collection_key": collection, "collection_count": len(in_collection),
                "scope": "Root collection and exact DOI matches cited in registered sources", "items": items}
    out = conf["export_dir"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "zotero-items.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    (out / "references.bib").write_text(combined_bibtex)
    (out / "source-doi-map.json").write_text(json.dumps(matches, ensure_ascii=False, indent=2) + "\n")
    readme = ["[Reference workflow](README.md)"] if (out / "README.md").is_file() else []
    index = f"[Wiki index]({quote(os.path.relpath(cfg['wiki']['index'], out), safe='/#-._~')})"
    catalog = ["---", "type: reference-index", f"updated: {checked[:10]}", "---", "# Zotero reference catalog", "",
               " · ".join([*readme, "[Reconciliation](reconciliation.md)", index]), "",
               f"Read-only export checked {checked}. {len(in_collection)} root-collection records; {len(items)} total records including additional exact DOI matches from this library. Metadata linkage does not establish full-text access or verify scientific claims.", ""]
    key_sources: dict[str, set[str]] = {}
    for match in matches:
        for key in match["zotero_keys"]:
            key_sources.setdefault(key, set()).update(x["source_id"] for x in match["occurrences"])
    for item in items:
        data, key = item["data"], item["key"]
        authors = "; ".join(x.get("name") or " ".join([x.get("firstName", ""), x.get("lastName", "")]).strip() for x in data.get("creators", []))
        catalog += [f"## {key}", "", f"**{clean_title(data.get('title', 'Untitled'))}**", "",
                    f"{authors}. {data.get('date', 'Date unspecified')}. {clean_title(data.get('publicationTitle', ''))}. Type: `{data.get('itemType', '')}`.", "",
                    f"[Open in Zotero](zotero://select/library/items/{key})"]
        if data.get("DOI"):
            catalog[-1] += f" · [DOI](https://doi.org/{quote(data['DOI'], safe='/()')})"
        catalog += ["", "Source links: " + ", ".join(sorted(key_sources.get(key, []))) if key in key_sources else "Included through the root collection; no literal DOI detected in the registered files.", ""]
    (out / "catalog.md").write_text("\n".join(catalog))
    unresolved = [x for x in matches if x["status"] != "matched"]
    queue = ["---", "type: reference-reconciliation", f"updated: {checked[:10]}", "---", "# Reference reconciliation", "",
             " · ".join([*readme, "[Catalog](catalog.md)", index]), "",
             f"The scan found {len(matches)} distinct DOI candidates: {len(matches)-len(unresolved)} uniquely matched in the live library and {len(unresolved)} unresolved or ambiguous. This is a literal identifier scan, not a complete bibliography parser. References given only as titles, PMIDs, URLs, images, or internal citation tokens require source-note follow-up. Line-wrapped PDF DOIs can also be incomplete.", "",
             "An unresolved row means the extracted string had no unique exact library match. It can be an absent record, a malformed/partial identifier, or a historical source artifact. Check the source before importing. No Zotero items were changed. Source ingestion is separate from primary-reference verification.", "",
             "| DOI candidate | Status | Source occurrence |", "|---|---|---|"]
    for match in unresolved:
        links = []
        for occurrence in match["occurrences"]:
            label = occurrence["source_id"] + ": " + occurrence["locator"]
            link = f"[{label}]({quote(os.path.relpath(root / occurrence['path'], out), safe='/')})"
            if link not in links:
                links.append(link)
        queue.append(f"| `{match['doi_candidate']}` | {match['status']} | {'; '.join(links)} |")
    (out / "reconciliation.md").write_text("\n".join(queue) + "\n")
    return {"collection_items": len(in_collection), "exported_items": len(items), "doi_candidates": len(matches),
            "unresolved": len(unresolved), "warnings": warnings}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory)")
    parser.add_argument("--config", type=Path, help="Configuration file (default: ROOT/living-wiki.toml)")
    args = parser.parse_args(argv)
    cfg = wikiconf.load(args.root, args.config)
    conf = cfg["zotero"]
    if conf["mode"] == "none":
        print('Zotero refresh is disabled; set [zotero] mode = "local-api" in living-wiki.toml to use it.')
        return
    if not conf["root_collection"]:
        raise SystemExit('living-wiki config error: zotero.root_collection is required when mode = "local-api"')
    try:
        result = refresh(cfg)
    except URLError as error:
        raise SystemExit(f"Zotero local API unavailable at {conf['api_base']} ({error.reason}); previous export preserved") from None
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
