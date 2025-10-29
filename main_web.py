import threading, time, uvicorn, config
from hardware.yaw_servo import AngularServoYaw
from hardware.tilt_servo import TiltServo
from hardware.shooter import Shooter
from tools.command_handler import CommandHandler
from web.app import app


def control_loop(yaw, tilt, shooter, stop_event):
    yaw.initialize()
    tilt.initialize()
    shooter.initialize()
    print("Control loop started (SIM, PC webcam).")
    try:
        while not stop_event.is_set():
            yaw.periodic()
            tilt.periodic()
            shooter.periodic()
            time.sleep(1.0 / config.MAIN_LOOP_HZ)
    finally:
        print("Shutting down subsystems...")
        yaw.shutdown()
        tilt.shutdown()
        shooter.shutdown()
        print("All subsystems shut down.")


if __name__ == "__main__":
    yaw = AngularServoYaw()
    tilt = TiltServo()
    shooter = Shooter()
    handler = CommandHandler(yaw, tilt, shooter)
    from web import app as webapp

    webapp.handler = handler
    stop_event = threading.Event()
    th = threading.Thread(
        target=control_loop, args=(yaw, tilt, shooter, stop_event), daemon=True
    )
    th.start()
    try:
        uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=False)
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        th.join()
