"""
motor.py
L298N motor driver control (2 motors, no ENA/ENB PWM speed pins wired
-- runs at fixed full speed via IN1..IN4 only).
"""

import RPi.GPIO as GPIO
import config


class MotorController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.pins = [config.IN1, config.IN2, config.IN3, config.IN4]
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def forward(self):
        GPIO.output(config.IN1, GPIO.HIGH)
        GPIO.output(config.IN2, GPIO.LOW)
        GPIO.output(config.IN3, GPIO.HIGH)
        GPIO.output(config.IN4, GPIO.LOW)

    def backward(self):
        GPIO.output(config.IN1, GPIO.LOW)
        GPIO.output(config.IN2, GPIO.HIGH)
        GPIO.output(config.IN3, GPIO.LOW)
        GPIO.output(config.IN4, GPIO.HIGH)

    def left(self):
        # left motor backward, right motor forward -> turn left
        GPIO.output(config.IN1, GPIO.LOW)
        GPIO.output(config.IN2, GPIO.HIGH)
        GPIO.output(config.IN3, GPIO.HIGH)
        GPIO.output(config.IN4, GPIO.LOW)

    def right(self):
        # left motor forward, right motor backward -> turn right
        GPIO.output(config.IN1, GPIO.HIGH)
        GPIO.output(config.IN2, GPIO.LOW)
        GPIO.output(config.IN3, GPIO.LOW)
        GPIO.output(config.IN4, GPIO.HIGH)

    def stop(self):
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)

    def cleanup(self):
        self.stop()
        GPIO.cleanup(self.pins)
