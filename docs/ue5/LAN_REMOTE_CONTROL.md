# Android-to-desktop LAN control in Blueprint

![Android-to-desktop Blueprint flow](../media/lan-blueprint-flow.svg)

This recipe reconstructs the observed design using an explicit protocol and clear ownership boundaries. Node labels for socket operations may differ by plugin. The inspected Android asset exposed nodes named `connectSocketClientTCP`, `socketClientSendTCP`, a TCP connection-event delegate, and a TCP receive-event delegate.

## 1. Desktop components

Create these Blueprints:

- `BP_LanCommandGateway` — owns server start/stop, sessions, receive buffer, timeout, and command dispatch;
- `BPC_RobotCommandTarget` — validates and applies robot commands;
- `BPC_DroneCommandTarget` — validates and applies drone commands;
- `WBP_ServerStatus` — displays bind address, port, session count, and last error without controlling the server directly.

Do not put all socket, parsing, movement, animation, camera, and UI logic in a Level Blueprint.

## 2. Start the desktop server

Recommended execution chain:

```text
Event BeginPlay
 -> Get Game Instance / configuration object
 -> Validate configured port
 -> Start TCP Server
      IP = 0.0.0.0 for LAN listening
      Port = configured example port
      Message Separator = String or Byte matching the client
 -> Store Server ID
 -> Bind server connection event
 -> Bind server receive-message event
 -> Set status = Listening
```

Use `127.0.0.1` only for same-machine tests. To accept a phone on Wi-Fi, bind to an appropriate local interface or `0.0.0.0`, then allow the selected port through the Windows firewall for the packaged application.

On `EndPlay`:

```text
Event EndPlay
 -> Stop All Active Commands
 -> Unbind delegates
 -> Stop TCP Server using stored Server ID
```

## 3. Receive and frame messages

Connection callback:

```text
Server Connection Event
 -> Branch Success
 -> Add Session ID to Session Map
 -> Initialize LastHeartbeat time
 -> Send hello/state response
```

Receive callback:

```text
Server Receive TCP Message
 -> Append chunk to ReceiveBuffer[Session ID]
 -> While buffer contains newline
      -> Split at first newline
      -> Keep remaining tail
      -> Parse JSON frame
      -> Validate command
      -> Dispatch command
      -> Send ack/error to that Session ID
```

If the selected socket plugin performs separator framing internally, configure the same separator on both client and server and still enforce a maximum message size.

## 4. Route a validated command

Create enums `EControlTarget`, `EControlAction`, and `EControlPhase`, plus a struct `ST_ControlCommand`.

```text
Validated ST_ControlCommand
 -> Switch on EControlTarget
      Robot -> BPC_RobotCommandTarget.HandleCommand
      Drone -> BPC_DroneCommandTarget.HandleCommand
      Camera -> BPC_CameraCommandTarget.HandleCommand
 -> Branch Accepted
      True  -> Send ack + updated state
      False -> Send structured error
```

Network callbacks may occur outside the normal gameplay execution context depending on the plugin. Use the plugin's documented game-thread callback or enqueue the parsed command for processing by a game-thread timer.

## 5. Android connection graph

Create `GI_RemoteSession` or a persistent controller component. Store:

- `ServerAddress` as string;
- `ServerPort` as integer;
- `ConnectionID` as string;
- `ConnectionState` as enum;
- `LastError` as text;
- `ReconnectAttempt` as integer.

Connect button:

```text
OnClicked Connect
 -> GetText(IP Text Box)
 -> Text To String
 -> Trim
 -> Validate IPv4/hostname and port
 -> Set State = Connecting
 -> Connect Socket Client TCP
      Domain Or IP = validated input
      Port = validated port
      Message Separator = newline-compatible option
      Optional Connection ID = stable local label
 -> Store returned Connection ID
```

Connection-event delegate:

```text
Socket Client TCP Connection Event
 -> Does event Connection ID equal stored ConnectionID?
 -> Branch Success
      True  -> State = Connected -> Send hello -> Enable controls
      False -> State = Disconnected -> Disable controls -> Schedule bounded reconnect
```

Receive-event delegate:

```text
Receive TCP Message Event
 -> Match Connection ID
 -> Parse response
 -> Switch on response type
      ack   -> clear pending indicator for matching id
      state -> update robot/drone UI model
      error -> display safe error text
```

## 6. Press/release movement controls

The inspected Android widget used separate press and release events for directional and joint buttons. Recreate that behavior:

```text
Forward.OnPressed
 -> MakeCommand(target=robot, action=forward, phase=start, value=Speed)
 -> SendCommand

Forward.OnReleased
 -> MakeCommand(target=robot, action=forward, phase=stop)
 -> SendCommand
```

Repeat the pattern for Back, Left, Right, Base, and JointA–JointE. Route all buttons through one `SendCommand` function instead of duplicating socket details in every handler.

`SendCommand`:

```text
Input ST_ControlCommand
 -> Branch ConnectionState == Connected
 -> Assign unique ID and protocol version
 -> Serialize to JSON
 -> Append newline
 -> Socket Client Send TCP using stored ConnectionID
 -> Add command to Pending Map with timestamp
```

## 7. Robot target graph

Avoid directly setting a skeletal bone from the network callback. Keep target angles and movement state in a component.

```text
HandleCommand
 -> Validate action and phase
 -> Update desired velocity or desired joint angle
 -> Clamp to configured limits
 -> Return Accepted + current state

Controlled Tick or Timer
 -> Interp current value toward desired value
 -> Apply movement / animation parameter
```

When a button is released, set the corresponding desired velocity to zero. On disconnect or timeout, call `StopAllMotion`.

## 8. Camera switching

```text
Camera button OnClicked
 -> Make command(target=camera, action=switch, phase=set)
 -> SendCommand

Zoom slider OnValueChanged
 -> Clamp 0..1
 -> Rate-limit updates
 -> Make command(target=camera, action=zoom, phase=set, value=slider)
 -> SendCommand
```

Do not send every tiny slider change without throttling. A 10–20 Hz UI update is usually enough for a control display.

## 9. Test matrix

| Test | Expected result |
| --- | --- |
| Desktop and phone on same Wi-Fi | Connect and receive hello/state |
| Wrong IP | Bounded timeout and readable error |
| Wrong port | Connection rejected without UI freeze |
| Hold and release movement | Starts, then stops immediately |
| Phone loses Wi-Fi while held | Desktop timeout stops motion |
| App backgrounds | Controls disable and server eventually stops motion |
| Two clients | Session ownership and rate limits remain correct |
| Long/malformed JSON | Rejected without crash or arbitrary execution |

## 10. Definition of done

The feature is complete only after a packaged Windows build and a packaged Android build pass the two-device test. PIE-to-PIE or loopback success is necessary but insufficient.
