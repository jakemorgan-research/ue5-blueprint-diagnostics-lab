# Versioned LAN control protocol

This protocol is an independently reproducible example for an Android controller and desktop UE application. It is intentionally small, observable, and safe to reject.

## Transport

- TCP over a trusted local network during development.
- UTF-8 JSON, one object per line (`\n`).
- Maximum line length: 4096 bytes.
- One command ID per client action.
- The server returns `ack`, `state`, or `error` messages.
- Production or untrusted networks require authentication and encrypted transport; LAN location alone is not authentication.

TCP may merge or split sends. Keep an accumulated receive buffer, extract complete newline-terminated frames, and leave the incomplete tail for the next callback.

## Command envelope

```json
{"v":1,"type":"command","id":"cmd-001","target":"robot","action":"joint","name":"A","phase":"start","value":0.5}
```

Fields:

| Field | Meaning |
| --- | --- |
| `v` | Protocol version; reject unsupported versions |
| `type` | `hello`, `command`, `heartbeat`, `ack`, `state`, or `error` |
| `id` | Client-generated correlation ID |
| `target` | `robot`, `drone`, or `camera` |
| `action` | Whitelisted action name |
| `phase` | `start`, `stop`, or `set` |
| `value` | Optional normalized numeric value |

Examples:

```json
{"v":1,"type":"hello","id":"hello-001","client":"android-controller"}
{"v":1,"type":"command","id":"cmd-002","target":"robot","action":"forward","phase":"start","value":0.4}
{"v":1,"type":"command","id":"cmd-003","target":"robot","action":"forward","phase":"stop"}
{"v":1,"type":"command","id":"cmd-004","target":"camera","action":"zoom","phase":"set","value":0.65}
{"v":1,"type":"heartbeat","id":"hb-001"}
```

Server responses:

```json
{"v":1,"type":"ack","id":"cmd-002","accepted":true}
{"v":1,"type":"state","target":"robot","joints":{"A":12.5,"B":-8.0},"moving":true}
{"v":1,"type":"error","id":"cmd-004","code":"OUT_OF_RANGE","message":"zoom must be between 0 and 1"}
```

## Validation order

```text
Complete frame?
 -> valid UTF-8 and JSON object?
 -> supported version?
 -> known client/session?
 -> allowed type/target/action/phase?
 -> value finite and within range?
 -> command rate within limit?
 -> dispatch to the matching component
 -> acknowledgement or error
```

Never feed an arbitrary received string directly into console execution, object lookup, file access, or unrestricted reflection.

## Fail-safe rules

- When a `start` command is accepted, require a corresponding `stop` or a short renewable lease.
- If heartbeat or connection is lost, clear every active movement state.
- On Android pause/background, send stop-all before disconnecting when possible.
- On the desktop, the timeout is authoritative; do not depend on the phone successfully sending its final packet.
- Clamp all speed, rotation, and zoom values again on the desktop.

## Blueprint-friendly parsing options

1. **JSON plugin or Blueprint JSON library:** parse fields directly and validate them.
2. **Struct-based C++ bridge:** preferred when the protocol grows; expose a validated `FControlCommand` to Blueprint.
3. **Minimal delimited protocol:** acceptable for a tiny prototype, but escape rules and versioning must be documented.

Avoid a large `Switch on String` as the permanent architecture. Convert strings into enums or a validated command struct at the transport boundary.
