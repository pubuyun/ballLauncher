#!/usr/bin/env python3
"""
Interactive test for AngularServoYaw (hardware/yaw_servo.py).

Commands:
  angle <deg>     : set target angle (-90 to +90 degrees)
  status          : print current/target angles
  help            : show this help
  quit            : exit program

Run:
  python test/test_yaw_servo.py
"""

import sys
import threading
import time
import config
from hardware.yaw_servo import AngularServoYaw


def periodic_thread(
    subsys: AngularServoYaw, stop_evt: threading.Event, hz: float = 100.0
):
    """Background thread for periodic updates"""
    tick = 1.0 / max(1e-3, hz)
    subsys.initialize()
    try:
        while not stop_evt.is_set():
            subsys.periodic()
            time.sleep(tick)
    except Exception as e:
        print(f"[periodic] Error: {e}", file=sys.stderr)
    finally:
        subsys.shutdown()


def main():
    yaw = AngularServoYaw()
    stop_evt = threading.Event()
    periodic_th = threading.Thread(
        target=periodic_thread, args=(yaw, stop_evt, 100.0), daemon=True
    )
    periodic_th.start()

    print(__doc__)
    print(f"Yaw servo test started. Pin: {config.YAW_SERVO_PIN}")
    print(f"Angle range: {config.YAW_MIN_DEG} to {config.YAW_MAX_DEG} degrees")

    try:
        while True:
            try:
                cmd = input("yaw> ").strip().lower()
                if not cmd:
                    continue

                if cmd == "quit" or cmd == "exit":
                    break
                elif cmd == "help":
                    print(__doc__)
                elif cmd == "status":
                    print(f"Current angle: {yaw._current_angle:.1f}°")
                    print(f"Target angle: {yaw._target_angle:.1f}°")
                elif cmd.startswith("angle "):
                    parts = cmd.split()
                    if len(parts) == 2:
                        try:
                            angle = float(parts[1])
                            yaw.set_target_angle(angle)
                            print(f"Set target angle to {angle:.1f}°")
                        except ValueError:
                            print("Error: angle must be a number")
                    else:
                        print("Usage: angle <degrees>")
                else:
                    print(f"Unknown command: {cmd}")
                    print("Type 'help' for available commands")

            except (KeyboardInterrupt, EOFError):
                break
            except Exception as e:
                print(f"Error: {e}")

    finally:
        print("[shutdown] Stopping...")
        stop_evt.set()
        periodic_th.join(timeout=2.0)
        print("[done] Cleanup complete.")


if __name__ == "__main__":
    main()
