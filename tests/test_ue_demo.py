from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_ue_demo.py"
SPEC = importlib.util.spec_from_file_location("validate_ue_demo", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VALIDATOR)


def copy_fixture(destination: Path) -> None:
    (destination / "examples").mkdir(parents=True)
    shutil.copytree(
        ROOT / "examples" / "ue5-lan-control-demo",
        destination / "examples" / "ue5-lan-control-demo",
        ignore=shutil.ignore_patterns("Binaries", "Build", "DerivedDataCache", "Intermediate", "Saved", ".vs"),
    )
    shutil.copy2(ROOT / "README.md", destination / "README.md")
    shutil.copy2(ROOT / "CITATION.cff", destination / "CITATION.cff")
    shutil.copy2(ROOT / ".gitattributes", destination / ".gitattributes")


class UEDemoValidationTests(unittest.TestCase):
    def test_current_demo_is_valid(self):
        self.assertEqual([], VALIDATOR.validate_demo(ROOT))

    def test_version_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            copy_fixture(fixture)
            plugin_path = fixture / "examples" / "ue5-lan-control-demo" / "Plugins" / "BlueprintEngineeringToolkit" / "BlueprintEngineeringToolkit.uplugin"
            plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
            plugin["VersionName"] = "9.9.9"
            plugin_path.write_text(json.dumps(plugin), encoding="utf-8")
            errors = VALIDATOR.validate_demo(fixture)
            self.assertTrue(any("release version mismatch" in error for error in errors))

    def test_missing_fail_safe_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            copy_fixture(fixture)
            source = fixture / "examples" / "ue5-lan-control-demo" / "Plugins" / "BlueprintEngineeringToolkit" / "Source" / "BlueprintEngineeringToolkit" / "Private" / "BlueprintLanSubsystem.cpp"
            source.write_text(source.read_text(encoding="utf-8").replace("LastMotionCommandSeconds > 0.5", "LastMotionCommandSeconds > Timeout"), encoding="utf-8")
            errors = VALIDATOR.validate_demo(fixture)
            self.assertTrue(any("motion timeout" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
