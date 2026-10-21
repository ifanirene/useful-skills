"""Exercise the config-driven wiki tools on disposable fixtures; no network."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import parse_qs, urlsplit

import pytest

import wikiconf
import wiki_zotero
from wiki_audit import audit, main as audit_main
from wiki_images import audit_images, checksum, gallery_documents, image_embed, render_thumbnails, thumbnail_path
from wiki_zotero import doi_occurrences

SCRIPTS = Path(__file__).resolve().parent


def configure(root: Path, toml: str | None = None) -> dict:
    if toml is not None:
        (root / "living-wiki.toml").write_text(toml)
    return wikiconf.load(root)


def setup_wiki(tmp_path: Path) -> Path:
    (tmp_path / "resources").mkdir(parents=True, exist_ok=True)
    (tmp_path / "wiki/sources").mkdir(parents=True, exist_ok=True)
    (tmp_path / "wiki/references").mkdir(exist_ok=True)
    source = tmp_path / "resources/source (copy).md"
    source.write_text("Original evidence")
    manifest = {"files": [{"path": "resources/source (copy).md", "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                            "source_id": "SRC-TEST", "note": "sources/test.md", "status": "ingested", "coverage": "Complete text"}]}
    (tmp_path / "wiki/source-manifest.json").write_text(json.dumps(manifest))
    (tmp_path / "wiki/index.md").write_text("[Source](sources/test.md)")
    (tmp_path / "wiki/sources/test.md").write_text(
        "---\nid: SRC-TEST\ntype: source\n---\n[Original](../../resources/source%20%28copy%29.md)\n[Index](../index.md)")
    (tmp_path / "wiki/references/zotero-items.json").write_text('{"items": [{"key": "ABCDEFGH"}]}')
    return tmp_path


# Source audit and DOI scan.


def test_pdf_scan_respects_selected_pages(tmp_path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    path = tmp_path / "source.pdf"
    with fitz.open() as doc:
        doc.new_page().insert_text((72, 72), "10.1000/excluded")
        doc.new_page().insert_text((72, 72), "10.1000/selected")
        doc.save(path)
    manifest = {"files": [{"path": "source.pdf", "source_id": "SRC-TEST", "pdf_pages": [2]}]}
    found, warnings = doi_occurrences(configure(tmp_path), manifest)
    assert set(found) == {"10.1000/selected"}
    assert found["10.1000/selected"][0]["locator"] == "PDF page 2"
    assert warnings == []


def test_source_drift_is_detected_not_accepted(tmp_path: Path) -> None:
    root = setup_wiki(tmp_path)
    assert not audit(configure(root))["errors"]
    source = root / "resources/source (copy).md"
    source.write_text("Revised evidence")
    before = (root / "wiki/source-manifest.json").read_bytes()
    (root / "resources/new.md").write_text("New input")
    result = audit(configure(root))
    assert any("Source changed" in x for x in result["errors"])
    assert any("Unregistered resource" in x for x in result["errors"])
    assert (root / "wiki/source-manifest.json").read_bytes() == before


def test_broken_orphan_and_unverified_key_are_reported(tmp_path: Path) -> None:
    root = setup_wiki(tmp_path)
    (root / "wiki/sources/test.md").write_text("[Missing](absent.md) [Unverified](zotero://select/library/items/UNKNOWN1)")
    (root / "wiki/orphan.md").write_text("Detached source")
    result = audit(configure(root))
    assert any("Broken link" in x for x in result["errors"])
    assert any("UNKNOWN1" in x for x in result["errors"])
    assert any("orphan.md" in x for x in result["warnings"])


def test_code_samples_are_not_treated_as_links(tmp_path: Path) -> None:
    root = setup_wiki(tmp_path)
    with (root / "wiki/sources/test.md").open("a") as handle:
        handle.write("\n```md\n[Example](nonexistent.md)\n```\n")
    assert not audit(configure(root))["errors"]


def test_doi_scan_preserves_parentheses_and_stops_at_markup(tmp_path: Path) -> None:
    root = setup_wiki(tmp_path)
    (root / "resources/source (copy).md").write_text(
        "[Paper](https://doi.org/10.1000/S0000-0000(15)00000-0) "
        r"\href{https://doi.org/10.1000/j.test.2025.02.005}{Title} "
        "[10.5555/example.2025.3242][reference]"
        " Project record https://doi.org/10.9999/123456789"
    )
    manifest = json.loads((root / "wiki/source-manifest.json").read_text())
    expected = {"10.1000/s0000-0000(15)00000-0", "10.1000/j.test.2025.02.005", "10.5555/example.2025.3242"}
    found, _ = doi_occurrences(configure(root), manifest)
    assert set(found) == expected | {"10.9999/123456789"}
    found, _ = doi_occurrences(configure(root, '[zotero]\nexclude_doi_prefixes = ["10.9999/"]'), manifest)
    assert set(found) == expected


def test_doi_scan_warns_about_and_skips_missing_sources(tmp_path: Path) -> None:
    root = setup_wiki(tmp_path)
    (root / "resources/source (copy).md").write_text("See https://doi.org/10.1000/present.")
    manifest = json.loads((root / "wiki/source-manifest.json").read_text())
    manifest["files"].append({"path": "resources/absent.pdf", "source_id": "SRC-ABSENT"})
    found, warnings = doi_occurrences(configure(root), manifest)
    assert set(found) == {"10.1000/present"}
    assert warnings == ["Missing source skipped in DOI scan: resources/absent.pdf"]


def test_source_note_frontmatter_must_carry_manifest_id(tmp_path: Path) -> None:
    root = setup_wiki(tmp_path)
    note = root / "wiki/sources/test.md"
    text = note.read_text()
    for header in ("id: SRC-TEST", "source_id: SRC-TEST", 'source_id: "SRC-TEST"'):
        note.write_text(text.replace("id: SRC-TEST", header))
        assert audit(configure(root))["warnings"] == []
    note.write_text(text.replace("id: SRC-TEST", "id: SRC-OTHER"))
    assert audit(configure(root))["warnings"] == ["Source note frontmatter lacks source_id/id SRC-TEST: sources/test.md"]


def test_configured_exclusions_need_no_registration_or_link_checks(tmp_path: Path) -> None:
    root = setup_wiki(tmp_path)
    (root / "resources/archive").mkdir()
    (root / "resources/archive/old.zip").write_bytes(b"archived")
    (root / "resources/.cache").write_text("hidden files are never registered")
    (root / "wiki/evidence").mkdir()
    (root / "wiki/evidence/extraction.md").write_text("[Page 3](missing.md)")
    assert audit(configure(root))["errors"] == ["Unregistered resource: resources/archive/old.zip"]
    assert audit(configure(root, '[wiki]\nignore = ["resources/archive/*"]'))["errors"] == []


def test_config_defaults_and_validation(tmp_path: Path) -> None:
    cfg = wikiconf.load(tmp_path)
    root = cfg["root"]
    assert cfg["config"] is None and cfg["zotero"]["mode"] == "none" and not cfg["images"]["enabled"]
    assert cfg["wiki"]["manifest"] == root / "wiki/source-manifest.json"
    assert cfg["zotero"]["export_dir"] == root / "wiki/references"
    assert cfg["images"]["scan_roots"] == [root / "resources", root / "wiki"]
    assert cfg["audit"]["baseline"] is None
    for text, message in [
        ('[wiki]\nraw_roots = "resources"', "wiki.raw_roots must be a list of strings"),
        ("[wiki]\nrawroots = []", "unknown key wiki.rawroots"),
        ("[wikis]\n", "unknown section"),
        ('[zotero]\nmode = "web"', "zotero.mode must be one of"),
        ("[images]\nthumbnail_size = [300]", "thumbnail_size"),
        ("[images]\nenabled = 1", "images.enabled must be true or false"),
        ("[wiki\n", "invalid TOML"),
    ]:
        (tmp_path / "living-wiki.toml").write_text(text)
        with pytest.raises(SystemExit, match=message):
            wikiconf.load(tmp_path)
    with pytest.raises(SystemExit, match="file not found"):
        wikiconf.load(tmp_path, tmp_path / "absent.toml")


def test_baseline_separates_known_from_new_errors(tmp_path: Path, capsys) -> None:
    root = setup_wiki(tmp_path)
    (root / "resources/known.md").write_text("Accepted gap")
    baseline = root / "wiki/audit-baseline.json"
    with pytest.raises(SystemExit) as stop:
        audit_main(["--root", str(root), "--write-baseline", str(baseline)])
    assert stop.value.code == 0
    assert json.loads(baseline.read_text()) == {"known_errors": ["Unregistered resource: resources/known.md"]}
    capsys.readouterr()
    (root / "resources/new.md").write_text("Unreviewed")
    with pytest.raises(SystemExit) as stop:
        audit_main(["--root", str(root), "--baseline", str(baseline)])
    report = json.loads(capsys.readouterr().out)
    assert stop.value.code == 1
    assert "errors" not in report
    assert report["known_errors"] == ["Unregistered resource: resources/known.md"]
    assert report["new_errors"] == ["Unregistered resource: resources/new.md"]
    (root / "resources/new.md").unlink()
    configure(root, '[audit]\nbaseline = "wiki/audit-baseline.json"')
    with pytest.raises(SystemExit) as stop:
        audit_main(["--root", str(root)])
    assert stop.value.code == 0
    assert json.loads(capsys.readouterr().out)["new_errors"] == []
    configure(root, "")
    with pytest.raises(SystemExit) as stop:
        audit_main(["--root", str(root)])
    assert stop.value.code == 1


def test_stub_prints_pending_manifest_rows(tmp_path: Path, capsys) -> None:
    root = setup_wiki(tmp_path)
    (root / "resources/new.md").write_text("New input")
    audit_main(["--root", str(root), "--stub", "resources/new.md"])
    rows = json.loads(capsys.readouterr().out)
    assert rows == [{"path": "resources/new.md", "sha256": hashlib.sha256(b"New input").hexdigest(),
                     "bytes": 9, "status": "pending"}]
    manifest = json.loads((root / "wiki/source-manifest.json").read_text())
    manifest["files"] += rows
    (root / "wiki/source-manifest.json").write_text(json.dumps(manifest))
    result = audit(configure(root))
    assert result["errors"] == ["Source lacks note: resources/new.md"]
    assert "Reading/integration status pending: resources/new.md" in result["warnings"]
    with pytest.raises(SystemExit, match="Not a file"):
        audit_main(["--root", str(root), "--stub", "resources/absent.md"])


# Zotero view, against a fake local API.


def test_zotero_refresh_is_disabled_by_default(tmp_path: Path, capsys) -> None:
    wiki_zotero.main(["--root", str(tmp_path)])
    assert "disabled" in capsys.readouterr().out


def test_zotero_refresh_links_exports_and_survives_missing_source(tmp_path: Path, monkeypatch) -> None:
    root = setup_wiki(tmp_path)
    (root / "resources/source (copy).md").write_text("Cites 10.1000/matched and 10.1000/unknown.")
    manifest = json.loads((root / "wiki/source-manifest.json").read_text())
    manifest["files"].append(dict(manifest["files"][0], path="resources/absent.md", source_id="SRC-ABSENT"))
    (root / "wiki/source-manifest.json").write_text(json.dumps(manifest))

    def item(key: str, collections: list[str], doi: str, kind: str = "journalArticle") -> dict:
        return {"key": key, "data": {"itemType": kind, "title": f"Title {key}", "DOI": doi, "date": "2025",
                                     "collections": collections, "creators": [{"firstName": "A", "lastName": "Author"}]}}

    library = [item("COLLITEM", ["ROOTCOLL"], ""), item("DOIMATCH", [], "10.1000/matched"),
               item("WEBPAGE1", ["ROOTCOLL"], "", "webpage")]

    def fake_urlopen(url: str, timeout: int) -> io.BytesIO:
        parts = urlsplit(url)
        query = parse_qs(parts.query)
        if parts.path.endswith("/items/top"):
            body = json.dumps(library if query["start"] == ["0"] else [])
        elif parts.path.endswith("/collections"):
            body = "[]"
        else:
            body = "\n".join(f"@article{{{key},\n}}" for key in query["itemKey"][0].split(","))
        return io.BytesIO(body.encode())

    monkeypatch.setattr(wiki_zotero, "urlopen", fake_urlopen)
    cfg = configure(root, '[zotero]\nmode = "local-api"\nroot_collection = "ROOTCOLL"\nexclude_item_types = ["webpage"]')
    assert wiki_zotero.refresh(cfg) == {"collection_items": 1, "exported_items": 2, "doi_candidates": 2, "unresolved": 1,
                                        "warnings": ["Missing source skipped in DOI scan: resources/absent.md"]}
    out = root / "wiki/references"
    assert [x["key"] for x in json.loads((out / "zotero-items.json").read_text())["items"]] == ["COLLITEM", "DOIMATCH"]
    assert "[SRC-TEST: document](../../resources/source%20%28copy%29.md)" in (out / "reconciliation.md").read_text()
    assert "README.md" not in (out / "catalog.md").read_text()
    assert not [x for x in audit(cfg)["errors"] if "Broken link" in x or "Zotero key" in x]


# Image registry and gallery.


def image_fixture(root: Path) -> tuple[dict, Path]:
    (root / "resources").mkdir(parents=True, exist_ok=True)
    (root / "wiki/sources").mkdir(parents=True, exist_ok=True)
    source = root / "resources/source.pdf"
    source.write_bytes(b"unchanged source fixture")
    image = root / "resources/image.png"
    image.write_bytes(b"image fixture")
    (root / "wiki/sources/paper.md").write_text("Source account")
    data = {
        "updated": "2026-01-01",
        "groups": {"paper": {"title": "Paper", "use": "Assay design", "source_note": "wiki/sources/paper.md"}},
        "images": [
            {
                "id": "IMG-TEST",
                "path": "resources/image.png",
                "sha256": checksum(image),
                "title": "Figure 1",
                "group": "paper",
                "role": "reference",
                "visual_kind": "conceptual-schematic",
                "selection_reason": "A compact overview connects the assay and biological compartment.",
                "source_id": "SRC-PAPER",
                "source_path": "resources/source.pdf",
                "source_sha256": checksum(source),
                "source_note": "wiki/sources/paper.md",
                "locator": "Figure 1",
                "derivation": "Test fixture",
            }
        ],
    }
    registry = root / "wiki/image-manifest.json"
    registry.write_text(json.dumps(data))
    cfg = configure(root, "[images]\nenabled = true\n")
    for path, body in gallery_documents(cfg, data).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
    return cfg, registry


def test_new_and_changed_images_are_reported_without_accepting_hashes(tmp_path: Path) -> None:
    cfg, registry = image_fixture(tmp_path)
    assert audit_images(cfg)["errors"] == []
    before = registry.read_bytes()
    (tmp_path / "resources/image.png").write_bytes(b"changed image")
    (tmp_path / "resources/new.jpg").write_bytes(b"new image")
    errors = audit_images(cfg)["errors"]
    assert any("Image changed" in e for e in errors)
    assert any("Unregistered image" in e for e in errors)
    assert registry.read_bytes() == before


def test_source_drift_and_stale_gallery_are_reported(tmp_path: Path) -> None:
    cfg, _ = image_fixture(tmp_path)
    (tmp_path / "resources/source.pdf").write_bytes(b"changed source")
    (tmp_path / "wiki/sources/images.md").write_text("Stale gallery")
    errors = audit_images(cfg)["errors"]
    assert any("Image source changed" in e for e in errors)
    assert any("Gallery needs rendering" in e for e in errors)


def test_missing_image_and_invalid_duplicate_are_reported(tmp_path: Path) -> None:
    cfg, registry = image_fixture(tmp_path)
    data = json.loads(registry.read_text())
    data["images"][0]["duplicate_of"] = "missing.png"
    registry.write_text(json.dumps(data))
    (tmp_path / "resources/image.png").unlink()
    errors = audit_images(cfg)["errors"]
    assert any("Missing image:" in e for e in errors)
    assert any("Invalid duplicate" in e for e in errors)


def test_supporting_images_remain_registered_without_entering_gallery(tmp_path: Path) -> None:
    cfg, registry = image_fixture(tmp_path)
    data = json.loads(registry.read_text())
    archived = tmp_path / "resources/complete-results.png"
    archived.write_bytes(b"complete result sheet retained for evidence")
    row = dict(data["images"][0])
    row.update(id="IMG-ARCHIVE", path="resources/complete-results.png",
               sha256=checksum(archived), role="supporting", title="Complete result sheet")
    row.pop("selection_reason")
    row.pop("visual_kind")
    data["images"].append(row)
    registry.write_text(json.dumps(data))
    documents = gallery_documents(cfg, data)
    for path, body in documents.items():
        path.write_text(body)
        assert "complete-results.png" not in body
        assert "Complete result sheet" not in body
        assert "Complete file inventory" not in body
    assert audit_images(cfg)["errors"] == []
    assert archived.exists()


def test_unreviewed_reference_is_flagged_and_not_displayed(tmp_path: Path) -> None:
    cfg, registry = image_fixture(tmp_path)
    data = json.loads(registry.read_text())
    del data["images"][0]["selection_reason"]
    registry.write_text(json.dumps(data))
    documents = gallery_documents(cfg, data)
    assert len(documents) == 1  # No collection page without a deliberate selection.
    assert "resources/image.png" not in next(iter(documents.values()))
    assert any("lacks selection reason" in error for error in audit_images(cfg)["errors"])


def test_portable_previews_preserve_original_and_fit_bounds(tmp_path: Path) -> None:
    Image = pytest.importorskip("PIL.Image")
    cfg, registry = image_fixture(tmp_path)
    data = json.loads(registry.read_text())
    row = data["images"][0]
    original = tmp_path / row["path"]
    Image.new("RGBA", (600, 1200), (255, 0, 0, 0)).save(original)
    original_bytes = original.read_bytes()
    render_thumbnails(cfg, data)
    with Image.open(thumbnail_path(cfg, row)) as preview:
        assert preview.size == (110, 220)
        assert preview.getpixel((0, 0)) == (255, 255, 255)
    assert original.read_bytes() == original_bytes
    embed = image_embed(cfg, tmp_path / "wiki/sources/images.md", row, preview=True)
    assert embed.startswith("[![")
    assert "<img" not in embed and "<a" not in embed
    assert embed.endswith("](../../resources/image.png)")


def test_gallery_layout_and_limits_follow_config(tmp_path: Path) -> None:
    _, registry = image_fixture(tmp_path)
    cfg = configure(tmp_path, '[images]\nenabled = true\ngallery = "gallery.md"\ngallery_dir = "gallery"\n'
                              'criteria_page = "AGENTS.md#images"\nthumbnail_size = [120, 90]\nmax_references = 0\n')
    documents = gallery_documents(cfg, json.loads(registry.read_text()))
    central = documents[cfg["root"] / "wiki/gallery.md"]
    assert "Previews fit within 120 × 90 pixels" in central
    assert "[Selection criteria](AGENTS.md#images)" in central and "Source library" not in central
    assert "](gallery/paper.md)**" in central
    assert "[Illustration gallery](../gallery.md)" in documents[cfg["root"] / "wiki/gallery/paper.md"]
    assert "More than 0 gallery images need a specific justification: paper" in audit_images(cfg)["errors"]


def test_audit_imports_image_checks_from_any_directory(tmp_path: Path) -> None:
    root = setup_wiki(tmp_path / "repo")
    image_fixture(root)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    run = subprocess.run([sys.executable, "-I", "-B", str(SCRIPTS / "wiki_audit.py"), "--root", str(root)],
                         cwd=elsewhere, capture_output=True, text=True, check=False)
    assert run.stderr == ""
    result = json.loads(run.stdout)
    assert result["registered_images"] == 1
    assert "Unregistered resource: resources/image.png" in result["errors"]
