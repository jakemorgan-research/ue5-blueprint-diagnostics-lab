# Practical Blueprint patterns

These are design patterns, not copy-paste graphs. Adapt them to the engine version and project architecture.

## Interface-driven interaction

Use a Blueprint Interface when many unrelated actors expose the same capability, such as `Interact`.

Flow:

```text
Input -> line trace -> hit actor -> implements interface? -> call Interact
```

Keep the trace and player intent in the controller/pawn; keep the resulting behavior in the target actor.

## Event Dispatcher for one-to-many updates

Use an Event Dispatcher when a source owns a state change and multiple listeners react, for example inventory changes updating UI and audio.

Bind and unbind deliberately. Avoid duplicate binding when widgets or actors are recreated.

## Component-based reusable behavior

Place cohesive behavior such as health, interaction highlighting, or cooldown management in an Actor Component when it must be reused across classes. Define ownership, initialization, and replication responsibilities explicitly.

## Explicit state machine

For interactions with several states, use an enum and a single transition function.

```text
Idle -> Activating -> Active -> Deactivating -> Idle
```

Reject or queue invalid transitions instead of letting multiple event paths write the same state independently.

## Timer instead of polling

Use a timer for periodic checks that do not require frame precision. Store the timer handle when cancellation or replacement matters.

## Safe save/load boundary

Save stable data, identifiers, and configuration—not live actor references. Reconstruct runtime references after loading and version the save structure when fields evolve.

