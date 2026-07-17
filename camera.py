"""
camera.py
Raspberry Pi Camera capture (via CSI connector) using picamera2.
"""

import time
import os
from picamera2 import Picamera2
import config


class CameraModule:
    def __init__(self):
        self.picam2 = Picamera2()
        cam_config = self.picam2.create_still_configuration(
            main={"size": config.CAMERA_RESOLUTION}
        )
        self.picam2.configure(cam_config)
        self.picam2.start()
        time.sleep(1)  # let sensor warm up

    def capture_frame(self, save=False):
        """Returns a numpy array (RGB frame). Optionally saves to disk."""
        frame = self.picam2.capture_array()
        if save:
            os.makedirs(config.IMAGE_DIR, exist_ok=True)
            filename = os.path.join(
                config.IMAGE_DIR, f"frame_{int(time.time())}.jpg"
            )
            self.picam2.capture_file(filename)
        return frame

    def close(self):
        self.picam2.stop()
