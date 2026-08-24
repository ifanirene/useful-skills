#!/usr/bin/env python3
"""Safely project a Skill profile into one or more Agent discovery directories."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BUILTIN_TARGETS = {
    "codex": Path.home() / ".agents" / "skills",
    "claude": Path.home() / ".claude" / "skills",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or create per-Skill links from a named profile."
    )
    parser.add_argument("--profile", required=True, help="Profile name from profiles/<name>.txt")
    parser.add_argument(
        "--agent",
        action="append",
        choices=["codex", "claude", "all"],
        default=[],
        help="Built-in Agent target; repeat as needed or use all",
    )
    parser.add_argument(
        "--target",
        action="append",
        type=Path,
        default=[],
        help="Additional absolute Agent Skill directory; repeat as needed",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create links. Without this flag the command is preview-only.",
    )
    return parser.parse_args()


def load_profile(name: str, known_skills: set[str]) -> list[str]:
    profile_path = REPO / "profiles" / f"{name}.txt"
    if not profile_path.is_file():
        raise ValueError(f"profile not found: {profile_path}")
    selected = [
        line.strip()
        for line in profile_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not selected:
        raise ValueError(f"profile is empty: {profile_path}")
    unknown = sorted(set(selected) - known_skills)
    if unknown:
        raise ValueError(f"profile contains unknown Skills: {', '.join(unknown)}")
    if len(selected) != len(set(selected)):
        raise ValueError(f"profile contains duplicate Skills: {profile_path}")
    return selected


def target_paths(args: argparse.Namespace) -> list[Path]:
    agents = set(args.agent)
    if "all" in agents:
        agents = set(BUILTIN_TARGETS)
    targets = [BUILTIN_TARGETS[name] for name in sorted(agents)]
    for target in args.target:
        if not target.is_absolute():
            raise ValueError(f"custom target must be absolute: {target}")
        targets.append(target)
    unique: list[Path] = []
    for target in targets:
        expanded = target.expanduser()
        if expanded not in unique:
            unique.append(expanded)
    if not unique:
        raise ValueError("choose at least one --agent or --target")
    return unique


def link_state(source: Path, destination: Path) -> str:
    if destination.is_symlink():
        try:
            if destination.resolve(strict=False) == source.resolve():
                return "already linked"
        except OSError:
            pass
        return "REFUSE: link points elsewhere"
    if destination.exists():
        return "REFUSE: real file or directory exists"
    return "create"


def main() -> int:
    args = parse_args()
    manifest = json.loads((REPO / "manifest.json").read_text(encoding="utf-8"))
    known_skills = {entry["name"] for entry in manifest["skills"] if entry["status"] == "active"}
    try:
        selected = load_profile(args.profile, known_skills)
        targets = target_paths(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    operations: list[tuple[Path, Path, str]] = []
    refused = False
    for target in targets:
        for name in selected:
            source = REPO / "skills" / name
            if not (source / "SKILL.md").is_file():
                print(f"ERROR: invalid source Skill: {source}", file=sys.stderr)
                return 2
            destination = target / name
            state = link_state(source, destination)
            refused = refused or state.startswith("REFUSE")
            operations.append((source, destination, state))

    for source, destination, state in operations:
        print(f"{state:38} {destination} -> {source}")

    if refused:
        print("No changes made because at least one destination is unsafe.", file=sys.stderr)
        return 1
    if not args.apply:
        print("Preview only. Re-run with --apply to create links.")
        return 0

    for source, destination, state in operations:
        if state == "create":
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(source, target_is_directory=True)
    print(f"Applied profile {args.profile!r} to {len(targets)} target(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
