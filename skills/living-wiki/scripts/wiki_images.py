"""Inventory and render the wiki's source-linked image gallery, configured by living-wiki.toml.

scan is read-only. render rebuilds gallery Markdown from reviewed registry metadata.
Neither operation silently registers files or accepts changed checksums.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from html import escape
from pathlib import Path
import sys
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))  # Sibling modules, from any working directory.
import wikiconf  # noqa: E402

EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".tif",
    ".tiff",
    ".avif",
}

VISUAL_KINDS = {"graphical-abstract", "conceptual-schematic", "key-image", "main-figure"}


def gallery_selection(rows: list[dict]) -> list[dict]:
    """Display only deliberate selections, never the complete file inventory."""
    return [
        row for row in rows
        if row.get("role") == "reference"
        and not row.get("duplicate_of")
        and row.get("selection_reason")
        and row.get("visual_kind") in VISUAL_KINDS
    ]


def image_paths(cfg: dict) -> set[str]:
    return {
        p.relative_to(cfg["root"]).as_posix()
        for folder in cfg["images"]["scan_roots"]
        for p in folder.rglob("*")
        if p.is_file()
        and p.suffix.lower() in EXTENSIONS
        and not any(part.startswith(".") for part in p.relative_to(folder).parts)
    }


def checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_images(cfg: dict) -> dict:
    root, conf = cfg["root"], cfg["images"]
    registry_path = conf["manifest"]
    if not registry_path.exists():
        return {
            "registered_images": 0,
            "errors": [],
            "warnings": ["Image registry is absent."],
        }
    registry = json.loads(registry_path.read_text())
    records = registry["images"]
    paths = [row["path"] for row in records]
    errors, warnings = [], []
    if len(paths) != len(set(paths)):
        errors.append("Duplicate image paths in image registry")
    ids = [row["id"] for row in records]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate image IDs in image registry")
    for folder in conf["scan_roots"]:
        if not folder.is_dir():
            warnings.append(f"Image scan root does not exist: {os.path.relpath(folder, root)}")
    current = image_paths(cfg)
    errors.extend(f"Unregistered image: {p}" for p in sorted(current - set(paths)))
    by_path = {row["path"]: row for row in records}
    for row in records:
        p = root / row["path"]
        if not p.is_file():
            errors.append(f"Missing image: {row['path']}")
        elif checksum(p) != row["sha256"]:
            errors.append(f"Image changed; inspect before updating hash: {row['path']}")
        for field in (
            "source_id",
            "source_path",
            "source_note",
            "locator",
            "role",
            "title",
            "group",
            "derivation",
        ):
            if not row.get(field):
                errors.append(f"Image lacks {field}: {row['path']}")
        for field in ("source_path", "source_note", "provenance_file", "legend_path"):
            if row.get(field) and not (root / row[field]).is_file():
                errors.append(f"Missing image {field}: {row['path']} -> {row[field]}")
        if row.get("source_sha256") and (root / row["source_path"]).is_file():
            if checksum(root / row["source_path"]) != row["source_sha256"]:
                errors.append(f"Image source changed: {row['path']}")
        duplicate = row.get("duplicate_of")
        if duplicate and (
            duplicate not in by_path or by_path[duplicate]["sha256"] != row["sha256"]
        ):
            errors.append(f"Invalid duplicate relationship: {row['path']}")
        if row["group"] not in registry["groups"]:
            errors.append(f"Unknown gallery group: {row['group']}")
        if row.get("role") == "reference" and not row.get("duplicate_of"):
            if not row.get("selection_reason"):
                errors.append(f"Gallery reference lacks selection reason: {row['path']}")
            if row.get("visual_kind") not in VISUAL_KINDS:
                errors.append(f"Gallery reference lacks a valid visual kind: {row['path']}")
    limit = conf["max_references"]
    for name, group in registry["groups"].items():
        selected = gallery_selection([r for r in records if r["group"] == name])
        if len(selected) > limit and not group.get("selection_exception"):
            errors.append(f"More than {limit} gallery images need a specific justification: {name}")
    # Deterministic generation makes stale galleries detectable without rewriting them.
    for path, body in gallery_documents(cfg, registry).items():
        if not path.exists() or path.read_text() != body:
            errors.append(f"Gallery needs rendering: {path.relative_to(root)}")
    return {"registered_images": len(records), "errors": errors, "warnings": warnings}


def link(root: Path, page: Path, target: str | Path) -> str:
    return quote(os.path.relpath(root / target, page.parent), safe="/#-._~")


def thumbnail_path(cfg: dict, row: dict) -> Path:
    return cfg["images"]["thumbnail_dir"] / f"{row['id']}.png"


def render_thumbnails(cfg: dict, registry: dict) -> None:
    """Save small, white-backed derivatives; never modify reference originals."""
    from PIL import Image  # Pillow is needed only to render previews.

    for row in gallery_selection(registry["images"]):
        with Image.open(cfg["root"] / row["path"]) as original:
            image = original.convert("RGBA")
            image.thumbnail(cfg["images"]["thumbnail_size"], Image.Resampling.LANCZOS)
            background = Image.new("RGBA", image.size, "white")
            background.alpha_composite(image)
            target = thumbnail_path(cfg, row)
            target.parent.mkdir(parents=True, exist_ok=True)
            background.convert("RGB").save(target)


def image_embed(cfg: dict, page: Path, row: dict, preview: bool = False) -> str:
    target = link(cfg["root"], page, row["path"])
    if preview:
        thumbnail = link(cfg["root"], page, thumbnail_path(cfg, row))
        return f"[![{row['title']}]({thumbnail})]({target})"
    if row.get("display_background") == "white":
        return (
            f'<img src="{escape(target)}" alt="{escape(row["title"])}" '
            'style="background-color:white;max-width:100%;height:auto;">'
        )
    return f"![{row['title']}]({target})"


def nav(root: Path, page: Path, *links: tuple[str, Path | None]) -> list[str]:
    """One navigation line plus a blank line; links without a configured target are omitted."""
    line = " · ".join(f"[{label}]({link(root, page, target)})" for label, target in links if target)
    return [line, ""] if line else []


def gallery_documents(cfg: dict, registry: dict) -> dict[Path, str]:
    root, conf = cfg["root"], cfg["images"]
    documents = {}
    central = conf["gallery"]
    width, height = conf["thumbnail_size"]
    intro = [
        "---",
        "type: image-gallery",
        f"updated: {registry['updated']}",
        "---",
        "# Illustration gallery",
        "",
        *nav(root, central, ("Source library", conf["library_page"]), ("Selection criteria", conf["criteria_page"])),
        "Selected schematics, graphical abstracts and key images for future illustration briefs. Each selection explains a useful concept through its composition, anatomy or visual logic.",
        "",
        "Usually one overview per source, with a second image only when it adds a distinct idea. Follow each collection for source credit, exact panels and interpretation limits. Complete paper figures remain with their source notes and in the "
        f"[image register]({link(root, central, conf['manifest'])}).",
        "",
        f"Previews fit within {width} × {height} pixels; click an image to open the full-size original.",
        "",
        "| Reference image | Why selected |",
        "|---|---|",
    ]
    for name, group in registry["groups"].items():
        rows = [r for r in registry["images"] if r["group"] == name]
        selected = gallery_selection(rows)
        if not selected:
            continue
        path = conf["gallery_dir"] / f"{name}.md"
        body = [
            "---",
            "type: image-gallery",
            f"updated: {registry['updated']}",
            "---",
            f"# {group['title']}",
            "",
            *nav(root, path, ("Illustration gallery", central), ("Selection criteria", conf["criteria_page"])),
            group["use"],
            "",
            f"[Source account and reading limits]({link(root, path, group['source_note'])})",
            "",
        ]
        if group.get("selection_exception"):
            body.extend([f"**Selection scope:** {group['selection_exception']}", ""])
        for row in selected:
            intro.append(
                f"| {image_embed(cfg, central, row, preview=True)} | "
                f"**[{row['title']}]({link(root, central, path)})** — {group['title']}. "
                f"{row['selection_reason']} |"
            )
            body.extend(
                [
                    f"## {row['title']}",
                    "",
                    image_embed(cfg, path, row),
                    "",
                    f"**Source:** [{row['source_id']}]({link(root, path, row['source_note'])}) · {row['locator']} · `{row['id']}`",
                    "",
                    f"**Why selected:** {row['selection_reason']}",
                    "",
                    f"**Illustration use:** {row.get('use', group['use'])}",
                    "",
                    f"**Reading / limits:** {row.get('reading_status', 'See source note; this inventory is not a fresh image review.')}",
                    "",
                ]
            )
            if row.get("caution"):
                body.extend([row["caution"], ""])
            if row.get("credit"):
                body.extend([f"**Credit:** {row['credit']}", ""])
            if row.get("source_url"):
                body.extend([f"[Original web image]({row['source_url']})", ""])
            if row.get("legend_path"):
                body.extend(
                    [f"[Full legend]({link(root, path, row['legend_path'])})", ""]
                )
            if row.get("provenance_file"):
                body.extend(
                    [
                        f"[Extraction and credit record]({link(root, path, row['provenance_file'])})",
                        "",
                    ]
                )
        body.extend(
            [
                "Full figures, controls and supporting renders remain available through the source account above and the "
                f"[image register]({link(root, path, conf['manifest'])}). They are not displayed as gallery selections.",
                "",
            ]
        )
        documents[path] = "\n".join(body) + "\n"
    intro.extend(
        [
            "",
            "Use these images to brief original illustrations. Read the caption and source note before carrying a biological relationship into a new diagram; retain attribution and distinguish measured findings from hypotheses.",
            "",
        ]
    )
    documents[central] = "\n".join(intro)
    return documents


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["scan", "render"], help="scan is read-only; render rewrites previews and gallery pages, then scans")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory)")
    parser.add_argument("--config", type=Path, help="Configuration file (default: ROOT/living-wiki.toml)")
    args = parser.parse_args(argv)
    cfg = wikiconf.load(args.root, args.config)
    conf = cfg["images"]
    if not conf["enabled"]:
        print("Image registry is disabled; set [images] enabled = true in living-wiki.toml to use it.")
        return
    if args.action == "render":
        registry = json.loads(conf["manifest"].read_text())
        render_thumbnails(cfg, registry)
        documents = gallery_documents(cfg, registry)
        for name in registry["groups"]:
            path = conf["gallery_dir"] / f"{name}.md"
            if path not in documents and path.exists():
                if path.read_text().startswith("---\ntype: image-gallery\n"):
                    path.unlink()
        for path, body in documents.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
    result = audit_images(cfg)
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["errors"]))


if __name__ == "__main__":
    main()
