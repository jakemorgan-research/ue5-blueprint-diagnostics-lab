<p align="center">
  <img src="docs/media/ue5-hero.svg" alt="UE5 Blueprint Engineering Lab" width="100%">
</p>

<p align="center">
  <a href="https://github.com/jakemorgan-research/ue5-blueprint-diagnostics-lab/actions/workflows/validate.yml"><img src="https://github.com/jakemorgan-research/ue5-blueprint-diagnostics-lab/actions/workflows/validate.yml/badge.svg" alt="Validate"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-059669.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/UE-5.4%20case-2563eb.svg" alt="UE 5.4 case">
  <img src="https://img.shields.io/badge/assets-docs%20only-7c3aed.svg" alt="Documentation only">
</p>

<p align="center"><strong>Blueprint debugging · Android ↔ Desktop · Drone · Sensors · Packaging</strong></p>
<p align="center"><sub>Visual guides and a Codex skill. No original project, private log, APK, or third-party asset.</sub></p>

## Choose your path

| 📱 Build remote control | 🚁 Build drone + data | 🧩 Read verified nodes | 📦 Ship Android |
| --- | --- | --- | --- |
| [Phone → desktop, node by node](docs/ue5/LAN_REMOTE_CONTROL.md) | [Sensors → charts → HUD](docs/ue5/DRONE_SENSOR_WORKFLOW.md) | [Actual graph → purpose → guard](docs/ue5/NODE_LIBRARY.md) | [Copy → configure → package → test](docs/ue5/ANDROID_PACKAGING.md) |

<p align="center">
  <img src="docs/media/lan-blueprint-flow.svg" alt="Android to desktop Blueprint flow" width="100%">
</p>

## Beginner route

### 1 — Understand the idea

The phone sends **intent**. The desktop validates it, changes the simulation, and sends state back.

### 2 — Build one safe button

~~~text
OnPressed → MakeCommand(start) → Send TCP
OnReleased → MakeCommand(stop)  → Send TCP
~~~

### 3 — Package both sides

<p align="center">
  <img src="docs/media/android-build-flow.svg" alt="Android packaging path" width="100%">
</p>

### 4 — Test the failure paths

<code>wrong IP</code> · <code>firewall</code> · <code>Wi-Fi loss</code> · <code>phone backgrounded</code> · <code>server restart</code>

## What came from the inspected projects?

**Observed:** TCP client calls, connection/receive delegates, IP and port input, press/release controls, Base + JointA–JointE, camera switching, drone Pawn, charts, and serial/Arduino references.

**Rebuilt for this repository:** the public protocol, safe server architecture, validation rules, diagrams, naming, and test plan.

[Open the evidence report →](docs/ue5/PROJECT_EVIDENCE_REPORT.md) · [Browse the node library →](docs/ue5/NODE_LIBRARY.md)

> **Release blocker found:** the private source project contained a credential in a Blueprint default. The value is excluded here; it must be revoked and removed before any project package is shared. [Read the remediation guide →](docs/ue5/SECURITY_REMEDIATION.md)

<details>
<summary><strong>Install the Codex skill</strong></summary>

Copy <code>skills/ue5-blueprint-troubleshooter</code> into your Codex skills directory and refresh Codex.

~~~text
Use $ue5-blueprint-troubleshooter to explain this Blueprint and give me the smallest reproducible test.
~~~

[Open the skill →](skills/ue5-blueprint-troubleshooter/SKILL.md)
</details>

<details>
<summary><strong>Repository map</strong></summary>

~~~text
docs/ue5/                              Visual engineering guides
docs/media/                            Original SVG diagrams
skills/ue5-blueprint-troubleshooter/   Installable Codex skill
scripts/                               Link, privacy, and skill checks
~~~
</details>

<details>
<summary><strong>Evidence and privacy boundary</strong></summary>

This repository does not claim that every hidden Blueprint path was reproduced end to end. Plugin node names can vary. Package and two-device tests remain required.

Original <code>.uasset</code>, <code>.umap</code>, Windows builds, APKs, Marketplace content, logs, tokens, addresses, and personal information are excluded. See [the release boundary](docs/OPEN_SOURCE_BOUNDARY.md).
</details>

<p align="center"><sub>Original documentation and diagrams: MIT. Unreal Engine and third-party components retain their own licenses.</sub></p>
