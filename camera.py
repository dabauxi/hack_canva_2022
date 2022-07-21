import cv2
import numpy as np

DS_FACTOR = 0.6


class VideoCamera:
    PLACEHOLDER_IMAGE = None

    def __init__(self, fps: int = 30):
        self.cap = cv2.VideoCapture(-1)
        self.cap.set(cv2.CAP_PROP_FPS, fps)

        with open("placeholder-image.png", "rb") as f:
            self.PLACEHOLDER_IMAGE = f.read()

    def __del__(self):
        self.cap.release()

    @staticmethod
    def resize(image, resize_factor=DS_FACTOR):
        image = cv2.resize(
            image, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_AREA
        )
        ret, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes()

    def get_frame(self):
        success, image = self.cap.read()
        if success:
            return self.resize(image)
        else:
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(-1)
            return self.PLACEHOLDER_IMAGE
