---
name: ue5-blueprint-troubleshooter
description: Diagnose and explain Unreal Engine 5 Blueprint problems and design evidence-backed Blueprint workflows for LAN remote control, Android controllers, drones, sensors, packaging, and project organization. Use for Blueprint screenshots, node descriptions, logs, package failures, or UE project architecture; do not invent project-specific causes without evidence.
---

# UE5 Blueprint Troubleshooter

## Goal

Turn a UE5 symptom into a small set of evidence-backed hypotheses, a plain-language Blueprint explanation, and a minimal verification plan.

## Start with evidence

Collect or inspect the UE version, platform, exact error text, expected/observed behavior, relevant Blueprint graph, object classes, reproduction steps, plugins, and networking mode. If key evidence is absent, label hypotheses rather than presenting a root cause.

## Diagnosis workflow

1. Locate the failing execution path, not only the visually suspicious node.
2. Trace object references back to their assignment and lifetime.
3. Separate type problems, missing references, timing/order, ownership, state, and replication.
4. Check whether latent nodes, timers, Tick, Construction Script, or async loading change timing.
5. Propose the smallest observable test: breakpoint, Blueprint debugger, Watch value, targeted print/log, or minimal reproduction.
6. Recommend a minimal fix only after the hypothesis has a way to be falsified.
7. State what remains untested and whether the change needs PIE, standalone, packaged, or multiplayer verification.

## Explain a Blueprint graph

Describe the graph in this order:

- trigger or entry event;
- execution sequence and branches;
- origin and meaning of important data pins;
- state or external side effects;
- object ownership and lifetime;
- failure points and guards;
- performance or networking implications.

Translate node-by-node details into intent. Do not claim that a screenshot proves runtime behavior when hidden defaults, child overrides, project settings, or another graph may change it.

## Project cleanup

Treat moves, renames, redirector fixes, asset deletion, plugin removal, and configuration changes as potentially destructive. Inspect references and version-control state first. Prefer a small branch/backup and representative load/package tests. Never infer that an asset is unused only because no hard reference is visible.

## References

- Read `references/common-failures.md` for symptom-based diagnosis.
- Read `references/blueprint-explanation.md` when documenting or teaching a graph.
- Read `references/project-organization.md` for asset layout, moves, renames, or cleanup.
- Read `references/lan-remote-control.md` for Android-to-desktop TCP control, command framing, press/release input, and fail-safe behavior.
- Read `references/android-packaging.md` for Android package diagnosis and real-device verification.
- Read `references/drone-sensors.md` for drone, serial sensor, telemetry, and chart workflows.
- Read `references/evidence-backed-nodes.md` for verified node chains from the sanitized two-project case and its credential-safety boundary.

## Completion

A diagnosis is complete when the symptom is reproduced or explicitly marked unverified, the likely cause is tied to evidence, the proposed fix is scoped, and the required verification modes are listed.
