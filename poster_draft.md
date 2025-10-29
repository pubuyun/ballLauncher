# Software Architecture Poster: Ball Launcher Project

## Main System

### Remote Control

- **Web Interface**: Provides a user-friendly interface for controlling the ball launcher.
- **WebSocket Communication**: Enables real-time command handling between the client and the server.
- **Video Streaming**: Streams live camera feed for precise targeting.

### Control Loop

- **Iteration**: Continuously updates subsystems at a frequency defined by `MAIN_LOOP_HZ`.
- **Sequence**: Ensures smooth operation by initializing, updating, and shutting down subsystems in order.

## Subsystems

### Stepper Motor (Yaw Control)

- **Selection**: Determines the direction of rotation based on the target angle.
- **Iteration**: Generates pulses to move the motor incrementally.
- **Sequence**: Initializes, updates, and disables the motor in a defined order.

### Tilt Servo (Pitch Control)

- **Selection**: Sets the target angle within the allowed range.
- **Sequence**: Updates the servo angle periodically to match the target.

### Shooter

- **Finite State Machine (FSM)**: 
  - **Purpose**: Ensures non-blocking execution of a series of actions by transitioning between predefined states.
  - **States**:
    - `IDLE`: The system is inactive, waiting for a trigger.
    - `SPINNING_UP`: The flywheels are accelerating to the required speed.
    - `PUSHING`: The pusher moves to launch the ball.
    - `AT_POSITION`: The pusher holds at the launch position.
    - `RETRACTING`: The pusher returns to its idle position.
  - **Transitions**:
    - `IDLE` → `SPINNING_UP`: Triggered by a shoot command.
    - `SPINNING_UP` → `PUSHING`: Occurs after the flywheels reach the required speed.
    - `PUSHING` → `AT_POSITION`: Triggered after the pusher reaches the launch position.
    - `AT_POSITION` → `RETRACTING`: Occurs after a brief hold at the launch position.
    - `RETRACTING` → `IDLE`: Triggered after the pusher returns to its idle position.
- **Selection**: Uses conditional logic to determine state transitions based on elapsed time and system conditions.
- **Iteration**: Periodically updates the flywheel power and pusher servo to reflect the current state.

## Alignment with IGCSE CS Syllabus

### Control Loop

- Iteratively updates subsystems at a frequency defined by `MAIN_LOOP_HZ`.
- Ensures smooth operation of the stepper motor, tilt servo, and shooter.

### Command Handling

- Maps commands like `yaw`, `tilt`, `shoot`, and `reload` to specific actions.
- Validates inputs and provides error handling for unknown or invalid commands.

### Shooter FSM

- States: `IDLE`, `SPINNING_UP`, `PUSHING`, `AT_POSITION`, `RETRACTING`.
- Transitions are time-based and controlled in the `periodic` method.

### Remote Control

- WebSocket endpoint for real-time command handling.
- Video streaming endpoint for live camera feed.
- Static file serving for the web interface.

## Alignment with IGCSE CS Syllabus

- **Selection**: Decision-making in `_process_command` and FSM transitions.
- **Iteration**: Continuous updates in the control loop and periodic hardware updates.
- **Sequence**: Ordered execution of initialization, periodic updates, and shutdown.

## Visual Representations

### Main System

- Flowchart illustrating the control loop and remote control architecture.

### Subsystems

- Diagram of the shooter FSM.
- Illustrations of stepper motor and tilt servo operations.

## Key Code Snippets

### Command Handling

```python
def _process_command(self, cmd, val):
    handlers = {
        "yaw": lambda v: self._set_angle(self.stepper, v, config.YAW_MIN_DEG, config.YAW_MAX_DEG, "yaw"),
        "tilt": lambda v: self._set_angle(self.tilt, v, config.PITCH_MIN_DEG, config.PITCH_MAX_DEG, "tilt"),
        "shoot": lambda v: self._set_power(self.shooter.shoot, v, "shoot power"),
    }
    return handlers.get(cmd, lambda _: f"ERR: unknown cmd '{cmd}'")(val)
```

### Shooter FSM

```python
def periodic(self):
    now = time.monotonic()
    elapsed = now - self._state_ts
    match self.state:
        case ShooterState.SPINNING_UP:
            if elapsed >= self._spinup_time:
                self._to_state(ShooterState.PUSHING)
        case ShooterState.PUSHING:
            if elapsed >= self._move_to_load_est:
                self._to_state(ShooterState.AT_POSITION)
        case ShooterState.AT_POSITION:
            if elapsed >= self._hold_sec:
                self._to_state(ShooterState.RETRACTING)
        case ShooterState.RETRACTING:
            if elapsed >= self._move_to_idle_est:
                self._to_state(ShooterState.IDLE)
```

### Remote Control WebSocket

```python
@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        msg = await ws.receive_text()
        resp = await run_in_threadpool(handler.handle_command, msg)
        await ws.send_text(resp)
```

## Conclusion

This poster highlights the modular design, key features, and alignment with the IGCSE CS syllabus. The system demonstrates effective use of selection, iteration, and sequence, along with a robust FSM and remote control interface.
