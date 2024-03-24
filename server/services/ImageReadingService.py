import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
from pytesseract import Output

class ImageReadingService:
    def readImage(self, img_file):
        in_memory_file = io.BytesIO(img_file.read())

        img_array = np.array(bytearray(in_memory_file.read()), dtype=np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  

        max_size = 3000

        height, width = image.shape[:2]
        print(f'Original image size: {width}x{height}')

        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        resized_image = cv2.resize(image, (new_width, new_height))
        unprocessed_resized_image = resized_image.copy()

        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # def process_image():
    #     if 'image' not in request.files:
    #         return 'No image file found in the request', 400

    #     image_file = request.files['image']

    #     # Convert image data to a NumPy array

    #     # Perform OpenCV operations on the image
    #     gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     edges = cv2.Canny(gray_img, 100, 200)

    #     # Prepare a response (e.g., encode the processed image)
    #     _, processed_img_encoded = cv2.imencode('.jpg', edges)
    #     response_data = processed_img_encoded.tobytes()

    #     return response_data