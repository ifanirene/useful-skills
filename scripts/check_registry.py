#!/usr/bin/env python3
"""Validate the central Skill registry without third-party dependencies."""

from __future__ import annotations

import configparser
import json
import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {"__pycache__"}
IGNORED_NAMES = {".DS_Store"}


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid JSON from {path.relative_to(REPO)}: {exc}") from exc


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"{path.relative_to(REPO)} has no YAML frontmatter")

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        scalar = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if not scalar:
            continue
        key, value = scalar.groups()
        if value.startswith(('"', "'")) and value.endswith(value[0]):
            value = value[1:-1]
        values[key] = value
    return values


def skill_files(skill_dir: Path) -> set[str]:
    files: set[str] = set()
    for path in skill_dir.rglob("*"):
        relative = path.relative_to(skill_dir)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if path.name in IGNORED_NAMES or path.suffix in {".pyc", ".pyo"}:
            continue
        if path.is_file() or path.is_symlink():
            files.add(relative.as_posix())
    return files


def profile_names(path: Path) -> list[str]:
    names = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#"):
            names.append(line)
    return names


def submodule_records() -> dict[str, str]:
    gitmodules = REPO / ".gitmodules"
    if not gitmodules.is_file():
        return {}
    parser = configparser.ConfigParser()
    parser.read(gitmodules, encoding="utf-8")
    records: dict[str, str] = {}
    for section in parser.sections():
        path_string = parser.get(section, "path", fallback="").strip()
        url = parser.get(section, "url", fallback="").strip()
        if path_string and url:
            records[path_string] = url
    return records


def gitlink_commit(project_path: str) -> str | None:
    result = subprocess.run(
        ["git", "ls-files", "--stage", "--", project_path],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    match = re.match(r"^160000 ([0-9a-f]{40}) 0\t", result.stdout)
    return match.group(1) if match else None


def normalized_git_url(url: str) -> str:
    return url.removesuffix(".git").rstrip("/")


def main() -> int:
    errors: list[str] = []

    try:
        manifest = read_json(REPO / "manifest.json")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if manifest.get("schema_version") != 1:
        errors.append("manifest schema_version must be 1")

    repository = manifest.get("repository", {})
    repo_url = repository.get("canonical_url")
    default_branch = repository.get("default_branch")
    if not isinstance(repo_url, str) or not repo_url.startswith("https://github.com/"):
        errors.append("repository.canonical_url must be a GitHub HTTPS URL")
    if not isinstance(default_branch, str) or not default_branch:
        errors.append("repository.default_branch is required")

    policy = manifest.get("policy", {})
    if policy.get("registry_source_of_truth") != "manifest.json":
        errors.append("policy.registry_source_of_truth must be manifest.json")
    if policy.get("private_context_allowed") is not False:
        errors.append("policy.private_context_allowed must be false")
    if policy.get("promotion_requires_human_review") is not True:
        errors.append("policy.promotion_requires_human_review must be true")

    entries = manifest.get("skills")
    if not isinstance(entries, list) or not entries:
        errors.append("manifest.skills must be a non-empty list")
        entries = []

    names: list[str] = []
    paths: list[str] = []
    canonical_urls: list[str] = []
    submodules = submodule_records()
    index_text = (REPO / "skills" / "INDEX.md").read_text(encoding="utf-8")
    readme_text = (REPO / "README.md").read_text(encoding="utf-8")

    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("every manifest skill entry must be an object")
            continue

        name = entry.get("name")
        path_string = entry.get("path")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"invalid skill name: {name!r}")
            continue
        names.append(name)

        expected_path = f"skills/{name}"
        if path_string != expected_path:
            errors.append(f"{name}: path must be {expected_path!r}")
            continue
        paths.append(path_string)
        skill_dir = REPO / path_string
        if not skill_dir.is_dir():
            errors.append(f"{name}: missing directory {path_string}")
            continue

        entrypoint = entry.get("entrypoint")
        if entrypoint != "SKILL.md":
            errors.append(f"{name}: entrypoint must be SKILL.md")
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue

        try:
            metadata = frontmatter(skill_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if metadata.get("name") != name:
            errors.append(f"{name}: frontmatter name does not match directory")
        if not metadata.get("description"):
            errors.append(f"{name}: frontmatter description is required")
        if metadata.get("license") != entry.get("license"):
            errors.append(f"{name}: manifest and frontmatter licenses disagree")

        listed_files = entry.get("files")
        if not isinstance(listed_files, list) or not all(isinstance(item, str) for item in listed_files):
            errors.append(f"{name}: files must be a list of relative paths")
        else:
            actual_files = skill_files(skill_dir)
            if set(listed_files) != actual_files:
                errors.append(
                    f"{name}: files differ; manifest={sorted(listed_files)!r}, "
                    f"actual={sorted(actual_files)!r}"
                )

        if any(path.is_symlink() for path in skill_dir.rglob("*")):
            errors.append(f"{name}: canonical Skill content must not contain symlinks")

        if not isinstance(entry.get("description"), str) or not entry["description"].strip():
            errors.append(f"{name}: registry description is required")
        if entry.get("status") not in {"active", "experimental", "deprecated"}:
            errors.append(f"{name}: unsupported status {entry.get('status')!r}")
        if not isinstance(entry.get("category"), str) or not entry["category"].strip():
            errors.append(f"{name}: category is required")
        if not isinstance(entry.get("compatibility"), list) or not entry["compatibility"]:
            errors.append(f"{name}: compatibility must be a non-empty list")

        expected_url = f"{repo_url}/tree/{default_branch}/{expected_path}"
        canonical_url = entry.get("canonical_url")
        canonical_urls.append(canonical_url)
        if canonical_url != expected_url:
            errors.append(f"{name}: canonical_url must be {expected_url}")

        source = entry.get("source")
        if not isinstance(source, dict) or not source.get("type") or not source.get("provider"):
            errors.append(f"{name}: source type and provider are required")
        elif source.get("upstream_url") is None and not source.get("review_note"):
            errors.append(f"{name}: unresolved upstream source needs a review_note")
        elif source.get("type") == "adapter":
            upstream_url = source.get("upstream_url")
            upstream_commit = source.get("upstream_commit")
            project_path = source.get("project_path")
            upstream_entrypoint = source.get("upstream_entrypoint")
            if not isinstance(upstream_url, str) or not upstream_url.startswith("https://github.com/"):
                errors.append(f"{name}: adapter upstream_url must be a GitHub HTTPS URL")
            if not isinstance(upstream_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", upstream_commit):
                errors.append(f"{name}: adapter upstream_commit must be a full commit hash")
            if not isinstance(project_path, str) or not project_path.startswith("projects/"):
                errors.append(f"{name}: adapter project_path must be under projects/")
            elif project_path not in submodules:
                errors.append(f"{name}: adapter project_path is not registered in .gitmodules")
            else:
                if isinstance(upstream_url, str) and normalized_git_url(submodules[project_path]) != normalized_git_url(upstream_url):
                    errors.append(f"{name}: submodule URL disagrees with upstream_url")
                pinned_commit = gitlink_commit(project_path)
                if pinned_commit != upstream_commit:
                    errors.append(
                        f"{name}: submodule commit {pinned_commit!r} disagrees with "
                        f"upstream_commit {upstream_commit!r}"
                    )
            if not isinstance(upstream_entrypoint, str) or upstream_entrypoint.startswith("/"):
                errors.append(f"{name}: adapter upstream_entrypoint must be a relative path")
            elif isinstance(project_path, str) and not (REPO / project_path / upstream_entrypoint).is_file():
                errors.append(f"{name}: missing upstream entrypoint {project_path}/{upstream_entrypoint}")

        if f"]({name}/SKILL.md)" not in index_text:
            errors.append(f"{name}: missing linked entry in skills/INDEX.md")
        if f"skills/{name}/SKILL.md" not in readme_text:
            errors.append(f"{name}: missing linked entry in README.md")

    for label, values in (
        ("skill names", names),
        ("skill paths", paths),
        ("canonical URLs", canonical_urls),
    ):
        if len(values) != len(set(values)):
            errors.append(f"duplicate {label} in manifest")

    skills_root = REPO / "skills"
    disk_names = {
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if disk_names != set(names):
        errors.append(
            f"manifest/disk Skill sets differ; manifest={sorted(names)!r}, "
            f"disk={sorted(disk_names)!r}"
        )

    profiles = sorted((REPO / "profiles").glob("*.txt"))
    if not profiles:
        errors.append("at least one profile is required")
    for profile in profiles:
        selected = profile_names(profile)
        if len(selected) != len(set(selected)):
            errors.append(f"{profile.relative_to(REPO)} contains duplicate Skill names")
        unknown = sorted(set(selected) - set(names))
        if unknown:
            errors.append(f"{profile.relative_to(REPO)} contains unknown Skills: {unknown!r}")

    claude_router = (REPO / "CLAUDE.md").read_text(encoding="utf-8").strip()
    if claude_router != "@AGENTS.md":
        errors.append("CLAUDE.md must import the canonical AGENTS.md router")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Registry OK: {len(names)} skills, {len(profiles)} profiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
