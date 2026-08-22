# Contributing

Use the UE5 case template and include the engine version, platform, plugins, project settings, expected/observed behavior, exact error, minimal reproduction, Blueprint node names or a redacted export, and verification modes.

Separate confirmed causes from hypotheses. A restart, validity guard, repeated cast, or global actor search is not a demonstrated root-cause fix by itself.

Remove proprietary assets, project/client names, credentials, machine paths, marketplace content, and unrelated logs before sharing.

Run:

```text
python scripts/validate_skills.py .
python scripts/check_public_release.py . --history
python scripts/check_links.py .
python scripts/package_skill.py --check
```
