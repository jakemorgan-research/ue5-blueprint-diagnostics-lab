# Packaging an UE Android controller

![Android packaging path](../media/android-build-flow.svg)

This guide targets the workflow rather than one historical SDK number. Android store and Unreal requirements change; verify the current Epic and distribution-channel documentation before release.

## Inspected-project snapshot

The Android derivative recorded UE 5.4, minimum SDK 26, target SDK 28, sensor-landscape orientation, packaged data inside the APK, Vulkan, and network permissions. An Android ARM64 Shipping APK, install script, native library, and cooked output were present on the inspected workstation. The maintainer confirms successful packaged LAN operation with the desktop application.

The template package name, legacy permissions, and historical SDK values are reproducibility evidence—not recommended current store defaults and not blockers for this documentation release. Replace the package identity, remove permissions without a real need, and revalidate SDK requirements before distributing a new application build. See the [full evidence report](PROJECT_EVIDENCE_REPORT.md).

## 1. Make a packaging branch or copy

Keep the working desktop project untouched. Create a dedicated Android branch/copy and record:

- exact Unreal Engine patch version;
- Android Studio, SDK, NDK, and JDK versions selected by that engine;
- plugin versions and Android support status;
- package name, version code, signing mode, and target architectures.

## 2. Reduce the mobile project

Migrate only referenced, redistributable assets into the Android controller project. The inspected mobile derivative was far smaller than the desktop platform and centered on one map, robot assets, controller UMG, and a camera switcher.

Before packaging:

- fix redirectors;
- audit reference viewer and size map;
- remove editor-only and unsupported plugins;
- exclude desktop-only assets;
- avoid publishing Marketplace content outside its license.

## 3. Configure Android identity

Replace template values such as `com.YourCompany.[PROJECT]` with a package identifier you control. Keep public documentation on placeholders such as `com.example.lancontroller`; never commit keystore passwords or private signing files.

Set:

- application display name;
- version code and version name;
- minimum and target SDK compatible with the engine and intended channel;
- ARM64 architecture unless another target is deliberately required;
- orientation appropriate for the control UI;
- application icon and launch image with redistribution rights.

## 4. Network and permission settings

For a LAN TCP controller, `INTERNET` is normally the key network permission. Add only permissions the application actually needs. Legacy external-storage permissions should not be copied forward without a concrete requirement.

Disable public log-file output for release builds unless there is a reviewed operational need. Logs can expose device details, IP addresses, session identifiers, and user paths.

Cleartext LAN traffic may be restricted by platform policy or network-security configuration. Prefer an authenticated/encrypted design for anything beyond a controlled demonstration network.

## 5. Blueprint lifecycle

Implement explicit mobile lifecycle handling:

```text
Widget Construct
 -> Load last non-secret server settings
 -> Bind connection and receive delegates
 -> Keep controls disabled until connected

Application Will Enter Background
 -> Send stop-all if connected
 -> Disable controls
 -> Close or mark connection stale

Application Has Entered Foreground
 -> Re-evaluate network state
 -> Reconnect only through bounded policy or user action

Widget Destruct / Game Instance Shutdown
 -> Unbind delegates
 -> Disconnect client
```

Never store passwords or long-lived authentication secrets in a Blueprint default value.

## 6. Package

In Unreal Editor:

1. confirm the intended Game Default Map;
2. set Shipping for release candidates and Development for diagnostics;
3. select Android ASTC or another format supported by target devices;
4. package to a clean output directory outside the repository;
5. verify the APK/AAB, architecture, version, and signing information;
6. retain a private build record, not private keys or raw logs in Git.

## 7. Test on a real phone

Test at minimum:

- fresh install and first launch;
- UI scaling and safe areas;
- IP input and invalid-input feedback;
- Wi-Fi connection to a packaged Windows server;
- press, hold, release, and multi-touch edge cases;
- screen rotation policy;
- background/foreground and screen lock;
- Wi-Fi loss, server restart, and reconnect;
- prolonged run for battery, heat, memory, and log growth.

## 8. Common packaging failures

| Symptom | Checks |
| --- | --- |
| Plugin missing on Android | Plugin descriptor platform allowlist, Android binaries/source, build log |
| Works in editor, fails packaged | cooked maps/assets, config staging, permissions, firewall, plugin runtime dependency |
| Connect button freezes | synchronous connection attempt on UI/game thread |
| Cannot reach desktop | same subnet, correct desktop IPv4, bind interface, Windows firewall, guest Wi-Fi isolation |
| Motion continues after phone sleeps | missing server-side timeout and stop-all lifecycle handling |
| Store rejects build | current target SDK, signing, package identity, ABI, privacy declarations |

## Release rule

Never upload the package output, signing material, generated logs, device identifiers, or private network defaults to this documentation repository.
