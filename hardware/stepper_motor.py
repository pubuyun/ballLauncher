from time import perf_counter as now
from subsystem_base import SubsystemBase
from gpiozero import DigitalOutputDevice, PWMOutputDevice
import config


class StepperYaw(SubsystemBase):

    def __init__(self):
        self.pulse = PWMOutputDevice(
            config.STEPPER_STEP_PIN, pin_factory=self.pin_factory
        )
        self.direction = DigitalOutputDevice(
            config.STEPPER_DIR_PIN, pin_factory=self.pin_factory
        )
        self.enable = DigitalOutputDevice(
            config.STEPPER_EN_PIN, pin_factory=self.pin_factory
        )

        self.enable.off()  # on
        self.direction.off()  # CW
        self.frequency = (
            config.YAW_MAX_SPEED_DPS / 360 * config.STEPS_PER_REV * config.MICROSTEPPING
        )

    def set_direction(self, clockwise=True):
        if clockwise:
            self.direction.off()
        else:
            self.direction.on()

    def periodic(self):
        pass

    def set_target_angle(self, angle):
        target_steps = int(angle / 360 * config.STEPS_PER_REV * config.MICROSTEPPING)
        delta_steps = target_steps - getattr(self, "_current_steps", 0)
        self.set_direction(clockwise=(delta_steps >= 0))
        self.pulse.blink(
            on_time=self.frequency,
            off_time=self.frequency,
            n=abs(delta_steps),
            background=False,
        )
        self._current_steps = target_steps

    def set_enabled(self, enabled: bool):
        if enabled:
            self.enable.off()  # on
        else:
            self.enable.on()  # off

    def shutdown(self):
        try:
            self.enable.value = 0
        finally:
            self._dir.close()
            self._step.close()
            self._en.close()
