import cv2

DS_FACTOR = 0.6


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        image = cv2.resize(
            image, None, fx=DS_FACTOR, fy=DS_FACTOR, interpolation=cv2.INTER_AREA
        )
        ret, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes()
