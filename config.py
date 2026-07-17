"""
config.py
Central configuration for Railway Track Crack Detection Robot.
All pin numbers use BCM numbering.
"""

# ---------------------------------------------------------------
# MOTOR DRIVER (L298N)
# ---------------------------------------------------------------
IN1 = 17   # Pin 11 - Left Motor
IN2 = 27   # Pin 13 - Left Motor
IN3 = 22   # Pin 15 - Right Motor
IN4 = 5    # Pin 29 - Right Motor

MOTOR_SPEED = 70  # duty cycle % if ENA/ENB PWM pins are wired; ignored otherwise

# ---------------------------------------------------------------
# ULTRASONIC SENSOR (HC-SR04)
# ---------------------------------------------------------------
TRIG_PIN = 23   # Pin 16
ECHO_PIN = 24   # Pin 18 (through voltage divider!)

OBSTACLE_DISTANCE_CM = 15   # stop/avoid threshold

# ---------------------------------------------------------------
# BUZZER
# ---------------------------------------------------------------
BUZZER_PIN = 21   # Pin 40 (+ve). GND -> breadboard GND.

# ---------------------------------------------------------------
# GPS (NEO-6M)
# ---------------------------------------------------------------
# NOTE: The NEO-6M is wired to the Pi's hardware UART (GPIO14/15).
# If your GSM module (e.g. SIM800L) is ALSO wired to GPIO14/15 as in
# wiring_diagram.md, both devices cannot share the same UART at once.
# Recommended fix: connect GSM via a USB-to-TTL adapter (shows up as
# /dev/ttyUSB0) and keep GPS on the Pi's onboard UART (/dev/ttyAMA0 or
# /dev/serial0). Update the ports below to match your actual setup.
GPS_PORT = "/dev/serial0"
GPS_BAUDRATE = 9600

# ---------------------------------------------------------------
# GSM MODULE (e.g. SIM800L)
# ---------------------------------------------------------------
# See note above re: UART conflict with GPS. Change GSM_PORT to
# "/dev/ttyUSB0" if using a USB-TTL adapter for the GSM module.
GSM_PORT = "/dev/ttyUSB0"
GSM_BAUDRATE = 9600
ALERT_PHONE_NUMBER = "+91XXXXXXXXXX"   # <-- set the alert recipient number

# ---------------------------------------------------------------
# CAMERA
# ---------------------------------------------------------------
CAMERA_RESOLUTION = (640, 480)
CAMERA_FRAMERATE = 30
CAPTURE_INTERVAL_SEC = 2   # how often to grab a frame for inference

# ---------------------------------------------------------------
# AI CRACK DETECTION MODEL
# ---------------------------------------------------------------
MODEL_PATH = "models/crack_detection_model.h5"   # trained weights file
CRACK_CONFIDENCE_THRESHOLD = 0.75

# ---------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------
LOG_DIR = "logs"
IMAGE_DIR = "images"
