# Roadmap

- [x] Reusable Blueprint diagnosis skill.
- [x] Common-failure and project-organization guides.
- [x] Verified-case intake template.
- [x] Review the supplied UE5 project and determine redistribution boundaries.
- [x] Add the first redacted, reproducible Blueprint case.
- [x] Add Android-to-desktop LAN control, packaging, drone, and sensor guides.
- [x] Add engine-version and packaged-build evidence from the inspected workstation.
- [x] Record maintainer-confirmed packaged Android-to-desktop LAN completion.
- [x] Pass current-tree and reachable-history privacy review.
- [x] Publish a deterministic installable Skill archive as a tagged release.
- [x] Publish a clean-room UE 5.4 source demo and reusable Blueprint runtime plugin.
- [x] Compile the demo for Editor, Win64, and Android ARM64 and assemble a local validation APK.
- [x] Add a visual five-minute route for developers and first-time UE users.
- [x] Scan rebuilt release ZIP contents in CI before publication.
- [x] Add an evidence-scoped compatibility matrix and contributor regression report.
- [x] Add a pull-request template and privacy-safe compatibility issue form.
- [x] Add a static demo validator with regression tests to the CI gate.
- [x] Include the clean-room C++ and C# demo in GitHub language classification.

## After 1.0

- Add optional clean-room Blueprint graph assets after a binary-asset review workflow is available.
- Accept regression reports for additional UE versions, Android devices, and network conditions as contributors provide reproducible evidence.

## Release policy

**v1.3.0 remains the current release.** Documentation and visual refinements accumulate on `main` without creating a new tag. A new tagged release is warranted only when at least one of these conditions is met:

- a reproducible compatibility report for a new engine, device, or network condition is accepted;
- demo or plugin behavior changes with regression coverage;
- a privacy or security issue is fixed; or
- a clean-room Blueprint asset passes redistribution and binary-asset review.

Every release must pass demo validation, regression tests, link checks, package checks, and current-tree plus reachable-history privacy scans.
