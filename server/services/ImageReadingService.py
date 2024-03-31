import io
import cv2
import numpy as np

class ImageReadingService:

    def __init__(self):
        self.image = None

    def read_image(self, img_file):
        in_memory_file = io.BytesIO(img_file.read())

        img_array = np.array(bytearray(in_memory_file.read()), dtype=np.uint8)
        self.image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  

        return self

    def resize_image(self, max_size): 
        height, width = self.image.shape[:2]
        if width > height:
            new_width = max_size
            ratio = max_size / width
            new_height = int(height * ratio)
        else:
            new_height = max_size
            ratio = max_size / height
            new_width = int(width * ratio)

        resized_image = cv2.resize(self.image, (new_width, new_height))

        return resized_image, ratio