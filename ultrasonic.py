"""
ultrasonic.py
HC-SR04 distance measurement.
ECHO must be wired through a voltage divider (5V -> 3.3V logic) before
reaching GPIO24, as noted in wiring_diagram.md.
"""

import time
import RPi.GPIO as GPIO
import config


class UltrasonicSensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(config.TRIG_PIN, GPIO.OUT)
        GPIO.setup(config.ECHO_PIN, GPIO.IN)
        GPIO.output(config.TRIG_PIN, GPIO.LOW)
        time.sleep(0.5)  # let sensor settle

    def get_distance_cm(self, timeout=0.03):
        """Returns distance in cm, or None on timeout/no echo."""
        GPIO.output(config.TRIG_PIN, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(config.TRIG_PIN, GPIO.LOW)

        start_time = time.time()
        stop_time = time.time()

        timeout_start = time.time()
        while GPIO.input(config.ECHO_PIN) == 0:
            start_time = time.time()
            if start_time - timeout_start > timeout:
                return None

        timeout_start = time.time()
        while GPIO.input(config.ECHO_PIN) == 1:
            stop_time = time.time()
            if stop_time - timeout_start > timeout:
                return None

        elapsed = stop_time - start_time
        distance = (elapsed * 34300) / 2  # speed of sound in cm/s
        return round(distance, 1)

    def is_obstacle(self):
        distance = self.get_distance_cm()
        if distance is None:
            return False
        return distance <= config.OBSTACLE_DISTANCE_CM

    def cleanup(self):
        GPIO.cleanup([config.TRIG_PIN, config.ECHO_PIN])
