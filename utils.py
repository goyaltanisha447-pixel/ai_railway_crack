"""
utils.py
Shared helpers: logging and GPIO buzzer control.
"""

import os
import time
import logging
import RPi.GPIO as GPIO
import config


def setup_logger():
    os.makedirs(config.LOG_DIR, exist_ok=True)
    log_path = os.path.join(config.LOG_DIR, "robot.log")

    logger = logging.getLogger("crack_bot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(log_path)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s"
        ))
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        logger.addHandler(sh)

    return logger


class Buzzer:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(config.BUZZER_PIN, GPIO.OUT)
        GPIO.output(config.BUZZER_PIN, GPIO.LOW)

    def beep(self, duration=0.5, times=1):
        for _ in range(times):
            GPIO.output(config.BUZZER_PIN, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(config.BUZZER_PIN, GPIO.LOW)
            time.sleep(0.2)

    def cleanup(self):
        GPIO.output(config.BUZZER_PIN, GPIO.LOW)
        GPIO.cleanup(config.BUZZER_PIN)
