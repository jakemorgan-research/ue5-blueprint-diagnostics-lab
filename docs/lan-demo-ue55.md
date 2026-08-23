# Reproduce the LAN demo on Unreal Engine 5.5

## Prerequisites

- Unreal Engine **5.5** (launcher or source build)
- Two machines or two editor/game instances on the same LAN/subnet
- This repository's demo map / project files

## Steps

1. Generate project files if required and open the `.uproject` with UE 5.5.
2. Set the map named in the demo (see project `Config/DefaultEngine.ini` GameDefaultMap).
3. **Host:** Play In Editor (or packaged build) as Listen Server / Host.
4. **Client:** use the on-screen LAN browse UI, or open console and `open <host-ip>`.
5. Confirm both instances see the same session and basic replication (pawn/move or demo actor).

## UE 5.5 notes

- If plugins fail to load, enable them under **Edit → Plugins** and restart.
- Firewall must allow the UE multiplayer ports on local networks.
- Use consistent `NetDriver` settings between host and client (project defaults).

## Report results

Open a PR or issue comment with: UE 5.5 patch version, host OS, whether PIE or packaged, and any log errors from `Saved/Logs`.
