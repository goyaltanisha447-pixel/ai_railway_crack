"""
main.py
Railway Track Crack Detection Robot — main control loop.

Flow:
  1. Move forward along the track.
  2. Continuously check the ultrasonic sensor; stop/reroute on obstacle.
  3. Periodically grab a camera frame and run it through the crack
     detection model.
  4. On crack detection: stop, sound buzzer, fetch GPS location, send
     SMS alert via GSM, log the event and save the frame.
"""

import time
import signal
import sys

import config
from motor import MotorController
from ultrasonic import UltrasonicSensor
from gps import GPSReader
from gsm import GSMModule
from camera import CameraModule
from ai_detection import CrackDetector
from utils import setup_logger, Buzzer

logger = setup_logger()


class CrackDetectionRobot:
    def __init__(self):
        logger.info("Initializing robot systems...")
        self.motor = MotorController()
        self.ultrasonic = UltrasonicSensor()
        self.buzzer = Buzzer()
        self.camera = CameraModule()
        self.detector = CrackDetector()

        # GPS/GSM share a UART line by default in this build — see the
        # warning in config.py. Wrap in try/except so one failing
        # doesn't take down the whole robot.
        try:
            self.gps = GPSReader()
        except Exception as e:
            logger.warning(f"GPS init failed: {e}")
            self.gps = None

        try:
            self.gsm = GSMModule()
        except Exception as e:
            logger.warning(f"GSM init failed: {e}")
            self.gsm = None

        self.last_capture_time = 0
        self.running = True
        logger.info("All systems initialized.")

    def get_location_string(self):
        if self.gps:
            return self.gps.get_location_string()
        return "GPS unavailable"

    def handle_crack_detected(self, confidence):
        logger.info(f"CRACK DETECTED (confidence={confidence:.2f})")
        self.motor.stop()
        self.buzzer.beep(duration=0.5, times=3)

        location_str = self.get_location_string()
        logger.info(f"Location: {location_str}")

        if self.gsm:
            try:
                self.gsm.send_crack_alert(location_str)
                logger.info("SMS alert sent.")
            except Exception as e:
                logger.error(f"Failed to send SMS alert: {e}")
        else:
            logger.warning("GSM not available — SMS alert skipped.")

    def run_cycle(self):
        # 1. Obstacle check
        if self.ultrasonic.is_obstacle():
            logger.info("Obstacle detected — stopping.")
            self.motor.stop()
            self.buzzer.beep(duration=0.2, times=1)
            time.sleep(1)
            return

        # 2. Move forward
        self.motor.forward()

        # 3. Periodic crack inference
        now = time.time()
        if now - self.last_capture_time >= config.CAPTURE_INTERVAL_SEC:
            self.last_capture_time = now
            frame = self.camera.capture_frame()
            is_crack, confidence = self.detector.predict(frame)
            if is_crack:
                self.camera.capture_frame(save=True)
                self.handle_crack_detected(confidence)
                time.sleep(2)  # pause after handling alert
                self.motor.forward()

    def run(self):
        logger.info("Starting main control loop.")
        try:
            while self.running:
                self.run_cycle()
                time.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Interrupted by user.")
        finally:
            self.shutdown()

    def shutdown(self):
        logger.info("Shutting down — cleaning up GPIO and connections.")
        self.motor.cleanup()
        self.ultrasonic.cleanup()
        self.buzzer.cleanup()
        self.camera.close()
        if self.gps:
            self.gps.close()
        if self.gsm:
            self.gsm.close()


def handle_sigterm(signum, frame):
    logger.info("SIGTERM received.")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)
    robot = CrackDetectionRobot()
    robot.run()
