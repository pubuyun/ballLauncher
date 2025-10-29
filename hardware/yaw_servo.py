from gpiozero import AngularServo
from subsystem_base import SubsystemBase
import config


class AngularServoYaw(SubsystemBase):
    def __init__(self):
        super().__init__()
        self.servo = AngularServo(
            pin=config.YAW_SERVO_PIN,
            min_angle=config.YAW_MIN_DEG,
            max_angle=config.YAW_MAX_DEG,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025,
            frame_width=0.02,
            pin_factory=self.pin_factory,
        )
        self._target_angle = 0.0
        self._current_angle = 0.0

    def initialize(self):
        self._target_angle = 0.0
        self._current_angle = 0.0
        self.servo.angle = 0.0

    def periodic(self):
        self._current_angle = self._target_angle
        self.servo.angle = self._current_angle

    def set_target_angle(self, angle):
        self._target_angle = max(config.YAW_MIN_DEG, min(config.YAW_MAX_DEG, angle))

    def shutdown(self):
        try:
            self.servo.close()
        except Exception as e:
            print(f"Error shutting down yaw servo: {e}")
        finally:
            self._initialized = False
