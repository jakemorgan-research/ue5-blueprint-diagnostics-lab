# Contributing

Use the UE5 case template and include the engine version, platform, plugins, project settings, expected/observed behavior, exact error, minimal reproduction, Blueprint node names or a redacted export, and verification modes.

For a new engine, platform, or device result, use the compatibility issue form and follow the [compatibility matrix](docs/ue5/COMPATIBILITY.md). A pull request should update the matrix only when its regression report states exactly what compiled, ran, packaged, and remained untested.

Separate confirmed causes from hypotheses. A restart, validity guard, repeated cast, or global actor search is not a demonstrated root-cause fix by itself.

Remove proprietary assets, project/client names, credentials, machine paths, marketplace content, and unrelated logs before sharing.

Run:

```text
python scripts/validate_skills.py .
python scripts/validate_ue_demo.py .
python -m unittest discover -s tests -v
python scripts/check_links.py .
python scripts/package_skill.py --output dist/ue5-blueprint-troubleshooter.zip
python scripts/package_ue_demo.py --output-dir dist
python scripts/check_public_release.py . --history --archives dist
```

The demo validator checks descriptor structure, aligned release versions, neutral package identity, Blueprint-callable APIs, network fail-safes, tracked release boundaries, and GitHub language classification. It does not replace an Unreal Editor build or real-device test.
