# Ball Launcher Control System

A Raspberry Pi-based turret control system with precise angular servo positioning, servo control, and integrated shooting mechanisms. This project provides a modular, real-time control system for a ball launcher with remote command capabilities.

## 🚀 Features

- **Precision Control**: Angular servo yaw control with direct angle positioning
- **Smooth Servo Operation**: Tilt control using AngularServo for direct angle positioning
- **Integrated Shooting System**: Combined flywheel motors and reload servo with state machine
- **Non-blocking Operations**: Optimized servo control for responsive operation
- **Modular Architecture**: Clean subsystem-based design with unified base class
- **Real-time Communication**: Web interface for remote control
- **Interactive Testing**: Comprehensive test suite with interactive command interfaces

## 📁 Project Structure

```
ballLauncher/
├── config.py                 # Hardware configuration and pin assignments
├── main.py                   # Main controller application
├── main_web.py               # Web interface controller
├── subsystem_base.py         # Base class for all subsystems
├── hardware/                 # Hardware control modules
│   ├── yaw_servo.py         # Angular servo yaw control
│   ├── tilt_servo.py        # Servo pitch control
│   └── shooter.py           # Integrated flywheel + reload system
├── tools/                    # Utility and communication tools
│   └── command_handler.py   # Command processing system
├── test/                     # Interactive test suite
│   ├── test_yaw_servo.py    # Yaw servo testing
│   ├── test_tilt_servo.py   # Tilt servo testing
│   ├── test_shooter.py      # Integrated shooter testing
│   └── test_servo.py        # General servo testing
└── web/                      # Web interface
    ├── app.py               # FastAPI web application
    └── static/
        └── index.html       # Web control interface
```

## 🔧 Hardware Requirements

### Electronics

- **Raspberry Pi 5** (or compatible)
- **Servo Motors** (3x) for yaw, tilt and reload mechanisms
- **L298N Motor Driver** for flywheel motors
- **DC Motors** (2x) for flywheel system
- **Power Supply** for motors and servos

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

# System Settings
MAIN_LOOP_HZ = 100.0  # 10ms tick
PIN_FACTORY = "RPiGPIOFactory"  # Use "MockFactory" for testing on non-RPi systems
```

## 🛠️ Installation

### Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
sudo apt install python3-pip python3-gpiozero

# Install Python packages
pip install gpiozero fastapi uvicorn
```

### Clone and Setup

```bash
git clone https://github.com/pubuyun/ballLauncher.git
cd ballLauncher

# Install requirements
pip install -r requirements.txt

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

### Web Interface

The system includes a web interface that runs on `http://0.0.0.0:8000` by default. This provides:

- Real-time control of yaw and tilt angles
- Flywheel power control
- Shooting functionality
- System status monitoring

## 🎯 API Reference

### Subsystem Base Class

All hardware components inherit from `SubsystemBase`:

```python
class SubsystemBase(ABC):
    def __init__(self):
        self._initialized = False
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

# Clean shutdown
yaw.shutdown()
```

### Tilt Servo Control

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
from hardware.shooter import Shooter

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
- **State Management**: Efficient state transitions prevent conflicts

### Hardware Optimizations

- **Direct Control**: Servo provides immediate angle positioning without complex stepping
- **Resource Management**: Proper initialization and cleanup
- **Safety Limits**: Hardware-enforced angle and power limits

## 🛡️ Safety Features

- **Angle Limits**: Hardware enforced min/max angles
- **State Protection**: Prevents conflicting operations
- **Emergency Stop**: Ctrl+C for immediate shutdown
- **Power Management**: Automatic motor control

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
- Ensure proper ground connections

**Motor driver issues:**

- Check motor power supply
- Verify motor driver connections
- Ensure proper voltage levels

**Import errors:**

- Install gpiozero: `pip install gpiozero`
- Check Python version (3.7+ required)
- Verify all dependencies in requirements.txt

### Debug Mode

Enable verbose output by running tests with debug prints or checking system logs.

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
- Uses [FastAPI](https://fastapi.tiangolo.com/) for web interface
- Inspired by modular robotics control patterns
- Raspberry Pi GPIO capabilities for real-time hardware control
