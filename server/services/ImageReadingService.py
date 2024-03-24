import io
import cv2
import numpy as np

class ImageReadingService:
    def readImage(self, app, img_file):
        in_memory_file = io.BytesIO(img_file.read())

        img_array = np.array(bytearray(in_memory_file.read()), dtype=np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  

        max_size = 3000

        height, width = image.shape[:2]
        app.logger.info(f'Original image size: {width}x{height}')

        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        resized_image = cv2.resize(image, (new_width, new_height))
        unprocessed_resized_image = resized_image.copy()

        return resized_image, unprocessed_resized_image