# Sanitized evidence report for the two UE projects

This report records what was actually observed in two private Unreal Engine projects and separates it from the safer public reconstruction in this repository. No original asset, package, log, network address, credential, or Marketplace content is included.

## Evidence labels

- **Verified** — read from the project descriptor, configuration, asset registry, or exported Blueprint graph metadata.
- **Reconstructed** — a clean implementation proposed for developers; it is not claimed to be the original graph.
- **Packaged artifact verified** — a Shipping output was present on the inspected workstation.
- **Maintainer-confirmed runtime** — the maintainer reports completing the two-device workflow; private device logs are not published as independent evidence.

## Project comparison

| Area | Desktop/reference project | Android/controller derivative |
| --- | --- | --- |
| Engine recorded by project | UE 5.4 | UE 5.4 |
| Asset count at inspection | 1,233 | 181 |
| Main focus | Menu, laboratory, robot, drone, sensors, charts, web/API features | Compact UMG remote controller, camera switching, robot assets |
| Networking evidence | Socket client/server plugins are enabled | TCP client connect/send nodes and connection/receive delegates are present |
| Packaging evidence | Windows Shipping executable and staged output present | Android ARM64 Shipping APK, install script, native library, cooked and staged outputs present |

The installed UE 5.5 editor was not used to convert these projects. Inspection used the matching UE 5.4 installation so the source assets were not upgraded.

## Verified Android controller graph

The main controller widget contains:

1. an editable server address field;
2. `connectSocketClientTCP` with IPv4 selected and a project example port of `5656`;
3. TCP connection and receive delegates;
4. `socketClientSendTCP` calls with line-break sending enabled;
5. separate pressed/released controls for Forward, Back, Left, Right, Base, and JointA through JointE;
6. compact numeric messages in the observed set `10`–`29`;
7. camera switching and zoom controls.

The exact number-to-control mapping was not fully verified and is therefore not published as fact. The public protocol in this repository replaces magic numbers with versioned, named commands.

## Verified reusable Blueprint patterns

- Camera switch: find robot actor → select actor → get player controller → set view target with blend (`0.5 s`, linear) → replace the widget and set UI input mode.
- Server address entry: text committed → text-to-string conversion → store address → confirm → remove widget → restore game input and hide cursor.
- Drone propellers: collect four propeller components → iterate → build rotation from configured propeller speed → add relative rotation.
- Drone follow camera: get player camera manager rotation → split and rebuild the desired rotation → set actor rotation.
- Drone functions also include screenshot capture, field-of-view control, night vision, thermal view, movement, sound, collision, and HUD state.

See the [evidence-backed node library](NODE_LIBRARY.md) for beginner-friendly graph sequences and failure checks.

## Historical Android settings found

| Setting | Observed value | Publication guidance |
| --- | --- | --- |
| Package name | Template placeholder | Replace before distribution |
| Minimum SDK | 26 | Historical evidence only; revalidate for the chosen engine/channel |
| Target SDK | 28 | Stale for modern distribution; do not copy blindly |
| Orientation | Sensor landscape | Keep only if the UI is tested in both landscape directions |
| Data inside APK | Enabled | Recheck package size and patching needs |
| Network permissions | Internet and network state | Keep only what the feature needs |
| Storage permissions | Legacy read/write permissions | Remove unless a current, justified requirement exists |
| Vulkan | Enabled | Test on representative devices and retain a fallback when needed |
| Multicast support | Disabled | The observed TCP design does not require multicast discovery |

## Critical credential finding

**Verified:** a long-lived third-party API credential was stored as a Blueprint default value in the desktop project. A packaged client cannot keep such a secret: asset extraction or runtime inspection can reveal it.

The public-release remediation completed for the inspected source and this repository:

1. removed the value from the inspected Blueprint source copies;
2. excluded original packages, logs, backups, and private project content from this repository;
3. scanned the current tree and reachable Git history for configured credential and personal-data patterns;
4. documented a controlled backend or local gateway as the safe replacement architecture;
5. kept provider-side revocation as an external account control that a repository scanner cannot prove.

The sanitized HTTP node chain is documented in [Security remediation](SECURITY_REMEDIATION.md). The credential value is deliberately not retained here.

## Completed workflow and remaining portability boundary

The inspected workstation contains Windows and Android Shipping outputs. The maintainer confirms that the packaged Android controller and desktop application were connected and operated over the LAN on real devices.

The following details are intentionally not promoted to universal facts:

- the exact original desktop TCP server Blueprint and final bind configuration;
- the precise mapping of every numeric mobile command;
- compatibility across every Android device, router, firewall policy, engine update, and distribution channel;
- current store-policy compliance of historical SDK values.

These are portability and disclosure boundaries, not blockers for releasing the original documentation, diagrams, and Codex Skill in this repository.
