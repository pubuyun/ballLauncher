# Ball Launcher Control System

A Raspberry Pi-based turret control system with angular servo positioning, servo control, and integrated shooting mechanisms. This project provides a modular, real-time control system for a ball launcher with remote command capabilities.

## 🚀 Features

- **Precision Control**: Angular servo yaw control with direct angle positioning
- **Smooth Servo Operation**: Tilt control using AngularServo for direct angle positioning
- **Integrated Shooting System**: Combined flywheel motors and reload servo with state machine
- **Non-blocking Operations**: Optimized servo control for responsive operation
- **Modular Architecture**: Clean subsystem-based design with unified base class
- **Real-time Communication**: TCP command receiver for remote control
- **Interactive Testing**: Comprehensive test suite with interactive command interfaces

## 📁 Project Structure

```
ballLauncher/
├── config.py                 # Hardware configuration and pin assignments
├── main.py                   # Main controller application
├── subsystem_base.py          # Base class for all subsystems
├── hardware/                  # Hardware control modules
│   ├── yaw_servo.py          # Angular servo yaw control
│   ├── tilt_servo.py         # Servo pitch control
│   └── shooter.py            # Integrated flywheel + reload system
├── tools/                     # Utility and communication tools
│   └── command_receiver.py   # TCP command receiver
└── test/                     # Interactive test suite
    ├── test_stepper.py       # Stepper motor testing
    ├── test_tilt_servo.py    # Servo testing
    ├── test_servo.py         # General servo testing
    └── test_shooter.py       # Integrated shooter testing
```

## 🔧 Hardware Requirements

### Electronics

- **Raspberry Pi 5** (or compatible)
- **Servo Motors** (3x) for yaw, tilt and reload mechanisms
- **L298N Motor Driver** for flywheel motors
- **DC Motors** (2x) for flywheel system

### Wiring (BCM Pin Numbers)

```
Yaw Servo:
└── PWM Pin:  GPIO 17

Tilt Servo:
└── PWM Pin:  GPIO 19

Reload Servo:
└── PWM Pin:  GPIO 20

L298N Motor Driver (Flywheels):
├── Motor A: IN1=13, IN2=6
└── Motor B: IN3=22, IN4=27
```

## ⚙️ Configuration

Edit `config.py` to match your hardware setup:

```python
# Yaw Servo Settings
YAW_SERVO_PIN = 17
YAW_MIN_DEG = -90.0
YAW_MAX_DEG = 90.0

# Tilt Servo Settings
TILT_SERVO_PIN = 19
PITCH_MIN_DEG = -10.0
PITCH_MAX_DEG = 10.0

# Reload Servo Settings
RELOAD_SERVO_PIN = 20
RELOAD_IDLE_ANGLE = 90
RELOAD_LOAD_ANGLE = 0

# Motor Driver Settings
MOTOR_A_IN1 = 13
MOTOR_A_IN2 = 6
MOTOR_B_IN3 = 22
MOTOR_B_IN4 = 27
```

## 🛠️ Installation

### Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
sudo apt install python3-pip python3-gpiozero

# Install Python packages
pip install gpiozero
```

### Clone and Setup

```bash
git clone https://github.com/pubuyun/ballLauncher.git
cd ballLauncher

# Verify configuration
python3 -c "import config; print('Configuration loaded successfully')"
```

## 🚦 Usage

### Basic Operation

```bash
# Run the main control system
python3 main.py
```

### Interactive Testing

Test individual subsystems with interactive commands:

```bash
# Test yaw servo
python3 test/test_yaw_servo.py

# Test tilt servo
python3 test/test_tilt_servo.py

# Test integrated shooter system
python3 test/test_shooter.py
```

### Shooter System Commands

The integrated shooter test provides these interactive commands:

```bash
shoot <speed>    # Trigger complete shoot cycle (speed: 0.0-1.0)
power <value>    # Set flywheel power directly (0.0-1.0)
push             # Manually move pusher to load position
retract          # Manually retract pusher to idle position
status           # Display current state and power levels
help             # Show command help
quit             # Exit program
```

## 🎯 API Reference

### Subsystem Base Class

All hardware components inherit from `SubsystemBase`:

```python
class SubsystemBase(ABC):
    def __init__(self):
        self._last_ts = None

    def _dt(self):
        """Calculate time delta for timing operations"""

    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def periodic(self): pass

    @abstractmethod
    def shutdown(self): pass
```

### Yaw Servo Control

```python
from hardware.yaw_servo import AngularServoYaw

yaw = AngularServoYaw()
yaw.initialize()

# Set target angle (-90 to +90 degrees)
yaw.set_target_angle(45.0)

# Run periodic updates
yaw.periodic()  # Applies position update
```

### Servo Control

```python
from hardware.tilt_servo import TiltServo

servo = TiltServo()
servo.initialize()

# Set target angle
servo.set_target_angle(25.0)  # Direct angle control

servo.periodic()  # Apply position update
```

### Integrated Shooter

```python
from hardware.shooter import Shooter, ShooterState

shooter = Shooter()
shooter.initialize()

# Complete shooting sequence
shooter.shoot(0.8)  # 80% flywheel power

# Manual component control
shooter.set_flywheel_power(0.6)  # Independent flywheel control

# Check status
print(f"State: {shooter.state}, Power: {shooter.target_flywheel_power}")
```

## 🔄 System States

### Shooter State Machine

```
IDLE → SPINNING_UP → PUSHING → AT_POSITION → RETRACTING → IDLE
```

- **IDLE**: Ready for new commands
- **SPINNING_UP**: Flywheels accelerating to target speed
- **PUSHING**: Pusher moving to load position
- **AT_POSITION**: Brief hold at load position
- **RETRACTING**: Pusher returning to idle position

## 🧪 Testing

### Individual Component Tests

```bash
# Interactive yaw servo testing
python3 test/test_yaw_servo.py
# Commands: angle <degrees>, status, help, quit

# Interactive tilt servo testing
python3 test/test_tilt_servo.py
# Commands: angle <degrees>, status, help, quit

# Comprehensive shooter testing
python3 test/test_shooter.py
# Commands: shoot, power, push, retract, status, help, quit
```

### Test Features

- **Real-time Control**: 100Hz background update threads
- **Interactive Commands**: Live command processing
- **Status Monitoring**: Real-time state and position feedback
- **Safety Checks**: Automatic limit enforcement
- **Graceful Shutdown**: Clean resource cleanup

## ⚡ Performance Optimizations

### Non-blocking Operations

- **Servo Control**: Direct `AngularServo` angle setting eliminates manual PWM calculations
- **Threading**: Separate periodic update threads prevent blocking

### Hardware Optimizations

- **Direct Control**: Servo provides immediate angle positioning without complex stepping
- **State Management**: Integrated shooter prevents component conflicts
- **Resource Management**: Proper initialization and cleanup

## 🛡️ Safety Features

- **Angle Limits**: Hardware enforced min/max angles
- **State Protection**: Prevents conflicting operations
- **Automatic Disable**: Motors disable when not needed
- **Emergency Stop**: Ctrl+C for immediate shutdown

## ⚠️ Safety Guidelines

1. **Verify Limits**: Check `config.py` angle limits match physical constraints
2. **Start Slow**: Begin with low flywheel power for testing
3. **Clear Area**: Ensure muzzle area is clear before operation
4. **Emergency Stop**: Keep Ctrl+C ready for immediate shutdown
5. **Power Down**: Always shut down properly to disable motors

## 🔧 Troubleshooting

### Common Issues

**Servo not responding:**

- Verify PWM pin connection
- Check servo power supply (5V recommended)
- Confirm angle limits in config

**Import errors:**

- Install gpiozero: `pip install gpiozero`
- Check Python version (3.7+ required)

### Debug Mode

Enable verbose output by running tests with `-v` flag or adding debug prints in periodic methods.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes following the subsystem pattern
4. Add appropriate tests
5. Submit a pull request

## 📝 License

This project is open source. Please check the repository for license details.

## 🙏 Acknowledgments

- Built with [gpiozero](https://gpiozero.readthedocs.io/) for clean GPIO control
- Uses Raspberry Pi GPIO capabilities for real-time hardware control
- Inspired by modular robotics control patterns
