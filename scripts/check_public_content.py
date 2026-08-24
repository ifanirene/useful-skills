#!/usr/bin/env python3
"""Flag common secrets and private machine context in repository text files."""

from __future__ import annotations

import configparser
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".local", ".venv", "venv", "__pycache__"}
SKIP_FILES = {".DS_Store", "check_public_content.py"}
TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".css",
    ".html",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "assigned secret": re.compile(
        r"(?im)^\s*['\"]?(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)"
        r"['\"]?\s*[:=]\s*['\"][^'\"<{][^'\"]{7,}['\"]\s*,?\s*(?:#.*)?$"
    ),
    "private IPv4 address": re.compile(
        r"(?<![\d.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
        r"192\.168\.\d{1,3}\.\d{1,3}|"
        r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![\d.])"
    ),
    "personal home path": re.compile(r"/(?:Users|home)/([A-Za-z0-9._-]+)"),
}


def submodule_roots() -> set[Path]:
    gitmodules = REPO / ".gitmodules"
    if not gitmodules.is_file():
        return set()
    parser = configparser.ConfigParser()
    parser.read(gitmodules, encoding="utf-8")
    roots: set[Path] = set()
    for section in parser.sections():
        path_string = parser.get(section, "path", fallback="").strip()
        if path_string:
            roots.add(Path(path_string))
    return roots


def inside_submodule(relative: Path, roots: set[Path]) -> bool:
    return any(relative == root or root in relative.parents for root in roots)


def candidate_files() -> list[Path]:
    paths: list[Path] = []
    roots = submodule_roots()
    for path in REPO.rglob("*"):
        relative = path.relative_to(REPO)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if inside_submodule(relative, roots):
            continue
        if not path.is_file() or path.name in SKIP_FILES:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            paths.append(path)
    return sorted(paths)


def main() -> int:
    findings: list[str] = []
    for path in candidate_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                if label == "personal home path" and match.group(1) in {
                    "...",
                    "USERNAME",
                    "yourname",
                }:
                    continue
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{path.relative_to(REPO)}:{line}: possible {label}")

    roots = submodule_roots()
    symlinks = [
        path.relative_to(REPO)
        for path in REPO.rglob("*")
        if ".git" not in path.relative_to(REPO).parts
        and not inside_submodule(path.relative_to(REPO), roots)
        and path.is_symlink()
    ]
    findings.extend(f"{path}: repository symlink requires review" for path in symlinks)

    if findings:
        for finding in findings:
            print(f"ERROR: {finding}", file=sys.stderr)
        print("Automated findings require manual review; do not publish yet.", file=sys.stderr)
        return 1

    print(f"Public-content scan OK: {len(candidate_files())} text files checked")
    print("Manual semantic privacy review is still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
