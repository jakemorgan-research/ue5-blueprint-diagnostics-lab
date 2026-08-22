# Compatibility claims and regression reports

Use the narrowest claim supported by the evidence. Keep these levels separate:

1. source or descriptor inspection;
2. project generation or compilation;
3. Editor or headless startup;
4. standalone execution;
5. packaged build or archive assembly;
6. installation and real-device behavior;
7. two-device network behavior under stated conditions.

A pass at one level does not imply a pass at a later level. An engine module allowlist does not prove that every listed platform compiles or runs.

For a regression report, record the repository release or commit, exact engine patch version, platform and architecture, build configuration, minimal clean-room steps, expected and observed results, and all untested modes. Separate workstation evidence, maintainer confirmation, and contributor reproduction.

Remove account names, machine paths, real network addresses, device identifiers, credentials, raw private logs, proprietary asset names, APKs, executables, and non-redistributable content before sharing. If the evidence cannot be shared safely, state the result as unverified.
