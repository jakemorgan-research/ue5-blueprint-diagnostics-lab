#!/usr/bin/env python3
"""Create a deterministic, installable ZIP for the UE5 troubleshooting skill."""

from __future__ import annotations

import argparse
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ue5-blueprint-troubleshooter"
REQUIRED = {
    "SKILL.md",
    "agents/openai.yaml",
    "references/android-packaging.md",
    "references/blueprint-explanation.md",
    "references/common-failures.md",
    "references/drone-sensors.md",
    "references/evidence-backed-nodes.md",
    "references/lan-remote-control.md",
    "references/project-organization.md",
}


def package(output: Path) -> list[str]:
    files = sorted(
        path
        for path in SKILL.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )
    relative = {path.relative_to(SKILL).as_posix() for path in files}
    missing = sorted(REQUIRED - relative)
    if missing:
        raise ValueError(f"missing required package files: {', '.join(missing)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            name = f"ue5-blueprint-troubleshooter/{path.relative_to(SKILL).as_posix()}"
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    return sorted(relative)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist" / "ue5-blueprint-troubleshooter.zip",
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as temp:
            files = package(Path(temp) / "skill.zip")
    else:
        files = package(args.output.resolve())
        print(f"Created: {args.output.resolve()}")

    print(f"Package validation passed: {len(files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
