import json
import time
import config


def _ts():
    return time.strftime("%H:%M:%S")


class CommandHandler:
    def __init__(self, yaw_servo, tilt_servo, shooter):
        self.yaw = yaw_servo
        self.tilt = tilt_servo
        self.shooter = shooter

    def handle_command(self, command: str):
        command = command.strip()
        try:
            if command.startswith("{"):
                obj = json.loads(command)
                cmd = (obj.get("cmd", "") or "").lower()
                val = obj.get("value", None)
                print(f"[{_ts()}] [CMD] raw={obj}")
                return self._process_command(cmd, val)
            parts = command.split()
            if not parts:
                return "ERR: empty"
            cmd, val = parts[0].lower(), float(parts[1]) if len(parts) > 1 else None
            print(f"[{_ts()}] [CMD] raw={{'cmd': '{cmd}', 'value': {val}}}")
            return self._process_command(cmd, val)
        except Exception as e:
            err = f"ERR: {e}"
            print(f"[{_ts()}] [CMD] error={err}")
            return err

    def _process_command(self, cmd, val):
        handlers = {
            "yaw": lambda v: self._set_angle(
                self.yaw, v, config.YAW_MIN_DEG, config.YAW_MAX_DEG, "yaw"
            ),
            "tilt": lambda v: self._set_angle(
                self.tilt, v, config.PITCH_MIN_DEG, config.PITCH_MAX_DEG, "tilt"
            ),
            "shoot": lambda v: self._set_power(self.shooter.shoot, v, "shoot power"),
            "flywheel": lambda v: self._set_power(
                self.shooter.set_flywheel_power, v, "flywheel power"
            ),
            "reload": lambda _: self._reload(),
            "status": lambda _: self._status(),
        }
        return handlers.get(cmd, lambda _: f"ERR: unknown cmd '{cmd}'")(val)

    def _set_angle(self, device, value, min_val, max_val, name):
        if value is None:
            return f"ERR: {name} needs value"
        value = max(min_val, min(max_val, float(value)))
        device.set_target_angle(value)
        return f"OK: {name}={value:.2f}"

    def _set_power(self, action, value, name):
        if value is None:
            return f"ERR: {name} needs power 0..1"
        value = max(0.0, min(1.0, float(value)))
        action(value)
        return f"OK: {name}={value:.2f}"

    def _reload(self):
        pass
        return "OK: reload"

    def _status(self):
        payload = {
            "ok": True,
            "state": self.shooter.state,
        }
        print(f"[{_ts()}] [CMD] status={payload}")
        return json.dumps(payload)
