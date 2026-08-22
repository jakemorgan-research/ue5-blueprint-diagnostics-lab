# UE5 Blueprint Diagnostics Lab

A focused Codex skill and evidence-oriented knowledge base for explaining Unreal Engine 5 Blueprint graphs, diagnosing failures, and recording reproducible project cases.

The repository intentionally contains guidance and templates only. Real project cases, screenshots, node exports, engine-version details, and regression results will be added after the source project is reviewed and redacted.

## Included

- `ue5-blueprint-troubleshooter` Codex skill;
- symptom-based failure routing;
- plain-language Blueprint explanation format;
- reusable Blueprint architecture patterns;
- project organization and safe asset-move guidance;
- a verified-case template for reproducible postmortems.

## Install

Copy `skills/ue5-blueprint-troubleshooter` into your personal Codex skills directory, then restart or refresh Codex.

Example:

```text
Use $ue5-blueprint-troubleshooter to explain this graph and design the smallest test for the reported Accessed None error.
```

## Evidence boundary

UE behavior varies by engine version, platform, plugins, project settings, object lifetime, input system, and networking mode. A screenshot or node list alone does not prove runtime behavior. Project-specific causes remain hypotheses until reproduced or otherwise evidenced.

See [COMMON_FAILURES.md](docs/ue5/COMMON_FAILURES.md), [BLUEPRINT_PATTERNS.md](docs/ue5/BLUEPRINT_PATTERNS.md), and [VERIFIED_CASE_TEMPLATE.md](docs/ue5/VERIFIED_CASE_TEMPLATE.md).

## Current status

The reusable skill and documentation are ready for review. The project-specific case library remains pending until shareable UE5 source material is available. The repository stays private during that review.

MIT licensed. Third-party UE assets retain their original licenses and are not covered by this repository's license.

