# UE5 Blueprint common failures

Use this guide as a diagnosis map. Confirm engine version, execution path, object lifetime, networking context, and exact error text before applying a fix.

## `Accessed None`

Meaning: a Blueprint attempted to read or call through an invalid object reference.

Check in this order:

1. Identify the exact node and execution path from the runtime message.
2. Determine where the reference should be assigned: editor default, spawn return value, overlap, lookup, or dependency injection.
3. Verify timing. `BeginPlay` order across actors is not a dependency contract.
4. Use `Is Valid` only as a guard; it does not repair missing initialization.
5. If the target can be destroyed, clear or reacquire the reference deliberately.

Common trap: repeatedly calling `Get All Actors of Class` hides lifecycle problems and can become expensive.

## Cast fails

A cast checks the runtime type; it does not find an object or establish communication.

- Print the actual object name/class before the cast.
- Confirm the object pin comes from the intended source.
- Prefer Blueprint Interfaces for capability-based interaction.
- Prefer Event Dispatchers when one object broadcasts state changes to listeners.

## Input does not fire

- Confirm which system is used: legacy input or Enhanced Input.
- For Enhanced Input, verify mapping context, local player subsystem, priority, and possession.
- Confirm the Player Controller possesses the expected Pawn.
- Avoid enabling input on many world actors without a clear ownership model.
- Check UI focus and input mode when widgets are involved.

## Construction Script behaves unpredictably

Construction Script can run repeatedly in the editor. Avoid persistent side effects, large searches, save operations, or logic that assumes a single execution.

For generated components, keep creation deterministic and verify cleanup when parameters change.

## Tick causes unstable or slow behavior

Use Tick only when work genuinely depends on every frame.

Prefer:

- events for state transitions;
- timers for periodic work;
- timelines for authored interpolation;
- latent nodes for controlled sequences;
- components for reusable behavior.

If Tick is necessary, gate it, disable it when idle, and make frame-rate dependence explicit with Delta Seconds.

## Timeline or animation state becomes inconsistent

- Decide whether reverse, replay, and interruption are allowed.
- Store explicit state instead of inferring it only from a visual value.
- Handle repeated interaction while the timeline is already playing.
- Replicate authoritative state rather than assuming Timeline playback itself is synchronized.

## Multiplayer works on server but not client

- Identify authority, owning client, and simulated proxies.
- Replication sends state; RPCs request or announce events under specific ownership rules.
- Do not trust client-only validation for authoritative game state.
- Test with dedicated-server and multiple-client modes, not only single-process PIE.

## Blueprint appears correct but old behavior remains

- Compile the Blueprint and inspect warnings.
- Check whether a child Blueprint overrides the relevant value or event.
- Confirm the level contains the expected class instance.
- Fix redirectors after deliberate asset moves.
- Restart the editor only after capturing diagnostics; a restart can hide a reproducible state problem.

