# Sanitized evidence report for the two UE projects

This report records what was actually observed in two private Unreal Engine projects and separates it from the safer public reconstruction in this repository. No original asset, package, log, network address, credential, or Marketplace content is included.

## Evidence labels

- **Verified** — read from the project descriptor, configuration, asset registry, or exported Blueprint graph metadata.
- **Reconstructed** — a clean implementation proposed for developers; it is not claimed to be the original graph.
- **Pending device test** — requires packaged Windows and Android builds on two devices.

## Project comparison

| Area | Desktop/reference project | Android/controller derivative |
| --- | --- | --- |
| Engine recorded by project | UE 5.4 | UE 5.4 |
| Asset count at inspection | 1,233 | 181 |
| Main focus | Menu, laboratory, robot, drone, sensors, charts, web/API features | Compact UMG remote controller, camera switching, robot assets |
| Networking evidence | Socket client/server plugins are enabled | TCP client connect/send nodes and connection/receive delegates are present |
| Packaging evidence | Windows-oriented project structure | Android configuration and mobile controller UI |

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

Required remediation before any package or repository release:

1. revoke and rotate the exposed credential in the provider dashboard;
2. remove it from every Blueprint default, config file, build artifact, log, backup, and history;
3. place provider authentication on a controlled backend or local gateway;
4. let UE call that gateway with a short-lived, scoped session credential if authentication is needed;
5. run the repository privacy scanner and inspect packaged assets separately.

The sanitized HTTP node chain is documented in [Security remediation](SECURITY_REMEDIATION.md). The credential value is deliberately not retained here.

## What is still unverified

- the exact original desktop TCP server Blueprint and final bind configuration;
- the precise mapping of every numeric mobile command;
- an end-to-end run of the packaged Windows and Android builds on the same LAN;
- timeout, reconnect, background/resume, and packet-framing behavior;
- compatibility with current Android distribution requirements.

These gaps are release gates, not details to fill by assumption.
