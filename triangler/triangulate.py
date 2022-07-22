import io

import cv2
import numpy as np
from PIL import Image

import triangler


def generate_del_tri(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))

    # convert PIL image to OpenCV image
    triangler_instance = triangler.Triangler()
    img = np.array(image.convert('RGB'))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = triangler_instance.triangulate_img(img)

    # convert OpenCV image back to PIL image
    img = np.asarray(img * 255.0).astype("uint8")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)
    return image