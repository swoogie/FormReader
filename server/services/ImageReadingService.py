import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
from pytesseract import Output

class ImageReadingService:
    def readImage(self, img_file):
        in_memory_file
        max_size = 3000

        height, width = image.shape[:2]

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