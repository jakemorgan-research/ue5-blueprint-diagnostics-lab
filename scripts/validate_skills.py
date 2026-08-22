#!/usr/bin/env python3
"""Validate Codex skill packaging without third-party dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def validate_skill(skill: Path) -> list[str]:
    errors: list[str] = []
    path = skill / "SKILL.md"
    if not path.is_file():
        return [f"{skill}: missing SKILL.md"]
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return [f"{path}: invalid frontmatter fence"]
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append(f"{path}: invalid skill name")
    if skill.name != name:
        errors.append(f"{path}: folder name must match skill name")
    if not description or len(description) > 1024 or "<" in description or ">" in description:
        errors.append(f"{path}: invalid description")
    if re.search(r"\[TODO:|\bTBD\b|PLACEHOLDER", text, re.IGNORECASE):
        errors.append(f"{path}: unfinished placeholder")
    for ref in sorted(
        set(re.findall(r"`((?:references|scripts|assets)/[^`\s<>]+)`", text))
    ):
        if not (skill / ref).exists():
            errors.append(f"{path}: missing referenced resource: {ref}")
    metadata = skill / "agents" / "openai.yaml"
    if metadata.is_file():
        meta = metadata.read_text(encoding="utf-8")
        if f"${name}" not in meta:
            errors.append(f"{metadata}: default prompt must mention ${name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    skills_root = args.root.resolve() / "skills"
    errors: list[str] = []
    for skill in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        errors.extend(validate_skill(skill))
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

