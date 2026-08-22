#!/usr/bin/env python3
"""Validate the clean-room UE5 demo structure and release invariants without Unreal Engine."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


REQUIRED_FILES = {
    "UE5LanControlDemo.uproject",
    "README.md",
    "Docs/demo-quickstart.svg",
    "Config/DefaultEngine.ini",
    "Config/DefaultGame.ini",
    "Plugins/BlueprintEngineeringToolkit/BlueprintEngineeringToolkit.uplugin",
    "Plugins/BlueprintEngineeringToolkit/Source/BlueprintEngineeringToolkit/Public/BlueprintLanSubsystem.h",
    "Plugins/BlueprintEngineeringToolkit/Source/BlueprintEngineeringToolkit/Private/BlueprintLanSubsystem.cpp",
    "Source/UE5LanControlDemo/LanDemoGameMode.cpp",
    "Source/UE5LanControlDemo/LanDemoPlayerController.cpp",
}
FORBIDDEN_DIRS = {"Binaries", "Build", "DerivedDataCache", "Intermediate", "Saved", ".vs"}
FORBIDDEN_SUFFIXES = {".apk", ".aab", ".dll", ".exe", ".lib", ".pdb", ".so", ".target", ".uasset", ".umap"}
PUBLIC_APIS = {
    "StartLanServer",
    "StopLanServer",
    "ConnectToLanServer",
    "DisconnectLanClient",
    "SendMoveCommand",
    "SendStopCommand",
    "IsLanConnected",
    "GetLanStatus",
}


def read_json(path: Path, errors: list[str]) -> dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid JSON: {path}: {error}")
        return {}


def version_from_citation(path: Path) -> str:
    match = re.search(r"(?m)^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", path.read_text(encoding="utf-8"))
    return match.group(1) if match else ""


def release_paths(root: Path, demo: Path) -> list[Path]:
    """Return tracked demo paths, or a generated-directory-free fallback for fixtures."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--", "examples/ue5-lan-control-demo"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        result = None
    if result and result.stdout.strip():
        return [root / line for line in result.stdout.splitlines() if line.strip()]
    return [
        path
        for path in demo.rglob("*")
        if not any(part in FORBIDDEN_DIRS for part in path.relative_to(demo).parts)
    ]


def validate_demo(root: Path) -> list[str]:
    root = root.resolve()
    demo = root / "examples" / "ue5-lan-control-demo"
    errors: list[str] = []
    for relative in sorted(REQUIRED_FILES):
        if not (demo / relative).is_file():
            errors.append(f"missing demo file: {relative}")

    if not demo.is_dir():
        return errors or ["missing demo directory"]
    for path in release_paths(root, demo):
        if any(part in FORBIDDEN_DIRS for part in path.relative_to(demo).parts):
            errors.append(f"generated directory is tracked in demo: {path.relative_to(demo)}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden release file: {path.relative_to(demo)}")

    project = read_json(demo / "UE5LanControlDemo.uproject", errors)
    plugin_path = demo / "Plugins" / "BlueprintEngineeringToolkit" / "BlueprintEngineeringToolkit.uplugin"
    plugin = read_json(plugin_path, errors)
    if project.get("EngineAssociation") != "5.4":
        errors.append("UE5LanControlDemo.uproject: EngineAssociation must remain 5.4 until another version is verified")
    project_modules = project.get("Modules") or []
    if not any(isinstance(module, dict) and module.get("Name") == "UE5LanControlDemo" and module.get("Type") == "Runtime" for module in project_modules):
        errors.append("UE5LanControlDemo.uproject: missing Runtime project module")
    plugin_modules = plugin.get("Modules") or []
    if not any(isinstance(module, dict) and module.get("Name") == "BlueprintEngineeringToolkit" and module.get("Type") == "Runtime" for module in plugin_modules):
        errors.append("BlueprintEngineeringToolkit.uplugin: missing Runtime plugin module")
    if plugin.get("CanContainContent") is not False:
        errors.append("BlueprintEngineeringToolkit.uplugin: CanContainContent must be false for the source-only plugin")

    citation_version = version_from_citation(root / "CITATION.cff")
    game_ini = (demo / "Config" / "DefaultGame.ini").read_text(encoding="utf-8")
    project_version_match = re.search(r"(?m)^ProjectVersion=([^\r\n]+)$", game_ini)
    project_version = project_version_match.group(1).strip() if project_version_match else ""
    plugin_version = str(plugin.get("VersionName", ""))
    readme = (root / "README.md").read_text(encoding="utf-8")
    readme_version_match = re.search(r"release-v([0-9]+\.[0-9]+\.[0-9]+)", readme)
    readme_version = readme_version_match.group(1) if readme_version_match else ""
    versions = {citation_version, project_version, plugin_version, readme_version}
    if "" in versions or len(versions) != 1:
        errors.append(
            "release version mismatch: "
            f"citation={citation_version or '<missing>'}, project={project_version or '<missing>'}, "
            f"plugin={plugin_version or '<missing>'}, readme={readme_version or '<missing>'}"
        )

    if not re.search(r"(?mi)^PackageName=com\.example\.uelancontroldemo\s*$", game_ini):
        errors.append("DefaultGame.ini: demo package name must remain the neutral com.example.uelancontroldemo")

    header = (demo / "Plugins" / "BlueprintEngineeringToolkit" / "Source" / "BlueprintEngineeringToolkit" / "Public" / "BlueprintLanSubsystem.h").read_text(encoding="utf-8")
    for api in sorted(PUBLIC_APIS):
        if not re.search(rf"\b{re.escape(api)}\s*\(", header):
            errors.append(f"BlueprintLanSubsystem.h: missing public API: {api}")
    implementation = (demo / "Plugins" / "BlueprintEngineeringToolkit" / "Source" / "BlueprintEngineeringToolkit" / "Private" / "BlueprintLanSubsystem.cpp").read_text(encoding="utf-8")
    safety_markers = {
        "message size limit": "MaxMessageBytes",
        "axis clamping": "ClampAxis",
        "newline framing": 'TEXT("\\n")',
        "motion timeout": "LastMotionCommandSeconds > 0.5",
        "disconnect detection": "SCS_ConnectionError",
    }
    for label, marker in safety_markers.items():
        if marker not in implementation:
            errors.append(f"BlueprintLanSubsystem.cpp: missing {label} invariant")

    attributes = root / ".gitattributes"
    if not attributes.is_file() or "linguist-detectable=true" not in attributes.read_text(encoding="utf-8"):
        errors.append(".gitattributes: demo source must be included in GitHub language detection")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()
    errors = validate_demo(args.root)
    if args.json_output:
        print(json.dumps({"passed": not errors, "errors": errors}, indent=2))
    elif errors:
        print("UE demo validation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print("UE demo validation passed: descriptors, versions, Blueprint APIs, safety markers, and release boundaries are consistent.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
