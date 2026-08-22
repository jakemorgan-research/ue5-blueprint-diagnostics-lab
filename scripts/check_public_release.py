#!/usr/bin/env python3
"""Find common privacy and packaging risks before publishing this repository."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


SKIP_DIRS = {".git", "node_modules", "__pycache__", "Binaries", "DerivedDataCache", "Intermediate", "Saved"}
BLOCKED_SUFFIXES = {".docx", ".xlsx", ".xls", ".pdf", ".ris", ".enw", ".nbib", ".uasset", ".umap"}
TEXT_SUFFIXES = {".csv", ".ini", ".json", ".md", ".ps1", ".py", ".svg", ".txt", ".yaml", ".yml"}
PATTERNS = {
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.IGNORECASE),
    "POSIX user path": re.compile(r"/(?:Users|home)/[^/\s]+", re.IGNORECASE),
    "possible personal phone number": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "possible email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "possible ORCID": re.compile(r"\b000[0-9]-[0-9]{4}-[0-9]{4}-[0-9]{4}\b"),
    "possible private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "possible API secret": re.compile(r"(?:api[_ -]?key|secret|token)\s*[:=]\s*['\"][^'\"]{8,}", re.IGNORECASE),
    "possible provider credential": re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
    "possible bearer credential": re.compile(r"Authorization[^\n\r]{0,80}Bearer\s+[A-Za-z0-9._~-]{20,}", re.IGNORECASE),
    "possible GitHub token": re.compile(r"gh[opsu]_[A-Za-z0-9]{30,}"),
    "possible GitHub fine-grained token": re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    "possible AWS access key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "possible Google API key": re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    "possible Slack token": re.compile(r"xox[abprs]-[A-Za-z0-9-]{20,}"),
    "possible JWT": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    "embedded URL credential": re.compile(r"[a-z][a-z0-9+.-]*://[^\s/:]+:[^\s/@]+@", re.IGNORECASE),
}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def scan_text(text: str, label: str) -> list[str]:
    findings: list[str] = []
    for finding_label, pattern in PATTERNS.items():
        matches = list(pattern.finditer(text))
        if finding_label == "possible email":
            matches = [match for match in matches if not match.group(0).lower().endswith("@users.noreply.github.com")]
        if matches:
            findings.append(f"{finding_label}: {label}")
    return findings


def git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def scan_history(root: Path) -> list[str]:
    findings: list[str] = []
    metadata = git(root, "log", "--all", "--format=%H%x00%an%x00%ae%x00%cn%x00%ce")
    if metadata.returncode != 0:
        return ["unable to inspect Git commit metadata"]
    for raw_line in metadata.stdout.decode("utf-8", errors="replace").splitlines():
        fields = raw_line.split("\x00")
        if len(fields) != 5:
            continue
        commit, author_name, author_email, committer_name, committer_email = fields
        for role, name, email in (
            ("author", author_name, author_email),
            ("committer", committer_name, committer_email),
        ):
            if email and not email.lower().endswith("@users.noreply.github.com"):
                findings.append(f"personal email in {role} metadata: {commit[:12]} ({name})")

    objects = git(root, "rev-list", "--objects", "--all")
    if objects.returncode != 0:
        return findings + ["unable to enumerate reachable Git objects"]
    seen_blobs: set[str] = set()
    for raw_line in objects.stdout.decode("utf-8", errors="replace").splitlines():
        sha, _, object_path = raw_line.partition(" ")
        if not object_path or sha in seen_blobs:
            continue
        object_type = git(root, "cat-file", "-t", sha)
        if object_type.returncode != 0 or object_type.stdout.strip() != b"blob":
            continue
        seen_blobs.add(sha)
        suffix = Path(object_path).suffix.lower()
        if suffix in BLOCKED_SUFFIXES:
            findings.append(f"blocked file type in history: {object_path} ({sha[:12]})")
            continue
        if suffix not in TEXT_SUFFIXES and Path(object_path).name not in {"LICENSE", ".gitignore"}:
            continue
        blob = git(root, "cat-file", "-p", sha)
        if blob.returncode != 0:
            findings.append(f"unable to inspect history blob: {object_path} ({sha[:12]})")
            continue
        if len(blob.stdout) > 5 * 1024 * 1024:
            findings.append(f"large history blob over 5 MiB: {object_path} ({sha[:12]})")
            continue
        try:
            text = blob.stdout.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(f"non-UTF-8 history text candidate: {object_path} ({sha[:12]})")
            continue
        findings.extend(scan_text(text, f"history {object_path} ({sha[:12]})"))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--history", action="store_true", help="scan reachable Git history and commit metadata")
    args = parser.parse_args()
    root = args.root.resolve()
    findings: list[str] = []

    for path in iter_files(root):
        rel = path.relative_to(root)
        if path.suffix.lower() in BLOCKED_SUFFIXES:
            findings.append(f"blocked file type: {rel}")
            continue
        if path.stat().st_size > 5 * 1024 * 1024:
            findings.append(f"large file over 5 MiB: {rel}")
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE", ".gitignore"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"non-UTF-8 text candidate: {rel}")
            continue
        findings.extend(scan_text(text, str(rel)))

    if args.history:
        findings.extend(scan_history(root))

    if findings:
        print("Public-release check failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Public-release check passed: no configured risks found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
