#!/usr/bin/env python3
"""Check local Markdown links without network access."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote


LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def check_links(root: Path) -> list[str]:
    errors: list[str] = []
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        text = document.read_text(encoding="utf-8")
        for raw in LINK.findall(text):
            target = raw.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(SKIP_PREFIXES):
                continue
            path_text = unquote(target.split("#", 1)[0])
            if not path_text:
                continue
            resolved = (document.parent / path_text).resolve()
            if not resolved.exists():
                errors.append(f"{document.relative_to(root)}: missing link target {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", type=Path)
    root = parser.parse_args().root.resolve()
    errors = check_links(root)
    if errors:
        print("Local link check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Local link check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

