# LAN remote control

Read `../../../docs/ue5/LAN_REMOTE_CONTROL.md` and `../../../docs/ue5/CONTROL_PROTOCOL.md` before designing or diagnosing Android-to-desktop control.

Preserve these invariants:

- identify which process is server and which is client;
- keep message framing identical on both ends;
- store and match connection/session IDs;
- route validated commands through a domain component;
- pair `OnPressed` start with `OnReleased` stop;
- implement server-side timeout and stop-all behavior;
- verify packaged Windows and Android builds on two devices;
- label plugin-specific node names and unverified defaults.
