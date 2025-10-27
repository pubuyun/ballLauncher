import threading, time, uvicorn, config
from tools.command_handler import CommandHandler
from web.app import app


def control_loop(stepper, tilt, shooter, stop_event):
    stepper.initialize()
    tilt.initialize()
    shooter.initialize()
    print("Control loop started (SIM, PC webcam).")
    try:
        while not stop_event.is_set():
            stepper.periodic()
            tilt.periodic()
            shooter.periodic()
            time.sleep(1.0 / config.MAIN_LOOP_HZ)
    finally:
        print("Shutting down subsystems...")
        stepper.shutdown()
        tilt.shutdown()
        shooter.shutdown()
        print("All subsystems shut down.")


if __name__ == "__main__":
    from web import app as webapp

    stop_event = threading.Event()
    try:
        uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=False)
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
