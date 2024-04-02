import io
import cv2
import numpy as np

class ImageReadingService:

    def __init__(self):
        self.image = None

    def read_image(self, img_file):
        in_memory_file = io.BytesIO(img_file.read())

        img_array = np.array(bytearray(in_memory_file.read()), dtype=np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  

        return image
