# Common failure routing

## Invalid reference

Search terms: `Accessed None`, pending kill, destroyed actor, unassigned variable, spawn timing.

Trace the reference to the first assignment. Check whether the object exists on this machine, at this time, and for this owner. A validity check prevents a crash path but does not establish correct initialization.

## Communication failure

Search terms: cast failed, interface not called, dispatcher not firing, widget not updating.

Determine whether the caller has the correct target object. Use a cast for runtime type checks, an interface for capabilities, and an event dispatcher for subscription/broadcast relationships.

## Input failure

Search terms: Enhanced Input, mapping context, possession, input mode, widget focus.

Confirm the local player, controller/pawn ownership, active mapping context and priority, and UI focus. Test the input action and the downstream gameplay event separately.

## Timing failure

Search terms: BeginPlay order, Construction Script, delay, async load, timer, Tick.

Do not treat actor BeginPlay ordering as a dependency guarantee. Make initialization explicit or wait for a verified readiness signal.

## Network failure

Search terms: authority, ownership, RPC, replication, listen server, dedicated server.

Record where the event starts and where the state must become authoritative. Verify RPC ownership rules and replicate durable state rather than relying only on transient visual execution.

## Performance problem

Search terms: Event Tick, Get All Actors of Class, repeated cast, widget binding, spawn loop.

Measure first. Replace repeated global searches with stored references or registries, polling with events/timers, and duplicated behavior with components when the architecture supports it.

