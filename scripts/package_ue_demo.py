#!/usr/bin/env python3
"""Create deterministic source archives for the UE5 plugin and minimal demo."""

from __future__ import annotations

import argparse
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.0"
DEMO = ROOT / "examples" / "ue5-lan-control-demo"
PLUGIN = DEMO / "Plugins" / "BlueprintEngineeringToolkit"
LICENSE = ROOT / "LICENSE"
EXCLUDED_PARTS = {"Binaries", "Build", "DerivedDataCache", "Intermediate", "Saved", ".vs", "__pycache__"}
EXCLUDED_SUFFIXES = {".apk", ".aab", ".dll", ".exe", ".lib", ".pdb", ".so", ".target", ".pyc"}

DEMO_REQUIRED = {
    "UE5LanControlDemo.uproject",
    "README.md",
    "Config/DefaultEngine.ini",
    "Source/UE5LanControlDemo.Target.cs",
    "Source/UE5LanControlDemo/LanDemoGameMode.cpp",
    "Plugins/BlueprintEngineeringToolkit/BlueprintEngineeringToolkit.uplugin",
}
PLUGIN_REQUIRED = {
    "BlueprintEngineeringToolkit.uplugin",
    "Source/BlueprintEngineeringToolkit/BlueprintEngineeringToolkit.Build.cs",
    "Source/BlueprintEngineeringToolkit/Public/BlueprintLanSubsystem.h",
    "Source/BlueprintEngineeringToolkit/Private/BlueprintLanSubsystem.cpp",
}


def source_files(folder: Path) -> list[Path]:
    return sorted(
        path
        for path in folder.rglob("*")
        if path.is_file()
        and not any(part in EXCLUDED_PARTS for part in path.parts)
        and path.suffix.lower() not in EXCLUDED_SUFFIXES
    )


def write_archive(source: Path, output: Path, root_name: str, required: set[str]) -> list[str]:
    files = source_files(source)
    relative = {path.relative_to(source).as_posix() for path in files}
    missing = sorted(required - relative)
    if missing:
        raise ValueError(f"missing required release files: {', '.join(missing)}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            name = f"{root_name}/{path.relative_to(source).as_posix()}"
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())

        license_info = zipfile.ZipInfo(f"{root_name}/LICENSE.txt", date_time=(2026, 1, 1, 0, 0, 0))
        license_info.compress_type = zipfile.ZIP_DEFLATED
        license_info.external_attr = 0o100644 << 16
        archive.writestr(license_info, LICENSE.read_bytes())
    return sorted(relative)


def package(output_dir: Path) -> tuple[list[str], list[str]]:
    demo_files = write_archive(
        DEMO,
        output_dir / f"ue5-lan-control-demo-v{VERSION}.zip",
        "ue5-lan-control-demo",
        DEMO_REQUIRED,
    )
    plugin_files = write_archive(
        PLUGIN,
        output_dir / f"blueprint-engineering-toolkit-v{VERSION}.zip",
        "BlueprintEngineeringToolkit",
        PLUGIN_REQUIRED,
    )
    return demo_files, plugin_files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as temp:
            demo_files, plugin_files = package(Path(temp))
    else:
        output_dir = args.output_dir.resolve()
        demo_files, plugin_files = package(output_dir)
        print(f"Created: {output_dir / f'ue5-lan-control-demo-v{VERSION}.zip'}")
        print(f"Created: {output_dir / f'blueprint-engineering-toolkit-v{VERSION}.zip'}")

    print(f"Demo package validation passed: {len(demo_files)} source files.")
    print(f"Plugin package validation passed: {len(plugin_files)} source files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
