#!/usr/bin/env python3
"""Find common privacy and packaging risks before publishing this repository."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SKIP_DIRS = {".git", "node_modules", "__pycache__", "Binaries", "DerivedDataCache", "Intermediate", "Saved"}
BLOCKED_SUFFIXES = {".docx", ".xlsx", ".xls", ".pdf", ".ris", ".enw", ".nbib", ".uasset", ".umap"}
TEXT_SUFFIXES = {".csv", ".ini", ".json", ".md", ".ps1", ".py", ".svg", ".txt", ".yaml", ".yml"}
PATTERNS = {
    "Windows user path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.IGNORECASE),
    "possible email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "possible private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
    "possible API secret": re.compile(r"(?:api[_ -]?key|secret|token)\s*[:=]\s*['\"][^'\"]{8,}", re.IGNORECASE),
}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", type=Path)
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
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}: {rel}")

    if findings:
        print("Public-release check failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("Public-release check passed: no configured risks found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

