"""
ai_detection.py
Runs crack-detection inference on camera frames.
"""

import config
from models.crack_detection_model import (
    load_trained_model,
    preprocess_frame,
)


class CrackDetector:
    def __init__(self):
        self.model = load_trained_model(config.MODEL_PATH)

    def predict(self, frame):
        """Returns (is_crack: bool, confidence: float)."""
        img = preprocess_frame(frame)
        pred = self.model.predict(img, verbose=0)
        confidence = float(pred[0][0])
        is_crack = confidence >= config.CRACK_CONFIDENCE_THRESHOLD
        return is_crack, confidence
