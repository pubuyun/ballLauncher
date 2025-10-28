# Global configuration for Raspberry Pi 5 turret project
# Adjust pin assignments to match your wiring.

from dataclasses import dataclass

# GPIO numbering mode: use BCM numbering
GPIO_MODE_BCM = True
PIN_FACTORY = (
    "RPiGPIOFactory"  # Options: "RPiGPIOFactory", "MockFactory", "PiGPIOFactory"
)

# ===== Stepper (Yaw) =====
STEPPER_DIR_PIN = 23
STEPPER_STEP_PIN = 25
STEPPER_EN_PIN = 24  # optional, set to None if not used

# Mechanical parameters
STEPS_PER_REV = 200  # 1.8°/step motor
MICROSTEPPING = 8  # e.g. A4988/DRV8825 microstep setting

# Motion limits and dynamics
YAW_MIN_DEG = -90.0
YAW_MAX_DEG = 90.0
YAW_MAX_SPEED_DPS = 180.0  # degrees per second

# ===== Tilt Servo (Pitch) =====
TILT_SERVO_PIN = 19
PITCH_MIN_DEG = -10.0
PITCH_MAX_DEG = 10.0

# ===== Reload Servo=====
RELOAD_SERVO_PIN = 20
RELOAD_IDLE_ANGLE = 90
RELOAD_LOAD_ANGLE = 0
RELOAD_HOLD_SEC = 0.2

# ===== Flywheel Motors =====

# Motor A (left)
MOTOR_A_IN1 = 13
MOTOR_A_IN2 = 6

# Motor B (right)
MOTOR_B_IN3 = 22
MOTOR_B_IN4 = 27


# ===== Loop timing =====
MAIN_LOOP_HZ = 100.0  # 10ms tick
